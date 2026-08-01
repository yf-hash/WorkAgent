# WorkAgent

> 以 **Claude Code 为算力入口**、以 **harness 五能力分层为执行框架**、以 **86 commands + 24 agents + 115 skills** 为业务组件的 AI 工作智能体系。
>
> 服务对象：产品经理、售前工程师、市场营销、内容作者、售前 SA。

## 快速上手

打开一个 Claude Code 会话（在本仓库目录），敲斜杠命令：

```bash
/prd 用户可以查看消费明细 --mode standard      # 生成 PRD
/bid RFP.pdf --phase all                        # 标书七阶段
/humanize ./draft.md --mode all                 # 三段式去 AI 味
/dashboard --metric aarrr                       # AARRR 漏斗看板
/market-research AI 写作工具市场                # 竞品调研
```

命令全清单见 [`.claude/README.md`](.claude/README.md)。

## 核心理念

**模型负责思考，harness 负责执行 / 约束 / 循环 / 记忆 / 安全。**

- 模型（Claude Opus / Sonnet）：理解、生成、决策、反思
- Harness（Claude Code + 本仓库 `.claude/harness/`）：工具白名单、权限画像、循环模板、记忆读写、危险动作拦截

架构与设计原理见 **[HARNESS_FRAMEWORK.md](HARNESS_FRAMEWORK.md)**。

## 顶层目录

```
WorkAgent/
├── HARNESS_FRAMEWORK.md          # 顶层框架文档（读这一份就够了）
├── README.md                     # 本文件
│
├── .claude/                      # harness 层
│   ├── CLAUDE.md                 # 项目级说明（每次会话必读）
│   ├── settings.json             # 全局权限 + hooks 位
│   ├── harness/                  # 五能力原语（execute/constrain/loop/memory/security）
│   ├── hooks/                    # hook 脚本（默认未启用）
│   ├── memory/                   # 项目级记忆
│   ├── scripts/                  # 维护脚本（migrate / validate）
│   └── README.md                 # 完整命令 / 组件索引
│
├── commands/                     # 86 个斜杠命令（用户直接调用的入口）
│   ├── writing/                  # 9  写作类
│   ├── product/                  # 30 产品管理
│   ├── presales/                 # 29 售前 / 方案
│   ├── media/                    # 12 PPT / 视频 / 图表
│   ├── research/                 # 5  调研
│   └── tools/                    # 1  工具
│
├── agents/                       # 24 个业务角色代理（编排多 skill）
├── skills/                       # 115 个原子知识模块（14 子域）
├── templates/                    # 25 个填充模板
│
└── docs/                         # 元文档归档（AGENT_ROUTING / AUDIT / HEALTH / CONSOLIDATION）
```

## 版本

- **v3.0（2026-08-01）**：引入 harness 五能力分层，225 个业务组件全部带 `harness:` 块（100% 覆盖）
- v2.8.2：合并 `/pm-prd-enterprise` 到 `/prd --mode enterprise`
- v2.8.1：合并 11 个 `prd-*` 命令到 `/prd --mode`
- v2.8：commands 按主题合并、skills 分入 14 子域
- 更早：见 `docs/HEALTH_REPORT.md`

## 编辑器支持

Claude Code（完整支持）> Cursor > OpenAI Codex

## 贡献

- 加新 command / skill / agent 前先看 [`.claude/memory/conventions.md`](.claude/memory/conventions.md)
- 补 harness 元数据：`python .claude/scripts/migrate.py --target all --apply`
- 校验：`python .claude/scripts/validate-harness.py --strict`
