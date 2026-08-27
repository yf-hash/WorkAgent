#!/usr/bin/env python3
"""
migrate.py — 统一 harness 元数据迁移入口（v3.1 合并版）

替代原来的两个脚本：
- migrate-harness.py（commands + agents）
- migrate-harness-skills.py（skills）

用法：
  python .claude/scripts/migrate.py --target commands            # 只跑 commands
  python .claude/scripts/migrate.py --target agents              # 只跑 agents
  python .claude/scripts/migrate.py --target skills              # 只跑 skills
  python .claude/scripts/migrate.py --target all                 # 全跑
  python .claude/scripts/migrate.py --target all --apply         # 实际写入
  python .claude/scripts/migrate.py --target all --apply --strict  # 幂等模式：结束时若还有 updated，退出码 1

不加 --apply 是 dry-run。幂等：多次运行结果一致。
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ─── 命令行域默认档 ────────────────────────────────────────────
CMD_DEFAULTS = {
    "commands/writing": dict(
        allowed_tools="[Read, Write, Edit, Grep, Glob, AskUserQuestion]",
        execute_preset="writing-scoped", constrain_profile="writing-safe",
        gates="[before-write]", loop_mode="one-shot",
        memory_scope="project", memory_reads="[project-context]", security_level="low"),
    "commands/product": dict(
        allowed_tools="[Read, Write, Edit, Grep, Glob, AskUserQuestion]",
        execute_preset="writing-scoped", constrain_profile="writing-safe",
        gates="[before-write]", loop_mode="one-shot",
        memory_scope="project", memory_reads="[project-context]", security_level="low"),
    "commands/presales": dict(
        allowed_tools="[Read, Write, Edit, Grep, Glob, AskUserQuestion]",
        execute_preset="writing-scoped", constrain_profile="writing-safe",
        gates="[before-write]", loop_mode="one-shot",
        memory_scope="project", memory_reads="[project-context]", security_level="medium"),
    "commands/media": dict(
        allowed_tools="[Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]",
        execute_preset="media-heavy", constrain_profile="shell-restricted",
        gates="[before-write, before-destructive]", loop_mode="one-shot",
        memory_scope="session", memory_reads="[project-context]", security_level="medium"),
    "commands/research": dict(
        allowed_tools="[Read, Write, Grep, Glob, WebSearch, WebFetch, AskUserQuestion]",
        execute_preset="research", constrain_profile="writing-safe",
        gates="[before-write]", loop_mode="one-shot",
        memory_scope="project", memory_reads="[project-context]", security_level="low"),
    "commands/tools": dict(
        allowed_tools="[Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]",
        execute_preset="agent-orchestrator", constrain_profile="shell-restricted",
        gates="[before-write, before-external-send]", loop_mode="one-shot",
        memory_scope="project", memory_reads="[project-context]", security_level="high"),
}

AGENT_DEFAULTS = dict(
    execute_preset="agent-orchestrator", constrain_profile="writing-safe",
    gates="[before-write, before-loop-restart]", loop_mode="iterative",
    memory_scope="project", memory_reads="[project-context, user-preferences]",
    security_level="medium")

SKILL_DEFAULTS = {
    sub: dict(execute_preset=e, constrain_profile=c, loop_mode=l,
              memory_scope=m, memory_reads="[project-context]", security_level=s)
    for sub, e, c, l, m, s in [
        ("writing",   "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("prd",       "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("pm",        "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("product",   "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("presales",  "writing-scoped", "writing-safe", "one-shot", "project", "medium"),
        ("sa",        "writing-scoped", "writing-safe", "one-shot", "project", "medium"),
        ("content",   "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("bid",       "writing-scoped", "writing-safe", "one-shot", "project", "medium"),
        ("dashboard", "research",       "read-only",    "one-shot", "project", "low"),
        ("ppt",       "media-heavy",    "shell-restricted", "one-shot", "session", "medium"),
        ("media",     "media-heavy",    "shell-restricted", "one-shot", "session", "medium"),
        ("diagram",   "media-heavy",    "shell-restricted", "one-shot", "session", "medium"),
        ("research",  "research",       "writing-safe", "one-shot", "project", "low"),
        ("data",      "research",       "writing-safe", "one-shot", "project", "low"),
        ("strategy",  "writing-scoped", "writing-safe", "one-shot", "project", "low"),
        ("tools",     "writing-scoped", "writing-safe", "one-shot", "project", "low"),
    ]
}

# ─── SKIP + SPECIAL 覆盖 ─────────────────────────────────────
SKIP = {"commands/product/prd.md", "commands/presales/bid.md", "commands/writing/article-writer.md"}

SPECIAL_CMD = {
    "commands/writing/humanize.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3\n    convergence-check: \"AI 味识别 < 5%\""},
    "commands/writing/polish.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "commands/writing/style-refine.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "commands/research/taskweaver.md": {"loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "commands/research/web-search.md": {"constrain_profile": "read-only", "loop_mode": "parallel", "loop_extra": "    fanout: 3"},
    "commands/product/market-research.md": {"execute_preset": "research", "loop_mode": "parallel", "loop_extra": "    fanout: 3"},
    "commands/product/analytics.md": {"execute_preset": "research"},
    "commands/product/user-research.md": {"execute_preset": "research"},
    "commands/product/churn-analysis.md": {"execute_preset": "research"},
    "commands/product/win-loss.md": {"execute_preset": "research"},
    "commands/product/pmf-survey.md": {"execute_preset": "research"},
    "commands/product/ai-red-team.md": {"execute_preset": "research", "security_level": "medium"},
    "commands/presales/solution-architecture.md": {"loop_mode": "pipeline", "loop_extra": "    stages: [discovery, gap, sa-blueprint, business-case, rfp, demo, poc]\n    gate-between: true"},
    "commands/presales/proposal.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "commands/presales/rfp-response.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
}

SPECIAL_AGENT = {
    "agents/bid-writer.md": {"loop_mode": "pipeline", "loop_extra": "    stages: [analyze, clarify, outline, write, review, check, export]\n    gate-between: true"},
    "agents/solution-architect.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "agents/proposal-writer.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "agents/style-evolver.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 6"},
    "agents/impeccable-designer.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "agents/doc-polisher.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "agents/research-analyst.md": {"loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "agents/web-search-analyst.md": {"loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "agents/paper-researcher.md": {"loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "agents/data-analyst.md": {"loop_mode": "one-shot"},
    "agents/qa-acceptance-designer.md": {"loop_mode": "one-shot"},
    "agents/prd-coach.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 6"},
    "agents/content-director.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "agents/ai-product-architect.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "agents/xqy-spec-writer.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "agents/product-director.md": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "agents/product-manager.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 5"},
    "agents/gtm-strategist.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "agents/growth-strategist.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "agents/product-enablement.md": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "agents/article-illustrator.md": {"loop_mode": "one-shot", "security_level": "medium"},
    "agents/diagram-architect.md": {"loop_mode": "one-shot", "security_level": "medium"},
    "agents/ppt-generator.md": {"loop_mode": "one-shot", "security_level": "medium"},
    "agents/video-maker.md": {"loop_mode": "one-shot", "security_level": "medium"},
}

SPECIAL_SKILL = {
    "writing/humanizer-scan": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3\n    convergence-check: \"AI 味 < 5%\""},
    "writing/humanizer-soul": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "writing/humanizer-academic": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "writing/style-writer-reviewer": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 5\n    convergence-check: \"Reviewer 通过\""},
    "writing/style-refine": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "writing/hv-analysis": {"execute_preset": "research"},
    "prd/prd-diagnose": {"loop_mode": "pipeline", "loop_extra": "    stages: [diagnose, concept, impl]\n    gate-between: true"},
    "prd/prd-concept-draft": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "prd/prd-implementation-draft": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "pm/working-backwards": {"loop_mode": "pipeline", "loop_extra": "    stages: [pr-faq, six-pager]\n    gate-between: true"},
    "presales/rfp-response": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "presales/proposal-generator": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "presales/solution-architecture": {"loop_mode": "pipeline", "loop_extra": "    stages: [discovery, gap, sa-blueprint, business-case, rfp, demo, poc]\n    gate-between: true"},
    "presales/doc-auditor": {"execute_preset": "read-only", "constrain_profile": "read-only"},
    "ppt/ppt-architect": {"execute_preset": "writing-scoped", "constrain_profile": "writing-safe", "security_level": "low"},
    "ppt/ppt-web-researcher": {"execute_preset": "research", "constrain_profile": "writing-safe", "security_level": "low"},
    "ppt/ppt-rag-indexer": {"execute_preset": "writing-scoped", "constrain_profile": "writing-safe", "security_level": "low"},
    "diagram/impeccable": {"execute_preset": "writing-scoped", "constrain_profile": "writing-safe", "loop_mode": "iterative", "loop_extra": "    max-iterations: 4", "security_level": "low"},
    "research/market-research": {"loop_mode": "parallel", "loop_extra": "    fanout: 3"},
    "research/user-research": {"loop_mode": "parallel", "loop_extra": "    fanout: 3"},
    "research/open-websearch": {"constrain_profile": "read-only", "loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "research/taskweaver": {"loop_mode": "parallel", "loop_extra": "    fanout: 3-5"},
    "research/chat2db": {"execute_preset": "shell-restricted", "constrain_profile": "shell-restricted", "security_level": "medium"},
    "strategy/launch-checklist": {"loop_mode": "pipeline", "loop_extra": "    gate-between: true"},
    "strategy/ai-red-team": {"execute_preset": "research", "security_level": "medium"},
    "strategy/sunset-plan": {"security_level": "medium"},
    "strategy/gtm-strategy": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 4"},
    "strategy/win-loss-analysis": {"execute_preset": "research"},
    "strategy/churn-analysis": {"execute_preset": "research"},
    "strategy/pmf-survey": {"execute_preset": "research"},
    "strategy/user-feedback": {"execute_preset": "research"},
    "strategy/product-report": {"execute_preset": "research"},
    "strategy/pricing-strategy": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "strategy/build-vs-buy": {"loop_mode": "iterative", "loop_extra": "    max-iterations: 3"},
    "strategy/tech-debt": {"execute_preset": "research"},
}

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def build_block(cfg: dict, is_agent_or_skill: bool = False) -> str:
    loop_extra = cfg.get("loop_extra", "")
    if loop_extra and not loop_extra.startswith("\n"):
        loop_extra = "\n" + loop_extra
    return f"""harness:
  execute:
    preset: {cfg['execute_preset']}
  constrain:
    profile: {cfg['constrain_profile']}{"" if is_agent_or_skill else f"\\n    gates: {cfg.get('gates', '[]')}"}
  loop:
    mode: {cfg['loop_mode']}{loop_extra}
  memory:
    scope: {cfg['memory_scope']}
    reads: {cfg['memory_reads']}
  security:
    danger-level: {cfg['security_level']}"""


def process(path: Path, rel: str, base: dict, add_allowed_tools: bool, dry: bool) -> str:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "no frontmatter"

    fm = m.group(1)
    body = text[m.end():]

    has_at = re.search(r"^allowed-tools:", fm, re.MULTILINE) is not None
    has_harness = re.search(r"^harness:", fm, re.MULTILINE) is not None

    additions = []
    if add_allowed_tools and not has_at and "allowed_tools" in base:
        additions.append(f"allowed-tools: {base['allowed_tools']}")
    if not has_harness:
        additions.append(build_block(base, is_agent_or_skill=not add_allowed_tools))

    if not additions:
        return "complete"

    new_fm = fm.rstrip() + "\n" + "\n".join(additions)
    new_text = f"---\n{new_fm}\n---\n{body}"

    if not dry:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return "updated"


def run_commands(dry: bool, stats: dict):
    for p in sorted((ROOT / "commands").rglob("*.md")):
        if p.name == "README.md":
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in SKIP:
            stats["skipped"] = stats.get("skipped", 0) + 1
            continue
        domain = "/".join(rel.split("/")[:2])
        if domain not in CMD_DEFAULTS:
            continue
        base = CMD_DEFAULTS[domain].copy()
        if rel in SPECIAL_CMD:
            base.update(SPECIAL_CMD[rel])
        result = process(p, rel, base, add_allowed_tools=True, dry=dry)
        stats[result] = stats.get(result, 0) + 1


def run_agents(dry: bool, stats: dict):
    for p in sorted((ROOT / "agents").glob("*.md")):
        if p.name == "README.md":
            continue
        rel = p.relative_to(ROOT).as_posix()
        base = AGENT_DEFAULTS.copy()
        if rel in SPECIAL_AGENT:
            base.update(SPECIAL_AGENT[rel])
        result = process(p, rel, base, add_allowed_tools=False, dry=dry)
        stats[result] = stats.get(result, 0) + 1


def run_skills(dry: bool, stats: dict):
    skills_dir = ROOT / "skills"
    for p in sorted(skills_dir.rglob("SKILL.md")):
        parts = p.relative_to(skills_dir).as_posix().split("/")
        if len(parts) < 3:
            continue
        subdomain, name = parts[0], parts[1]
        if subdomain not in SKILL_DEFAULTS:
            continue
        base = SKILL_DEFAULTS[subdomain].copy()
        rel_key = f"{subdomain}/{name}"
        if rel_key in SPECIAL_SKILL:
            base.update(SPECIAL_SKILL[rel_key])
        result = process(p, rel_key, base, add_allowed_tools=False, dry=dry)
        stats[result] = stats.get(result, 0) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["commands", "agents", "skills", "all"], required=True)
    ap.add_argument("--apply", action="store_true", help="实际写入；不加为 dry-run")
    ap.add_argument("--strict", action="store_true", help="幂等模式：若还有 updated，退出码 1")
    args = ap.parse_args()

    dry = not args.apply
    stats = {}

    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'}, target={args.target}\n")

    if args.target in ("commands", "all"):
        run_commands(dry, stats)
    if args.target in ("agents", "all"):
        run_agents(dry, stats)
    if args.target in ("skills", "all"):
        run_skills(dry, stats)

    print("=== 汇总 ===")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    if args.strict and stats.get("updated", 0) > 0:
        print("\n[STRICT] 检测到 updated，退出码 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
