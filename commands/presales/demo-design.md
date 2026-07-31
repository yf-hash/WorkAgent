---
name: demo-design
description: >
  Demo 设计与沙盘演练 — 售前 SE 向客户演示产品的完整准备工作流。含 Demo 三段式
  （场景对齐 / 价值演示 / Next Step）、客户化故事线、三套数据集（行业脱敏 / 客户化 /
  异常）、5 类异常应对剧本、5 类反对意见库、Demo 评分自检（节奏 / 情感 / 信息 / 防御）。
user-invocable: true
argument-hint: "<客户公司或场景> [--mode storyline|data|rehearse|review|kit] [--type business|technical|poc|demo-day] [--industry fintech|gov|healthcare|saas] [--duration 30|60|90]"
---

# /demo-design — Demo 设计与沙盘演练

加载技能：`skills/presales/demo-design/SKILL.md`
配套 Skill：`marketing-copy --type demo`（写脚本）、`discovery-call`（提取客户痛点）

## 触发条件
- 客户化关键 Demo 需要专门设计故事线
- Demo 前演练 / 异常应对剧本准备
- Demo 后评分复盘 / 改进
- Demo 后续物料打包

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<客户公司或场景>` | — | — |
| `--mode` | 工作模式 | `storyline` |
| `--type` | Demo 类型 | `business` |
| `--industry` | 客户行业 | — |
| `--duration` | Demo 时长（分钟）| `30` |

### 工作模式

| `--mode` | 输出 |
|----------|------|
| `storyline` | 客户化故事线（业务场景 / 痛点剧情 / 解决路径 / 量化成果）|
| `data` | 数据集准备清单 + 客户化定制建议（低 / 中 / 高三档成本）|
| `rehearse` | 演练 SOP + 5 类异常应对剧本 + 5 类反对意见应答 |
| `review` | Demo 后评分（节奏 30 / 情感曲线 30 / 信息 30 / 防御 10）|
| `kit` | Demo 后 24 小时内跟进物料清单 |

### Demo 类型

| `--type` | 受众 | 时长 | 重点 |
|----------|------|------|------|
| `business` | EB / 业务负责人 | 20-30 分钟 | 业务场景 + 价值 + ROI |
| `technical` | TB / 工程师 | 60-90 分钟 | 架构 / API / 集成 / 部署 |
| `poc` | 客户混合团队 | PoC 周期 | 客户真实数据 + Phase 1 量化结果 |
| `demo-day` | 多客户路演 | 5-10 分钟 | 极简版 + 强情感 |

## 使用示例

```
/demo-design 某城商行 --mode storyline --type business --industry fintech --duration 30
/demo-design 某 SaaS 客户技术评估 --mode storyline --type technical --duration 60
/demo-design 某关键客户 --mode rehearse --type business
/demo-design 上次 Demo 复盘 --mode review --type business
/demo-design 客户 X --mode kit
```

## 执行流程

### `--mode storyline`（客户化故事线）
```
Step 1: 客户场景对齐
  → 加载 discovery-call 输出（如有）
  → 提炼客户业务场景 + 客户原话 + 痛点

Step 2: 故事线四件套
  → 业务场景（30 秒）
  → 痛点剧情（90 秒）
  → 解决路径（10-15 分钟，3 个动作）
  → 量化成果（90 秒）

Step 3: 时间分配
  → 0-5 场景对齐 / 5-22 价值演示 / 22-27 客户化深谈 / 27-30 Next Step

Step 4: 反模式扫描
  → 避免 Feature Tour / 60 分钟一气呵成 / 默认数据 / 没结尾
```

### `--mode data`（数据集准备）
```
Step 1: 必备三套数据
  → 行业脱敏 / 客户化 / 异常场景
Step 2: 客户化定制级别
  → 低（1-2 小时）：菜单 / Logo / 字段名
  → 中（半天）：业务流程 / 行业术语
  → 高（1-3 天）：客户真实数据 / 模拟客户工作流
Step 3: 防御性检查
  → 数据量级 / 中文本地化 / 日期未过期 / 异常兜底
```

### `--mode rehearse`（演练）
```
Step 1: 三遍演练 SOP
  → 自跑 / 同事旁观 / 模拟难客户
Step 2: 5 类异常应对剧本
  → 崩溃 / 加载慢 / 网络断 / 超出范围 / 效果不达预期
Step 3: 5 类反对意见应答
  → 复杂 / 迁移成本 / 价格 / 决策慢 / 对手有
Step 4: 关键检查点
  → 时长 / 衔接 / 数字记忆 / 异常背诵
```

### `--mode review`（评分）
```
Step 1: 节奏（30 分）
  □ 场景共鸣（10）□ 时间分配（10）□ Next Step（10）
Step 2: 情感曲线（30 分）
  □ 痛点共鸣（10）□ 演示惊喜 ≥2 次（10）□ 收尾给行动（10）
Step 3: 信息密度（30 分）
  □ 行业关键词（10）□ ≥5 个数字（10）□ ≥1 个同行案例（10）
Step 4: 防御性（10 分）
  □ 异常应对（5）□ 反对意见（5）

合格 80 / 优秀 90
```

### `--mode kit`（后续物料）
```
1. Demo 录屏（≤30 分钟精华版）
2. Demo 中提到的客户案例 PPT
3. 客户现场提问的事后答复
4. Business Case 一页纸（如客户问到）
5. Next Step 时间确认
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/demo-design` vs `/marketing-copy --type demo` | Demo 设计与演练方法论 | Demo 脚本撰写 |
| `/demo-design` vs `/sales-guide` | Demo 这一具体场景 | 销售一页禅（产品总体）|
| `/demo-design` vs `/discovery-call` | 第 3+ 次会议（产品演示）| 第 1-2 次（需求挖掘）|
| `/demo-design` vs `/poc-plan` | 30-90 分钟现场演示 | 4-12 周完整 PoC |
