---
name: illustrate
description: 文章配图生成 — 为 Markdown 文章自动识别配图位置并生成图像。主管道：Claude ASCII草图 → HTML → Playwright截图（零成本）；备选：Mermaid/PlantUML/Markmap（精确图表）、AI插图（article-illustrator/document-illustrator）、Stable Diffusion（创意封面）
user-invocable: true
argument-hint: "[<article.md>] [--backend html|mermaid|plantuml|markmap|ai-illus|sd] [--style business-blue|tech|warm|minimal|pixel-art|ghibli] [--mode auto|staged|single] [--type flow|arch|compare|steps|chart|mindmap|image] [--desc <描述>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_close
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
    gates: [before-write, before-destructive]
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# /illustrate — 文章配图生成

加载技能：
- `skills/diagram/html-chart/SKILL.md`（主管道：ASCII → HTML → 截图）
- `skills/diagram/mermaid-chart/SKILL.md`（备选：精确图表）
- `skills/diagram/diagram-plantuml/SKILL.md` · `skills/diagram/diagram-markmap/SKILL.md`（扩展：UML 系列与思维导图）
- `skills/diagram/ai-illustrator/SKILL.md`（AI插图：article-illustrator/document-illustrator/thesis-figure）
- `skills/diagram/stable-diffusion/SKILL.md`（备选：创意图像，需本地 SD WebUI）
- `skills/diagram/mermaid-chart/SKILL.md`（备选：精确图表）
- `skills/diagram/stable-diffusion/SKILL.md`（备选：创意图像，需本地 SD WebUI）

---

## 核心理念

```
主管道（零成本）：Claude ASCII草图 → HTML/CSS → Playwright截图 → PNG
备选 Mermaid：    Mermaid代码 → 浏览器渲染 → Playwright截图 → PNG
备选 SD：         提示词 → Stable Diffusion API → PNG
```

**为什么优先 HTML 管道？**
- 零 API 成本，无需外部服务
- 输出 1600×900 PPT 标准尺寸，可直接复用
- ASCII 草图可快速预览和迭代
- 风格统一（4种商务风格）
- 生成时间：1-3 秒/张

---

## 快速示例

```
# 为整篇文章自动配图（全自动）
/illustrate article.md

# 阶段模式（每步确认）
/illustrate article.md --mode staged

# 单图：指定内容生成
/illustrate --mode single --desc "用户登录流程：输入账号→验证→跳转主页"

# 用 Mermaid 生成时序图
/illustrate --mode single --backend mermaid --type sequence --desc "微服务 API 调用链"

# 用 SD 生成封面图（需本地 SD WebUI）
/illustrate --mode single --backend sd --desc "AI多智能体协作的科技感封面图"

# 指定风格
/illustrate article.md --style tech

# 只生成 ASCII 草图预览，不截图
/illustrate article.md --dry-run
```

---

## 参数说明

### 位置参数

| 参数 | 说明 |
|------|------|
| `<article.md>` | 要配图的 Markdown 文章路径（文章模式必填） |

### 模式控制

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode auto` | 全自动，一键生成所有配图并插入文章 | ✅ 默认 |
| `--mode staged` | 阶段模式，每步暂停确认 | — |
| `--mode single` | 单图模式，只生成一张图（无需传文章路径） | — |
| `--dry-run` | 仅生成 ASCII 草图，不执行 HTML 转换和截图 | — |
| `--no-insert` | 生成图片但不自动插入文章 | — |
| `--overwrite` | 覆盖已存在的图片 | — |

### 后端选择

| 参数 | 说明 | 适用图表类型 |
|------|------|------------|
| `--backend html` | Claude ASCII → HTML → 截图 | 流程图/架构图/对比表/步骤图 |
| `--backend mermaid` | Mermaid代码 → 浏览器渲染 | 时序图/ER图/甘特图/类图 |
| `--backend sd` | Stable Diffusion（需本地 WebUI） | 创意封面/插图/照片感图像 |

**自动后端选择规则**（未指定 `--backend` 时）：
```
IF 图表类型 IN [flow, arch, compare, steps]  → html（默认）
IF 图表类型 IN [sequence, er, gantt, class]  → mermaid
IF 图表类型 IN [cover, illustration, photo]  → sd
IF 描述含 "封面/插图/创意/人物/场景"          → sd
IF 描述含 "流程/架构/对比/步骤/层级"          → html
IF 描述含 "时序/实体关系/甘特/类图"           → mermaid
```

### 风格控制（仅 html 后端）

| 参数 | 风格 | 适用场景 |
|------|------|---------|
| `--style business-blue` | 商务蓝白（默认） | 报告/演示/PPT，深蓝 #1E3A8A + 纯白 |
| `--style tech` | 科技深色 | AI/编程文章，靛紫 #6366F1 + 暗底 |
| `--style warm` | 温暖亲和 | 个人成长/情感文章，橙黄暖色调 |
| `--style minimal` | 极简线条 | 教程/文档，黑白灰 |

### 图表类型（单图模式必填，文章模式自动推断）

| `--type` 值 | 说明 | 后端 |
|------------|------|------|
| `flow` | 水平流程图（步骤→步骤） | html |
| `arch` | 垂直架构图（分层系统结构） | html |
| `compare` | 左右对比表 | html |
| `steps` | 垂直步骤图（含说明文字） | html |
| `sequence` | 时序图（参与者交互） | mermaid |
| `er` | 实体关系图 | mermaid |
| `gantt` | 甘特图/时间线 | mermaid |
| `class` | 类图/数据模型 | mermaid |
| `mindmap` | 思维导图 | mermaid |
| `cover` | 封面图/创意图像 | sd |
| `illustration` | 文章插图 | sd |

### 其他参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--desc <描述>` | 图表内容描述（单图模式必填） | — |
| `--output-dir <路径>` | 图片保存目录 | `./imgs` |
| `--size <宽x高>` | 输出尺寸（html/mermaid后端有效） | `1600x900` |
| `--steps <数量>` | SD 采样步数 | `30` |
| `--sd-style <风格>` | SD 艺术风格 | `digital-art` |

---

## 执行流程

### 文章模式（`--mode auto` / `--mode staged`）

```
Phase 1: 文章分析
  → 读取 Markdown 文章
  → 识别适合配图的段落：
    ✅ 流程描述（"开发流程包括..."）
    ✅ 架构说明（"系统分为三层..."）
    ✅ 对比分析（"方案A vs 方案B..."）
    ✅ 步骤教程（"第一步...第二步..."）
    ❌ 简单列表（已够直观）
    ❌ 代码块（不需要重复）
  → 输出：配图位置列表 + 推荐图表类型 + 推荐后端

[staged: 展示位置列表，询问确认]

Phase 2: 图表生成（按后端分支）
  → html 后端：生成 ASCII 草图
  → mermaid 后端：生成 Mermaid 代码
  → sd 后端：生成英文提示词

[staged: 展示草图/代码/提示词，询问确认，支持调整]

Phase 3: 渲染转换
  → html 后端：ASCII → HTML/CSS → 保存临时 .html
  → mermaid 后端：代码 → 写入 HTML（内嵌 Mermaid CDN）→ 保存临时 .html
  → sd 后端：调用 http://127.0.0.1:7860/sdapi/v1/txt2img

[staged: 展示 HTML 预览路径，询问确认]

Phase 4: 截图 / 保存
  → html/mermaid 后端：Playwright 截图（1600×900）
    mcp__playwright__browser_navigate → 等待渲染 → take_screenshot → close
  → sd 后端：base64 解码保存 PNG
  → 清理临时文件

Phase 5: 插入文章（--no-insert 时跳过）
  → 在对应段落后插入：![图表描述](imgs/article-N.png)
  → 输出完成摘要
```

### 单图模式（`--mode single`）

```
Step 1: 解析 --desc 和 --type（自动推断 --backend）
Step 2: 生成草图/代码/提示词（展示预览）
Step 3: 渲染转换
Step 4: 截图/保存 → 输出文件路径
```

---

## HTML 管道详细步骤

### Step A：生成 ASCII 草图
```
根据图表类型选择模板：
- flow  → 横向流程：[步骤1] → [步骤2] → [步骤3]
- arch  → 分层架构：┌层1┐ ↓ ┌层2┐ ↓ ┌层3┐
- compare → 双栏对比：[方案A] VS [方案B]
- steps → 纵向步骤：① 步骤 ↓ ② 步骤 ↓ ③ 步骤

保存草图：imgs/ascii/<article-name>-<N>.txt
```

### Step B：生成 HTML
```
1. 解析 ASCII 草图的结构数据
2. 选择对应的 HTML 模板（来自 skills/diagram/html-chart/SKILL.md）
3. 注入风格 CSS 变量（business-blue / tech / warm / minimal）
4. 填充内容数据
5. 保存到 workspace/.tmp/html/chart-<timestamp>.html
6. [可选] 备份到 imgs/sources/<name>.html
```

### Step C：Playwright 截图
```javascript
mcp__playwright__browser_navigate({
  url: "file:///workspace/.tmp/html/chart-TIMESTAMP.html"
})
// 等待 CSS/字体加载完成（约 500ms）
mcp__playwright__browser_take_screenshot({
  filename: "imgs/ARTICLE-N.png"
})
mcp__playwright__browser_close()
// 清理临时 HTML
```

---

## Mermaid 管道详细步骤

生成包含 Mermaid CDN 的独立 HTML，让 Playwright 渲染后截图：

```html
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<style>
  body { background: white; display: flex; justify-content: center; 
         align-items: center; width: 1600px; height: 900px; margin: 0; }
  .mermaid { width: 100%; }
</style>
</head>
<body>
<div class="mermaid">
[Mermaid 代码]
</div>
<script>mermaid.initialize({startOnLoad: true, theme: 'default'});</script>
</body>
</html>
```

支持的图表类型：`sequence` `er` `gantt` `class` `flowchart` `mindmap` `pie` `state`

---

## Stable Diffusion 管道详细步骤

```python
import requests, base64

payload = {
    "prompt": "[中文描述转英文], [--sd-style 对应关键词], masterpiece, best quality",
    "negative_prompt": "low quality, blurry, distorted, watermark, text, signature",
    "steps": 30,            # --steps 参数
    "cfg_scale": 7,
    "width": 1600,          # 文章封面宽
    "height": 900,          # 16:9
    "sampler_name": "DPM++ 2M Karras",
    "seed": -1
}

response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
image_data = base64.b64decode(response.json()['images'][0])

with open(f"imgs/{article_name}-{index}.png", "wb") as f:
    f.write(image_data)
```

### SD 风格关键词对照
| `--sd-style` | 英文提示词 | 适用场景 |
|-------------|-----------|---------|
| `digital-art` | digital art, vibrant colors | AI/科技封面 |
| `photorealistic` | photorealistic, 8k, sharp | 写实场景 |
| `oil-painting` | oil painting, impressionist | 艺术感封面 |
| `watercolor` | watercolor, soft edges | 清新风格 |
| `sketch` | pencil sketch, line art | 概念草图感 |
| `3d-render` | 3d render, octane render | 产品/建筑 |

---

## 输出格式

### 文章模式完成摘要
```markdown
## 配图生成完成

**文章**：`article.md`
**后端**：html（3张）/ mermaid（1张）
**风格**：business-blue
**生成数量**：4 张

**插入位置**：
- 图1：Phase 1 → "系统架构" 段落后 → `imgs/article-1.png`（arch，html）
- 图2：Phase 3 → "开发流程" 段落后 → `imgs/article-2.png`（flow，html）
- 图3：Phase 5 → "方案对比" 段落后 → `imgs/article-3.png`（compare，html）
- 图4：Phase 6 → "API交互" 段落后 → `imgs/article-4.png`（sequence，mermaid）

**文件保存**：
- 截图：`imgs/*.png`
- ASCII草图：`imgs/ascii/*.txt`
- HTML源码：`imgs/sources/*.html`（可随时调整样式后重新截图）
```

### 单图模式输出
```markdown
## 图表生成完成

**描述**：[用户输入]
**类型**：flow | arch | compare | steps | sequence | ...
**后端**：html | mermaid | sd
**风格**：business-blue

**文件**：`imgs/output-1.png`（1600×900）

**中间产物**：
- ASCII草图：`imgs/ascii/output-1.txt`
- HTML源码：`imgs/sources/output-1.html`

**复用提示**：
- 修改文字：编辑 `imgs/sources/output-1.html` 后重新截图
- 修改风格：改 `--style` 参数重新生成
```

---

## 最佳实践

**1. 默认先跑全自动**
```
/illustrate article.md
```
90% 情况直接可用。

**2. 重要文档用阶段模式**
```
/illustrate report.md --mode staged
```
可在每步确认 ASCII 草图布局和 HTML 效果。

**3. 保留 HTML 源码**
生成后的 `imgs/sources/*.html` 可在浏览器直接打开调整，比重新生成快。

**4. 风格一致性**
同一篇文章始终用同一个 `--style`，确保视觉统一。

**5. Mermaid 用于关系图**
时序图、ER图、甘特图用 `--backend mermaid` 表达更精确，HTML 管道难以表达图的拓扑关系。

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| Playwright 截图空白 | HTML 渲染未完成 | 增加等待时间；手动打开 HTML 检查 |
| ASCII 草图布局偏移 | 终端字体宽度不一致 | 使用阶段模式，选择"调整草图" |
| HTML 效果与草图不一致 | 结构解析偏差 | 查看 `imgs/sources/*.html` 手动修改 |
| SD 连接失败 | WebUI 未启动 | 启动 SD WebUI：`./webui.sh --api --listen` |
| Mermaid 渲染失败 | CDN 超时 | 将 Mermaid JS 下载到本地 |

---

## 依赖

- **Playwright MCP**（必需，html/mermaid 后端）：Claude Code 内置
- **Stable Diffusion WebUI**（可选，sd 后端）：`http://127.0.0.1:7860`
- **ImageMagick**（可选，图片压缩）：`brew install imagemagick`
