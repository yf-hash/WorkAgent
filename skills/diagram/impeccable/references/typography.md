# typography.md — Impeccable 排版参考

> 字号尺度 / 字体配对 / 层级 / optical sizing / vertical rhythm。**任何带文字的 UI 都该加载这份。**

---

## 1. 拒绝默认（最重要）

| 不要 | 为什么 | 替代 |
|------|--------|------|
| Inter | AI 默认字体第一名 | 见下方"字体光谱" |
| Roboto / Arial / system-ui | AI 默认字体第二批 | 同上 |
| DM Sans / Outfit / Plus Jakarta Sans | AI "我懂避坑了" 的二级 default | 跳出 sans-only 思维 |
| 单字体家族 | 视觉太单薄 | 2 家族（display + body） |
| 3+ 字体家族 | 视觉散架 | 收回到 2 |

---

## 2. 字体光谱（按 Register 选）

### Brand register（设计 IS 产品）

| 流派 | Display | Body | 适用 |
|------|---------|------|------|
| Editorial Magazine | 衬线（GT Sectra / Tiempos / PP Editorial Old / Source Serif） | 中性 sans（IBM Plex / Söhne / Geist） | 长文、品牌站、深度内容 |
| Tech-Minimal | 大写 grotesque（Helvetica Now / Untitled Sans / Söhne） | 同家族 weight 切换 | 开发者工具、infra |
| Luxury / Fashion | 高对比 modern serif（Didot / Bodoni / GT Super） | grotesque | 高端品牌、时尚 |
| Brutalist | mono / 工业感（Berkeley Mono / Pitch / JetBrains Mono） | 同 mono 或 system | 反主流、实验性 |
| Consumer-Warm | 圆润 humanist（Recoleta / Söhne Breit / GT America） | humanist sans | 消费 App、生活方式 |

### Product register（设计 SERVES 产品）

| 流派 | Display | Body | 适用 |
|------|---------|------|------|
| App UI | 同 body | Söhne / Inter Display（不是 Inter 本体）/ Geist | Linear / Notion 调性 |
| Dashboard | 同 body | 高 x-height sans（Söhne / IBM Plex Sans） | 数据密集 |
| Admin | 同 body | 中规中矩 sans（避免太有个性） | 工具型 |

> 用 Inter Display（display variant）≠ 用 Inter Regular，是合法的。但能避就避。

---

## 3. 字号尺度（Type Scale）

### 模块化尺度

```
ratio = 1.25（minor third，密集型）
ratio = 1.333（perfect fourth，平衡）
ratio = 1.5（perfect fifth，宽敞编辑式）
ratio = 1.618（golden，奢华／编辑）
```

### 推荐起点

| 用途 | base | ratio | 输出 |
|------|------|-------|------|
| Dashboard / App | 14px | 1.25 | 11.2 / 14 / 17.5 / 21.9 / 27.4 / 34.3 / 42.8 |
| Marketing 落地页 | 16px | 1.333 | 12 / 16 / 21.3 / 28.4 / 37.9 / 50.5 / 67.3 |
| Editorial 长文 | 18px | 1.5 | 12 / 18 / 27 / 40.5 / 60.8 / 91.1 |

### Fluid Typography（仅标题）

```css
/* ✅ 对：标题流体，正文固定 */
h1 { font-size: clamp(2.5rem, 5vw + 1rem, 5rem); }
h2 { font-size: clamp(1.875rem, 3vw + 1rem, 3.5rem); }
body { font-size: 1rem; }  /* 不要 clamp，否则正文在小屏变得不可读 */

/* ❌ 错：所有文字都 clamp */
body { font-size: clamp(0.875rem, 1.5vw + 0.5rem, 1.125rem); }
```

---

## 4. Vertical Rhythm（垂直节奏）

行高 = baseline grid 的倍数。如果 baseline grid 是 8px：

```css
:root {
  --baseline: 8px;
  --line-tight: calc(var(--baseline) * 2.5);   /* 20px - 用于标题 */
  --line-normal: calc(var(--baseline) * 3);    /* 24px - 用于 16px 正文 */
  --line-loose: calc(var(--baseline) * 3.5);   /* 28px - 用于长文阅读 */
}

body { font-size: 16px; line-height: 1.5; }  /* 24px = 3 × 8 ✅ */
h1 { font-size: 48px; line-height: 1.1; }    /* 52.8 ≈ 6.6 × 8 — 不对齐时优先 optical */
```

**关键判断**：垂直节奏对齐 < optical 美观。标题该 1.0–1.2 就该这么紧，不要为了对齐 grid 拉到 1.5。

---

## 5. 行宽（Measure / Line Length）

| 内容 | 行宽 | CSS |
|------|------|-----|
| 正文（阅读） | 65–75ch | `max-width: 65ch` |
| Caption / 辅助文字 | 45–55ch | `max-width: 50ch` |
| 标题 | 不限（视觉决定） | 不加 max-width |
| Form / 输入 | 32–48ch | 看密度 |

> `ch` 单位是当前字体下 "0" 的宽度，比 px 更鲁棒。

---

## 6. 字重 / 字号搭配

### 黄金组合

| 场景 | 字号 | 字重 | letter-spacing |
|------|------|------|---------------|
| H1 hero | 56–96px | 500–600（不是 700+） | -0.02em |
| H2 section | 32–48px | 500–600 | -0.015em |
| H3 subsection | 24–32px | 500–600 | -0.01em |
| Body | 16–18px | 400 | 0 |
| Caption | 13–14px | 400 | 0.01em |
| Button | 14–16px | 500 | 0.01em |
| Label / Uppercase | 11–12px | 500 | 0.08em |

### 陷阱

- **不要 800/900 weight 做大标题**：现代 display 字体的 500-600 已经够"重"，再加重就压垮 layout
- **不要正文用 weight 表达情感**：italic 才是声音
- **不要混 weight 表达层级**：用 size 区分层级，weight 在同一层级里做"次强调"

---

## 7. Optical Sizing（光学尺寸）

带 OpenType `opsz` axis 的字体可以根据使用尺寸自适应 stroke：

```css
h1 { font-size: 72px; font-variation-settings: "opsz" 72; }
body { font-size: 16px; font-variation-settings: "opsz" 16; }
```

支持 opsz 的字体：Source Serif 4、Newsreader、Roboto Flex、IBM Plex Serif Variable、Recursive、Söhne。**用上之后大标题不再"瘦死"，小字号不再"糊"。**

---

## 8. 数字 / 表格场景

- 表格里用 **tabular-nums**：`font-variant-numeric: tabular-nums;`
- 价格 / 财务用 **lining-nums**（默认）
- 长文里穿插数字用 **oldstyle-nums**（更优雅）
- 大段全数字（订单号 / hash）用 mono 字体（JetBrains Mono / Berkeley Mono / IBM Plex Mono）

---

## 9. 反模式速查

| 反模式 | 例子 | 修正 |
|--------|------|------|
| All-caps 长段落 | "OUR FEATURES INCLUDE…" | 句首大写 + weight |
| Letter-spacing 滥用 | 正文加 `letter-spacing: 0.05em` | 只在小字号 uppercase 用 |
| Italic 做正文强调 | "this is *important*" | 改成 weight 600 |
| Gradient text | `bg-clip-text` 配渐变 | 改用纯色 + size |
| 太多字号 | 8+ 层级 | 收回到 4–6 层 |
| 居中正文 | center-aligned 长正文 | 左对齐 |
| Justify 短行 | 短行 justify 出大窟窿 | 改 left align |
