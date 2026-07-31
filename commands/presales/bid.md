---
name: bid
description: 标书七阶段全流程（analyze / clarify / outline / write / review / check / export）。用 --phase 单跑一阶段，或 --phase all 走完整流水线。三色标记 + 偏离表 + 双轮评审 + 合规核查。
user-invocable: true
argument-hint: "[--phase 1..7|analyze|clarify|outline|write|review|check|export|all] [<输入路径>] [其他 phase 特定参数]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Bash]
---

# /bid — 标书全流程

## 一句话

七阶段原子技能串成一个入口。默认交互式串行，`--phase` 可跳到任意一阶段。

## 用法

```bash
# 全流程（默认，交互式串行）
/bid RFP.pdf --phase all

# 单阶段
/bid RFP.pdf --phase 1                          # 或 --phase analyze
/bid --phase clarify                            # Phase 2：技术要求澄清
/bid --phase outline --from 要求清单.xlsx --with-deviation
/bid --phase write --section solution --mode interactive
/bid --phase write --section all --mode batch
/bid --phase review draft-v1.md
/bid --phase check final.md
/bid --phase export final.md
```

## 七阶段清单

| Phase | 别名 | 技能 | 交付物 |
|---|---|---|---|
| 1 | `analyze` | `skills/bid-analyze/SKILL.md` | 三色标记（🔴 废标 / 🟡 高分 / 🔵 基础）+ 技术要求清单 |
| 2 | `clarify` | `skills/bid-clarify/SKILL.md` | 内部评审 + 正式澄清问题 + 最终技术要求清单 |
| 3 | `outline` | `skills/bid-outline/SKILL.md` | 技术偏离表骨架 + 按评分细则的章节顺序 + 字数配比 |
| 4 | `write` | `skills/bid-write/SKILL.md` | 9 模块（understanding/solution/implementation/management/quality/service/performance/team/commercial） |
| 5 | `review` | `skills/bid-review/SKILL.md` | 第一轮五视角（business/technical/delivery/risk/competitive）+ 第二轮专家评审 |
| 6 | `check` | `skills/bid-check/SKILL.md` | 合规性核查 + 一致性验证 + 查重检测 |
| 7 | `export` | `skills/bid-export/SKILL.md` | 最终通读 + 文档生成规范 + 移交清单 |

## 分派规则

- `--phase 1..7` 或 `--phase <alias>` → 加载对应 skill，独立执行
- `--phase all` → 依次跑 1→7，每阶段结束用 `AskUserQuestion` 确认 gate
- 不带 `--phase` 且首个位置参数是 `.pdf/.docx` → 默认 `--phase analyze`
- 不带 `--phase` 且不带位置参数 → 报错并提示可用 phases

## 与其他售前命令的边界

| 场景 | 用 |
|---|---|
| 客户拿来的正式招标文件（多章节文档） | **本命令** |
| 项目建议书 / 可研 / 初步设计（无正式招标） | `/proposal` |
| RFP Excel（多单选题）| `/rfp-response` |
| 安全问卷（CAIQ/SIG/VSA） | `/security-questionnaire` |
| 售前全链路（首访 → PoC → 合同） | `@solution-architect` |

## 迁移说明（v2.8）

旧命令 `/bid-analyze` / `/bid-clarify` / `/bid-outline` / `/bid-write` / `/bid-review` / `/bid-check` / `/bid-export` 已合并至本命令，用 `--phase <name>` 或 `--phase 1..7` 替代。7 个 skill 未变。
