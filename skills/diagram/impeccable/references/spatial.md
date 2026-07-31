# spatial.md — Impeccable 空间设计参考

> 8px baseline grid / optical alignment / layout container / 间距尺度。**任何排版必加载。**

---

## 1. 8px Baseline Grid（铁律）

所有 padding / margin / gap 是 8 的倍数。4 可接受（细粒度调整）。3 / 5 / 7 / 13 / 17 绝对禁用。

```css
:root {
  --space-0: 0;
  --space-1: 4px;     /* 半 grid，谨慎用 */
  --space-2: 8px;     /* 1 grid */
  --space-3: 12px;    /* 1.5 grid，谨慎 */
  --space-4: 16px;    /* 2 grid */
  --space-5: 24px;    /* 3 grid */
  --space-6: 32px;    /* 4 grid */
  --space-7: 48px;    /* 6 grid */
  --space-8: 64px;    /* 8 grid */
  --space-9: 96px;    /* 12 grid */
  --space-10: 128px;  /* 16 grid */
  --space-11: 160px;
  --space-12: 192px;
}
```

> 不是绝对禁用 4/12，是"用之前问自己一遍：能不能 8/16 解决"。

---

## 2. 间距尺度的"语义"

| 用途 | 推荐 | 不推荐 |
|------|------|--------|
| Icon 和文字间距 | 8 / 12 | 6 / 7 / 9 |
| Button 内边距（h/v） | 12/24 或 16/32 | 13/26 这种"差不多" |
| Form field 间距 | 16 / 24 | 18 / 20 |
| Card 内边距 | 24 / 32 | 28 / 30 |
| Section 之间（landing） | 96 / 128 / 160 | 100 / 120（不是 8 倍） |
| Hero section 高度 | viewport 计算 + 96 padding | 写死 800px |

---

## 3. 容器宽度（Container）

```css
:root {
  --container-xs: 480px;    /* 表单、登录 */
  --container-sm: 640px;    /* 阅读型长文（66ch ≈ 640px @16px） */
  --container-md: 768px;    /* 中等阅读 */
  --container-lg: 1024px;   /* App 内容主区 */
  --container-xl: 1280px;   /* 落地页 hero */
  --container-2xl: 1536px;  /* 宽屏 dashboard */
  --container-full: 100%;
}

.container {
  margin-inline: auto;
  padding-inline: var(--space-5);  /* 24px 移动 */
}
@media (min-width: 768px) {
  .container { padding-inline: var(--space-7); }  /* 48px 桌面 */
}
```

---

## 4. Layout Grid（栅格）

### 12-column（最稳）

```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-5);
}
```

### Container Queries（推荐）

```css
.card-list { container-type: inline-size; }

.card {
  grid-column: span 12;  /* 默认占满 */
}
@container (min-width: 480px) {
  .card { grid-column: span 6; }
}
@container (min-width: 768px) {
  .card { grid-column: span 4; }
}
```

> 比 media query 更智能：组件根据**自己的容器**响应，而不是窗口。

---

## 5. Optical Alignment（视觉对齐 > 数学对齐）

数学居中 ≠ 视觉居中。三个最常见场景：

### 圆形 icon 在 box 里
```css
/* ❌ 数学居中（看起来偏左） */
.icon-container { display: grid; place-items: center; }

/* ✅ 偏向"视觉重心" */
.icon-container { padding-left: 1px; }  /* 微调，1-2px 即可 */
```

### Play icon（三角）
三角形的视觉重心在 1/3 处，不在几何中心。绝对居中会"看起来偏左"。需要往右挪 2-3px。

### 大数字 vs 小标签
```
1,234   ← 数字
USERS   ← 标签

数字 baseline 和标签 baseline 数学对齐时，大数字看起来"飘"
解决：标签往下挪 1-2px，或用 align-items: baseline 让它"看起来稳"
```

---

## 6. Visual Density（信息密度）

| 场景 | row height | 字号 | gap |
|------|-----------|------|-----|
| Dashboard 表格 | 40-48px | 13-14px | 8-12 |
| 设置项列表 | 56-64px | 14-16px | 12-16 |
| 文章列表（编辑式） | 80-120px | 16-18px | 24-32 |
| Hero card grid | 200+px | 由内容定 | 32-48 |

**判断标准**：用户的扫描行为决定。
- 表格 → 扫描型，高密度，行间小
- 阅读型 → 沉浸型，低密度，行间大
- 决策型（pricing） → 中密度，要呼吸

---

## 7. 留白即组合

> Whitespace is composition, not leftover.

留白不是"没填的"，是 active 设计决策。两个用法：

### Macro whitespace（大留白）
section 之间、page 边缘 → 表达 hierarchy 和呼吸节奏

### Micro whitespace（小留白）
字间距、行间距、padding → 表达**可读性和触感**

**反模式**：
- 所有 section 间距一样（节奏死板）
- card 之间挤到一起（消除了 card 边界感）
- 移动端 padding-inline 16px 太挤（推荐 20-24）

---

## 8. 反模式速查

| 反模式 | 修正 |
|--------|------|
| 嵌套卡片（card 套 card 套 card） | 拆扁，用 divider 替代 |
| Hero 是巨大 metric + 旁边 icon + 渐变 | 去掉 icon 和渐变，metric 独立 |
| 等大卡片 + icon-tile + heading + text 网格 | 改成排印对比（不同 size）的列表 |
| Section 之间 padding 用 100/120/140 | 改 96/128/160（8 倍数） |
| Card 边缘紧贴容器 | 容器加 padding-inline，card 留呼吸 |
| 移动端横向滑动条 | 永远禁，除非是 carousel |
| Fixed height 内容溢出 | 用 min-height + 弹性 |

---

## 9. SOP：从空白页到布局

```
1. 确定 container width（mobile 100% with padding，desktop 1024-1280）
2. 决定栅格（12 col 通用）
3. 确定 section 间距尺度（编辑型用 128/160，dashboard 用 32/48）
4. 决定元素间距尺度（小元素 8/12，组件 16/24，section 32-48）
5. 写 layout：先 structure，再 spacing
6. 反 slop 自检：
   - 卡片有几层嵌套？> 1 层就警惕
   - icon-tile 网格？换排印
   - 等大卡片？尺寸有对比吗
7. 用真实长内容（长 30 字的标题）压力测试
```
