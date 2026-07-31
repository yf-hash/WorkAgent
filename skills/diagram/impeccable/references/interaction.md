# interaction.md — Impeccable 交互参考

> 按钮 / 表单 / 输入 / 焦点 / 键盘 / 手势。**任何带交互的组件加载。**

---

## 1. 按钮（Button）

### 三档优先级

| 类型 | 用法 | 视觉 |
|------|------|------|
| **Primary** | 主路径 CTA，**整页 1-2 个** | 实色填充 + 高对比文字 |
| **Secondary** | 备选路径 | 描边 + 中性文字，或浅填充 |
| **Tertiary / Ghost** | 取消、辅助 | 纯文字 + 微 hover bg |

**铁律**：一个 viewport 内 Primary 不超过 2 个。10 个 button 都是 primary = 没有 primary。

### 尺寸

```css
:root {
  --btn-sm: { h: 32, px: 12, font: 13 };
  --btn-md: { h: 40, px: 16, font: 14 };
  --btn-lg: { h: 48, px: 24, font: 16 };
  --btn-xl: { h: 56, px: 32, font: 17 };   /* 仅 hero / landing */
}
```

> 触控目标 ≥ 44×44px。Form 里小按钮可破，但不要在移动端。

### 状态完整性

每个按钮必须有 5 个状态：

```
default → hover → active(pressed) → focus → disabled
```

```css
.btn {
  background: var(--accent);
  color: var(--accent-fg);
  transition: background 120ms var(--ease-out), transform 120ms var(--ease-out);
}
.btn:hover { background: oklch(from var(--accent) calc(l - 0.05) c h); }
.btn:active { transform: translateY(1px); }
.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

### 反模式

- ❌ Button 是 gradient
- ❌ Button 有 rotation hover
- ❌ Button 比文字大 3 倍 padding（看起来"按到外太空"）
- ❌ Primary 用浅色描边（无层级）
- ❌ 一个按钮里塞 icon + 长 label + arrow + badge（拆）

---

## 2. 表单（Form）

### 字段布局

```
Label (上方，weight 500)
↓ 4-8px
Input (h 40-48)
↓ 4px
Helper / Error (12-13px, muted / danger)
↓ 24px
下一个字段
```

**永远 label-above，不要 label-inside（floating label 在密集表单是反模式）**。

### Input 状态

```
default | hover | focus | filled | error | disabled | readonly
```

```css
.input {
  border: 1px solid var(--border);
  border-radius: 6px;     /* 4-6 是 sweet spot */
  padding: 10px 12px;
  background: var(--surface);
  transition: border-color 120ms var(--ease-out);
}
.input:hover { border-color: var(--border-hover); }
.input:focus-visible {
  border-color: var(--accent);
  outline: 3px solid color-mix(in oklch, var(--accent) 20%, transparent);
  outline-offset: 0;
}
.input[aria-invalid="true"] { border-color: var(--danger); }
```

### Error 显示

```
✗ 红字"必填"在字段下方（够了）
✗ 红 border + 红字（也行）
✗ 红 border + 红字 + 红 icon + 弹 toast + 红边阴影 + 抖动（过度）
```

错误文案公式见 `ux-writing.md`。

---

## 3. Focus 状态（无障碍核心）

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

**永远不要 `outline: none` 不带替代**。

### 焦点环颜色

主品牌色 + offset，**或**反色 box-shadow 双环（深色 + 浅色），保证在任意背景上可见。

---

## 4. Hover

### 桌面端 only

```css
@media (hover: hover) {
  .card:hover { background: var(--surface-hover); }
}
```

> 移动触屏的 hover 会"卡"在最后触摸的元素上，必须 media query 隔离。

### Hover 反模式

- 整 card 上浮 8px + scale 1.05 + shadow + border 变色（信息过载）
- Hover 改变内容（露出新文字 / 替换 icon）—— 移动端永远不会看到
- Hover 触发 modal / tooltip —— 同上

### Hover 推荐

```css
.card {
  transition: background-color 120ms var(--ease-out);
}
.card:hover {
  background-color: var(--surface-hover);   /* 仅 1 个变化 */
}
```

---

## 5. 键盘

### 必须支持

| 键 | 行为 |
|---|------|
| `Tab` | 焦点前进 |
| `Shift+Tab` | 焦点后退 |
| `Enter` | 触发 button / 提交 form |
| `Space` | 触发 button / 切换 checkbox |
| `Esc` | 关闭 modal / drawer / dropdown |
| `Arrow` | 在选项组 / radio / menu 内移动 |

### Tab 顺序

跟着**视觉阅读顺序**走（top-left → bottom-right）。如果 visual 顺序和 DOM 顺序不一致 → 改 DOM 顺序，不要用 `tabindex` 强改。

### 跳过链接

```html
<a href="#main" class="sr-only focus:not-sr-only">跳到主内容</a>
```

任何带顶导航的页面必加。

---

## 6. 触屏 / 手势

### 最小触控目标
- 标准 44×44px（iOS）/ 48×48dp（Android）
- 列表项 ≥ 48px 高
- 图标按钮 padding 充足，让点击区 ≥ 44²

### 手势规范

| 手势 | 推荐用途 | 慎用 |
|------|---------|------|
| Tap | 点击 | — |
| Long-press | 上下文菜单 | 不要承载主路径 |
| Swipe | 切换 carousel / 删除列表项 | 不要做"独家"操作（无 fallback） |
| Pull-to-refresh | iOS / Android 标准模式 | 不要发明新的"双指上拉"等 |
| Pinch / rotate | 图片 / 地图 | 其他场景禁 |

---

## 7. Modal / Dialog

```
触发：用户行为（不是定时器！）
打开：fade in + scale 0.95→1，250ms ease-out
关闭：fade out 200ms
背景：半透明遮罩（黑 50%）
焦点：进入后自动 focus 到第一个可交互元素
键盘：Esc 关闭，焦点 trap 在内部
ARIA：role="dialog" aria-modal="true" aria-labelledby
```

### 反模式

- 进站立刻弹 newsletter modal
- Modal 里嵌 modal
- Modal 关闭按钮藏在右上角且 < 32px
- 没有 outside-click 关闭（也没明显关闭按钮）

---

## 8. Tooltip / Popover

| 类型 | 触发 | 用途 |
|------|------|------|
| Tooltip | Hover / focus | 解释 icon 含义，**纯文字** |
| Popover | Click | 富内容，可包含 button |

**Tooltip 不能承载关键信息**（移动端不会触发）。

```css
.tooltip {
  background: var(--neutral-900);
  color: var(--neutral-50);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  /* 不需要 shadow / border / arrow（除非真有视觉脱节） */
}
```

---

## 9. Loading / Skeleton

| 等待时长 | 用什么 |
|---------|--------|
| < 300ms | 啥都不显示（避免闪烁） |
| 300ms - 1s | Skeleton 或微 spinner |
| 1s - 10s | Skeleton + 进度暗示 |
| > 10s | 显式进度条 + 取消按钮 |

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--neutral-200) 0%,
    var(--neutral-300) 50%,
    var(--neutral-200) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**反模式**：转圈 spinner 配大 logo，blocking 整个屏 5 秒（任何场景都错）。

---

## 10. 反模式速查

| 反模式 | 改 |
|--------|----|
| `outline: none` 无替代 | 加 `:focus-visible` outline |
| Hover 改 5 属性 | 改 1-2 |
| Tooltip 承载关键信息 | 改文案 inline 显示 |
| Modal 里塞表单滚动条 | 减字段或改全屏 |
| Floating label 在密集表单 | label-above |
| 移动端 hover 错觉 | media `(hover: hover)` 隔离 |
| Click 区域只有 icon | 扩展 click 区到 44² |
| 没有 keyboard navigation | 全键盘可达 |
| 没有 ARIA labels | 给 icon-only button 加 `aria-label` |
| 触屏 long-press 做主路径 | 加替代按钮 |
