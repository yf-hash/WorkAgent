---
name: md-visual
description: >
  Markdown 转视觉图像命令，支持 Markdown 内容/表格/文章转为精美图片、海报、卡片，
  整合 mark-pic / Madopic / tablesnap / markdown-table-imagifier 四大工具
user-invocable: true
argument-hint: "<markdown内容或文件路径> [--tool mark-pic|madopic|tablesnap|imagifier|auto] [--format png|pdf|html] [--theme light|dark|gradient] [--type card|poster|table|article]"
---

# /md-visual — Markdown 转视觉图像

加载技能：`skills/md-visual/SKILL.md`

## 触发条件
需要将 Markdown 内容、表格、文章转为图片、海报、分享卡片时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<内容或路径>` | Markdown 文本或 .md 文件路径（必填） | — |
| `--tool` | 使用的工具 | `auto` |
| `--format` | 输出格式 | `png` |
| `--theme` | 主题风格 | `light` |
| `--type` | 内容类型 | `auto` |

### 工具选择（--tool）
| 值 | 工具 | 最适合 |
|----|------|--------|
| `mark-pic` | mark-pic | 代码卡片、技术分享图、知识卡片 |
| `madopic` | Madopic | 完整文章海报、含公式/图表的长图 |
| `tablesnap` | tablesnap | 表格快速截图（CLI，适合自动化）|
| `imagifier` | table-imagifier | 浏览器端表格转图（无需安装）|
| `auto` | 自动选择 | 根据内容类型智能路由 |

### 内容类型（--type）
| 值 | 说明 | 推荐工具 |
|----|------|---------|
| `card` | 知识卡片/代码卡片（≤300字） | mark-pic |
| `poster` | 完整文章海报/长图 | madopic |
| `table` | 表格截图 | tablesnap / imagifier |
| `article` | 文章转图（含图表/公式） | madopic |

### 主题（--theme）
| 值 | 说明 |
|----|------|
| `light` | 浅色主题 |
| `dark` | 深色主题 |
| `gradient` | 渐变背景（mark-pic 40+主题）|

---

## 执行流程

```
Step 1: 内容分析
  → 判断内容类型（表格/代码/文章/公式）
  → 根据 --type 和 --tool 选择最优工具
  → 检查工具是否已安装（CLI工具）

Step 2: 内容预处理
  → 优化 Markdown 格式（适配目标工具）
  → 处理特殊语法（KaTeX/Mermaid/ECharts）
  → 确认输出尺寸和比例

Step 3: 生成图像
  → 调用对应工具生成图像
  → 或输出工具使用说明（工具未安装时）

Step 4: 输出
  → 图像文件路径
  → 或工具调用命令（可直接复制执行）
```

---

## 与其他命令的协同

```
/md-visual → Markdown 转图像
  ├── /table    → 先生成 Markdown 表格，再转图
  ├── /diagram  → 先生成 Mermaid 图表，再转图
  └── @visual-suite → 完整视觉内容编排
```

---

## 使用示例

```bash
# 将 Markdown 文章转为分享海报
/md-visual article.md --tool madopic --type poster

# 生成技术分享卡片（渐变背景）
/md-visual "## 今日学到\n- 知识点A\n- 知识点B" --tool mark-pic --theme gradient

# 表格快速截图（CLI）
/md-visual table.md --tool tablesnap --theme dark

# 含数学公式的内容转图
/md-visual math-notes.md --tool madopic --type article

# 浏览器端表格转图（无需安装）
/md-visual "| A | B |\n|---|---|\n| 1 | 2 |" --tool imagifier --type table

# 代码卡片（深色主题）
/md-visual code-snippet.md --tool mark-pic --theme dark --type card
```
