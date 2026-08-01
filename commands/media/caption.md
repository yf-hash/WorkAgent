---
name: caption
description: 视频字幕自动生成 — 转录+翻译+双语输出，支持30+格式，YouTube下载，Claude翻译无需额外API
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
argument-hint: "<video_url|filepath> [--lang <代码>] [--translate <目标语言>] [--bilingual] [--format srt|vtt|ass|json] [--engine whisper|gemini]"
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

# /caption

为视频自动生成字幕，支持转录、翻译、双语输出。

> 参考：[lattifai/omni-captions-skills](https://github.com/lattifai/omni-captions-skills)

## 用法

```
/caption <视频URL或文件路径> [选项]
```

## 示例

```bash
# 基础转录（中文视频 → SRT字幕）
/caption video.mp4

# YouTube 视频转录
/caption https://youtube.com/watch?v=xxx

# 转录 + 翻译为中文
/caption video.mp4 --translate zh

# 双语字幕（英文原文 + 中文翻译）
/caption video.mp4 --bilingual --translate zh --format ass

# 高精度转录（Gemini引擎）
/caption video.mp4 --engine gemini --translate zh

# 词级对齐（用于卡拉OK效果）
/caption video.mp4 --word-align --format json
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--lang <代码>` | 源语言（`zh`/`en`/`ja`/`auto`） | `auto` |
| `--translate <代码>` | 翻译目标语言（`zh`/`en`/`ja` 等） | 不翻译 |
| `--bilingual` | 输出双语字幕（原文+译文） | 否 |
| `--format <格式>` | `srt`/`vtt`/`ass`/`json`/`txt` | `srt` |
| `--engine <引擎>` | `whisper`（本地）/ `gemini`（高精度）/ `auto` | `auto` |
| `--word-align` | 词级时间轴对齐（需 LattifAI） | 否 |
| `--output <路径>` | 输出文件路径 | 同输入文件名 |

## 支持格式

`SRT` `VTT` `ASS/SSA` `JSON` `TXT` `YouTube XML` `Bilibili XML`

## 执行流程

1. 加载 `skills/media/omni-captions/SKILL.md` 完整规范
2. 输入处理（YouTube下载 / 本地文件读取）
3. 语音转录（Whisper / Gemini）
4. 翻译（Claude，无需额外 API Key）
5. 双语合并（可选）
6. 词级对齐（可选）
7. 输出指定格式字幕文件

## 依赖

```bash
pip install yt-dlp openai-whisper
# 可选高精度转录
pip install google-generativeai
```

## 相关命令

- `/video-gen --engine native|prompt2video|vidosy` — 生成动态视频（可传入字幕文件）
- `/videocut` — AI 视频剪辑
- `/pdf2video` — 文档转视频
