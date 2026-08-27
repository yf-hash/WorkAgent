---
name: pm-archive
description: 【模块 7】产物审阅与版本归档 Agent — 扫描 pm-pipeline 目录，生成 README 索引 / CHANGELOG / 版本号 / 交叉引用检查报告，并按语义化版本递增号存档。
user-invocable: true
argument-hint: "<pm-pipeline 目录路径> [--bump major|minor|patch] [--freeze] [--tag <name>]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
model: sonnet  # 轻量：归档 + 版本递增 + 交叉引用检查，无需 opus
harness:
  execute:
    preset: writing-scoped
    tools: [Bash]  # extend: freeze 打包 / 版本 tag / 交叉引用检查
  constrain:
    profile: writing-safe
    gates: [before-write, before-freeze]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
    writes: [archive-history]
  security:
    danger-level: low
---

# /pm-archive — 产物审阅与版本归档 Agent（Module 7）

> **端到端 6 模块流水线的第 6 站（收尾）**
>
> /pm-clarify → /pm-solution → /pm-prototype → /prd → /pm-tech-spec →【本命令】

## 一句话

**扫描 pm-pipeline 目录里的 6 类产物，生成 README 索引 + CHANGELOG + 版本号 + 交叉引用完整性检查报告，并按需 freeze 成只读版本快照**。

## 输入

```bash
# 归档一个已完成的流水线目录（默认递增 patch 版本）
/pm-archive ./output/pm-pipeline/invoice-import-20260827/

# 递增 minor 版本（新增功能场景）
/pm-archive ./output/pm-pipeline/invoice-import-20260827/ --bump minor

# 递增 major 版本（不兼容变更）
/pm-archive ./output/pm-pipeline/xxx/ --bump major

# freeze 冻结（生成不可修改的 v1.0-frozen 只读快照）
/pm-archive ./output/pm-pipeline/xxx/ --freeze --tag "v1.0-上线版"
```

## 产物

在指定的 pm-pipeline 目录下生成/更新：

```
./output/pm-pipeline/{topic}-{yyyymmdd}/
  ├── README.md                    ← 【本命令产出】目录索引 + 版本
  ├── CHANGELOG.md                 ← 【本命令产出】变更历史
  ├── VERSION                       ← 【本命令产出】语义化版本号
  ├── 01-clarify-report.md          ← M2 产出
  ├── 02-business-solution.md       ← M3 产出
  ├── 03-prototype/                 ← M4 产出
  │   ├── 03-prototype-desc.md
  │   ├── 03-prototype.json
  │   ├── 03-flow.mmd
  │   ├── 03-flow-exception.mmd
  │   └── 03-validate.md
  ├── 04-PRD.md                     ← M5 产出
  ├── 04-PRD-validate.md            ← M5 校验
  ├── 05-tech-metrics.md            ← M6 产出
  ├── 05-tech-spec.md               ← M6 产出
  ├── 05-tech-spec-validate.md      ← M6 校验
  ├── review-notes.md               ← 【本命令产出】人工审阅记录（可选）
  ├── archive-report.md             ← 【本命令产出】交叉引用完整性报告
  └── _frozen/                     ← --freeze 生成
      └── v1.0-上线版/              ← 只读快照
```

## 内部三步

### 步骤 1：扫描 & 完整性检查

调用 `skills/pm/pm-artifact-archive` 里的规则库检查：

**必备产物 checklist**：
- [ ] 01-clarify-report.md（M2）
- [ ] 02-business-solution.md（M3）
- [ ] 03-prototype/*.json + *.md + *.mmd（M4）
- [ ] 04-PRD.md（M5）
- [ ] 05-tech-metrics.md + 05-tech-spec.md（M6）

**交叉引用检查**：
- [ ] PRD 引用的功能是否都在业务方案里
- [ ] PRD 引用的页面是否都在原型 JSON 里
- [ ] 技术规格书引用的模块是否都在 PRD 里
- [ ] 澄清报告的假设项是否在下游被响应
- [ ] 每份文档的时间戳先后顺序合理

**校验报告状态确认**：
- [ ] 04-PRD-validate.md 总体结论 ≠ "需重写"
- [ ] 05-tech-spec-validate.md 总体结论 ≠ "需重写"
- [ ] 03-validate.md 总体结论 ≠ "需重设计"

任一项不满足 → **拒绝归档**，输出待补清单。

### 步骤 2：生成 README.md（索引）

```markdown
# 产品需求包：{{topic}}

> 版本：v{{semver}}
> 状态：草稿 / 评审中 / 已冻结
> 生成日期：{{yyyy-mm-dd}}
> 归档人：{{git user.name 或询问}}

## 一句话

{{从澄清报告 § 1 提取}}

## 交付物索引

| # | 阶段 | 产物 | 状态 |
|---|---|---|---|
| M2 | 需求澄清 | [01-clarify-report.md](./01-clarify-report.md) | ✅ |
| M3 | 业务方案 | [02-business-solution.md](./02-business-solution.md) | ✅ |
| M4 | 原型底稿 | [03-prototype/](./03-prototype/) | ✅ |
| M5 | PRD 主文档 | [04-PRD.md](./04-PRD.md) + [validate](./04-PRD-validate.md) | ✅ |
| M6 | 技术规格 | [05-tech-spec.md](./05-tech-spec.md) + [metrics](./05-tech-metrics.md) + [validate](./05-tech-spec-validate.md) | ✅ |

## 关键决策

（从澄清报告的假设项 + 业务方案的优先级 + 规格书的验收标准 汇总提取）

## 关键指标

（从技术规格书总表提取严重度 = 高的指标）

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)

## 与研发协作

- 系统技术设计交给研发：将 04-PRD.md + 05-tech-spec.md 作为输入，交由研发团队进行系统设计
- 测试用例设计：将 04-PRD.md + 05-tech-spec.md 作为输入，交由 QA 团队编写用例
- UI 设计交付：将 03-prototype/ 目录（含 JSON）交给设计师做高保真

## 反向溯源

如果需要修改：
- 需求方向变了 → 回 `/pm-clarify --refine`
- 功能优先级变了 → 回 `/pm-solution --refine`
- 原型页面变了 → 回 `/pm-prototype --refine`
- 单点功能微调 → `/prd --mode update`
- 技术指标微调 → `/pm-tech-spec --mode update`
```

### 步骤 3：生成 CHANGELOG.md（变更历史）

首次归档：
```markdown
# CHANGELOG

## v1.0.0 - 2026-08-27

### 初次归档
- [x] M2 需求澄清（auto 模式）
- [x] M3 业务方案（P0: {n}, P1: {m}, P2: {k}）
- [x] M4 原型底稿（{page-count} 页）
- [x] M5 PRD full 模式
- [x] M6 技术规格书（{metric-count} 项指标）

### 关键假设（待验证）
- {从 M2 假设项拷贝}

### 已知未解决问题
- {从校验报告的 ❌ 项汇总}
```

后续归档（--bump patch/minor/major）：

```markdown
## v1.0.1 - 2026-08-30

### 修改（patch）
- [x] M5 PRD 修正批量导入的错误提示文案
- [x] M6 邮件依赖 SLA 从 99% 调整为 99.9%

### 未变
- M2 / M3 / M4 保持 v1.0.0

## v1.1.0 - 2026-09-05

### 新增（minor）
- [x] M3 新增 "P1 - 支持导入模板下载"
- [x] M4 新增 P3-1 模板下载页
- [x] M5 PRD 补充 § 3.5 模板下载
```

## Harness 卡点

- **归档前 gate**：如果任一校验报告状态 = "需重写"，AskUserQuestion：
  ```
  以下产物未通过校验：
    - 04-PRD-validate.md：需重写（缺失异常流程 3 处）
    - 05-tech-spec-validate.md：需重写（歧义指标 5 项）

  是否仍要归档？
  - n（推荐）：先回上游修复
  - y-force：强制归档，问题写入 known-issues.md
  ```
- **freeze 前 gate**：`--freeze` 会创建只读快照，AskUserQuestion 二次确认：
  ```
  Freeze 后：
    - _frozen/{tag}/ 目录下所有文件将被设置为只读
    - 后续再改必须新起版本（v1.1.0 起）
  确认？(y / n)
  ```

## 目录规范

### {topic} 命名规则
- 优先从 M2 clarify-report 的关键词提取
- 长度 ≤ 20 字符，英文小写 + 连字符
- 例：`invoice-import` / `ai-contract-review` / `sso-onboarding`

### 版本号规则（语义化）
- `major`：需求范围变化 / 目标用户变化 / 不兼容变更
- `minor`：新增功能 / 新增模块 / 新增指标类别
- `patch`：文案修正 / 指标数值微调 / 校验发现的小问题

### freeze 场景
- 上线前的最终版
- 提交给客户的交付版
- 招投标响应版
- 审计留档版

## review-notes.md（可选，人工审阅记录）

```markdown
# 审阅记录

## 审阅时间：{{yyyy-mm-dd}}
## 审阅人：{{name}}

### 通过 ✅
- M2 澄清报告完整
- M4 原型逻辑校验通过

### 需修改 ⚠️
- M3 P1 功能"XX"应下沉到 P2 —— 已在 v1.0.1 修正
- M5 埋点缺"批量导出成功率"事件 —— 已在 v1.0.1 补齐

### 拒绝 ❌
- 无
```

## archive-report.md（交叉引用检查报告）

```markdown
# 归档检查报告

## 完整性 ✅
所有 6 类产物齐全。

## 交叉引用 ✅
- PRD 引用的所有功能都在业务方案中
- PRD 引用的所有页面都在原型 JSON 中
- 技术规格书引用的所有模块都在 PRD 中
- M2 假设项 12 条，全部在 M3-M6 中被响应

## 校验状态 ✅
- M4 逻辑校验：通过
- M5 PRD 校验：有修改建议（已合并到 v1.0.0）
- M6 技术规格校验：有修改建议（已合并到 v1.0.0）

## 时间线合理性 ✅
M2 (17:22) < M3 (18:05) < M4 (19:14) < M5 (20:33) < M6 (21:48)
```

## 与其他命令的边界

| 场景 | 用 |
|---|---|
| **完成 6 模块流水线，归档** | 本命令 |
| 单文档版本控制 | 手动 git commit |
| 生成客户交付包（PDF / 打包） | 本命令归档后手动打包 |
| 冻结版本用于对外发送 | 本命令 `--freeze` |
| 需要一键跑完整 6 模块流水线 | `/pm-pipeline`（本命令是其最后一步 M7） |

## 反模式

- ❌ 校验报告没过就归档——违规
- ❌ 修改 freeze 版本内容——违规
- ❌ 不更新 CHANGELOG 直接改文件——违规
- ❌ 版本号乱跳（1.0.0 → 3.0.0）——违规
