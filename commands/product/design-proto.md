---
name: design-proto
description: >
  设计原型与线框图 — UI / UX 设计与交互原型工具台。覆盖 ASCII 线框图、
  交互原型流程、组件库选型、新手引导（Onboarding）方案、动效设计、
  Penpot / Figma / Pencil 工具评估。
  适用于：早期需求快速沟通、研发对接前的设计、Onboarding 优化、动效规划。
user-invocable: true
argument-hint: "<设计需求> [--mode wireframe|prototype|component|onboarding|motion] [--tool penpot|figma|pencil]"
---

# /design-proto — 设计与原型工具台

加载技能：`skills/strategy/design-proto/SKILL.md`

## 触发条件
需要设计产品原型、选择 UI 组件库、设计用户引导流程、添加动效，或评估设计工具选型时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<设计需求>` | 需要设计的功能或场景（必填） | — |
| `--mode` | 设计模式 | `wireframe` |
| `--tool` | 目标工具 | `penpot` |

### 设计模式
| `--mode` | 输出内容 | 适用场景 |
|----------|---------|---------|
| `wireframe` | 线框图（ASCII 草图 + 布局说明） | 快速沟通需求 |
| `prototype` | 交互原型流程（页面流 + 交互说明） | 研发对接 |
| `component` | 组件库建议（设计规范 + 代码对照） | 设计系统建设 |
| `onboarding` | 新手引导方案（步骤 + 触发时机 + 文案） | 提升激活率 |
| `motion` | 动效方案（Framer Motion 代码示例） | 提升产品质感 |

## 参考工具生态

| 工具 | 特点 | GitHub |
|------|------|--------|
| Penpot | 开源 Figma 替代，SVG原生，可自托管 | penpot/penpot |
| Pencil | 桌面端线框图工具，轻量快速 | evolus/pencil |
| UIBakery | 低代码 UI 构建器 | uibakery/uibakery |
| Framer Motion | React 动效库（生产级） | framer/motion |
| Onborda | Next.js 新手引导组件库 | uixmat/onborda |

## 执行流程（onboarding 模式）

```
Step 1: 激活问题诊断
  → 当前激活率是多少？
  → 用户在哪一步流失最多？
  → 「aha moment」是什么？

Step 2: 引导策略设计
  → 触发时机（首次登录 / 功能点击 / 空状态）
  → 引导形式（Tooltip / Modal / Checklist / Video）
  → 跳过 & 记忆逻辑

Step 3: 步骤内容设计
  → 每步标题（≤10字）+ 描述（≤30字）
  → CTA 按钮文案
  → 高亮目标元素

Step 4: 代码实现建议
  → Onborda（Next.js）配置示例
  → 埋点：started / step_completed / skipped / finished

Step 5: 效果衡量
  → 引导完成率（目标 >60%）
  → 激活率对比（A/B 测试）
```

## 输出示例（onboarding 模式）

```tsx
// Onborda 新手引导配置示例
const steps = [
  {
    icon: <>👋</>,
    title: "欢迎使用",
    content: "这是您的工作台，让我们快速上手！",
    selector: "#dashboard-main",
    side: "bottom",
    pointerPadding: 10,
  },
  {
    icon: <>✨</>,
    title: "创建第一个 PRD",
    content: "点击「新建」开始您的第一份产品需求文档",
    selector: "#create-button",
    side: "right",
  },
  // ...
]
```

## 输出示例（wireframe 模式）

```
┌─────────────────────────────────────┐
│  [Logo]        导航栏      [头像]    │
├─────────────────────────────────────┤
│  侧边栏    │  内容区域               │
│  > 首页    │  ┌───────────────────┐ │
│  > 项目    │  │  卡片标题          │ │
│  > 设置    │  │  描述文字...       │ │
│           │  │  [操作按钮]        │ │
│           │  └───────────────────┘ │
└─────────────────────────────────────┘
```

## 使用示例

```
/design-proto 设计 SaaS 产品仪表盘页面 --mode wireframe
/design-proto 用户注册到激活的完整交互流程 --mode prototype
/design-proto 设计一套 B2B 产品组件规范 --mode component
/design-proto 提升新用户激活率的引导方案 --mode onboarding
/design-proto 为按钮添加点击动效 --mode motion
/design-proto 评估是否用 Penpot 替代 Figma --tool penpot
```
