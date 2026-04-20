# Marp — Markdown Presentation Ecosystem

## 概述
Marp 是最轻量的 Markdown → 幻灯片转换工具。写 Markdown，输出 HTML / PDF / PPTX。无需安装复杂依赖，VS Code 插件秒开预览，是"快速出片"的最优解。

## 核心能力
- **零学习成本** — 标准 Markdown 加几个特殊指令即可
- **三格式导出** — HTML（交互）、PDF（打印）、PPTX（可编辑）
- **主题系统** — default、gaia、uncover 三套内置主题
- **自定义 CSS** — 完全支持 CSS 覆盖样式
- **VS Code 插件** — 实时预览，所见即所得
- **CI 友好** — 命令行工具可集成到自动化流程

## 安装

```bash
# CLI 工具
npm install -g @marp-team/marp-cli

# 或使用 npx（无需安装）
npx @marp-team/marp-cli slides.md
```

VS Code 插件：搜索 `Marp for VS Code` 安装。

## Markdown 语法

### 基础结构
```markdown
---
marp: true
theme: default
paginate: true
---

# 演示标题

---

## 第一张幻灯片

- 要点一
- 要点二

---

## 包含图片

![bg right:40%](image.png)

正文内容在左侧，图片在右侧占 40% 宽度。
```

### 常用指令
```markdown
---
marp: true
theme: gaia           # 主题：default | gaia | uncover
size: 16:9            # 尺寸：16:9 | 4:3
paginate: true        # 显示页码
header: '标题'        # 页眉
footer: '公司名'      # 页脚
backgroundColor: #fff # 背景色
color: #333           # 字体颜色
---
```

### 背景图片语法
```markdown
<!-- 全屏背景 -->
![bg](background.jpg)

<!-- 右侧分栏 -->
![bg right](image.png)

<!-- 左侧分栏，自定义宽度 -->
![bg left:30%](logo.png)

<!-- 模糊背景 -->
![bg blur:5px](photo.jpg)
```

### 局部样式覆盖
```markdown
---

<!-- _class: lead -->
<!-- _backgroundColor: #1a1a2e -->
<!-- _color: white -->

# 深色封面幻灯片

副标题文字
```

### 自定义 CSS 主题
```css
/* custom-theme.css */
section {
  font-family: 'Noto Sans SC', sans-serif;
  background: #f8f9fa;
}

section.lead {
  background: linear-gradient(135deg, #1F4E79, #2E75B6);
  color: white;
}

h1 {
  font-size: 2.5rem;
  color: #1F4E79;
}
```

```markdown
---
marp: true
theme: custom
---
```

## 导出命令

```bash
# 导出 HTML
marp slides.md

# 导出 PDF（需要 Chrome/Chromium）
marp --pdf slides.md

# 导出 PPTX
marp --pptx slides.md

# 导出 HTML + PDF
marp --pdf --html slides.md

# 指定输出路径
marp slides.md --output output/deck.pdf

# 监听模式（自动重新生成）
marp --watch slides.md
```

## 使用场景

| 场景 | 推荐配置 |
|------|---------|
| 快速会议汇报 | `theme: default`, 导出 PDF |
| 技术文档演示 | `theme: gaia`, 导出 HTML |
| 分享给客户 | 导出 PPTX（可在 Office 中编辑） |
| 博客配套幻灯片 | 导出 HTML，嵌入网页 |

## 最佳实践

1. **已有 Markdown 文档** → 在开头加 `marp: true` 即可转为幻灯片
2. **快速原型** → 5 分钟完成一套幻灯片草稿
3. **团队协作** → Markdown 格式可直接 Git 管理，diff 清晰
4. **批量生成** → CI 中批量将 `.md` 转为 PDF 分发

## 输出格式

```markdown
## Marp 幻灯片输出

**源文件**：`slides.md`
**导出文件**：
- HTML：`slides.html`（在线分享或嵌入）
- PDF：`slides.pdf`（打印/归档）
- PPTX：`slides.pptx`（可用 Office 编辑）

**预览**：打开 `slides.html` 或使用 VS Code Marp 插件
```

## 相关资源
- 官网: https://marp.app/
- GitHub: https://github.com/marp-team/marp
- Marp CLI: https://github.com/marp-team/marp-cli
- VS Code 插件: https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode
- 主题文档: https://marpit.marp.app/theme-css
