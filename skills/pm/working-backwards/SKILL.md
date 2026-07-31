---
name: working-backwards
description: >
  Working Backwards 方法论知识库（亚马逊范式）— 倒推产品价值，先写新闻稿+FAQ+6-pager，
  评审通过后才进入 PRD 写作。强制"客户先于产品"的思维约束，避免"工程驱动"立项。
  触发词：Working Backwards、逆向工作法、新闻稿、PR-FAQ、6 页备忘录、6-pager、
  press release、亚马逊范式、客户先于产品、倒推法。
user-invocable: true
effort: high
argument-hint: "[产品/功能想法]"
---

# Working Backwards Skill — 逆向工作法

> 灵感来源：亚马逊产品开发文化。

## 核心思想

**从客户出发，倒着工作回来**。先想象产品发布后客户看到什么、读到什么、怎么用，再决定要不要做、怎么做。

```
用户场景 → 新闻稿 → FAQ → 6-pager → MVP 范围 → PRD → 工程
   1         2        3      4         5         6     7
            ↑
       多数人从这里跳到工程
```

## 三大工件

### 1. 新闻稿（PR）— 1 页

模拟产品发布日的真实新闻稿。写不出动人新闻稿 = 客户价值不清晰 = 不该做。

**结构**：标题 / 副标题 / 摘要 / 客户问题 / 解决方案 / 高管引用 / 客户引用 / 调用动作。

参考模板：`templates/pr-faq-template.md`。

### 2. FAQ（含外部 + 内部）— 1-3 页

- **外部 FAQ**：客户会问的（"这和现有方案啥区别"、"我数据安全吗"、"我不喜欢能退吗"）
- **内部 FAQ**：老板 / 工程 / 销售 / 法务会问的（"客户付多少钱"、"工程多复杂"、"上线节奏"）

参考模板：`templates/pr-faq-template.md`。

### 3. 6-Pager — 6 页备忘录

战略决策评审用。完整段落叙述，**禁用 PPT 与子弹点**。会议形式：开会前 20 分钟集体静默读稿，再讨论。

**结构**：
1. 摘要 / Why now
2. 客户问题
3. 解决方案
4. 成功指标 + 砍项目硬条件
5. 风险（含 Pre-Mortem）
6. 投入与节奏

参考模板：`templates/six-pager-template.md`。

## 何时用 Working Backwards

| 场景 | 是否用 |
|------|--------|
| 新产品立项 | ✅ 必用 |
| 大功能 / 重大改版 | ✅ 必用 |
| 跨团队战略决策 | ✅ 必用 |
| 小功能优化 / Bug 修复 | ❌ 不用，直接 PRD |
| 已经 PMF 后的迭代 | ❌ 不用，直接故事图 / Spec |

## 与既有 PM 工具的关系

```
/pm-intake "想法"          ← 收集 + 缺口判断
   ↓
/working-backwards "想法"   ← 先写 PR-FAQ
   ↓
（PR-FAQ 评审过）
   ↓
/working-backwards --mode six-pager  ← 给老板看
   ↓
（6-pager 评审过 → 立项）
   ↓
/pm-prd-enterprise / /prd --mode standard   ← 进入 PRD
   ↓
@qa-acceptance-designer + /launch-checklist ← 发布
```

## 评审准则（PR-FAQ 评审会用这个清单）

- [ ] **客户语言**：新闻稿能让媒体读懂客户价值（无术语 / 无工程实现）
- [ ] **真差异化**：竞品看到也不慌张吗？是真差异还是包装差异？
- [ ] **客户引用是否真实**：能找到至少 1 个真实客户说同样的话吗？
- [ ] **FAQ 覆盖反对意见**：销售 / 客户 / 法务 / 投资人会问的都覆盖了吗？
- [ ] **假设清单完整**：每条假设有验证方式 + 截止日期吗？
- [ ] **不做范围明确**：写了"V1 不做什么"吗？
- [ ] **可砍指标**：定义了什么情况下应该砍掉这个项目吗？

## 反模式（不要做）

- ❌ **写 PR-FAQ 来包装已经决定要做的东西**：那是营销文案，不是 Working Backwards
- ❌ **PR-FAQ 写得像 PRD**：充满字段 / 流程 / 状态，已经偏离客户视角
- ❌ **跳过 FAQ**：FAQ 才是真实压力测试，新闻稿光鲜不算数
- ❌ **6-pager 用 PPT 做**：违反核心规则，绕过了"完整论证"的强制约束
- ❌ **不做评审就开始写 PRD**：等于浪费工程团队

## 输出格式

```
1. 生成 PR-FAQ（templates/pr-faq-template.md 结构）
2. 标注每条客户价值的"信心度"（高 / 中 / 低）
3. 列出关键假设清单（每条带验证方式）
4. 列出"不做范围"
5. 列出 PR-FAQ 评审建议参会人

进一步（用 --mode six-pager）：
6. 生成 6-pager（templates/six-pager-template.md 结构）
7. 含 Pre-Mortem（"12 个月后这个项目被关停，最可能的 3 个死因")
8. 含砍项目硬条件
```

## 配套资源

- 模板：`templates/pr-faq-template.md`、`templates/six-pager-template.md`
- 命令：`/working-backwards`
- 上游：`/pm-intake`、`/pm-discovery`
- 下游：`/pm-prd-enterprise`、`/prd --mode standard`、`@product-director`
