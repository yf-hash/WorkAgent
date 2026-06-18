---
name: impeccable
description: >
  Impeccable 设计语言知识库 — 让 AI 生成的 UI 不再像"AI 做的"。集成 Paul Bakaus 的 impeccable.style
  设计语言：7 个领域参考文件（typography / color / motion / spatial / interaction / responsive / ux-writing）
  + 27 条反 AI slop 反模式规则 + brand-vs-product 双轨寄存器。触发词：UI 设计、前端设计、网页设计、
  AI slop、设计语言、设计规范、OKLCH、tinted neutrals、8px baseline grid、fluid typography、
  vertical rhythm、impeccable、design vocabulary、frontend design、视觉规范、配色规范、字体规范、
  动效规范、间距规范、响应式规范、UX 文案、按钮设计、卡片设计、表单设计、登录页、落地页、
  仪表盘、editorial、tech-minimal、消除 AI 味、去 AI 感、不要紫色渐变、不要 Inter 字体、
  不要嵌套卡片、不要纯黑纯白。
user-invocable: false
effort: high
---

# Impeccable — 让你的 AI 写前端不再像 AI

> 改编自 Paul Bakaus 的 [impeccable.style](https://impeccable.style/) / [pbakaus/impeccable](https://github.com/pbakaus/impeccable)（MIT-ish）。
>
> 核心断言：**LLM 不是"设计能力差"，而是"设计词汇缺失"**。Claude / GPT / Gemini 都知道 OKLCH、tinted neutrals、8px baseline grid、vertical rhythm 是什么，但没人告诉它们要用，于是默认输出"AI slop"。Impeccable 在意图和执行之间塞进一层**词汇**：用专业术语向 AI 描述要做什么，再用**显式反模式**拒绝它"想"反射式给出的那些 SaaS 模板。

---

## 何时加载

被 `@impeccable-designer` agent 或 `/impeccable` 命令调用。在 WorkAgent 的 `design-proto` / `ui` / `landing page` / `dashboard` 等设计任务对话中可自动激活。

**不适用**：纯产品文档（用 design-proto）、纯营销文案（用 marketing-copy）、PPT 设计（用 ppt-master 自有风格）。Impeccable 的最佳战场是 HTML/CSS/Tailwind/React/Vue 等真正会渲染的前端代码。

---

## 工作流：意图 → 词汇 → 执行 → 反模式过滤

```
Brief（用户的模糊意图："给我做个 SaaS 落地页"）
   │
   ├─► 1. 锁定 Register（Brand vs Product，详见下方）
   │
   ├─► 2. 选择性加载 references/ 文件（不是全部！）
   │      不是所有任务都需要 7 个文件全部进上下文
   │      典型组合：
   │        - 落地页 → typography + color + spatial + motion + ux-writing
   │        - 仪表盘 → spatial + interaction + responsive + typography
   │        - 表单 → interaction + ux-writing + responsive
   │
   ├─► 3. 按固定顺序生成代码
   │      structure → spacing & hierarchy → type & color → states → motion → responsive
   │
   ├─► 4. 反 slop 过滤（27 条 deterministic 规则）
   │      在写完代码前自检：紫蓝渐变？嵌套卡片？Inter 字体？
   │
   └─► 5. 必要时切换到 /impeccable critique（LLM）或 /impeccable audit（确定性）二次验证
```

---

## Register 一：Brand vs Product（最关键的决策）

**先回答这个问题，不然下面所有规则都用错了**：

| Register | 含义 | 适用 | 评判标准 | 视觉光谱 |
|----------|------|------|---------|---------|
| **Brand** | 设计 **IS** 产品 | 营销页、品牌站、活动页、Portfolio、长文 | **Distinctiveness（独特性）** | 跨多个流派：tech-minimal / luxury / editorial / consumer-warm / brutalist… 不要默认一种 |
| **Product** | 设计 **SERVES** 产品 | SaaS App UI、Admin、Dashboard、工具 | **Earned familiarity（熟悉感）** | 熟用 Linear / Figma / Notion / Raycast / Stripe 的人应该一看就敢用 |

错位的代价：Brand 站做成 Product 长得像所有人 → 没人记住；Product 做成 Brand → 没人敢点。

---

## 27 条反 AI Slop 反模式（Deterministic Rules）

> 这些是"无脑也能打"的硬规则，不需要 LLM 判断，写代码前过一遍即可。Impeccable 的 CLI 工具就是用 grep 级别的检测器实现的。

### 字体 / 排版
1. **不用 Inter / Roboto / Arial / system-ui 作为唯一字体**。这是 AI 字体单调的元凶。
2. **不要"Inter 的替代款"**（DM Sans / Outfit / Plus Jakarta Sans）作为默认。这只是把同一个 monoculture 换了张皮。
3. **不要超过 3 种字体家族**。两种几乎总是更好。
4. **不要 all-caps 的 eyebrow 标签**（"OUR FEATURES" / "WHY US"），这是典型 AI 模板。
5. **不要给 section 加 numbered marker**（"01 / Overview" / "02 / Pricing"），AI 一写就这样。
6. **正文行宽 cap 在 65–75ch**（`max-width: 65ch`）。
7. **标题用 `clamp()` fluid sizing，正文用固定 `rem`**——别给正文也 clamp。
8. **正文强调用 weight，不用 italic**。Italic 是声音（display type 的语气），不是 emphasis。

### 颜色
9. **不要 `#000` 或 `#fff` 纯黑纯白**。永远使用 tinted neutrals（Deep Graphite / Warm Ash Cream / Crisp Paper White 之类暖灰）。
10. **不要紫→蓝渐变**（`from-purple-500 to-blue-500`）。AI tells 排行第一。
11. **不要 cyan-on-dark 主题**。AI tells 排行第二。
12. **不要 neon accents on dark background**（"Vercel-y" 看起来很酷但 100% AI 默认）。
13. **不要 cream/beige 背景的"温暖系"**（GPT 命中率 74%，已被 ban）。
14. **不要 `background-clip: text` 配渐变文字**。要强调用 weight 或 size。
15. **新颜色必须用 OKLCH 定义**，hex 只保留给历史 token。
16. **不要 dark mode default**。编辑式阅读 = light mode。Dark mode + 发光 accent = AI tool 美学。
17. **不要 colored stripe（左边/右边 >1px 的彩色边框）**——卡片、列表项、callout、alert 都禁。这是 AI 仪表盘最容易被一眼识别的 tell。
18. **One Voice Rule**：整套系统只能有一个 vibrant color。第二个 emphasis 用 scale 或 weight，不用第二个 hue。

### 间距 / 布局
19. **8px baseline grid**：所有 padding / margin / gap 是 8 的倍数（4 也能接受，3/5/7 不行）。
20. **不要给所有东西都套卡片**。"hero metric + supporting stats + gradient accent" 是 AI 仪表盘 tells。
21. **不要嵌套卡片**（卡里套卡，卡里套卡里套卡）。立刻让信息层级稀烂。
22. **不要 icon-tile + heading + text 的等大卡片网格**。AI 一写 features 就这样。
23. **Flat by default**：rest 状态不要 shadow，shadow 只用在 hover 或刻意的 elevation。

### 动效
24. **不要 bounce / elastic easing 在界面元素上**。spring physics 只给真正物理性的东西（拖拽、弹簧）。界面 motion 一律 ease-out-quart / quint / expo。
25. **不要动 width / height / padding / margin**（触发 layout thrash）。用 `transform` + `opacity`，或 `grid-template-rows` 做高度动画。
26. **所有动画必须 `prefers-reduced-motion` 友好**。

### 兜底
27. **永远尊重 contrast 底线**：正文 ≥ 4.5:1（WCAG AA），大字号 ≥ 3:1。不达就改色，不要"看起来还行就过"。

---

## 7 个领域参考文件（按需加载）

放在 `references/` 目录下，agent / command 根据 brief 选择性加载（**不要无脑全加载，token 不便宜**）：

| 文件 | 涵盖 | 何时加载 |
|------|------|---------|
| [typography.md](references/typography.md) | 字号尺度构造、字体配对、层级、optical sizing、vertical rhythm | 任何有文本的任务（几乎总要） |
| [color.md](references/color.md) | OKLCH 入门、tinted neutrals 构造、调色板策略、对比度 | 颜色决策、配色方案、品牌色定义 |
| [spatial.md](references/spatial.md) | 8px baseline grid、optical alignment、layout container、间距尺度 | 布局、栅格、卡片设计、组件间距 |
| [motion.md](references/motion.md) | 100/300/500ms 规则、easing 库、purposeful vs decorative motion | 微交互、过渡动画、入场退场 |
| [interaction.md](references/interaction.md) | 按钮 / 表单 / 输入 / 焦点状态 / 键盘 / 手势 | 交互组件、状态机、焦点设计 |
| [responsive.md](references/responsive.md) | 移动优先、container queries、fluid typography、断点策略 | 任何需要多屏适配的场景 |
| [ux-writing.md](references/ux-writing.md) | 微文案、空状态模板、错误消息公式、按钮文案 | 文案撰写、按钮命名、错误处理 |

---

## 12 条 LLM Critique Pass（需要模型判断）

deterministic 27 条之外，还有 12 条需要 LLM 主观评判：

1. **Hierarchy（层级）**：用户的眼睛是否被引导到最重要的内容？还是平铺直叙？
2. **Emotional Resonance（情感共鸣）**：这个界面有"声音"吗？还是任何人都能做？
3. **Information Density（信息密度）**：太空旷（像演讲稿）还是太挤（像 Excel）？
4. **Visual Hierarchy via Scale**：尺寸对比是否拉得够开？
5. **Optical Alignment**：mathematically 对齐 vs 视觉上对齐（icon 的视觉重心常常不在 bounding box 中心）。
6. **Whitespace as Composition**：留白是 active 设计决策，还是没填的边角料？
7. **Restraint（克制）**：每个元素都在喊。能不能让 80% 安静下来，让 20% 说话？
8. **Specificity（特异性）**：能从设计里认出"这是某个产品"吗？还是 5 家 SaaS 都能用？
9. **Genre Awareness（流派意识）**：编辑式杂志 vs Linear-style tool vs 高奢品牌 — 你选了哪个？显形了吗？
10. **Microcopy Voice**：按钮、错误、空状态的文案是不是同一个人写的？
11. **Real Content Stress Test**：用真实的长名字、长内容塞进去看会不会爆？
12. **Reading the Room**：B 端 dashboard 不要 emoji 满天飞；消费级 app 不要五体投地的"我们的使命是"。

---

## 命令矩阵（被 /impeccable command 路由）

| 子命令 | 一句话定位 | 触发时机 |
|--------|-----------|---------|
| `craft` | Shape → Build 完整闭环（带视觉迭代） | 从零做一个页面 |
| `teach` | 一次性 setup：交互式访谈 → 写 `PRODUCT.md` + `DESIGN.md` | 新项目首次配置 |
| `document` | 反向：从现有代码生成 `DESIGN.md` | 已有项目盘点设计系统 |
| `extract` | 把可复用组件 + token 抽到设计系统 | 项目散乱了想收敛 |
| `shape` | 写代码前先规划 UX/UI | 别人上来就写 JSX，你先 shape |
| `critique` | LLM UX review（层级 / 清晰度 / 情感） | 主观评判 |
| `audit` | 确定性技术检查（a11y / 性能 / 响应式 / 反模式） | 上线前体检 |
| `polish` | 收尾：设计系统对齐、ship-ready | merge 前最后一次过 |
| `bolder` | 太单调？放大对比、加粗、加密 | "这个看起来太平了" |
| `quieter` | 太喧闹？降强度（不是删元素） | "信息量太大眼花" |
| `distill` | 删元素到本质（注意：≠ quieter） | "这页啥都有就是说不清" |
| `harden` | error handling / i18n / 文本溢出 / 边界 | 上线前的工程性兜底 |
| `onboard` | 首次使用流 / 空状态 / 激活路径 | 新用户第一次进来怎么办 |

**`quieter` vs `distill` 的区别**（最容易混淆）：
- `quieter` 降"音量"：减少 saturation、减重、减大小，元素还在
- `distill` 删"内容"：去掉非本质元素，留下的更大声

---

## 实战示例：从 brief 到 code

### 用户输入
> "帮我做一个 B 端 AI 安全产品的 marketing landing page"

### Impeccable 推理链

```
Register: Brand（marketing 页 = 设计 IS 产品）
↓
加载 references: typography.md + color.md + spatial.md + motion.md + ux-writing.md
（不加载 interaction.md：因为没有复杂表单状态）
（不加载 responsive.md：单页布局，typography 里已含 fluid）
↓
生成顺序：
  1. structure：Hero → Problem → Solution → Social proof → CTA
  2. spacing：8px grid，section 间距 96/128px，element 间距 16/24/32
  3. type：Display = serif italic（带语气）；Body = 中性 sans，65ch
  4. color：Warm Ash Cream 背景，Editorial Magenta 单色强调（One Voice）
  5. states：hover 用色变 + transform，不用 shadow 强加
  6. motion：进入用 ease-out-quint 200-300ms，避免 bounce
↓
反 slop 自检：
  ✗ 紫蓝渐变？无
  ✗ Inter 字体？无（改用 serif + 非主流 sans）
  ✗ 嵌套卡片？无（落地页本就不该有）
  ✗ all-caps eyebrow？无
  ✗ icon-tile + heading 网格？无（feature 用排印对比，不用卡片）
↓
输出代码 + 一句话设计语言摘要给用户
```

### 反例（典型 AI 输出，被 Impeccable 拒绝）

```jsx
<section className="bg-gradient-to-br from-purple-500 to-blue-500">
  <p className="uppercase tracking-widest text-xs">OUR FEATURES</p>
  <h2 className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
    Powered by AI
  </h2>
  <div className="grid grid-cols-3 gap-4">
    {features.map(f => (
      <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-purple-500">
        <div className="bg-purple-100 rounded-xl w-12 h-12 flex items-center">
          <Icon />
        </div>
        <h3 className="font-bold">{f.title}</h3>
        <p className="text-gray-500">{f.desc}</p>
      </div>
    ))}
  </div>
</section>
```

被 Impeccable 命中的 slop tells（一段代码 8 个）：
- 紫蓝渐变背景（#10）
- all-caps eyebrow（#4）
- gradient-text（#14）
- 等大卡片网格（#22）
- 左边彩色 stripe border（#17）
- rounded-square icon tile（#22 衍生）
- 卡片的 shadow-lg at rest（#23）
- gray-500 灰字（#9 衍生）

---

## 与 WorkAgent 现有模块的协同

| 协同对象 | 关系 |
|---------|------|
| `design-proto` skill | design-proto 偏 ASCII 线框 / 流程，Impeccable 偏真实代码的视觉规范。可以串：design-proto 出框 → impeccable 出代码 |
| `marketing-copy` skill | marketing-copy 写文案，impeccable 写承载文案的页面。落地页场景两者必须搭配 |
| `article-illustrator` agent | 文章配图走 illustrator；页面配色 / 排版走 impeccable |
| `ppt-master` skill | PPT 有自己的 5 种 style，不走 Impeccable（PPT 是固定画布，不是 web） |
| `humanizer-scan` / `humanizer-soul` | humanizer 让文字像人，impeccable 让 UI 不像 AI，思路同源（反 AI 默认） |

---

## 已知限制（用户必须知道）

1. **Vocabulary 不是 taste**：知道 "tinted neutrals" 不等于知道何时用。最终的"哪个看起来好"还要人判断。
2. **Single-generation scope**：Impeccable 优化单次生成；多页一致性要靠 `/impeccable extract` 把规则沉淀成 `DESIGN.md`。
3. **Opinion codified**：很多规则（"不要 bounce"、"不要纯黑"）是 Paul Bakaus 的审美而非宇宙真理。如果你的品牌就是要 brutalist + bounce，请显式覆盖。
4. **Token 不便宜**：7 个 references 全加载约 8-15k tokens。所以**按需加载是默认**，不是优化。

---

## 来源 / 致谢

- 原作者：[Paul Bakaus](https://www.paulbakaus.com/)（jQuery UI 作者 / ex-Google AMP & Creators DevRel / Spotter Studio）
- 仓库：[pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- 站点：[impeccable.style](https://impeccable.style/)
- 我们的整合方式：把 Impeccable 的 7 个 reference + 27 条反模式翻译成 WorkAgent 的 skill + agent + command 三件套，命令前缀用 `/impeccable <sub>` 与原生兼容。
