---
description: Working Backwards 逆向工作法 — 生成 PR-FAQ（默认）或 6-pager 备忘录（--mode six-pager），倒推客户价值与产品需求
argument-hint: "[产品/功能想法]"
---

# /working-backwards — Amazon 逆向工作法

请基于以下输入，使用 Working Backwards 方法倒推产品价值：

$ARGUMENTS

## 工作模式

| 标志 | 输出 |
|------|------|
| 默认 | PR-FAQ（新闻稿 + 外部 FAQ + 内部 FAQ）|
| `--mode six-pager` | 6 页备忘录（给老板做决策评审用）|
| `--mode both` | 先 PR-FAQ，评审通过后 6-pager |

## 输出要求

1. **客户语言为主**，避免技术术语
2. **结论先行**，客户价值前 30 秒能读懂
3. **每条假设带验证方式 + 截止日期**
4. **明确"V1 不做范围"**
5. **PR-FAQ 中的客户引用必须真实**（来自访谈），不能是 PM 想象

## 输出格式

### PR-FAQ 模式（默认）

按 `templates/pr-faq-template.md` 结构：

1. **新闻稿（1 页）**：标题 / 副标题 / 摘要 / 客户问题 / 解决方案 / 高管引用 / 客户引用 / 调用动作
2. **外部 FAQ（对客户）**：6+ 条
3. **内部 FAQ（对老板 / 工程 / 销售 / 法务）**：12+ 条
4. **关键假设清单**：含验证方式与截止
5. **不做范围**

### 6-Pager 模式

按 `templates/six-pager-template.md` 结构，**完整段落叙述，禁用子弹点 / PPT**：

1. 摘要 / Why now（½ 页）
2. 客户问题（1 页）
3. 解决方案 / 提议（1.5 页）
4. 成功指标 + 砍项目硬条件（½ 页）
5. 风险（含 Pre-Mortem）（1 页）
6. 投入与节奏（1 页）

## 路由建议

| 场景 | 推荐 |
|------|------|
| 新产品立项 / 大功能 / 跨团队战略 | ✅ 用本命令 |
| 已 PMF 后的小迭代 | ❌ 直接 `/product-spec` |
| 想法模糊 / 缺信息 | 先 `/pm-intake` 收集 |
| PR-FAQ 评审过 → 进入 PRD | `/pm-prd-enterprise`（B 端）/ `/product-spec --mode prd`（C 端）|

## 评审清单

PR-FAQ 输出后，团队做"读稿评审"：

- [ ] 客户语言（无术语）
- [ ] 真差异化（竞品看到也不慌）
- [ ] 客户引用真实
- [ ] FAQ 覆盖反对意见
- [ ] 假设清单完整
- [ ] 不做范围明确
- [ ] 可砍指标定义

**如果 PR-FAQ 评审不过**：回到 `/pm-discovery` 或 `@research-analyst` 继续验证，**不要写 PRD**。
