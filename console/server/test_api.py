import json, os, urllib.request, urllib.error, io
from urllib.parse import quote

B = "http://127.0.0.1:8765"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "output")
TOKEN = {"value": None}

def call(method, path, body=None, token=True):
    headers = {"Content-Type": "application/json"}
    if token and TOKEN["value"]:
        headers["Authorization"] = "Bearer " + TOKEN["value"]
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(B + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw}

ok = True
def check(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + label + ((" | " + str(extra)) if extra != "" else ""))

# ---- auth
s, _ = call("GET", "/api/bootstrap", token=False)
check("unauthenticated bootstrap rejected", s == 401, s)
s, bad = call("POST", "/api/auth/login", {"username": "admin", "password": "wrong"}, token=False)
check("wrong password rejected", s == 401)
s, login = call("POST", "/api/auth/login", {"username": "admin", "password": "admin123"}, token=False)
check("login succeeds", s == 200 and login.get("token"), login.get("user", {}).get("username"))
TOKEN["value"] = login["token"]
s, me = call("GET", "/api/auth/me")
check("me returns user", s == 200 and me["user"]["username"] == "admin")

s, boot = call("GET", "/api/bootstrap")
check("bootstrap authorized", s == 200 and len(boot["requirements"]) == 12,
      f'{len(boot.get("requirements", []))} requirements')

# ---- requirements from chat
s, new = call("POST", "/api/requirements",
              {"title": "客户希望告警直接派单", "role": "sa", "source": "对话整理", "raw": "告警生成工单派给车间负责人"})
check("requirement created from message", s == 201 and new["ref"].startswith("REQ-"), new["ref"])
rid = new["id"]
s, upd = call("POST", f"/api/requirements/{rid}/element", {"index": 1, "value": "车间安全员"})
check("element edit persists", upd["fields"][1]["v"] == "车间安全员")

# ---- artifacts
s, art = call("POST", "/api/artifacts", {"reqId": rid, "name": "恒信精工 · 交付方案", "type": "方案"})
check("artifact create", s == 201, art["path"])
rel = art["path"].replace("./output/", "")
check("artifact file on disk", os.path.isfile(os.path.join(OUT, rel)))
with urllib.request.urlopen(B + "/download/" + quote(rel)) as r:
    body = r.read().decode("utf-8")
check("download works", "恒信精工" in body)

# ---- SA guard + PM linear
s, err = call("POST", "/api/mcp/linear/push", {"reqId": rid})
check("SA linear push rejected", s == 400)
s, lin = call("POST", "/api/mcp/linear/push", {"reqId": "r3"})
check("PM linear push", s == 200 and lin["issue"].startswith("LIN-"), lin.get("issue"))

# ---- skills upload: new
md = """---
name: 威胁建模能力
description: 对架构做 STRIDE 威胁建模并输出缓解建议
---

# 威胁建模能力

## 输入
- 架构图或组件清单

## 输出
- 威胁清单与缓解措施
"""
s, up = call("POST", "/api/skills/upload",
             {"filename": "threat-model.md", "content": md, "mode": "new"})
check("skill new upload", s == 201 and up["skill"]["source"] == "uploaded", up.get("skill", {}).get("slug"))
new_slug = up["skill"]["slug"]

# ---- skills upload: merge into repo skill
md2 = "# PRD 补充规则\n\n- 验收标准必须可量化\n- 每个功能需给出埋点建议\n"
s, before = call("GET", "/api/skills/prd-writer/content")
v_before = next(sk["version"] for sk in call("GET", "/api/skills")[1] if sk["slug"] == "prd-writer")
s, mg = call("POST", "/api/skills/upload",
             {"filename": "prd-rules.md", "content": md2, "mode": "merge", "target": "prd-writer"})
check("skill merge upload", s == 200 and mg["skill"]["version"] != v_before,
      f'{v_before} -> {mg["skill"]["version"]}')
s, after = call("GET", "/api/skills/prd-writer/content")
check("merged content appended", "验收标准必须可量化" in after["content"] and len(after["content"]) > len(before["content"]))
check("supplement history recorded", len(after["supplements"]) == 1)

# ---- todo / skill toggle / config
s, todo = call("POST", "/api/todos", {"title": "复核补充规则", "pri": "high", "group": "today", "role": "售前"})
check("todo create", s == 201)
s, _ = call("PATCH", f"/api/todos/{todo['id']}", {"done": True})
s, todos = call("GET", "/api/todos")
check("todo toggled", next(t for t in todos if t["id"] == todo["id"])["done"] is True)
s, sk = call("PATCH", f"/api/skills/{new_slug}", {"enabled": False})
check("skill toggle", sk["enabled"] is False)
s, cfg = call("PUT", "/api/config", {"model": "sonnet"})
check("config persisted", s == 200 and cfg["model"] == "sonnet")

# ---- audit + search + errors
s, audit = call("GET", "/api/audit?limit=60")
actions = [a["action"] for a in audit]
check("audit covers auth and skills",
      all(a in actions for a in ["auth.login", "skill.upload", "skill.merge", "artifact.create"]), len(actions))
s, srch = call("GET", "/api/search?q=" + quote("恒信"))
check("search finds requirement", len(srch["requirements"]) >= 1)
s, _ = call("GET", "/api/requirements/missing")
check("404 for unknown requirement", s == 404)

# ---- password change
s, pw = call("POST", "/api/auth/password", {"old_password": "admin123", "new_password": "newpass12345"})
check("password change", s == 200)
s, _ = call("POST", "/api/auth/login", {"username": "admin", "password": "newpass12345"}, token=False)
check("login with new password", s == 200)
s, _ = call("POST", "/api/auth/login", {"username": "admin", "password": "admin123"}, token=False)
check("old password rejected", s == 401)

print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
