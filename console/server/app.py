"""WorkAgent Console — REST API server (stdlib only).

Run:  python server/app.py [--port 8765]
Open: http://127.0.0.1:8765/  (serves web/index.html)
"""
import argparse
import json
import mimetypes
import os
import re
import threading
import time
import traceback
import uuid
from datetime import datetime
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

import db

HOST = os.environ.get("WORKAGENT_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("WORKAGENT_PORT", "8765"))
WEB_DIR = os.path.join(db.BASE_DIR, "web")
STARTED_AT = time.time()
SESSION_TTL_HOURS = int(os.environ.get("WORKAGENT_SESSION_HOURS", "72"))

LINEAR_SEQ = {"value": 142}
WORKER_LOCK = threading.Lock()


# ------------------------------------------------------------------ helpers
def parse_body(handler):
    length = int(handler.headers.get("Content-Length") or 0)
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return {}


def req_row_to_json(row, conn):
    r = dict(row)
    r["fields"] = json.loads(r.get("fields") or "[]")
    r["qa"] = json.loads(r.get("qa") or "[]")
    linear_status = r.pop("linear_status", "none") or "none"
    linear_id = r.pop("linear_id", None)
    r["linear"] = {
        "status": linear_status,
        "id": linear_id,
        "at": r.get("updated_at") if linear_status == "synced" and linear_id else None,
    }
    arts = conn.execute("SELECT id FROM artifacts WHERE req_id = ?", (r["id"],)).fetchall()
    r["artifact_ids"] = [a["id"] for a in arts]
    r["artifact_count"] = len(r["artifact_ids"])
    return r


def artifact_row_to_json(row, conn):
    a = dict(row)
    versions = conn.execute(
        "SELECT version, path, size, note, created_at FROM artifact_versions "
        "WHERE artifact_id = ? ORDER BY rowid DESC", (a["id"],)
    ).fetchall()
    a["history"] = [
        {"v": v["version"], "path": v["path"], "size": v["size"], "note": v["note"], "at": v["created_at"]}
        for v in versions
    ]
    a["rev"] = len(a["history"])
    return a


def task_row_to_json(row):
    t = dict(row)
    t["reqId"] = t.pop("req_id", None)
    t["updated"] = t.pop("updated_at", "")
    return t


def todo_row_to_json(row):
    t = dict(row)
    t["reqId"] = t.pop("req_id", None)
    t["done"] = bool(t["done"])
    t["urgent"] = bool(t["urgent"])
    t["group"] = t.pop("grp", "today")
    return t


def skill_row_to_json(row):
    s = dict(row)
    s["group"] = s.pop("grp")
    s["enabled"] = bool(s["enabled"])
    s["desc"] = s.pop("description")
    s["source"] = s.get("source") or "repo"
    s.pop("content", None)
    return s


def read_config(conn):
    cfg = {}
    for row in conn.execute("SELECT key, value FROM config"):
        try:
            cfg[row["key"]] = json.loads(row["value"])
        except ValueError:
            cfg[row["key"]] = row["value"]
    merged = dict(db.DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


def next_ref(conn):
    rows = conn.execute("SELECT ref FROM requirements WHERE ref LIKE 'REQ-%'").fetchall()
    nums = []
    for r in rows:
        m = re.match(r"REQ-(\d+)", r["ref"] or "")
        if m:
            nums.append(int(m.group(1)))
    return "REQ-%03d" % ((max(nums) if nums else 0) + 1)


def add_audit(conn, action, target_type=None, target_id=None, detail="", actor="林轩"):
    db.log_audit_row(conn, actor, action, target_type, target_id, detail)
    conn.commit()


def artifact_content(art, req):
    """Generate a readable markdown body for a generated artifact."""
    lines = [
        f"# {art['name']}",
        "",
        f"- 需求编号：{art.get('ref') or '—'}",
        f"- 归属：{'售前' if art.get('role') == 'sa' else '产品'}",
        f"- 类型：{art.get('type')}",
        f"- 版本：{art.get('version')}",
        f"- 负责人：{art.get('author')}",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 一、需求背景",
        "",
        (req["raw_text"] if req else "（无关联需求）"),
        "",
        "## 二、七要素",
        "",
        "| 要素 | 内容 |",
        "| --- | --- |",
    ]
    if req:
        for f in json.loads(req["fields"] or "[]"):
            lines.append(f"| {f.get('k')} | {f.get('v')} |")
    lines += [
        "",
        "## 三、澄清记录",
        "",
    ]
    if req:
        for qa in json.loads(req["qa"] or "[]"):
            lines.append(f"- **Q**：{qa.get('q')}  ")
            lines.append(f"  **A**：{qa.get('a')}")
    lines += [
        "",
        "## 四、交付说明",
        "",
        "- 售前材料沉淀到产物库，保留存储地址与历史版本，可随时回溯。"
        if art.get("role") == "sa" else
        "- 产品需求经 Linear MCP 推送后由研发接手，PRD / 原型 / 交底书归档在本产物库。",
        "",
        "---",
        "由 WorkAgent 自动生成，请在归档前人工复核。",
        "",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ API
class ApiState:
    def __init__(self):
        self.conn = db.connect()
        self.conn.executescript(db.SCHEMA)
        db.seed_if_empty(self.conn)
        self.lock = threading.Lock()


STATE = None


def get_conn():
    # sqlite3 connections are not shareable across threads: create per request.
    return db.connect()


def api_bootstrap(conn, query):
    reqs = [req_row_to_json(r, conn) for r in conn.execute("SELECT * FROM requirements ORDER BY created_at DESC").fetchall()]
    arts = [artifact_row_to_json(r, conn) for r in conn.execute("SELECT * FROM artifacts ORDER BY created_at DESC").fetchall()]
    tasks = [task_row_to_json(r) for r in conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()]
    todos = [todo_row_to_json(r) for r in conn.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()]
    skills = [skill_row_to_json(r) for r in conn.execute("SELECT * FROM skills ORDER BY rowid").fetchall()]
    return {
        "requirements": reqs,
        "artifacts": arts,
        "tasks": tasks,
        "todos": todos,
        "skills": skills,
        "config": read_config(conn),
        "linearSeq": _linear_seq(conn),
    }


def _linear_seq(conn):
    rows = conn.execute("SELECT linear_id FROM requirements WHERE linear_id IS NOT NULL").fetchall()
    nums = [int(r["linear_id"].split("-")[1]) for r in rows if r["linear_id"] and "-" in r["linear_id"]]
    return max(nums) + 1 if nums else 142


def api_requirements(conn, query, method, body, path):
    m = re.match(r"^/api/requirements/([^/]+)(?:/(\w+))?/?$", path)
    if not m:
        # collection
        if method == "GET":
            rows = conn.execute("SELECT * FROM requirements ORDER BY created_at DESC").fetchall()
            return 200, [req_row_to_json(r, conn) for r in rows]
        if method == "POST":
            title = (body.get("title") or "").strip()
            if not title:
                return 400, {"error": "title is required"}
            rid = "r" + uuid.uuid4().hex[:8]
            fields = [{"k": n, "v": "待补充", "ok": False} for n in db.ELEMENT_NAMES]
            fields[5] = {"k": "优先级", "v": body.get("priority", "中"), "ok": True}
            data = dict(
                id=rid, ref=next_ref(conn), title=title, role=body.get("role", "sa"),
                source=body.get("source", "客户转述"), client=body.get("client", "待补充"),
                stage="raw", priority=body.get("priority", "中"), owner=body.get("owner", "林轩"),
                team="SA" if body.get("role", "sa") == "sa" else "PROD",
                project=body.get("project", "待归类"),
                deliverable=body.get("deliverable", "技术方案 · 标书" if body.get("role", "sa") == "sa" else "PRD · 原型 · 技术交底书"),
                raw_text=body.get("raw", "") or "原始输入待补充。", fields=fields,
                qa=[{"q": "请补充目标用户与使用场景", "a": "待需求方确认。"}],
                updated_at="刚刚",
            )
            db.insert_requirement(conn, data)
            task = dict(
                id="t" + uuid.uuid4().hex[:8], side=body.get("role", "sa"),
                title=title[:24], status="queued", step=0, req_id=rid,
                owner=body.get("owner", "林轩"), elapsed="—", last="等待调度", started="—",
                note="新建需求已进入整理队列，将依次执行输入清洗、要素抽取与澄清问题生成。",
                updated_at="排队中",
            )
            db.insert_task(conn, task)
            add_audit(conn, "requirement.create", "requirement", rid, title)
            conn.commit()
            return 201, req_row_to_json(conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone(), conn)
        return 405, {"error": "method not allowed"}

    rid, action = m.group(1), m.group(2)
    row = conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone()
    if not row:
        return 404, {"error": "requirement not found"}

    if method == "GET" and not action:
        return 200, req_row_to_json(row, conn)

    if method == "PATCH" and not action:
        allowed = ["title", "client", "priority", "owner", "source", "project", "deliverable", "stage", "elements"]
        sets, vals = [], []
        for key in allowed:
            if key in body:
                col = {"elements": "elements"}.get(key, key)
                sets.append(f"{col}=?")
                vals.append(body[key])
        if "fields" in body:
            sets.append("fields=?")
            vals.append(json.dumps(body["fields"], ensure_ascii=False))
            sets.append("elements=?")
            vals.append(sum(1 for f in body["fields"] if f.get("ok")))
        if "qa" in body:
            sets.append("qa=?")
            vals.append(json.dumps(body["qa"], ensure_ascii=False))
        if not sets:
            return 400, {"error": "nothing to update"}
        sets.append("updated_at=?")
        vals.append("刚刚")
        vals.append(rid)
        conn.execute(f"UPDATE requirements SET {', '.join(sets)} WHERE id=?", vals)
        add_audit(conn, "requirement.update", "requirement", rid, row["title"])
        return 200, req_row_to_json(conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone(), conn)

    if method == "DELETE" and not action:
        conn.execute("DELETE FROM requirements WHERE id=?", (rid,))
        conn.execute("UPDATE artifacts SET req_id=NULL WHERE req_id=?", (rid,))
        conn.execute("UPDATE tasks SET req_id=NULL WHERE req_id=?", (rid,))
        add_audit(conn, "requirement.delete", "requirement", rid, row["title"])
        conn.commit()
        return 200, {"ok": True}

    if action == "element" and method == "POST":
        idx = body.get("index")
        value = body.get("value")
        fields = json.loads(row["fields"] or "[]")
        if not isinstance(idx, int) or idx < 0 or idx >= len(fields):
            return 400, {"error": "invalid element index"}
        fields[idx]["v"] = value
        fields[idx]["ok"] = bool(value) and not str(value).startswith("待")
        elements = sum(1 for f in fields if f.get("ok"))
        stage = row["stage"]
        if elements >= 7 and stage in ("raw", "clarify", "structured"):
            stage = "ready"
        conn.execute(
            "UPDATE requirements SET fields=?, elements=?, stage=?, updated_at=? WHERE id=?",
            (json.dumps(fields, ensure_ascii=False), elements, stage, "刚刚", rid),
        )
        add_audit(conn, "requirement.element", "requirement", rid, f"{fields[idx]['k']} → {value}")
        conn.commit()
        return 200, req_row_to_json(conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone(), conn)

    if action == "export" and method == "POST":
        arts = conn.execute("SELECT * FROM artifacts WHERE req_id=?", (rid,)).fetchall()
        payload = {
            "requirement": req_row_to_json(row, conn),
            "artifacts": [artifact_row_to_json(a, conn) for a in arts],
            "exported_at": datetime.now().isoformat(timespec="seconds"),
        }
        add_audit(conn, "requirement.export", "requirement", rid, "导出交付包")
        conn.commit()
        return 200, payload

    return 404, {"error": "unknown requirement action"}


def api_artifacts(conn, query, method, body, path):
    m = re.match(r"^/api/artifacts/([^/]+)(?:/(\w+))?/?$", path)
    if not m:
        if method == "GET":
            rows = conn.execute("SELECT * FROM artifacts ORDER BY created_at DESC").fetchall()
            return 200, [artifact_row_to_json(r, conn) for r in rows]
        if method == "POST":
            name = (body.get("name") or "").strip()
            if not name:
                return 400, {"error": "name is required"}
            req_id = body.get("reqId") or body.get("req_id")
            req = conn.execute("SELECT * FROM requirements WHERE id=?", (req_id,)).fetchone() if req_id else None
            role = req["role"] if req else body.get("role", "sa")
            ref = req["ref"] if req else "REQ-XXX"
            art = dict(
                id="a" + uuid.uuid4().hex[:8], req_id=req_id, ref=ref, name=name,
                type=body.get("type", "方案"), role=role, version=body.get("version", "v1.0"),
                size=body.get("size", "—"), author=body.get("author") or (req["owner"] if req else "林轩"),
                note=body.get("note", "由 WorkAgent 生成"), updated_at="刚刚", created_at=now_str_safe(),
            )
            art["path"] = body.get("path") or db.make_artifact_path(art)
            db.insert_artifact(conn, art)
            full = db.write_artifact_file(art, artifact_content(art, req))
            conn.execute("UPDATE artifacts SET size=? WHERE id=?", (f"{os.path.getsize(full)/1024:.0f} KB", art["id"]))
            if req:
                conn.execute("UPDATE requirements SET stage='done', updated_at='刚刚' WHERE id=?", (req_id,))
                conn.execute(
                    "UPDATE tasks SET status='done', step=5, updated_at='刚刚', last='刚刚 已沉淀产物' "
                    "WHERE req_id=? AND status!='done'", (req_id,)
                )
            add_audit(conn, "artifact.create", "artifact", art["id"], art["path"])
            conn.commit()
            row = conn.execute("SELECT * FROM artifacts WHERE id=?", (art["id"],)).fetchone()
            return 201, artifact_row_to_json(row, conn)
        return 405, {"error": "method not allowed"}

    aid, action = m.group(1), m.group(2)
    row = conn.execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()
    if not row:
        return 404, {"error": "artifact not found"}

    if method == "GET" and not action:
        return 200, artifact_row_to_json(row, conn)

    if method == "DELETE" and not action:
        conn.execute("DELETE FROM artifact_versions WHERE artifact_id=?", (aid,))
        conn.execute("DELETE FROM artifacts WHERE id=?", (aid,))
        add_audit(conn, "artifact.delete", "artifact", aid, row["name"])
        conn.commit()
        return 200, {"ok": True}

    if action == "content" and method == "GET":
        req = conn.execute("SELECT * FROM requirements WHERE id=?", (row["req_id"],)).fetchone() if row["req_id"] else None
        return 200, {"markdown": artifact_content(dict(row), req)}

    if action == "versions" and method == "GET":
        return 200, artifact_row_to_json(row, conn)["history"]

    return 404, {"error": "unknown artifact action"}


def now_str_safe():
    return datetime.now().strftime("%m-%d %H:%M")


def api_tasks(conn, query, method, body, path):
    m = re.match(r"^/api/tasks/([^/]+)(?:/(\w+))?/?$", path)
    if m:
        tid, action = m.group(1), m.group(2)
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not row:
            return 404, {"error": "task not found"}
        if method == "GET" and not action:
            return 200, task_row_to_json(row)
        if method == "POST" and action in ("retry", "pause", "resume", "cancel"):
            # retry/resume restart from the current step; pause holds the step; cancel keeps progress
            if action in ("retry", "resume"):
                step = 0 if action == "retry" else row["step"]
                conn.execute(
                    "UPDATE tasks SET status='running', step=?, updated_at=? WHERE id=?",
                    (step, "刚刚", tid),
                )
            else:
                next_status = "queued" if action == "pause" else "blocked"
                conn.execute(
                    "UPDATE tasks SET status=?, updated_at=? WHERE id=?",
                    (next_status, "—", tid),
                )
            add_audit(conn, f"task.{action}", "task", tid, row["title"])
            conn.commit()
            return 200, task_row_to_json(conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone())
        if method == "DELETE" and not action:
            conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
            add_audit(conn, "task.delete", "task", tid, row["title"])
            conn.commit()
            return 200, {"ok": True}

    if method == "GET":
        rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
        return 200, [task_row_to_json(r) for r in rows]
    if method == "POST":
        task = dict(
            id="t" + uuid.uuid4().hex[:8], side=body.get("side", "sa"), title=body.get("title", "新任务"),
            status="queued", step=0, req_id=body.get("reqId"), owner=body.get("owner", "林轩"),
            elapsed="—", last="等待调度", started="—", note=body.get("note", ""), updated_at="排队中",
        )
        db.insert_task(conn, task)
        conn.commit()
        return 201, task_row_to_json(conn.execute("SELECT * FROM tasks WHERE id=?", (task["id"],)).fetchone())
    return 405, {"error": "method not allowed"}


def api_todos(conn, query, method, body, path):
    m = re.match(r"^/api/todos/([^/]+)/?$", path)
    if m and method in ("PATCH", "DELETE"):
        tid = m.group(1)
        row = conn.execute("SELECT * FROM todos WHERE id=?", (tid,)).fetchone()
        if not row:
            return 404, {"error": "todo not found"}
        if method == "DELETE":
            conn.execute("DELETE FROM todos WHERE id=?", (tid,))
            add_audit(conn, "todo.delete", "todo", tid, row["title"])
        else:
            sets, vals = [], []
            for key in ("title", "pri", "due", "grp", "role"):
                if key in body:
                    sets.append(f"{key}=?")
                    vals.append(body[key])
            if "done" in body:
                sets.append("done=?")
                vals.append(1 if body["done"] else 0)
            if not sets:
                return 400, {"error": "nothing to update"}
            vals.append(tid)
            conn.execute(f"UPDATE todos SET {', '.join(sets)} WHERE id=?", vals)
            add_audit(conn, "todo.update", "todo", tid, row["title"])
        conn.commit()
        return 200, {"ok": True}

    if method == "GET":
        rows = conn.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()
        return 200, [todo_row_to_json(r) for r in rows]
    if method == "POST":
        tid = "td" + uuid.uuid4().hex[:6]
        conn.execute(
            """INSERT INTO todos (id,title,pri,due,grp,role,req_id,done,urgent,created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (tid, body.get("title", ""), body.get("pri", "mid"), body.get("due", "今天"),
             body.get("group", "today"), body.get("role", "通用"), body.get("reqId"), 0,
             1 if body.get("urgent") else 0, now_str_safe()),
        )
        add_audit(conn, "todo.create", "todo", tid, body.get("title", ""))
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id=?", (tid,)).fetchone()
        return 201, todo_row_to_json(row)
    return 405, {"error": "method not allowed"}


def api_skills(conn, query, method, body, path):
    m = re.match(r"^/api/skills/([^/]+)(?:/(\w+))?/?$", path)
    if m and method in ("PATCH", "PUT") and not m.group(2):
        slug = m.group(1)
        enabled = 1 if body.get("enabled") else 0
        conn.execute("UPDATE skills SET enabled=? WHERE slug=?", (enabled, slug))
        add_audit(conn, "skill.toggle", "skill", slug, "启用" if enabled else "停用")
        conn.commit()
        row = conn.execute("SELECT * FROM skills WHERE slug=?", (slug,)).fetchone()
        if not row:
            return 404, {"error": "skill not found"}
        return 200, skill_row_to_json(row)
    if m and m.group(2) == "content":
        slug = m.group(1)
        row = conn.execute("SELECT * FROM skills WHERE slug=?", (slug,)).fetchone()
        if not row:
            return 404, {"error": "skill not found"}
        docs = conn.execute(
            "SELECT id, filename, title, size, created_at FROM skill_docs WHERE slug=? ORDER BY id DESC", (slug,)
        ).fetchall()
        sups = conn.execute(
            "SELECT summary, appended_chars, created_at FROM skill_supplements WHERE slug=? ORDER BY id DESC", (slug,)
        ).fetchall()
        return 200, {
            "slug": slug,
            "content": row["content"] or "",
            "docs": [dict(d) for d in docs],
            "supplements": [dict(s) for s in sups],
        }
    if method == "GET":
        return 200, [skill_row_to_json(r) for r in conn.execute("SELECT * FROM skills ORDER BY rowid").fetchall()]
    return 405, {"error": "method not allowed"}


def parse_markdown_skill(content, filename):
    """Extract a title, description and optional frontmatter from a Markdown skill file."""
    title, description, body = "", "", content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            meta, body = parts[1], parts[2]
            for line in meta.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip().lower(), v.strip().strip('"').strip("'")
                    if k in ("name", "title") and not title:
                        title = v
                    elif k in ("description", "desc", "summary") and not description:
                        description = v
    if not title:
        for line in body.splitlines():
            if line.strip().startswith("#"):
                title = line.strip().lstrip("#").strip()
                break
    if not title:
        title = os.path.splitext(filename)[0] if filename else "未命名 Skill"
    if not description:
        for line in body.splitlines():
            t = line.strip()
            if t and not t.startswith("#") and not t.startswith("---"):
                description = t[:120]
                break
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug or not re.search(r"[a-z]", slug):
        base = os.path.splitext(filename or "")[0]
        slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    if not slug or not re.search(r"[a-z]", slug):
        slug = "skill-" + uuid.uuid4().hex[:6]
    return title, description, slug, body.strip()


def api_skills_upload(conn, query, method, body, path):
    """POST /api/skills/upload  {filename, content, mode: new|merge, target: slug}"""
    if method != "POST":
        return 405, {"error": "method not allowed"}
    content = body.get("content") or ""
    filename = body.get("filename") or "skill.md"
    if not content.strip():
        return 400, {"error": "文件内容为空"}
    if len(content) > 2_000_000:
        return 400, {"error": "文件超过 2MB 限制"}
    title, description, slug, md_body = parse_markdown_skill(content, filename)
    mode = body.get("mode") or "new"
    actor = body.get("actor") or "林轩"

    if mode == "merge":
        target = (body.get("target") or "").strip()
        row = conn.execute("SELECT * FROM skills WHERE slug=?", (target,)).fetchone()
        if not row:
            return 404, {"error": "目标 Skill 不存在"}
        appended = "\n\n<!-- 来自 " + filename + " -->\n" + md_body
        new_content = (row["content"] or row["description"] or "") + appended
        new_desc = (row["description"] or "") + "\n\n补充：" + description[:160]
        version = bump_version(row["version"] or "v1.0")
        conn.execute(
            "UPDATE skills SET content=?, description=?, version=? WHERE slug=?",
            (new_content, new_desc, version, target),
        )
        doc_id = conn.execute(
            "INSERT INTO skill_docs (slug,filename,title,content,size,uploaded_by,created_at) VALUES (?,?,?,?,?,?,?)",
            (target, filename, title, content, len(content.encode("utf-8")), actor, now_str_safe()),
        ).lastrowid
        conn.execute(
            "INSERT INTO skill_supplements (slug,doc_id,summary,appended_chars,created_at) VALUES (?,?,?,?,?)",
            (target, doc_id, description[:200], len(appended), now_str_safe()),
        )
        add_audit(conn, "skill.merge", "skill", target, f"{filename} → {version}")
        conn.commit()
        updated = conn.execute("SELECT * FROM skills WHERE slug=?", (target,)).fetchone()
        return 200, {"mode": "merge", "skill": skill_row_to_json(updated), "appended_chars": len(appended)}

    existing = conn.execute("SELECT * FROM skills WHERE slug=?", (slug,)).fetchone()
    if existing:
        suffix = "skill-" + uuid.uuid4().hex[:4]
        slug = f"{slug}-{suffix}"
    grp = body.get("group") or "custom"
    if grp not in ("pm", "prd", "sa", "content", "custom"):
        grp = "custom"
    name = body.get("name") or title
    conn.execute(
        """INSERT INTO skills (slug,name,grp,glyph,description,version,calls,enabled,source,content)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (slug, name[:40], grp, (name[:2] or "SK").upper(), description, "v1.0", 0, 1, "uploaded", md_body),
    )
    doc_id = conn.execute(
        "INSERT INTO skill_docs (slug,filename,title,content,size,uploaded_by,created_at) VALUES (?,?,?,?,?,?,?)",
        (slug, filename, title, content, len(content.encode("utf-8")), actor, now_str_safe()),
    ).lastrowid
    conn.execute(
        "INSERT INTO skill_supplements (slug,doc_id,summary,appended_chars,created_at) VALUES (?,?,?,?,?)",
        (slug, doc_id, description[:200], len(md_body), now_str_safe()),
    )
    add_audit(conn, "skill.upload", "skill", slug, filename)
    conn.commit()
    row = conn.execute("SELECT * FROM skills WHERE slug=?", (slug,)).fetchone()
    return 201, {"mode": "new", "skill": skill_row_to_json(row)}


def bump_version(v):
    m = re.match(r"v?(\d+)\.(\d+)", v or "")
    if not m:
        return "v1.1"
    return f"v{m.group(1)}.{int(m.group(2)) + 1}"


# ------------------------------------------------------------------ auth
def create_session(conn, user_id):
    import secrets
    from datetime import timedelta
    token = secrets.token_urlsafe(32)
    expires = (datetime.now() + timedelta(hours=SESSION_TTL_HOURS)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO sessions (token,user_id,created_at,expires_at) VALUES (?,?,?,?)",
        (token, user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expires),
    )
    return token, expires


def bearer_token(headers):
    auth = headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def resolve_user(conn, token):
    if not token:
        return None
    row = conn.execute(
        """SELECT u.id, u.username, u.display_name, u.role, s.expires_at
           FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ?""",
        (token,),
    ).fetchone()
    if not row:
        return None
    if row["expires_at"] < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        conn.commit()
        return None
    return dict(row)


def api_auth_login(conn, query, method, body, path):
    if method != "POST":
        return 405, {"error": "method not allowed"}
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not row or not db.verify_password(password, row["password_hash"]):
        add_audit(conn, "auth.login_failed", "user", username, "密码错误或用户不存在")
        conn.commit()
        return 401, {"error": "用户名或密码错误"}
    token, expires = create_session(conn, row["id"])
    conn.execute("UPDATE users SET last_login_at=? WHERE id=?",
                 (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row["id"]))
    add_audit(conn, "auth.login", "user", username, "登录成功")
    conn.commit()
    return 200, {
        "token": token, "expires_at": expires,
        "user": {"id": row["id"], "username": row["username"],
                 "display_name": row["display_name"] or row["username"], "role": row["role"]},
    }


def api_auth_me(conn, query, method, body, path, user=None, token=None):
    if not user:
        return 401, {"error": "未登录"}
    return 200, {"user": {"id": user["id"], "username": user["username"],
                          "display_name": user["display_name"], "role": user["role"]}}


def api_auth_logout(conn, query, method, body, path, user=None, token=None):
    if token:
        conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        conn.commit()
    return 200, {"ok": True}


def api_auth_password(conn, query, method, body, path, user=None, token=None):
    if method != "POST":
        return 405, {"error": "method not allowed"}
    if not user:
        return 401, {"error": "未登录"}
    old = body.get("old_password") or ""
    new = body.get("new_password") or ""
    if len(new) < 8:
        return 400, {"error": "新密码至少 8 位"}
    row = conn.execute("SELECT * FROM users WHERE id=?", (user["id"],)).fetchone()
    if not row or not db.verify_password(old, row["password_hash"]):
        return 400, {"error": "原密码不正确"}
    conn.execute("UPDATE users SET password_hash=? WHERE id=?", (db.hash_password(new), user["id"]))
    # invalidate every other session for this user, keep the current one
    conn.execute("DELETE FROM sessions WHERE user_id=? AND token!=?", (user["id"], token or ""))
    add_audit(conn, "auth.password", "user", user["username"], "修改密码")
    conn.commit()
    return 200, {"ok": True}


def api_config(conn, query, method, body, path):
    if method == "GET":
        return 200, read_config(conn)
    if method in ("PUT", "POST"):
        for key, value in body.items():
            if key == "apiKey" and not value:
                continue
            conn.execute(
                "INSERT INTO config (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, json.dumps(value, ensure_ascii=False)),
            )
        add_audit(conn, "config.update", "config", "global", "更新模型与接入配置")
        conn.commit()
        return 200, read_config(conn)
    return 405, {"error": "method not allowed"}


def api_linear_push(conn, query, method, body, path):
    """Mock Linear MCP push. Only product requirements are allowed."""
    if method != "POST":
        return 405, {"error": "method not allowed"}
    rid = body.get("reqId")
    row = conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone()
    if not row:
        return 404, {"error": "requirement not found"}
    if row["role"] == "sa":
        return 400, {"error": "售前需求不走 Linear，请沉淀产物库"}
    issue = "LIN-%d" % _linear_seq(conn)
    conn.execute(
        "UPDATE requirements SET linear_status='synced', linear_id=?, stage='done', updated_at='刚刚' WHERE id=?",
        (issue, rid),
    )
    conn.execute(
        "UPDATE tasks SET status='done', step=5, updated_at='刚刚', last=? WHERE req_id=? AND status!='done'",
        ("刚刚 已推送 " + issue, rid),
    )
    add_audit(conn, "linear.push", "requirement", rid, issue)
    conn.commit()
    return 200, {
        "issue": issue,
        "team": row["team"] or "PROD",
        "requirement": req_row_to_json(conn.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone(), conn),
    }


def api_search(conn, query):
    q = (query.get("q", [""])[0] or "").strip()
    if not q:
        return 200, {"requirements": [], "artifacts": [], "tasks": []}
    like = f"%{q}%"
    reqs = conn.execute(
        "SELECT * FROM requirements WHERE title LIKE ? OR client LIKE ? OR ref LIKE ? OR raw_text LIKE ?",
        (like, like, like, like),
    ).fetchall()
    arts = conn.execute(
        "SELECT * FROM artifacts WHERE name LIKE ? OR path LIKE ? OR ref LIKE ?", (like, like, like)
    ).fetchall()
    tasks = conn.execute("SELECT * FROM tasks WHERE title LIKE ? OR note LIKE ?", (like, like)).fetchall()
    return 200, {
        "requirements": [req_row_to_json(r, conn) for r in reqs],
        "artifacts": [artifact_row_to_json(a, conn) for a in arts],
        "tasks": [task_row_to_json(t) for t in tasks],
    }


def api_audit(conn, query):
    limit = int(query.get("limit", ["80"])[0])
    rows = conn.execute("SELECT * FROM audit ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return 200, [dict(r) for r in rows]


def api_stats(conn, query):
    total_req = conn.execute("SELECT COUNT(*) AS n FROM requirements").fetchone()["n"]
    by_stage = {r["stage"]: r["n"] for r in conn.execute(
        "SELECT stage, COUNT(*) AS n FROM requirements GROUP BY stage").fetchall()}
    art_rows = conn.execute("SELECT type, COUNT(*) AS n FROM artifacts GROUP BY type").fetchall()
    audit_count = conn.execute("SELECT COUNT(*) AS n FROM audit").fetchone()["n"]
    return 200, {
        "requirements": total_req,
        "by_stage": by_stage,
        "artifacts_by_type": {r["type"]: r["n"] for r in art_rows},
        "audit_count": audit_count,
        "uptime_seconds": int(time.time() - STARTED_AT),
    }


ROUTES = [
    (r"^/api/health$", lambda c, q, m, b, p: (200, {"ok": True, "service": "workagent-console", "time": datetime.now().isoformat(timespec="seconds")})),
    (r"^/api/auth/login$", api_auth_login),
    (r"^/api/auth/me$", api_auth_me),
    (r"^/api/auth/logout$", api_auth_logout),
    (r"^/api/auth/password$", api_auth_password),
    (r"^/api/bootstrap$", lambda c, q, m, b, p: (200, api_bootstrap(c, q)) if m == "GET" else (405, {})),
    (r"^/api/stats$", lambda c, q, m, b, p: api_stats(c, q)),
    (r"^/api/search$", lambda c, q, m, b, p: api_search(c, q)),
    (r"^/api/audit$", lambda c, q, m, b, p: api_audit(c, q)),
    (r"^/api/requirements(/[^/]+)?(/[^/]+)?/?$", lambda c, q, m, b, p: api_requirements(c, q, m, b, p)),
    (r"^/api/artifacts(/[^/]+)?(/[^/]+)?/?$", lambda c, q, m, b, p: api_artifacts(c, q, m, b, p)),
    (r"^/api/tasks(/[^/]+)?(/[^/]+)?/?$", lambda c, q, m, b, p: api_tasks(c, q, m, b, p)),
    (r"^/api/todos(/[^/]+)?/?$", lambda c, q, m, b, p: api_todos(c, q, m, b, p)),
    (r"^/api/skills/upload$", api_skills_upload),
    (r"^/api/skills(/[^/]+)?(/[^/]+)?/?$", lambda c, q, m, b, p: api_skills(c, q, m, b, p)),
    (r"^/api/config$", lambda c, q, m, b, p: api_config(c, q, m, b, p)),
    (r"^/api/mcp/linear/push$", lambda c, q, m, b, p: api_linear_push(c, q, m, b, p)),
]


PUBLIC_PATHS = ("/api/health", "/api/auth/")


def dispatch(method, path, query, body, user=None, token=None):
    conn = get_conn()
    try:
        for pattern, handler in ROUTES:
            if re.match(pattern, path):
                if handler in (api_auth_me, api_auth_logout, api_auth_password):
                    return handler(conn, query, method, body, path, user=user, token=token)
                if handler is api_auth_login:
                    return handler(conn, query, method, body, path)
                return handler(conn, query, method, body, path)
        return 404, {"error": "not found", "path": path}
    finally:
        conn.close()


# ------------------------------------------------------------------ worker
def task_worker():
    """Advance running tasks so the console reflects live execution."""
    while True:
        time.sleep(6)
        try:
            conn = db.connect()
            rows = conn.execute("SELECT * FROM tasks WHERE status='running'").fetchall()
            for row in rows:
                step = row["step"]
                if step >= 4:
                    new_status, new_step = "done", 5
                else:
                    new_status, new_step = "running", step + 1
                conn.execute(
                    "UPDATE tasks SET step=?, status=?, updated_at=? WHERE id=?",
                    (new_step, new_status, now_str_safe(), row["id"]),
                )
            if rows:
                conn.commit()
            conn.close()
        except Exception:
            traceback.print_exc()


class Handler(SimpleHTTPRequestHandler):
    server_version = "WorkAgentConsole/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,X-Actor")
        self.send_header("Access-Control-Max-Age", "86400")

    def _json(self, status, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _serve_api(self, method):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        body = parse_body(self) if method in ("POST", "PATCH", "PUT") else {}
        token = bearer_token(self.headers)
        path = parsed.path.rstrip("/") or "/"
        user = None
        conn = get_conn()
        try:
            user = resolve_user(conn, token)
        finally:
            conn.close()
        if not path.startswith(PUBLIC_PATHS) and user is None:
            self._json(401, {"error": "未登录或登录已过期"})
            return
        try:
            status, payload = dispatch(method, path, query, body, user=user, token=token)
        except Exception as exc:
            traceback.print_exc()
            status, payload = 500, {"error": str(exc)}
        self._json(status, payload)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/favicon.ico":
            # keep browsers quiet; the page uses an inline SVG icon
            self.send_response(204)
            self._cors()
            self.end_headers()
            return
        if parsed.path.startswith("/api/"):
            return self._serve_api("GET")
        # artifact file download
        if parsed.path.startswith("/download/"):
            rel = unquote(parsed.path[len("/download/"):])
            try:
                full = db.resolve_output_path("./output/" + rel)
            except ValueError:
                return self._json(400, {"error": "invalid path"})
            if not os.path.isfile(full):
                return self._json(404, {"error": "file not found"})
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
            data = open(full, "rb").read()
            filename = os.path.basename(full)
            ascii_name = filename.encode("ascii", "ignore").decode() or "artifact"
            self.send_response(200)
            self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") else ""))
            # RFC 5987: keep a plain ASCII fallback and the UTF-8 name for browsers
            from urllib.parse import quote
            self.send_header(
                "Content-Disposition",
                f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{quote(filename)}",
            )
            self.send_header("Content-Length", str(len(data)))
            self._cors()
            self.end_headers()
            self.wfile.write(data)
            return
        if parsed.path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        return self._serve_api("POST") if urlparse(self.path).path.startswith("/api/") else self._json(404, {"error": "not found"})

    def do_PATCH(self):
        return self._serve_api("PATCH")

    def do_PUT(self):
        return self._serve_api("PUT")

    def do_DELETE(self):
        return self._serve_api("DELETE")

    def log_message(self, fmt, *args):
        try:
            text = fmt % args
        except Exception:
            text = " ".join(str(a) for a in args)
        if "/api/" in text:
            print("[api]", self.address_string(), text)


def main():
    parser = argparse.ArgumentParser(description="WorkAgent Console API")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", default=HOST)
    args = parser.parse_args()

    conn = db.connect()
    conn.executescript(db.SCHEMA)
    created = db.seed_if_empty(conn)
    conn.close()

    threading.Thread(target=task_worker, daemon=True).start()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"WorkAgent Console running at http://{args.host}:{args.port}/")
    print(f"  API : http://{args.host}:{args.port}/api/health")
    print(f"  DB  : {db.DB_PATH}")
    print(f"  Data: {db.OUTPUT_DIR}")
    if created:
        print(f"  初始账号已创建: {created[0]} / {created[1]}  （登录后请在「账户设置」修改密码）")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
