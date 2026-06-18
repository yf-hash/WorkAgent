# motion.md — Impeccable 动效参考

> 100/300/500ms 规则 / easing 库 / purposeful vs decorative motion。**有任何 transition 加载这份。**

---

## 1. 时长黄金三档

| 时长 | 用途 | 例子 |
|------|------|------|
| **80–150ms** | 微反馈（用户感知"立刻"） | hover、focus、按下 |
| **200–350ms** | 状态转换（用户感知"有发生"） | drawer 进出、modal 出现、tab 切换 |
| **400–600ms** | 大变化 / 入场（用户感知"在发生"） | 页面入场、大区块切入、orchestrated 动画 |
| **> 600ms** | **基本都错** | 用户感知"卡顿"，除非有意做奢华品牌感 |

```css
:root {
  --t-fast: 120ms;
  --t-base: 240ms;
  --t-slow: 480ms;
}
```

---

## 2. Easing（缓动曲线）

### 用 ease-out 家族，不用 ease-in-out

```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);          /* expo-out，最通用 */
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);   /* quint-out，更紧 */
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);    /* quart-out，温和 */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);      /* 谨慎，仅循环动画 */
}
```

### 为什么 ease-out？

UI motion 的核心错觉：东西从快变慢"落"到位。`ease-in`（慢→快）适合"离开"，但 UI 多数是"出现"或"切换"，需要"快→慢"。

### 何时用 ease-in-out？

- 持续循环的动画（loading spinner）
- 数值滑块的连续过渡

### 永远不用

```
❌ ease-in（慢→快）单独用
❌ linear（除非有特殊原因）
❌ cubic-bezier 带 overshoot（bounce）
❌ spring 物理（除非真的在做"物理"，例如拖拽）
```

---

## 3. 反 Bounce / Elastic 规则

> "Bounce and elastic easing on interface elements feels dated and tacky."

```css
/* ❌ 禁 */
animation: bounce 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* ❌ 禁 */
transition: transform 300ms cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* ✅ 用 */
transition: transform 240ms cubic-bezier(0.16, 1, 0.3, 1);
```

bounce 的合理场景：游戏 UI、儿童 App、刻意 playful 品牌。其他全部禁。

---

## 4. 性能：只动 transform 和 opacity

```css
/* ❌ 触发 layout / paint：jank 元凶 */
.bad {
  transition: width 300ms, height 300ms, padding 300ms, margin 300ms;
}

/* ✅ 只触发 composite */
.good {
  transition: transform 300ms, opacity 300ms;
}
```

### 高度动画的合法做法

```css
/* 用 grid-template-rows: 0fr → 1fr */
.expandable {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms var(--ease-out);
}
.expandable.open { grid-template-rows: 1fr; }
.expandable > .inner { overflow: hidden; }
```

### 备选

```css
/* CSS @starting-style + interpolate-size（2024+） */
.expandable {
  height: 0;
  overflow: hidden;
  transition: height 300ms var(--ease-out);
  interpolate-size: allow-keywords;
}
.expandable.open { height: auto; }
```

---

## 5. Purposeful vs Decorative Motion

### Purposeful（必要）
- 反馈：点击后按钮缩 2%（确认收到）
- 引导注意力：错误时输入框抖动 1 次
- 解释空间关系：drawer 从右滑入 → 用户知道它来自哪
- 减负担：spring loading 让等待"流动"

### Decorative（多数应该删）
- 每个 card 入场时上滑 + fade
- 数字滚动到位（除非这本来是 hero metric）
- 鼠标 hover 时整个 card 上浮 + shadow + scale + border 变色（5 个变化一起来）
- 滚动到位时所有 section 都 stagger 进入

**判断标准**：去掉这个动画用户**任何感知**改变吗？没有 → 删。

---

## 6. Orchestration（编排）

入场多元素时不要全部同时进入：

```
Stagger pattern: 每个元素延迟 50-80ms
Sequential pattern: 一个完了再下一个（200ms 间隔）
Cascade pattern: 上→下 / 左→右 依次进入
```

```css
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 60ms; }
.item:nth-child(3) { animation-delay: 120ms; }
/* … */
```

**上限**：6 个元素以内 stagger 是优雅，10+ 就是"AI 默认全 fade-in"。

---

## 7. prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**永远加。**

---

## 8. 滚动驱动动画（Scroll-Driven Animations）

2024 起 Chrome / Safari 原生支持，不再需要 IntersectionObserver：

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fade-up 300ms var(--ease-out) both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
```

**但是**：节制使用。整页滚都在动 = 晕车感。

---

## 9. 反模式速查

| 反模式 | 改 |
|--------|----|
| Bounce / elastic easing | ease-out-quint |
| 动 width/height/margin | transform + opacity，或 grid-template-rows |
| 所有元素入场都 stagger | 选 2-3 关键元素 stagger，其他静态 |
| hover 时变 5 个属性 | 只变 1-2（推荐：color + transform） |
| 动画时长 800ms+ | 收回 200-400 |
| ease-in-out 给短交互 | 改 ease-out |
| 无 prefers-reduced-motion 兜底 | 必加 |
| 鼠标跟随效果 | 99% 场景是炫技，删 |
| Number ticker（数字滚动） | 仅给真正 hero metric，其他静态 |
| Page transitions 全屏 wipe | 除非是 portfolio，否则删 |

---

## 10. 快速决策树

```
要加动画吗？
  ├─ 用户操作的反馈？→ 80-150ms ease-out transform/opacity
  ├─ 状态变化？→ 200-350ms ease-out
  ├─ 入场？→ 400-600ms ease-out + 50ms stagger
  └─ 只是"看起来好看"？→ 删
```
