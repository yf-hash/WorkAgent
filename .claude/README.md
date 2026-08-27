# .claude — Harness 层配置

WorkAgent（PM Harness + SA Harness + Content Harness）的 Claude Code 层配置目录。所有 harness 原语在此。

## 目录

```
.claude/
├── CLAUDE.md              # 项目级说明（每次会话必读）
├── README.md              # 本文件
├── settings.json          # 全局权限 + hooks 位
├── harness/                # 五能力原语
│   ├── execute/           # 工具预设
│   ├── constrain/         # 权限画像
│   ├── loop/              # 循环模式
│   ├── memory/            # 记忆作用域
│   ├── security/          # 安全策略
│   └── role/              # 角色路由 SOP
├── hooks/                 # hook 脚本
├── memory/                # 项目级记忆
│   ├── MEMORY.md          # 索引
│   ├── project-context.md
│   ├── conventions.md
│   └── decisions.md
└── scripts/               # 校验 / 迁移
```

## 快速索引

- 顶层框架：[../HARNESS_FRAMEWORK.md](../HARNESS_FRAMEWORK.md)
- PM 6 模块流水线：[../docs/PM_HARNESS.md](../docs/PM_HARNESS.md)
- SA 7 模块流水线：[../docs/SA_HARNESS.md](../docs/SA_HARNESS.md)
- Content 5 模块流水线：[../docs/CONTENT_HARNESS.md](../docs/CONTENT_HARNESS.md)
- 项目级会话说明：[CLAUDE.md](CLAUDE.md)

## 三条流水线命令一览

### PM Harness（6 模块主流水线 + 竞品分析横向能力）

**推荐一键入口**：
```bash
# 主流水线（需求 → PRD → 技术规格）
/pm-pipeline "一句话原始需求" --mode human --product-type saas-b

# 竞品分析工程化（横向能力）
/pm-competitive "产品定位" [--mode full|monitor|refresh]

# 自然语言智能路由
/pm 客户要一个批量导入发票功能，做完整交付包
/pm 帮我分析下 AI 写作赛道的竞品
```

| 命令 | 阶段 | 作用 |
|---|---|---|
| **主流水线** | | |
| `/pm-clarify` | M2 | 一句话 → 澄清报告 |
| `/pm-solution` | M3 | 澄清 → 业务方案 |
| `/pm-prototype` | M4 | 方案 → 原型底稿（JSON/Mermaid） |
| `/prd --validate` | M5 | → PRD + 4 类校验 |
| `/pm-tech-spec` | M6 | → 技术规格书 |
| `/pm-archive` | M7 | 归档 |
| `/pm-pipeline` | 编排 | 一键跑 6 模块 |
| **竞品分析（横向能力）** | | |
| `/pm-competitive-scan` | 阶段 1 | 竞品发现 + 情报采集 |
| `/pm-competitive-benchmark` | 阶段 2 | 5 维对标 + 战略 + 话术 |
| `/pm-competitive` | 编排 | 一键跑两阶段（含 monitor/refresh） |

### SA Harness（7 模块 - 对外售前）

**推荐一键入口**：
```bash
/sa-pipeline "客户信息" --client "XX" --industry finance --compliance 等保三级
/sa 某客户要替换老系统，需要私有化 + 国产化   # 自然语言智能路由
```

| 命令 | 阶段 | 作用 |
|---|---|---|
| `/sa-intake` | M1 | 销售/RFP → 结构化项目对象 |
| `/sa-clarify` | M2 | → 客户调研痛点报告 |
| `/sa-solution-map` | M3 | → 业务能力映射 + 竞品 + 风险 |
| `/sa-architect` | M4 | → 总体方案 + 架构 + 三项校验 |
| `/sa-poc` | M5.1 | POC 测试方案 |
| `/sa-impl` | M5.2 | 实施方案 |
| `/sa-rfp` | M5.3 | RFP 应答 + 偏离表 |
| `/sa-quote` | M6 | 配置估算 + 宣讲底稿 |
| `/sa-archive` | M7 | 归档 |
| `/sa-pipeline` | 编排 | 一键跑 7 模块 |

### Content Harness（5 模块 - 八大文体内容创作）

**推荐一键入口**（**单一调用入口**）：
```bash
# 一句自然语言（自动识别文体）
/content "基于 VulnHunter 项目写一份解决方案白皮书" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --writeback

# 或用角色总入口
/content 帮我给项目 X 出一份汇报 PPT
```

| 命令 | 阶段 | 作用 |
|---|---|---|
| `/content-intake` | M1 | 自然语言 → ContentRequest JSON（文体识别 + 需求解析） |
| `/content-materials` | M2 | 拉取 PM/SA 项目产物 → 素材池 |
| `/content-generate` | M3 | 八大文体专项生成初稿 |
| `/content-validate` | M4 | 5 类校验（事实/合规/风格/完整/引用） |
| `/content-archive` | M5 | 归档 + 多格式导出 + 回写 |
| `/content` | 统一入口 | 一键跑 5 模块（对外唯一入口） |

**八大文体**：promo / solution-doc / tech-whitepaper / ppt / solution-whitepaper / activity-tweet / pr / tech-popular

## 三条流水线的关系

```
                        WorkAgent
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
      /pm                  /sa                /content
    (内部 PRD)           (对外方案)           (内容传播)
       │                    │                    │
       └───────素材──────► /content ◄──────素材──┘
                            │
                            ▼
                   产出可回写到 PM/SA
                   {project}/_content/
```

- **PM**：内部产品 PM 视角，从需求想法到 PRD + 技术规格书
- **SA**：售前工程师视角，从客户输入 / RFP 到方案 + POC + 应答 + 报价
- **Content**：内容 / 市场 / 品牌视角，一句话到八大文体物料
- **共用**：都基于本目录五能力分层框架
- **Content 特有**：跨流水线复用 PM/SA 素材 + 回写附属产物

详见 [../README.md](../README.md)。

## 反模式

- ❌ 编辑 `.claude/settings.json` 未经用户确认 —— 属于 security.deny list
- ❌ 写 memory 记录 API key / 密码 / 敏感路径 —— 属于 security 拦截项
- ❌ 编辑 `HARNESS_FRAMEWORK.md` 未同步更新 `docs/*_HARNESS.md`
- ❌ 混用不同流水线的输出目录
- ❌ Content 生成时不关联 PM/SA 项目却引用具体数字 —— 事实错误温床

## 版本

- v3.2（2026-08-27）：新增 Content Harness 5 模块流水线（八大文体内容创作）
- v3.1（2026-08-27）：PM Harness 新增竞品分析工程化能力（横向能力）
- v3.0（2026-08-27）：新增 SA Harness 7 模块流水线（对外售前场景）
- v2.0（2026-08-27）：精简至端到端 6 模块 PM 流水线
- v1.x：见 git history
