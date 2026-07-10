---
name: product-writer-router
description: >
  产品资料写作路由 skill — 承载 12 类"轻量产品资料"（彩页 / 商务 PPT / 技术 PPT /
  功能清单 / 销售 FAQ / 竞品分析 / 投标参数 / 用户手册 / 部署 / 兼容性 / 发布说明 / 培训）的
  **共享写作规范** + **模板路由表**。收到 `/product-*` 命令时，本 skill 决定加载哪一份
  `templates/product/*.md` 结构模板，然后按共享规范执行。触发词：产品彩页、销售 FAQ、
  投标参数、用户手册、部署说明、兼容性说明、发布说明、培训材料、产品介绍 PPT、竞品分析、
  功能清单、product-writer。
user-invocable: false
effort: low
---

# 产品资料写作路由

> **单一职责**：为 12 类轻量产品资料承载**共享写作规范** + **模板路由**。
> 4 类"重内容"资料（whitepaper / tech-whitepaper / solution / case）保留各自专职 skill，本 skill 不覆盖。

---

## 一、路由表（收到 `/product-*` 命令时用）

| 命令 | 加载模板 | 一句话定位 |
|------|---------|-----------|
| `/product-brochure` | [templates/product/brochure.md](../../templates/product/brochure.md) | A4 双面 / 三折页展会物料 |
| `/product-intro-business` | [templates/product/intro-business.md](../../templates/product/intro-business.md) | 15-25 页商务路演 PPT |
| `/product-intro-tech` | [templates/product/intro-tech.md](../../templates/product/intro-tech.md) | 20-40 页技术演讲 PPT |
| `/product-function-list` | [templates/product/function-list.md](../../templates/product/function-list.md) | 带优先级 / 密级的功能全景表 |
| `/product-sales-faq` | [templates/product/sales-faq.md](../../templates/product/sales-faq.md) | 30-60 条按客户类型分组的问答 |
| `/product-competitive` | [templates/product/competitive.md](../../templates/product/competitive.md) | 3-5 家竞品对照表 |
| `/product-bid-params` | [templates/product/bid-params.md](../../templates/product/bid-params.md) | 逐条投标参数应答（含偏离） |
| `/product-manual` | [templates/product/manual.md](../../templates/product/manual.md) | 最终用户操作手册 |
| `/product-deploy` | [templates/product/deploy.md](../../templates/product/deploy.md) | 运维部署配置指南 |
| `/product-compat` | [templates/product/compat.md](../../templates/product/compat.md) | 兼容矩阵（OS / DB / 浏览器 / 硬件） |
| `/product-release-note` | [templates/product/release-note.md](../../templates/product/release-note.md) | 版本 changelog |
| `/product-training` | [templates/product/training.md](../../templates/product/training.md) | 销售 / 交付 / 运维培训体系 |

> 4 类**保留独立 skill** 的 rich 类型（本 skill 不介入）：
> - `/product-whitepaper` → `skills/product-whitepaper-writer/`
> - `/product-tech-whitepaper` → `skills/product-tech-whitepaper-writer/`
> - `/product-solution` → `skills/product-solution-writer/`
> - `/product-case` → `skills/product-case-writer/`

---

## 二、共享写作规范（所有 12 类都要遵守）

### 客户视角（第一原则）

- **写给谁 → 写他关心的什么 → 用他能懂的说法**。
- 商务受众关心 ROI / 案例 / 采购流程；技术受众关心架构 / 兼容性 / 部署；操作用户关心界面 / 步骤 / 报错。
- 每一段问一次：**这段话读者看完之后会做什么决策 / 采取什么行动？** 说不清就删。
- **禁**："业界领先 / 行业翘楚 / 卓越性能 / 一站式解决方案" 这类无信息量套话。

### 数据胜过形容词

- 用**数字 + 度量单位 + 场景**，而非形容词。
  - ✗ "高性能防护"
  - ✓ "在 5000 qps 混合流量下，误报率 <0.1%，测试环境：Intel Xeon 8360Y + 32C64G"
- 每一份产品资料至少含 **3 个可核实的数字**（性能 / 案例数 / 认证数 / 部署规模）。数字必须能追溯到源头（测试报告 / 客户合同 / 官方认证）。

### 边界声明（B 端的诚实是竞争力）

- **不能做什么** 和 **能做什么** 一样重要。
- 每份材料显式声明：适用场景、不适用场景、依赖的前置条件、当前版本的已知限制。
- 未发布功能不写进公开材料。技术核心算法 / 内部数据结构不写进对外资料。

### 密级与命名（B 端交付纪律）

- 每份资料明确密级：**可公开 / 客户限阅 / 内部 / 机密**。密级决定分发范围。
- 命名规范：`[产品名]_[资料类型]_v[版本].pdf`，例：`零信任访问控制_销售FAQ_v2.1.pdf`。
- 版本变化按 semver：功能新增 → minor，仅文字勘误 → patch。

### 交付前的四步自检

1. **信息核对**：所有数字 / 客户 logo / 认证 logo 是否已授权？未授权的移除。
2. **术语一致**：全文对同一概念是否使用一致术语？（例："RBAC 权限"和"角色权限"不要混用）
3. **视觉密度**：一屏 / 一页信息量是否过载？B 端读者会漏掉密度过高的段落。
4. **闭环检查**：读完能不能触发下一步动作？（点开链接 / 联系销售 / 转发内部）动作路径不清 = 材料没用。

> 完整 doc-auditor 14 项自查见 `skills/doc-auditor/SKILL.md`，命令执行时自动调用。

---

## 三、写作流程

```
Step 1: 意图确认
  → 用户是什么产品？受众是谁？密级是什么？
  → 命中路由表中的哪个模板？
  → 缺信息时用 AskUserQuestion 补齐

Step 2: 结构模板加载
  → Read templates/product/<type>.md，按其结构组织内容

Step 3: 内容填充（应用本 skill 的四原则）
  → 客户视角 → 数据支撑 → 边界声明 → 密级命名

Step 4: 自检（doc-auditor）
  → 命令层会自动串接 doc-auditor，本 skill 不重复实现

Step 5: 输出
  → 产物 + 密级标注 + 建议衔接的下一份材料
```

---

## 四、与 4 个 rich 独立 skill 的边界

| 场景 | 用本 skill (router) | 用独立 skill |
|------|-------------------|-------------|
| 篇幅 ≤ 10 页 / 单一模板结构 | ✅ | — |
| 篇幅 20+ 页 / 多章节复合 | — | ✅ `product-whitepaper-writer` |
| 技术架构侧重、含深度架构图 | — | ✅ `product-tech-whitepaper-writer` |
| 面向具体客户场景的完整方案 | — | ✅ `product-solution-writer` |
| 客户故事叙事结构（挑战 → 方案 → 结果） | — | ✅ `product-case-writer` |

发现走错入口 → 转介绍到对应 skill，不要在本 skill 内硬扩。
