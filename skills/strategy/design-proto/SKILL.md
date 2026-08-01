---
name: design-proto
description: >
  产品设计与原型知识库。触发词：原型设计、线框图、交互设计、组件库、设计系统、新手引导、
  Onboarding、Penpot、Figma 替代、Framer Motion、动效设计、UI 规范、用户旅程、
  可用性测试、空状态设计、表单设计、响应式设计、设计交付。
user-invocable: false
effort: medium
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Design Proto — 产品设计与原型知识库

## 原型保真度选择

```markdown
| 保真度 | 适用场景 | 工具 | 时间成本 |
|--------|---------|------|---------|
| 低（纸笔/ASCII） | 初期探索，快速发散 | 纸笔/FigJam | 分钟级 |
| 中（线框图） | 需求对齐，结构确认 | Penpot/Pencil | 小时级 |
| 高（可点击原型） | 用研测试，研发对接 | Penpot/Figma | 天级 |
| 真实交互（代码） | AB测试，验证细节 | Next.js + Framer Motion | 周级 |
```

## ASCII 线框图规范

```markdown
## 基础元素符号
┌─┐  └─┘  ├─┤  按钮外框
[按钮文字]  可点击按钮
{输入框}    文本输入
(单选)      Radio Button
[x] 复选框  Checkbox
▼ 下拉菜单
═══════     分割线
░░░░░       加载骨架屏
[图片区域]

## 常见布局模板

### 仪表盘布局
┌─────────────────────────────────────────┐
│  [Logo]  搜索框          [通知] [头像▼]  │
├────────┬────────────────────────────────┤
│        │  概览卡片区                     │
│  侧边  │  ┌──────┐ ┌──────┐ ┌──────┐  │
│  导航  │  │ 指标1 │ │ 指标2 │ │ 指标3 │  │
│        │  └──────┘ └──────┘ └──────┘  │
│  首页  │                                │
│  项目  │  ┌────────────┐  ┌──────────┐ │
│  分析  │  │   折线图    │  │  活动流  │ │
│  设置  │  └────────────┘  └──────────┘ │
└────────┴────────────────────────────────┘

### 表单布局
┌─────────────────────┐
│      标题            │
│  ────────────────   │
│  标签 *             │
│  {输入框           }│
│                     │
│  标签               │
│  {输入框           }│
│  ─ 提示文字          │
│                     │
│  [取消]   [确认提交] │
└─────────────────────┘
```

## Penpot 开源设计工具

```markdown
## Penpot vs Figma 对比
| 特性 | Penpot | Figma |
|------|--------|-------|
| 价格 | 免费/可自托管 | $12-45/人/月 |
| 数据所有权 | 完全自控 | SaaS，数据在 Figma |
| 格式 | SVG 原生 | 专有格式 |
| 协作 | ✅ 实时协作 | ✅ 实时协作 |
| 组件库 | ✅ | ✅ |
| 开发者工具 | ✅ CSS 直出 | ✅ |
| 插件生态 | 成长中 | 丰富 |
| 私有部署 | ✅ Docker | ❌ |

## 自托管部署
docker-compose up -d  # 官方 Docker 一键部署
默认端口：3449（前端），6060（后端），5432（PostgreSQL）
```

## Framer Motion 动效模式

```typescript
// 1. 基础入场动效（淡入 + 上移）
import { motion } from 'framer-motion'

const FadeInUp = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3, ease: 'easeOut' }}
  >
    {children}
  </motion.div>
)

// 2. 列表错落动效（Stagger）
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08 }
  }
}
const itemVariants = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0 }
}

// 3. 页面切换（路由动效）
const pageVariants = {
  initial: { opacity: 0, x: -20 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
}

// 4. 按钮反馈
<motion.button
  whileHover={{ scale: 1.03 }}
  whileTap={{ scale: 0.97 }}
>
  提交
</motion.button>

// 5. 骨架屏脉冲
<motion.div
  animate={{ opacity: [0.4, 0.8, 0.4] }}
  transition={{ duration: 1.5, repeat: Infinity }}
  className="h-4 bg-gray-200 rounded"
/>
```

## Onborda 新手引导配置

```tsx
// Next.js + Onborda 引导配置
import { Onborda, OnbordaProvider } from 'onborda'

const steps = [
  {
    icon: <>✨</>,
    title: "欢迎！先来了解一下",
    content: "这是您的工作台，30秒快速上手",
    selector: "#main-dashboard",
    side: "bottom",
    showControls: true,
    pointerPadding: 8,
  },
  {
    icon: <>📝</>,
    title: "创建第一个项目",
    content: "点击「新建」，填入您的产品描述",
    selector: "#new-project-btn",
    side: "right",
  },
  {
    icon: <>🎯</>,
    title: "查看分析数据",
    content: "这里汇总了所有关键指标",
    selector: "#analytics-panel",
    side: "left",
  }
]

// 触发条件：首次登录 + 未完成引导
const showOnboarding = isFirstVisit && !hasCompletedOnboarding

// 埋点
const handleStepChange = (step: number) => {
  posthog.capture('onboarding_step_viewed', { step })
}
const handleOnboardingComplete = () => {
  posthog.capture('onboarding_completed')
  setHasCompletedOnboarding(true)
}
```

## 新手引导设计原则

```markdown
1. 时机原则
   → 在用户需要时出现，不要开屏就弹
   → 首次接触某功能时触发
   → 永远提供"跳过"选项

2. 内容原则
   → 每步专注一个行动
   → 标题 ≤ 10 字
   → 描述 ≤ 25 字
   → 配动效（吸引注意力但不喧宾夺主）

3. 进度原则
   → 显示进度（Step 2/4）
   → 总步骤不超过 5 步
   → 记住用户中断位置

4. 衡量原则
   → 跟踪：开始率 / 完成率 / 每步跳过率
   → 目标：完成率 > 60%
   → A/B 测试不同文案和顺序
```

## 设计交付规范

```markdown
## 研发交付清单
- [ ] 所有状态覆盖（默认/悬停/聚焦/禁用/加载/错误/空状态）
- [ ] 移动端适配（断点：375/768/1280/1920）
- [ ] 暗色模式（如有）
- [ ] 动效标注（时长/缓动函数/触发条件）
- [ ] 间距规范（使用 4px 基础网格）
- [ ] 颜色 Token（使用语义化命名，非直接颜色值）
- [ ] 字体规范（size/weight/line-height）
- [ ] 交互说明（操作 → 反馈 → 下一状态）

## 空状态设计
每个列表/数据区域都需要：
1. 首次空状态（没有数据，引导创建）
2. 搜索无结果（提示修改搜索词）
3. 错误状态（加载失败，提供重试）
4. 权限限制（升级/申请权限）
```
