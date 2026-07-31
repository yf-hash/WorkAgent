# responsive.md — Impeccable 响应式参考

> Mobile-first / container queries / fluid typography / 断点策略。**任何多屏场景加载。**

---

## 1. Mobile-First（铁律）

```css
/* ❌ Desktop-first：要写一堆 max-width override */
.card { padding: 32px; }
@media (max-width: 768px) { .card { padding: 16px; } }

/* ✅ Mobile-first：从小屏开始向上加 */
.card { padding: 16px; }
@media (min-width: 768px) { .card { padding: 32px; } }
```

理由：
- 移动占 70%+ 流量，先写它的体验
- `max-width` 链容易冲突，`min-width` 是 monotonic 安全

---

## 2. 断点

### 推荐断点（按设备族群）

```css
:root {
  --bp-sm: 480px;    /* 大屏手机 */
  --bp-md: 768px;    /* 平板竖屏 */
  --bp-lg: 1024px;   /* 平板横屏 / 小笔记本 */
  --bp-xl: 1280px;   /* 桌面 */
  --bp-2xl: 1536px;  /* 大桌面 */
}
```

### 媒体查询风格

```css
/* ❌ 写死 px，重复 */
@media (min-width: 768px) { … }
@media (min-width: 768px) { … }

/* ✅ 用 CSS 自定义变量（PostCSS / Tailwind 配置好） */
@media (min-width: theme('screens.md')) { … }
```

### 断点不是设备清单

不要给每个 device 写一档。**只在 content 真的需要时加断点**。一个落地页 2-3 个断点足够；一个 dashboard 可能 4-5 个。

---

## 3. Container Queries（推荐）

`@media` 看的是 viewport，`@container` 看的是**组件自身的宽度**。组件库时代必备：

```css
.card-grid {
  container-type: inline-size;
  container-name: cards;
}

.card { grid-column: span 12; }

@container cards (min-width: 480px) {
  .card { grid-column: span 6; }
}
@container cards (min-width: 768px) {
  .card { grid-column: span 4; }
}
```

**好处**：同一个组件放进 sidebar 和放进 main，自动用不同布局。`media query` 做不到。

**支持度**：Chrome 105+ / Safari 16+ / Firefox 110+，2024 起可放心用。

---

## 4. Fluid Typography（标题用，正文不用）

```css
/* ✅ 标题：clamp(min, fluid, max) */
h1 { font-size: clamp(2.25rem, 5vw + 1rem, 4.5rem); }
h2 { font-size: clamp(1.75rem, 3vw + 1rem, 3rem); }

/* ✅ 正文：固定 rem，让用户浏览器设置生效 */
body { font-size: 1rem; line-height: 1.6; }
small { font-size: 0.875rem; }

/* ❌ 正文也 clamp：小屏变 14px 用户难读 */
body { font-size: clamp(0.875rem, 1vw, 1.125rem); }
```

### Fluid 公式速查

```
font-size: clamp(min, calc(min + (max - min) * (100vw - vp_min) / (vp_max - vp_min)), max);
```

简化为 `clamp(min_rem, calc_vw + rem, max_rem)`：

```css
/* 想 320px → 24px，1280px → 48px */
h1 { font-size: clamp(1.5rem, 1rem + 2.5vw, 3rem); }
```

---

## 5. 流体间距

间距也能 fluid：

```css
.section {
  padding-block: clamp(3rem, 6vw + 1rem, 8rem);
}
```

但不要所有 padding 都 fluid——会失去 8px grid 的节奏。**关键 hero / section 用 fluid，组件内部用固定 token**。

---

## 6. Layout 模式选择

| 屏幕 | Hero | Feature 卡片 | 表单 | 导航 |
|------|------|------------|------|------|
| Mobile | 单列，文字优先，CTA 全宽 | 单列堆叠 | 单列 label-above | Hamburger / Tab bar |
| Tablet | 单列或左文右图（垂直堆叠优先） | 2 列 | 单列，max-width 480 | 顶部 nav |
| Desktop | 左右 split 或大 hero 居中 | 3-4 列 | 1-2 列（视字段多） | 顶部 nav / sidebar |

---

## 7. Image / Media

### Responsive image

```html
<img
  src="hero-640.webp"
  srcset="hero-640.webp 640w, hero-1280.webp 1280w, hero-1920.webp 1920w"
  sizes="(min-width: 1024px) 1024px, 100vw"
  alt=""
  loading="lazy"
  decoding="async"
/>
```

### `aspect-ratio` 防 CLS

```css
.media { aspect-ratio: 16 / 9; object-fit: cover; }
```

永远给图片占位，不让加载时 layout 重排。

---

## 8. Touch targets vs Mouse targets

```css
.btn {
  min-height: 44px;       /* 触控基线 */
  min-width: 44px;
  padding: 10px 16px;
}

@media (pointer: fine) {
  /* 鼠标精度更高，可以更紧凑 */
  .btn { min-height: 36px; }
}
```

---

## 9. Safe Area（iOS notch / Android gesture bar）

```css
.bottom-bar {
  padding-bottom: max(16px, env(safe-area-inset-bottom));
}
.top-bar {
  padding-top: env(safe-area-inset-top);
}
```

落地页 hero 全屏时一定要加，否则文字会被 notch 遮。

---

## 10. 反模式速查

| 反模式 | 改 |
|--------|----|
| Desktop-first + 一堆 max-width | 改 mobile-first + min-width |
| 横向滚动条 | 永远禁，除非是 carousel |
| 正文用 vw | 改固定 rem |
| 所有间距用 vw | 仅 hero / section，组件内固定 |
| 移动端隐藏关键内容 | 移动端也要看 — 改 layout 不是删 |
| 移动端 hover 提示 | 改 inline 显示或 long-press popover |
| 表格不能横向滚（小屏） | 加 `overflow-x: auto` + 阴影提示 |
| 没给 image 设 aspect-ratio | 必加，防 CLS |
| Hamburger 装所有导航 | 移动端思考"哪 3 个最重要"，剩下进 hamburger |
| Fixed header 占 30%+ 屏高 | 收回 ≤ 56-64px |

---

## 11. 设计 SOP

```
1. 320px viewport 起步设计（不是 1440 起）
2. 单列布局，最简内容
3. 加大字号、间距，确认 mobile 体验
4. 向上加断点：768 → 1024 → 1280
5. 每个断点问：是 content 需要变？还是只是空间多了？
6. Container queries：组件能否自适应自己的容器？
7. 真实设备测试（Chrome DevTools 不够）
8. 慢网络测试（Slow 3G）
9. 键盘导航测试（移动用蓝牙键盘）
```
