"""WorkAgent Console — SQLite schema, seed data and query helpers.

Zero external dependencies: uses only the Python standard library.
"""
import json
import os
import sqlite3
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
DB_PATH = os.path.join(DATA_DIR, "workagent.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS requirements (
    id TEXT PRIMARY KEY,
    ref TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    role TEXT NOT NULL,
    source TEXT,
    client TEXT,
    stage TEXT NOT NULL DEFAULT 'raw',
    elements INTEGER NOT NULL DEFAULT 0,
    priority TEXT DEFAULT '中',
    owner TEXT,
    raw_text TEXT,
    fields TEXT NOT NULL DEFAULT '[]',
    qa TEXT NOT NULL DEFAULT '[]',
    linear_status TEXT DEFAULT 'none',
    linear_id TEXT,
    team TEXT,
    project TEXT,
    deliverable TEXT,
    updated_at TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY,
    req_id TEXT,
    ref TEXT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    role TEXT NOT NULL,
    version TEXT NOT NULL,
    size TEXT,
    author TEXT,
    path TEXT NOT NULL,
    note TEXT,
    updated_at TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS artifact_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_id TEXT NOT NULL,
    version TEXT NOT NULL,
    path TEXT NOT NULL,
    size TEXT,
    note TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    side TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    step INTEGER NOT NULL DEFAULT 0,
    req_id TEXT,
    owner TEXT,
    elapsed TEXT,
    last TEXT,
    note TEXT,
    started TEXT,
    updated_at TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    pri TEXT DEFAULT 'mid',
    due TEXT,
    grp TEXT DEFAULT 'today',
    role TEXT,
    req_id TEXT,
    done INTEGER DEFAULT 0,
    urgent INTEGER DEFAULT 0,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS skills (
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    grp TEXT NOT NULL,
    glyph TEXT,
    description TEXT,
    version TEXT,
    calls INTEGER DEFAULT 0,
    enabled INTEGER DEFAULT 1,
    source TEXT DEFAULT 'repo',
    content TEXT
);
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT,
    action TEXT NOT NULL,
    target_type TEXT,
    target_id TEXT,
    detail TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    role TEXT DEFAULT 'admin',
    created_at TEXT,
    last_login_at TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TEXT,
    expires_at TEXT
);
CREATE TABLE IF NOT EXISTS skill_docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    filename TEXT,
    title TEXT,
    content TEXT NOT NULL,
    size INTEGER,
    uploaded_by TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS skill_supplements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    doc_id INTEGER,
    summary TEXT,
    appended_chars INTEGER,
    created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_req_stage ON requirements(stage);
CREATE INDEX IF NOT EXISTS idx_art_req ON artifacts(req_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit(created_at);
"""

DEFAULT_CONFIG = {
    "model": "opus",
    "provider": "anthropic",
    "apiKey": "sk-ant-api03-Wa7dK-2mN8qL-xR4t-9vB3-sY6u-fQ1p-f9Qm",
    "baseUrl": "https://api.anthropic.com",
    "tempClarify": 0.3,
    "tempGen": 0.6,
    "tempValidate": 0.2,
    "maxTokens": 8192,
    "ctxStrategy": "summary",
    "fallback": "sonnet",
    "routing": {
        "需求 · 输入理解": "sonnet",
        "需求 · 要素抽取": "sonnet",
        "需求 · 结构化": "opus",
        "需求 · 完整性校验": "sonnet",
        "方案 / 标书生成": "opus",
        "产物归档与摘要": "haiku",
    },
}

ELEMENT_NAMES = ["业务目标", "目标用户", "使用场景", "功能范围", "验收标准", "优先级", "时间约束"]
ART_EXTS = {
    "方案": "docx", "标书": "pdf", "PPT": "pptx", "竞品分析": "md",
    "PRD": "md", "原型": "fig", "技术交底书": "docx", "技术规格": "md", "需求文档": "md",
}


def now_str(offset_minutes=0):
    t = datetime.now() + timedelta(minutes=offset_minutes)
    return t.strftime("%m-%d %H:%M")


def connect():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def row_to_dict(row):
    return dict(row) if row is not None else None


# ---------------------------------------------------------------- seed data
def seed_requirements():
    """Return seed requirement dicts (shared with the front-end demo data)."""
    raw_fields = lambda vals: [
        {"k": ELEMENT_NAMES[i], "v": vals[i], "ok": not str(vals[i]).startswith("待")}
        for i in range(len(ELEMENT_NAMES))
    ]
    return [
        dict(id="r1", ref="REQ-024", title="远大制造 MES 替换 · 安全接入需求", role="sa", source="客户转述",
             client="远大制造", stage="done", priority="高", owner="陈默", team="SA", project="MES 替换",
             deliverable="技术方案 · 客户 PPT · 适配清单", updated_at="10 分钟前",
             raw_text="销售转述：客户要替换跑了 8 年的老 MES，要求私有化部署和国产化适配，2027 年 3 月上线。接入侧要能看到谁在什么时间访问了哪些生产数据，出问题能追溯。",
             fields=raw_fields(["替换老 MES 的同时补齐生产数据访问审计与追溯能力", "生产运维、安全审计、车间主管",
                                "生产数据访问审计、异常访问追溯", "统一接入、访问审计、国产化适配（达梦 / 金仓 / 麒麟）",
                                "审计覆盖 100% 接入链路，查询响应 ≤2s，满足等保三级", "高 · 配合 2027-03 上线节点",
                                "2026-12 方案确认，2027-01 分批上线"]),
             qa=[{"q": "客户当前 MES 的数据库与中间件是什么？", "a": "待销售确认；已按信创目录给出两套适配方案。"},
                 {"q": "审计日志留存多久？", "a": "客户要求 12 个月，超出当前默认 6 个月，需要在方案中标注成本。"},
                 {"q": "是否需要对接客户已有 SIEM？", "a": "确认需要，方案中预留 Syslog / Kafka 输出。"}]),
        dict(id="r2", ref="REQ-023", title="能源集团安全运营中心需求", role="sa", source="RFP",
             client="能源集团 · 华北", stage="done", priority="高", owner="周婕", team="SA", project="安全运营中心",
             deliverable="投标文件 · 技术方案摘要", updated_at="40 分钟前",
             raw_text="RFP 第二章：建设集团级安全运营中心，覆盖 12 个厂区，要求统一告警、自动化处置与监管报送。共 214 条应答条目。",
             fields=raw_fields(["集团级安全运营中心，统一告警与自动化处置", "集团 SOC、厂区安全员、监管接口人",
                                "日常运营、重大活动保障、监管报送", "日志接入、告警降噪、编排处置、报表报送",
                                "214 条应答全部满足，重大告警处置时长下降 40%", "高", "2027-Q1 试点，Q3 全量"]),
             qa=[{"q": "12 个厂区的网络是否互通？", "a": "跨域专网，需要支持多级部署与数据同步。"},
                 {"q": "监管报送口径以哪份文件为准？", "a": "客户已提供最新报送模板，应答文件按此编制。"}]),
        dict(id="r3", ref="REQ-021", title="AI 一体机安全能力补齐", role="pm", source="内部规划",
             client="产品线 · 安全", stage="ready", priority="高", owner="林轩", team="PROD", project="AI 一体机",
             deliverable="PRD · 技术交底书 · 技术规格书", updated_at="1 小时前",
             raw_text="一体机在模型越权、Agent 工具调用审计与数据外带检测三块能力不足，需要补齐后进入投标。",
             fields=raw_fields(["补齐一体机安全能力，满足投标基线", "安全管理员、交付工程师",
                                "模型访问控制、工具调用审计、数据外带检测", "三类能力的策略配置与审计报表",
                                "30 条基线用例全部通过，审计覆盖率 100%", "高", "本季度完成开发，下季度投标"]),
             qa=[{"q": "基线用例集由谁提供？", "a": "安全实验室已于本周提供 30 条用例。"},
                 {"q": "数据外带检测是否需要覆盖加密流量？", "a": "首版不覆盖，作为二期规划。"}]),
        dict(id="r4", ref="REQ-020", title="政务云等保三级需求梳理", role="sa", source="访谈纪要",
             client="华南某政务云", stage="clarify", priority="高", owner="周婕", team="SA", project="政务云",
             deliverable="等保差距分析（初稿）", updated_at="2 小时前",
             raw_text="访谈记录：客户希望把分散的安全能力收敛到统一中台，等保三级是硬约束，预算和上线时间还没定。",
             fields=raw_fields(["安全能力收敛，满足等保三级", "云平台运维、租户安全管理员", "待补充", "待补充",
                                "待补充", "高", "待确认"]),
             qa=[{"q": "中台覆盖多少个租户？", "a": "访谈提到约 40 个，需客户确认。"},
                 {"q": "现有安全设备如何纳管？", "a": "待补充访谈。"}]),
        dict(id="r5", ref="REQ-018", title="VulnHunter 批量导入需求", role="pm", source="客户反馈",
             client="产品线 · 漏洞管理", stage="done", priority="中", owner="林轩", team="PROD", project="VulnHunter",
             deliverable="PRD · 原型", updated_at="今天 09:44", linear_status="synced", linear_id="LIN-138",
             raw_text="客户希望批量导入资产与漏洞数据，支持 CSV、API 和存量库迁移，重复数据要能按规则合并。",
             fields=raw_fields(["降低首次接入成本，支持存量迁移", "实施工程师、客户管理员", "首次接入、周期性数据同步",
                                "CSV / API / 库迁移三条通道，冲突合并策略", "10 万条数据导入 ≤10 分钟，错误报告可下载",
                                "中", "Q4 版本内"]),
             qa=[{"q": "单次导入上限？", "a": "确认支持 50 万条，超出分批处理。"},
                 {"q": "冲突策略？", "a": "按资产唯一标识判重，默认覆盖并保留历史。"}]),
        dict(id="r6", ref="REQ-017", title="OpsCenter 告警中心改版需求", role="pm", source="内部规划",
             client="产品线 · 运营平台", stage="done", priority="中", owner="苏沐", team="PROD", project="OpsCenter",
             deliverable="PRD · 信息架构原型", updated_at="昨天 17:20", linear_status="synced", linear_id="LIN-131",
             raw_text="重做告警中心与工单流的信息架构，减少重复告警，支持按资产与业务线聚合。",
             fields=raw_fields(["降低告警噪音，提升处置效率", "值班工程师、安全运营", "值班处置、复盘分析",
                                "告警聚合、工单流转、处置看板", "重复告警下降 60%，工单流转可追溯", "中", "Q4 上线"]),
             qa=[{"q": "聚合规则由谁定义？", "a": "运营团队提供初版规则，产品固化到配置项。"}]),
        dict(id="r7", ref="REQ-015", title="某银行等保三级需求包", role="sa", source="RFP",
             client="城商行 · 华东", stage="done", priority="高", owner="陈默", team="SA", project="银行等保",
             deliverable="安全接入方案 · 技术偏离表", updated_at="11-01 16:02",
             raw_text="银行采购文件：等保三级 + 金融监管双重约束，要求安全接入、审计与数据脱敏三部分能力。",
             fields=raw_fields(["满足等保三级与金融监管要求", "银行安全部、数据中心", "生产接入、审计取证、脱敏测试",
                                "安全接入、审计、数据脱敏", "通过等保测评，审计留存 6 个月", "高", "2027-Q1 交付"]),
             qa=[{"q": "脱敏是否需要支持动态脱敏？", "a": "静态 + 动态都要，已在方案范围中。"}]),
        dict(id="r8", ref="REQ-026", title="数据分类分级需求收集", role="pm", source="销售邮件",
             client="产品线 · 数据安全", stage="raw", priority="中", owner="苏沐", team="PROD", project="数据安全",
             deliverable="需求初稿", updated_at="昨天",
             raw_text="销售邮件：至少 3 个客户在问自动识别敏感数据并完成分级，能不能做？先把需求收集起来。",
             fields=raw_fields(["自动识别敏感数据并完成分级", "待补充", "待补充", "待补充", "待补充", "中", "待补充"]),
             qa=[{"q": "客户的数据源类型有哪些？", "a": "待向销售与客户确认。"}]),
        dict(id="r9", ref="REQ-025", title="城商行数据脱敏需求补充", role="sa", source="销售邮件",
             client="城商行 · 华东", stage="raw", priority="中", owner="陈默", team="SA", project="银行等保",
             deliverable="待确认", updated_at="昨天",
             raw_text="客户追加：测试环境需要动态脱敏，要求保留数据分布特征，不能影响下游测试。",
             fields=raw_fields(["测试环境动态脱敏，保留数据分布", "待补充", "测试数据准备", "待补充",
                                "待补充", "中", "与原项目同期"]),
             qa=[{"q": "涉及哪些数据库？", "a": "待销售补充客户清单。"}]),
        dict(id="r10", ref="REQ-022", title="制造企业工单闭环需求", role="sa", source="客户转述",
             client="恒信精工", stage="ready", priority="中", owner="陈默", team="SA", project="恒信精工",
             deliverable="POC 方案 · 对接说明", updated_at="昨天 15:40",
             raw_text="销售转述：客户希望安全告警能直接生成工单，派给对应车间负责人，处置结果回写。",
             fields=raw_fields(["告警到工单的闭环处置", "安全员、车间负责人", "日常告警处置、复盘",
                                "告警转工单、指派、回写", "工单闭环率 ≥95%，平均处置时长下降 30%", "中", "Q1 试点"]),
             qa=[{"q": "工单系统是否已有？", "a": "客户已有 ITSM，需通过 API 对接。"}]),
        dict(id="r11", ref="REQ-019", title="政企客户报表导出需求", role="pm", source="客户反馈",
             client="产品线 · 报表", stage="clarify", priority="低", owner="林轩", team="PROD", project="报表中心",
             deliverable="待生成", updated_at="2 天前",
             raw_text="客户反馈：希望报表能按自定义字段导出 Excel，并且支持定时发送到邮箱。",
             fields=raw_fields(["提升报表可用性，减少人工导出", "运营、业务主管", "周报 / 月报导出",
                                "自定义字段、定时发送", "待确认数据量级", "低", "待补充"]),
             qa=[{"q": "单次导出上限？", "a": "待确认，暂按 10 万行设计。"}]),
        dict(id="r12", ref="REQ-027", title="某制造业客户接入审计需求", role="sa", source="RFP",
             client="精工集团 · 华东", stage="structured", priority="高", owner="周婕", team="SA", project="精工集团",
             deliverable="待生成标书", updated_at="3 天前",
             raw_text="RFP 第一章：需具备生产设备接入审计、异常访问告警与月度合规报表能力，覆盖 6 个生产基地。",
             fields=raw_fields(["设备接入审计与异常访问告警", "集团安全部、基地运维", "审计取证、监管报送",
                                "接入审计、异常告警、月度报表", "待 RFP 第三章评审确认", "高", "2027-Q2 交付"]),
             qa=[{"q": "6 个基地是否统一网络？", "a": "部分隔离，需支持本地缓存与断点回传。"}]),
    ]


def seed_artifacts():
    return [
        dict(id="a1", req_id="r1", ref="REQ-024", name="远大制造 MES · 总技术方案", type="方案", role="sa",
             version="v2.1", size="2.4 MB", author="陈默", note="补充国产化适配章节", updated_at="11-03 10:48",
             history=[("v2.1", "补充国产化适配章节", "2.4 MB", "11-03 10:48"),
                      ("v2.0", "客户评审后修订", "2.1 MB", "11-01 17:20"),
                      ("v1.0", "初稿归档", "1.7 MB", "10-28 09:12")]),
        dict(id="a2", req_id="r1", ref="REQ-024", name="远大制造 MES · 客户汇报 PPT", type="PPT", role="sa",
             version="v2", size="8.1 MB", author="陈默", note="增加国产化适配页", updated_at="11-02 19:20",
             history=[("v2", "增加国产化适配页", "8.1 MB", "11-02 19:20"),
                      ("v1", "首版汇报材料", "7.4 MB", "10-30 14:05")]),
        dict(id="a3", req_id="r1", ref="REQ-024", name="远大制造 MES · 国产化适配清单", type="方案", role="sa",
             version="v1.0", size="320 KB", author="陈默", note="达梦 / 金仓 / 麒麟适配矩阵", updated_at="11-02 15:06",
             history=[("v1.0", "达梦 / 金仓 / 麒麟适配矩阵", "320 KB", "11-02 15:06")]),
        dict(id="a4", req_id="r2", ref="REQ-023", name="能源集团 · 投标应答文件（正本）", type="标书", role="sa",
             version="v4", size="14.6 MB", author="周婕", note="盖章版正本", updated_at="11-02 22:10",
             history=[("v4", "盖章版正本", "14.6 MB", "11-02 22:10"),
                      ("v3", "技术偏离表修订", "14.2 MB", "11-01 21:40"),
                      ("v2", "内部评审版", "13.8 MB", "10-31 16:30")]),
        dict(id="a5", req_id="r2", ref="REQ-023", name="能源集团 · 技术方案摘要", type="方案", role="sa",
             version="v1", size="86 KB", author="周婕", note="方案要点摘录", updated_at="11-01 17:32",
             history=[("v1", "方案要点摘录", "86 KB", "11-01 17:32")]),
        dict(id="a6", req_id="r4", ref="REQ-020", name="政务云 · 等保三级差距分析", type="方案", role="sa",
             version="v1", size="46 KB", author="周婕", note="基于访谈初步梳理", updated_at="11-01 11:20",
             history=[("v1", "基于访谈初步梳理", "46 KB", "11-01 11:20")]),
        dict(id="a7", req_id="r7", ref="REQ-015", name="城商行 · 技术偏离表", type="标书", role="sa",
             version="v2", size="320 KB", author="陈默", note="补充脱敏条款", updated_at="10-31 16:44",
             history=[("v2", "补充脱敏条款", "320 KB", "10-31 16:44"),
                      ("v1", "首版偏离表", "298 KB", "10-30 10:20")]),
        dict(id="a8", req_id="r7", ref="REQ-015", name="城商行 · 安全接入方案", type="方案", role="sa",
             version="v1.2", size="1.2 MB", author="陈默", note="审计章节细化", updated_at="10-30 10:12",
             history=[("v1.2", "审计章节细化", "1.2 MB", "10-30 10:12"),
                      ("v1.0", "初版方案", "1.1 MB", "10-27 15:40")]),
        dict(id="a9", req_id="r10", ref="REQ-022", name="恒信精工 · POC 测试方案", type="方案", role="sa",
             version="v1", size="38 KB", author="陈默", note="工单对接验证用例", updated_at="10-30 09:05",
             history=[("v1", "工单对接验证用例", "38 KB", "10-30 09:05")]),
        dict(id="a10", req_id="r5", ref="REQ-018", name="VulnHunter 批量导入 · PRD", type="PRD", role="pm",
             version="v1.3", size="128 KB", author="林轩", note="补齐冲突合并策略", updated_at="11-03 09:40",
             history=[("v1.3", "补齐冲突合并策略", "128 KB", "11-03 09:40"),
                      ("v1.2", "验收标准量化", "121 KB", "11-01 20:10"),
                      ("v1.0", "PRD 初稿", "110 KB", "10-29 11:30")]),
        dict(id="a11", req_id="r5", ref="REQ-018", name="VulnHunter · 原型与流程图", type="原型", role="pm",
             version="v2", size="2.1 MB", author="林轩", note="三步导入流程", updated_at="11-02 16:30",
             history=[("v2", "三步导入流程", "2.1 MB", "11-02 16:30"),
                      ("v1", "首版原型", "1.9 MB", "10-30 14:12")]),
        dict(id="a12", req_id="r6", ref="REQ-017", name="OpsCenter 告警中心 · PRD", type="PRD", role="pm",
             version="v2.0", size="156 KB", author="苏沐", note="信息架构定稿", updated_at="11-01 15:12",
             history=[("v2.0", "信息架构定稿", "156 KB", "11-01 15:12"),
                      ("v1.6", "工单流补充", "148 KB", "10-30 10:40"),
                      ("v1.0", "PRD 初稿", "132 KB", "10-26 09:20")]),
        dict(id="a13", req_id="r6", ref="REQ-017", name="OpsCenter · 信息架构原型", type="原型", role="pm",
             version="v2", size="6.4 MB", author="苏沐", note="告警聚合视图", updated_at="10-31 14:20",
             history=[("v2", "告警聚合视图", "6.4 MB", "10-31 14:20"),
                      ("v1", "首版 IA", "5.8 MB", "10-28 16:50")]),
        dict(id="a14", req_id="r3", ref="REQ-021", name="AI 一体机 · 技术交底书", type="技术交底书", role="pm",
             version="v1.0", size="1.8 MB", author="林轩", note="三类安全能力交底", updated_at="11-03 10:33",
             history=[("v1.0", "三类安全能力交底", "1.8 MB", "11-03 10:33")]),
        dict(id="a15", req_id="r3", ref="REQ-021", name="AI 一体机 · 技术规格书", type="技术规格", role="pm",
             version="v2", size="88 KB", author="林轩", note="量化审计指标", updated_at="11-02 18:05",
             history=[("v2", "量化审计指标", "88 KB", "11-02 18:05"),
                      ("v1", "首版规格", "82 KB", "10-31 10:15")]),
        dict(id="a16", req_id="r8", ref="REQ-026", name="数据分类分级 · 需求初稿", type="需求文档", role="pm",
             version="v1", size="24 KB", author="苏沐", note="销售邮件整理稿", updated_at="昨天 17:40",
             history=[("v1", "销售邮件整理稿", "24 KB", "昨天 17:40")]),
    ]


def seed_tasks():
    return [
        dict(id="t1", side="sa", title="远大制造 MES · 技术方案生成", status="running", step=3, req_id="r1",
             owner="陈默", elapsed="46 分钟", last="10:41 方案正文生成中", started="10:02",
             note="已完成输入清洗、要素抽取与澄清，正在生成技术方案正文并引用适配清单。"),
        dict(id="t2", side="sa", title="能源集团 · 标书应答整理", status="running", step=3, req_id="r2",
             owner="周婕", elapsed="1 小时 12 分", last="10:28 214 条应答归并中", started="09:16",
             note="214 条应答条目已归并，正在生成投标文件正本并核对技术偏离。"),
        dict(id="t3", side="sa", title="政务云 · 访谈纪要整理", status="running", step=2, req_id="r4",
             owner="周婕", elapsed="18 分钟", last="10:39 生成澄清问题中", started="10:21",
             note="访谈内容已清洗，正在识别缺失要素并生成追问清单。"),
        dict(id="t4", side="sa", title="城商行 · 方案沉淀归档", status="done", step=5, req_id="r7",
             owner="陈默", elapsed="56 分钟", last="10:12 已沉淀 2 份产物", started="09:16",
             note="方案与技术偏离表已沉淀到 ./output/sa/REQ-015/，版本可回溯。"),
        dict(id="t5", side="sa", title="恒信精工 · 等待客户确认工单接口", status="blocked", step=1, req_id="r10",
             owner="陈默", elapsed="—", last="等待客户 ITSM 接口文档", started="昨天 18:04",
             note="缺少客户 ITSM 接口文档与测试环境，已生成追问邮件，等待销售回复。"),
        dict(id="t6", side="pm", title="AI 一体机 · 技术交底书整理", status="running", step=3, req_id="r3",
             owner="林轩", elapsed="55 分钟", last="10:33 交底书章节生成中", started="09:40",
             note="三类安全能力需求已结构化，正在生成技术交底书，完成后待推送 Linear。"),
        dict(id="t7", side="pm", title="VulnHunter · PRD 归档", status="done", step=5, req_id="r5",
             owner="林轩", elapsed="1 小时 05 分", last="09:40 已归档 PRD v1.3", started="08:35",
             note="PRD 与原型已归档到 ./output/pm/REQ-018/，Linear 已同步。"),
        dict(id="t8", side="pm", title="数据分类分级 · 7 要素补全", status="queued", step=0, req_id="r8",
             owner="苏沐", elapsed="—", last="等待调度", started="—",
             note="已进入队列，等待当前任务完成后开始要素补全。"),
        dict(id="t9", side="pm", title="OpsCenter · 原型与 PRD 归档", status="done", step=5, req_id="r6",
             owner="苏沐", elapsed="38 分钟", last="17:20 已归档 2 份产物", started="16:42",
             note="PRD v2.0 与信息架构原型已归档，研发在 Linear 中接手。"),
        dict(id="t10", side="pm", title="政企报表导出 · 澄清问题生成", status="running", step=2, req_id="r11",
             owner="林轩", elapsed="12 分钟", last="10:42 生成 4 个澄清问题", started="10:30",
             note="基础要素已抽取，正在生成数据量级与导出频率相关的问题。"),
    ]


def seed_todos():
    return [
        dict(id="td1", title="审核「远大制造」技术方案 V2.1 并确认沉淀", pri="high", due="今天 18:00", grp="today", role="售前", req_id="r1", done=0, urgent=1),
        dict(id="td2", title="补全「政务云」需求缺失的 3 项要素", pri="high", due="今天", grp="today", role="售前", req_id="r4", done=0, urgent=1),
        dict(id="td3", title="确认「AI 一体机」交付后推送 Linear", pri="high", due="今天", grp="today", role="产品", req_id="r3", done=0, urgent=1),
        dict(id="td4", title="对照 RFP 复核「能源集团」投标文件正本", pri="mid", due="明天", grp="week", role="售前", req_id="r2", done=0, urgent=0),
        dict(id="td5", title="向销售索要「城商行」数据源清单", pri="mid", due="周四", grp="week", role="售前", req_id="r9", done=0, urgent=0),
        dict(id="td6", title="检查产物库路径规范与版本命名", pri="mid", due="周四", grp="week", role="通用", req_id=None, done=0, urgent=0),
        dict(id="td7", title="复盘本周产物归档遗漏项", pri="low", due="周五", grp="later", role="通用", req_id=None, done=0, urgent=0),
        dict(id="td8", title="归档上周需求整理对话记录", pri="low", due="上周", grp="later", role="产品", req_id=None, done=1, urgent=0),
    ]


def seed_skills():
    data = [
        ("pm-requirement-clarify", "需求澄清", "pm", "CL", "识别 7 要素缺失、伪需求与内部冲突，产出澄清报告与待确认问题清单。", "v1.3", 214, 1),
        ("pm-solution-decompose", "方案拆解", "pm", "SO", "输出业务流程、P0/P1/P2 优先级、依赖关系与风险矩阵。", "v1.2", 176, 1),
        ("pm-prototype-design", "原型设计", "pm", "PT", "生成页面结构、组件清单与 Mermaid 流程，沉淀为原型产物。", "v1.1", 98, 1),
        ("pm-prd-validate", "PRD 校验", "pm", "PV", "完整性 / 一致性 / 歧义 / 埋点四类校验，按严重度输出问题分级。", "v1.4", 143, 1),
        ("pm-tech-spec", "技术规格", "pm", "TS", "从已成型需求推导 6 大类技术指标与规格书。", "v1.5", 121, 1),
        ("pm-tech-spec-validate", "规格校验", "pm", "SV", "校验指标可测性、口径一致性与工程可行性。", "v1.2", 88, 1),
        ("pm-artifact-archive", "产物归档", "pm", "AR", "生成 README、CHANGELOG 与冻结快照，保留可回溯地址。", "v1.0", 66, 1),
        ("pm-competitive-intel", "竞品情报", "pm", "CI", "多信源采集竞品功能、定价与动态，结构化入库并标记可信度。", "v1.1", 57, 1),
        ("pm-competitive-benchmark", "竞品对标", "pm", "CB", "多维能力打分与差距定位，输出对标矩阵与短板优先级。", "v1.1", 41, 1),
        ("pm-competitive-strategy", "差异化战略", "pm", "CS", "基于对标结论生成定位、打法与话术。", "v1.0", 22, 0),
        ("prd-writer", "结构化撰写", "prd", "PR", "把已成型需求写成研发可读的结构化描述，内置验收标准与边界条件。", "v2.0", 188, 1),
        ("sa-input-gateway", "输入网关", "sa", "IN", "从销售转述 / RFP / 访谈纪要中抽取客户元信息并清洗。", "v1.2", 134, 1),
        ("sa-clarify", "客户调研", "sa", "CO", "识别信息缺口，生成调研问题与痛点收敛报告。", "v1.2", 112, 1),
        ("sa-capability-mapping", "能力映射", "sa", "CM", "业务需求到产品能力的映射，附竞品差距与风险评估。", "v1.1", 97, 1),
        ("sa-architect", "总体架构", "sa", "AT", "生成业务与技术架构，执行三项一致性校验。", "v1.3", 83, 1),
        ("sa-solution-validate", "方案校验", "sa", "SV", "校验方案完整性、合规约束覆盖度与交付可行性。", "v1.1", 74, 1),
        ("sa-poc-plan", "POC 方案", "sa", "PO", "设计验证目标、测试用例、成功标准与资源排期。", "v1.0", 51, 1),
        ("sa-impl-plan", "实施方案", "sa", "IM", "输出里程碑、交付物、角色分工与风险预案。", "v1.0", 46, 1),
        ("sa-rfp-response", "RFP / 标书应答", "sa", "RF", "逐条应答并生成技术偏离表，标出高风险条款与建议口径。", "v1.4", 69, 1),
        ("sa-quote-estimate", "报价估算", "sa", "QT", "基于规则库生成配置与工时估算底稿。", "v1.1", 44, 1),
        ("sa-presentation-draft", "方案 PPT 生成", "sa", "PD", "生成客户汇报 PPT 大纲与关键页文案，自动对齐方案口径。", "v1.0", 29, 1),
        ("sa-artifact-archive", "方案沉淀归档", "sa", "AD", "方案 / PPT / 标书统一沉淀，生成版本快照与可回溯地址。", "v1.0", 33, 1),
        ("content-intake", "内容网关", "content", "CI", "识别八大文体、目标读者与传播渠道。", "v1.1", 61, 1),
        ("content-materials", "素材抽取", "content", "MA", "从关联需求与产物中抽取可用事实、数据与图表。", "v1.1", 52, 1),
        ("content-templates", "文体模板", "content", "TP", "文体结构模板与写作规范库，保证跨渠道口径一致。", "v1.2", 47, 0),
        ("content-validate", "内容校验", "content", "VA", "事实一致性、合规、文风、结构与品牌口径五类校验。", "v1.0", 39, 1),
        ("content-archive", "内容归档", "content", "CA", "多格式导出并回写关联需求与产物库。", "v1.0", 35, 1),
    ]
    return [
        dict(slug=s, name=n, grp=g, glyph=gl, description=d, version=v, calls=c, enabled=e)
        for (s, n, g, gl, d, v, c, e) in data
    ]


def seed_if_empty(conn):
    cur = conn.execute("SELECT COUNT(*) AS n FROM requirements")
    if cur.fetchone()["n"] == 0:
        for r in seed_requirements():
            insert_requirement(conn, r, log_audit=False)
    cur = conn.execute("SELECT COUNT(*) AS n FROM artifacts")
    if cur.fetchone()["n"] == 0:
        for a in seed_artifacts():
            insert_artifact(conn, a, log_audit=False)
    cur = conn.execute("SELECT COUNT(*) AS n FROM tasks")
    if cur.fetchone()["n"] == 0:
        for t in seed_tasks():
            insert_task(conn, t, log_audit=False)
    cur = conn.execute("SELECT COUNT(*) AS n FROM todos")
    if cur.fetchone()["n"] == 0:
        for t in seed_todos():
            conn.execute(
                """INSERT INTO todos (id,title,pri,due,grp,role,req_id,done,urgent,created_at)
                   VALUES (:id,:title,:pri,:due,:grp,:role,:req_id,:done,:urgent,:created_at)""",
                dict(t, created_at=now_str()),
            )
    cur = conn.execute("SELECT COUNT(*) AS n FROM skills")
    if cur.fetchone()["n"] == 0:
        for s in seed_skills():
            conn.execute(
                """INSERT INTO skills (slug,name,grp,glyph,description,version,calls,enabled,source,content)
                   VALUES (:slug,:name,:grp,:glyph,:description,:version,:calls,:enabled,'repo',:content)""",
                dict(s, content=skill_capability_doc(s)),
            )
    if conn.execute("SELECT COUNT(*) AS n FROM config").fetchone()["n"] == 0:
        for k, v in DEFAULT_CONFIG.items():
            conn.execute("INSERT INTO config (key,value) VALUES (?,?)", (k, json.dumps(v, ensure_ascii=False)))
    created = ensure_admin(conn)
    conn.commit()
    return created


def skill_capability_doc(skill):
    """Initial capability text for a repository skill — the base an upload can extend."""
    return (
        f"# {skill['name']}\n\n"
        f"- slug: `{skill['slug']}`\n"
        f"- 分组: {skill['grp']}\n"
        f"- 版本: {skill['version']}\n\n"
        "## 能力说明\n\n"
        f"{skill['description']}\n\n"
        "## 输入\n\n"
        "- 结构化需求、原始转述或相关产物\n\n"
        "## 输出\n\n"
        "- 与该能力对应的结构化结果或交付物\n\n"
        "## 约束\n\n"
        "- 不臆造事实；缺失信息显式标注\n"
    )


def ensure_admin(conn):
    """Create the initial admin account, or reset it when WORKAGENT_RESET_ADMIN=1."""
    username = os.environ.get("WORKAGENT_ADMIN_USER", "admin")
    password = os.environ.get("WORKAGENT_ADMIN_PASSWORD", "admin123")
    if os.environ.get("WORKAGENT_RESET_ADMIN") == "1":
        conn.execute("UPDATE users SET password_hash=? WHERE username=?",
                     (hash_password(password), username))
        conn.execute("DELETE FROM sessions")
        print(f"[auth] admin password reset for {username}")
        return None
    if conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"] > 0:
        return None
    conn.execute(
        "INSERT INTO users (username,password_hash,display_name,role,created_at) VALUES (?,?,?,?,?)",
        (username, hash_password(password), "管理员", "admin", now_str()),
    )
    return username, password


def hash_password(password, salt=None):
    import hashlib
    import secrets
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return f"{salt}${digest.hex()}"


def verify_password(password, stored):
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return hash_password(password, salt) == stored


# ---------------------------------------------------------------- writers
def insert_requirement(conn, data, log_audit=True):
    fields = data.get("fields") or [
        {"k": ELEMENT_NAMES[i], "v": "待补充", "ok": False} for i in range(7)
    ]
    qa = data.get("qa") or []
    elements = data.get("elements")
    if elements is None:
        elements = sum(1 for f in fields if f.get("ok"))
    created = data.get("created_at") or now_str()
    conn.execute(
        """INSERT OR REPLACE INTO requirements
           (id,ref,title,role,source,client,stage,elements,priority,owner,raw_text,fields,qa,
            linear_status,linear_id,team,project,deliverable,updated_at,created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            data["id"], data["ref"], data["title"], data["role"], data.get("source", ""),
            data.get("client", ""), data.get("stage", "raw"), elements, data.get("priority", "中"),
            data.get("owner", ""), data.get("raw_text", ""),
            json.dumps(fields, ensure_ascii=False), json.dumps(qa, ensure_ascii=False),
            data.get("linear_status", "none"), data.get("linear_id"), data.get("team"),
            data.get("project"), data.get("deliverable"), data.get("updated_at") or created, created,
        ),
    )
    if log_audit:
        log_audit_row(conn, "system", "requirement.create", "requirement", data["id"], data["title"])


def insert_artifact(conn, data, log_audit=True):
    path = data.get("path") or make_artifact_path(data)
    created = data.get("created_at") or now_str()
    conn.execute(
        """INSERT OR REPLACE INTO artifacts
           (id,req_id,ref,name,type,role,version,size,author,path,note,updated_at,created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            data["id"], data.get("req_id"), data.get("ref"), data["name"], data["type"],
            data.get("role", "sa"), data["version"], data.get("size", "—"), data.get("author", ""),
            path, data.get("note", ""), data.get("updated_at") or created, created,
        ),
    )
    history = data.get("history")
    if history:
        for (ver, note, size, at) in history:
            vpath = data.get("path") or make_artifact_path(data, version=ver)
            conn.execute(
                """INSERT INTO artifact_versions (artifact_id,version,path,size,note,created_at)
                   VALUES (?,?,?,?,?,?)""",
                (data["id"], ver, vpath, size, note, at),
            )
    else:
        conn.execute(
            """INSERT INTO artifact_versions (artifact_id,version,path,size,note,created_at)
               VALUES (?,?,?,?,?,?)""",
            (data["id"], data["version"], path, data.get("size", "—"), data.get("note", "初始版本"), created),
        )
    if log_audit:
        log_audit_row(conn, data.get("author") or "system", "artifact.create", "artifact", data["id"], data["name"])


def insert_task(conn, data, log_audit=True):
    created = data.get("created_at") or now_str()
    conn.execute(
        """INSERT OR REPLACE INTO tasks
           (id,side,title,status,step,req_id,owner,elapsed,last,note,started,updated_at,created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            data["id"], data["side"], data["title"], data["status"], data.get("step", 0),
            data.get("req_id"), data.get("owner", ""), data.get("elapsed", "—"),
            data.get("last", ""), data.get("note", ""), data.get("started", "—"),
            data.get("updated_at") or created, created,
        ),
    )
    if log_audit:
        log_audit_row(conn, "system", "task.create", "task", data["id"], data["title"])


def log_audit_row(conn, actor, action, target_type, target_id, detail):
    conn.execute(
        """INSERT INTO audit (actor,action,target_type,target_id,detail,created_at)
           VALUES (?,?,?,?,?,?)""",
        (actor or "system", action, target_type, target_id, detail, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )


def make_artifact_path(data, version=None):
    role = data.get("role", "sa")
    ref = data.get("ref") or "REQ-XXX"
    ver = version or data.get("version", "v1.0")
    ext = ART_EXTS.get(data.get("type", "方案"), "md")
    safe = "".join(c if c not in '\\/:*?"<>|' else "_" for c in data["name"])
    return f"./output/{role}/{ref}/{safe}_{ver}.{ext}"


def resolve_output_path(artifact_path):
    """Map './output/sa/REQ-X/file.md' to an absolute path under DATA_DIR/output."""
    rel = artifact_path.replace("\\", "/")
    for prefix in ("./output/", "output/", "/output/"):
        if rel.startswith(prefix):
            rel = rel[len(prefix):]
            break
    rel = rel.lstrip("./").lstrip("/")
    rel = os.path.normpath(rel).replace("\\", "/")
    if rel.startswith(".."):
        raise ValueError("path escapes output directory")
    return os.path.join(OUTPUT_DIR, rel)


def write_artifact_file(artifact, content):
    """Persist the artifact body to disk so it can be downloaded for real."""
    full = resolve_output_path(artifact["path"])
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return full
