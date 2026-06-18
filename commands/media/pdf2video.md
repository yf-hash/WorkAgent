---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
description: PDF/PPT 文档转动态视频 — 自动解析文档内容，生成 stack/focus/zoom/fan 四种场景动画，输出 MP4
argument-hint: "<filepath.pdf|.pptx> [--scene-type stack|focus|zoom|fan] [--style corporate|tech|minimal|academic] [--music] [--duration <seconds>] [--render]"
---

# /pdf2video

将 PDF 或 PPT 文档自动转换为动态视频演示。

> 参考：[DangJin/pdf2video](https://github.com/DangJin/pdf2video)

## 用法

```
/pdf2video <文件路径> [选项]
```

## 示例

```bash
# 基础转换（生成配置，不渲染）
/pdf2video report.pdf

# 直接渲染输出 MP4
/pdf2video presentation.pptx --render

# 指定风格和场景类型
/pdf2video research.pdf --style academic --scene-type stack --render

# 添加背景音乐，每页5秒
/pdf2video product-deck.pdf --music --duration 5 --style tech --render

# 预览后手动调整再渲染
/pdf2video annual-report.pdf --preview
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--scene-type <类型>` | `stack`（堆叠）/ `focus`（聚焦）/ `zoom`（缩放）/ `fan`（扇形）/ `auto`（自动选择） | `auto` |
| `--style <风格>` | `corporate` / `tech` / `minimal` / `academic` | `corporate` |
| `--duration <秒>` | 每页默认时长 | `5` |
| `--music` | 添加背景音乐（淡入淡出） | 否 |
| `--render` | 直接渲染输出 MP4 | 仅生成 scenes.json |
| `--preview` | 启动 Remotion Studio 预览 | — |
| `--output <路径>` | 输出文件路径 | `./output.mp4` |

## 场景动画类型

| 类型 | 效果 | 最适合 |
|------|------|--------|
| `stack` | 内容块逐层堆叠出现 | 列表、要点、步骤 |
| `focus` | 聚焦高亮关键内容 | 数据对比、重点强调 |
| `zoom` | 内容从中心缩放出现 | 标题页、封面 |
| `fan` | 内容扇形展开 | 图表、分类展示 |

## 执行流程

1. 加载 `skills/pdf2video/SKILL.md` 完整规范
2. 解析文件（PDF → pdfplumber / PPTX → python-pptx）
3. 分析每页内容，自动选择最优动画类型
4. 生成 `scenes.json` 场景配置
5. `--preview`：启动 Remotion Studio 预览
6. `--render`：渲染输出 MP4

## 依赖

```bash
pip install pdfplumber python-pptx
npm install -g @remotion/cli
```

## 相关命令

- `/remotion-native` / `/remotion-prompt2video` / `/remotion-vidosy` — 从提示词或模板生成视频
- `/caption` — 为视频生成多语言字幕
- `/ppt` — PPT 生成（反向：内容→PPT）
