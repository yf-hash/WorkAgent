# color.md — Impeccable 颜色参考

> OKLCH / Tinted Neutrals / 调色板策略 / 对比度。**颜色决策必须加载这份。**

---

## 1. 颜色定义：只用 OKLCH

```css
/* ❌ 不要 */
:root {
  --primary: #6366f1;
  --bg: #ffffff;
  --text: #1f2937;
}

/* ✅ 要 */
:root {
  --primary: oklch(0.55 0.2 285);      /* L Chroma Hue */
  --bg: oklch(0.97 0.005 85);           /* tinted neutral, 暖灰 */
  --text: oklch(0.2 0.01 285);          /* deep tint，不是纯黑 */
}
```

### 为什么 OKLCH？

| 优点 | 说明 |
|------|------|
| 感知均匀 | L=0.5 的红和 L=0.5 的蓝看起来一样亮（HSL 不是） |
| 容易调 | 改 L 就是变亮变暗，改 C 就是变饱和，改 H 就是换色相 |
| 容易做主题 | 通过共享 H、调 L 生成整套灰阶 |
| 浏览器支持 | Chrome 111+ / Safari 16.4+ / Firefox 113+，2024 起可放心用 |

### 实战速查

```
L (Lightness): 0 黑 → 1 白
  - 文本主色：0.15 - 0.25
  - 文本次色：0.45 - 0.55
  - 边框/分割线：0.85 - 0.92
  - 背景：0.95 - 0.99

C (Chroma): 0 灰 → 0.4 极饱和
  - 中性灰：0.005 - 0.02（带一点 tint）
  - 品牌色：0.15 - 0.25
  - 危险/警示：0.18 - 0.22

H (Hue): 0-360
  - 0 红 / 30 橙 / 90 黄 / 140 绿 / 200 青 / 260 蓝 / 320 紫红
```

---

## 2. Tinted Neutrals（带色相的灰）

**永远不用纯黑 `#000` 和纯白 `#fff`**。所有灰阶都带一点 hue。

### 构造方法

1. 选一个主品牌色相 H_brand（例如 280 紫）
2. 灰阶用 H_brand ± 20° 的 H（或者干脆和 brand 一致）
3. C 设到 0.005-0.02（几乎是中性灰，但有微妙暖意/冷意）

```css
:root {
  /* 暖灰系（H 约 60-90，更亲和） */
  --neutral-50: oklch(0.99 0.005 85);
  --neutral-100: oklch(0.97 0.005 85);
  --neutral-200: oklch(0.93 0.008 85);
  --neutral-300: oklch(0.85 0.01 85);
  --neutral-400: oklch(0.7 0.012 85);
  --neutral-500: oklch(0.55 0.014 85);
  --neutral-600: oklch(0.42 0.016 85);
  --neutral-700: oklch(0.32 0.018 85);
  --neutral-800: oklch(0.22 0.015 85);
  --neutral-900: oklch(0.15 0.01 85);
  --neutral-950: oklch(0.1 0.008 85);
}
```

### Warmth is load-bearing（暖意是承重的）

> "Without warmth, the site reads as generic and the decisive accent reads as abrasive rather than decisive."

把灰阶往暖里偏（H 60-90），整个站会立刻"有体温"。冷灰（H 240-280）适合 tech-tool 调性，暖灰适合编辑、品牌、消费类。

---

## 3. One Voice Rule（一个声音规则）

> **整套系统只能有一个 vibrant color。**

```css
:root {
  --accent: oklch(0.55 0.25 0);   /* Editorial Magenta，唯一 vibrant */
  
  /* ❌ 错：再加一个 secondary accent */
  --secondary: oklch(0.6 0.2 200);  /* NO */
  
  /* ✅ 对：要第二个强调点？用 scale 或 weight */
}
```

需要"第二个强调"时：
- 用 **更大的 size**（H1 vs H2）
- 用 **更重的 weight**（500 vs 400）
- 用 **更深的 neutral**（neutral-900 vs neutral-700）
- 用 **更多的留白**包围

绝不动 hue。

---

## 4. 调色板的"声音"

| 流派 | 主 vibrant | 灰阶倾向 | 背景 |
|------|-----------|---------|------|
| Editorial（杂志） | Magenta / Vermillion / Cobalt（饱和 1-2 个） | 暖灰 H~80 | Warm Ash Cream（oklch(0.95 0.012 85)） |
| Tech-Minimal | 单一中性强调（深 neutral 即可） | 中性偏冷 H~250 | 接近纯白但带一丝冷 |
| Luxury | 金 / 深绿 / 酒红 + 深色 | 深暖灰 + 中性 | 深背景 + 高对比 |
| Brutalist | 高饱和原色（纯红/纯黄/纯蓝） | 没有灰阶过渡，直接对撞 | 纯白 + 高对比黑 |
| Consumer-Warm | 桃 / 蜜 / 奶油 | 极暖 | 米色 / 奶油 |

---

## 5. 反模式（颜色禁区）

| ✗ 禁 | 为什么 | 改用 |
|------|--------|------|
| `from-purple-500 to-blue-500` | AI tell 第一名 | 单色 accent + tinted neutrals |
| `from-cyan-400 to-purple-400` 文字 | AI tell 文字版 | weight + size |
| 纯黑 `#000` / 纯白 `#fff` | AI 反射式默认 | tinted neutrals |
| 灰字配色背景（`text-gray-500` on `bg-purple-500`） | 对比度差 + AI dashboard 典型 | 提亮文本或换深背景 |
| 左/右边 >1px 彩色 stripe | AI dashboard #1 tell | 不要 stripe，或全 border 同 1px |
| Dark mode default | AI tool 美学 | 默认 light，dark 是可选 |
| Cream/Beige + 高饱和 vibrant | GPT 命中率 74% 的 tell | 警惕 |
| 4+ vibrant 同时出现 | 视觉散架 | One Voice |

---

## 6. 对比度（不可妥协）

```
WCAG AA:
  正文（< 18px）       ≥ 4.5:1
  大字号（≥ 18px / 14px bold） ≥ 3:1
  非文本（图标 / 边框） ≥ 3:1

WCAG AAA（推荐编辑型）:
  正文 ≥ 7:1
  大字号 ≥ 4.5:1
```

**OKLCH 对比度估算（粗算）**：两色 L 差 > 0.55 大致达 AA。精确测用 [APCA](https://www.myndex.com/APCA/) 或 `Contrast.app`。

---

## 7. 状态色（不是 vibrant）

```css
:root {
  --success: oklch(0.5 0.15 145);   /* 绿 */
  --warning: oklch(0.7 0.15 75);    /* 琥珀 */
  --danger: oklch(0.55 0.2 25);     /* 红 */
  --info: oklch(0.55 0.15 240);     /* 蓝 */
}
```

> 状态色是"功能性"颜色，独立于 One Voice。但 visual weight 要弱于品牌 accent，免得抢戏。

---

## 8. 调色板生成 SOP

```
1. 选 brand hue（One Voice）
2. brand 色 OKLCH 三档：L=0.45（深）/ L=0.55（中）/ L=0.75（浅）
3. neutrals：H 跟 brand ±20°，C=0.005-0.02，L 从 0.99 到 0.1 分 10-11 档
4. 决定背景（light = neutral-50 暖偏；dark = neutral-900）
5. 决定 text 主次（主 = neutral-900 on light；次 = neutral-600）
6. 状态色：基于 OKLCH 标准 H 选，C 略低于 brand
7. 对比度全 AA 自查
```

---

## 9. 暗色模式（如果一定要）

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: oklch(0.15 0.008 85);    /* 暖深 */
    --text: oklch(0.95 0.005 85);
    /* 关键：暗色不能直接反转 light，C 要降，L 要重新平衡 */
  }
}
```

**禁忌**：
- 暗色 + neon 高饱和 accent（典型 AI tool 美学，自动失败）
- 直接 `filter: invert()`（颜色逻辑全乱）
- 暗色文字依然 `text-gray-500`（暗背景上的灰字基本不可读）
