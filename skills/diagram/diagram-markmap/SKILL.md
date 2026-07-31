---
name: diagram-markmap
description: >
  Markmap 思维导图引擎技能。Markdown 直接转思维导图（SVG/HTML/PNG），层级清晰。
  适合文章/报告大纲可视化、知识体系梳理、会议记录结构化、产品功能树。
  触发词：思维导图、mindmap、Markmap、知识树、大纲可视化、产品功能树
user-invocable: false
effort: low
---

# Diagram Markmap — 思维导图

> 单一职责：用 Markmap 把 Markdown 转思维导图。
> 不做：UML（→ `diagram-plantuml`）、流程图/时序图（→ `mermaid-chart`）、云架构图（→ `arch-diagram`）

## 适用场景

- 文章/报告大纲可视化
- 知识体系梳理
- 会议记录结构化
- 产品功能树

## 语法规范

```markdown
# 根节点（中心主题）

## 一级分支
### 二级分支
- 叶节点
  - 子叶节点

## 另一个一级分支
### 子分支
- 内容 A
- 内容 B
```

## 高级配置

```markdown
---
markmap:
  colorFreezeLevel: 2    # 冻结颜色层级
  maxWidth: 300          # 节点最大宽度
  initialExpandLevel: 2  # 初始展开层级
---

# 带配置的思维导图
## 分支 1
- 支持 **加粗**、*斜体*、`代码`
- 支持 [链接](https://example.com)
- 支持 $LaTeX$ 数学公式
```

## 渲染方式

```bash
# 方式 1：在线 REPL（推荐）
# https://markmap.js.org/repl 粘贴 Markdown 即可

# 方式 2：CLI
npm install -g markmap-cli
markmap input.md                    # 生成 input.html
markmap input.md --output out.svg   # 导出 SVG

# 方式 3：VSCode 插件
# 安装 "Markmap" 插件，Ctrl+Shift+P → "Open as Markmap"
```

## 质量基线

```
✓ 层级 ≤ 4 层（再深就难读）
✓ 每节点标签 ≤ 12 字
✓ 单分支节点 ≤ 7 个（米勒定律 7±2）
✓ 配色按层级一致
```
