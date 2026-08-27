---
name: content-intake
description: 内容请求网关方法论工具箱 — 供 /content-intake 命令调用。含八大文体分类规则库、需求解析字段抽取规则、项目关联识别、ContentRequest JSON Schema、可信度分级。
user-invocable: false
---

# content-intake — 内容请求网关工具箱

> 本 skill 被 `/content-intake` 命令调用。

## 一、八大文体分类规则库

### 分类关键词表

| Style ID | 名称 | 高置信度触发词 | 中置信度触发词 |
|---|---|---|---|
| `promo` | 产品推广文 | 推广文、产品推广、卖点、场景化 | 客户价值、决策者、软文 |
| `solution-doc` | 产品解决方案文 | 解决方案文、方案文档、客户方案 | 应用场景、行业痛点 |
| `tech-whitepaper` | 产品技术白皮书 | 技术白皮书、技术架构、技术原理 | 技术挑战、架构说明、性能 |
| `ppt` | 产品 PPT | PPT、演示文稿、幻灯片、slides | 大纲、汇报、Deck |
| `solution-whitepaper` | 产品解决方案白皮书 | 解决方案白皮书、行业白皮书 | 行业方案、行业趋势、落地路径 |
| `activity-tweet` | 产品活动推文 | 推文、公众号、活动、新品上线 | 引流、传播、福利 |
| `pr` | 企业 PR 稿 | PR 稿、新闻稿、媒体稿、发布稿 | 媒体、通稿、Press Release |
| `tech-popular` | 产品技术科普文 | 科普、由浅入深、通俗、讲清楚 | 是什么、怎么工作、原理 |

### 二级消歧规则

如果一个输入命中多个文体，用以下规则消歧：

| 冲突情形 | 消歧 |
|---|---|
| 推广文 vs 解决方案文 | 有明确"客户 / 方案 / 场景"→ 解决方案文；只是"介绍产品" → 推广文 |
| 技术白皮书 vs 解决方案白皮书 | "技术架构 / 技术原理" → 技术白皮书；"行业 / 落地 / 案例" → 解决方案白皮书 |
| 推文 vs PR 稿 | "公众号 / 社群 / 引流" → 推文；"媒体 / 通稿 / 记者" → PR 稿 |
| 科普 vs 技术白皮书 | 有"通俗 / 讲清楚 / 面向初学者" → 科普；有"技术指标 / 严谨" → 技术白皮书 |

命中零个 or 冲突无法消歧 → **AskUserQuestion 展示八选一**。

## 二、项目关联识别规则

### 显式路径（优先级最高）
- `--project ./output/pm-pipeline/xxx/` → 直接采用
- `--project ./output/sa-pipeline/xxx/` → 直接采用

### 项目 ID（PM-xxx / SA-xxx）
- 从输入抽取 `PM-\d+` 或 `SA-\d+`
- 在 `./output/pm-pipeline/` 或 `./output/sa-pipeline/` 下查找

### 项目 slug（模糊匹配）
- 从输入抽取产品 / 项目名（如 "VulnHunter"）
- 在 `./output/pm-pipeline/*vulnhunter*` 或 `sa-pipeline` 中查找
- 找到多个 → AskUserQuestion 让用户选
- 找到一个 → 直接采用（信心度=medium）
- 找到零个 → `project.linked = false`

### 项目路径校验
必须存在以下核心产物之一：
- PM 项目：`04-PRD.md` 或 `05-tech-spec.md`
- SA 项目：`03-overall-solution.md` 或 `04-rfp-response.md`

不存在 → 提示"项目未完成，M2 可能素材不足"。

## 三、需求解析字段抽取规则

### audience（受众）

| 触发模式 | 举例 |
|---|---|
| "面向 XX / 目标读者 XX / 给 XX 看" | "面向企业安全负责人" → primary |
| "适合 XX / 针对 XX" | "针对政企客户" → primary |
| "同时给 XX" | "同时给 IT 决策者" → secondary |
| 未提及 | 依 style 默认 |

**style 默认受众**（如未指定）：
- promo → "潜在客户 + 决策者"
- solution-doc → "客户 IT + 业务负责人"
- tech-whitepaper → "技术受众（CTO / 架构师）"
- ppt → "会议汇报对象"
- solution-whitepaper → "客户决策者 + 技术负责人"
- activity-tweet → "现有 / 潜在用户"
- pr → "媒体 + 公众"
- tech-popular → "开发者 / 技术爱好者"

### length（篇幅）

| 触发 | 解析 |
|---|---|
| "N 字左右 / N 字上下" | value=N, unit=字 |
| "N-M 字" | value=(N+M)/2, unit=字 |
| "N 页" | value=N, unit=页（PPT 用） |
| "简短 / 精简" | 依 style 最短档 |
| "详细 / 完整" | 依 style 最长档 |
| 未提及 | 依 style 中位数 |

**style 默认篇幅**：
- promo: 1500 字
- solution-doc: 3000 字
- tech-whitepaper: 8000 字
- ppt: 20 页
- solution-whitepaper: 12000 字
- activity-tweet: 1000 字
- pr: 1000 字
- tech-popular: 3000 字

### tone（语气 / 风格）

| 触发关键词 | 标签 |
|---|---|
| "正式 / 严肃" | 正式 |
| "专业 / 严谨 / 技术" | 专业 |
| "轻量 / 活泼 / 有趣" | 轻量 |
| "通俗 / 易懂" | 通俗 |
| "商业 / 营销" | 商业 |
| "客观 / 中立" | 客观 |

**style 默认 tone**：见 manifest.yaml。

### emphasis（重点突出）
- "突出 XX / 重点讲 XX / 强调 XX / 主要说 XX"
- 抽取名词短语作为 emphasis 项

### forbidden（禁止内容）
- "不要 XX / 避免 XX / 禁止 XX / 不能说 XX"
- 常见禁止：
  - "过度技术细节"
  - "夸大宣传"
  - "价格 / 报价"
  - "内部信息"
  - "竞品名字"

### format_out（输出格式）
- `--format-out markdown|word|ppt-json`
- 或从输入："输出 XX 格式 / 导出 XX"
- 默认：markdown

### include_mermaid（架构图）
- "架构图 / Mermaid / 流程图" → true
- style = tech-whitepaper / solution-whitepaper / ppt → 默认 true
- 其他 → 默认 false

### include_cases（案例）
- "含案例 / 客户故事 / case study" → true
- style = solution-whitepaper / solution-doc → 默认 true

## 四、ContentRequest JSON Schema

见 `commands/content/content-intake.md` § 阶段 4 输出示例。

## 五、可信度分级

| 字段 | 信心度 | 处理 |
|---|---|---|
| 用户显式给出 | high | 直接采用 |
| 从输入清晰抽取 | medium | 采用，但在 gate 让用户确认 |
| 根据 style 默认推断 | low | 采用，明确标注"默认值" |
| 无法确定 | none | 加入 unresolved 列表，让 gate 询问 |

## 六、常见解析陷阱

| 陷阱 | 症状 | 修正 |
|---|---|---|
| 文体识别不准 | "写点东西关于 X" 无法识别 | AskUserQuestion 八选一 |
| 项目路径无效 | --project 目录不存在 | 校验后报错，让用户改 |
| 篇幅数字歧义 | "N 字" 是字 / 页 / 章节？ | 按 style 默认单位 |
| forbidden 未抽取到 | "不涉及价格" 被漏 | 双关键词扫描 |
| 语言检测错 | 中英混合内容 | --lang 显式指定 |

## 七、反模式

- ❌ 文体识别失败仍继续 —— 违规
- ❌ 项目关联但未校验目录 —— 会在 M2 崩
- ❌ length 用推测值而不标"默认" —— 用户误以为是他自己设置
- ❌ ambiguity 字段留空 —— 违规
- ❌ 覆盖用户显式参数 —— 违规
