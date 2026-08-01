---
name: omni-captions
description: >
  视频字幕自动生成技能。支持30+字幕格式，自动转录、翻译、双语输出。
  支持 YouTube 视频下载、本地视频文件、Claude 翻译（无需额外API）、
  可选 Gemini 转录和 LattifAI 词级对齐。
  触发关键词：字幕生成、视频字幕、subtitle、caption、转录、翻译字幕、双语字幕、srt、vtt
user-invocable: false
effort: medium
argument-hint: "<video_url|filepath> [--lang <语言代码>] [--bilingual] [--format srt|vtt|ass|json] [--translate <目标语言>]"
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# 视频字幕自动生成技能

> 参考：[lattifai/omni-captions-skills](https://github.com/lattifai/omni-captions-skills)

## 核心能力

- 视频音频自动转录（语音→文字）
- 30+ 字幕格式输出（SRT/VTT/ASS/JSON/TXT 等）
- Claude 驱动翻译（无需额外 API Key）
- 双语字幕输出（原文 + 译文同屏）
- YouTube 视频直接下载并处理
- 可选 Gemini 转录（更高精度）
- 可选 LattifAI 词级时间轴对齐

---

## 转录引擎

| 引擎 | 精度 | 速度 | 要求 |
|------|------|------|------|
| `whisper` | 高 | 中 | 本地安装 openai-whisper |
| `gemini` | 极高 | 快 | Gemini API Key |
| `auto` | 自动选择 | — | 优先 gemini，回退 whisper |

---

## 翻译引擎

| 引擎 | 说明 | 要求 |
|------|------|------|
| `claude` | Claude 翻译，无需额外 Key，质量高 | 默认，无需配置 |
| `deepl` | DeepL API | DEEPL_API_KEY |
| `none` | 不翻译，仅转录 | — |

---

## 执行流程

```
Step 1: 输入处理
  YouTube URL → yt-dlp 下载音频
  本地文件 → 直接读取音频轨道

Step 2: 转录
  音频 → Whisper / Gemini → 带时间戳的文字段落

Step 3: 翻译（可选）
  原文字幕 → Claude 翻译 → 目标语言字幕
  双语模式：原文 + 译文合并为双语字幕

Step 4: 词级对齐（可选，LattifAI）
  段落级时间戳 → 词级精确时间戳
  用于卡拉OK效果、精确高亮

Step 5: 格式输出
  → SRT（最通用）
  → VTT（Web/YouTube）
  → ASS（高级样式，支持双语布局）
  → JSON（程序化处理）
```

---

## 支持的字幕格式

```
通用：SRT, VTT, TXT
高级：ASS/SSA（支持样式/位置/颜色）
程序化：JSON（含词级时间戳）
平台专用：YouTube XML, Bilibili XML
```

---

## 双语字幕布局（ASS格式）

```
┌─────────────────────────────────┐
│                                 │
│         视频内容                 │
│                                 │
│   This is the original text     │  ← 原文（底部第二行）
│       这是原文的翻译              │  ← 译文（底部第一行）
└─────────────────────────────────┘
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--lang <代码>` | 源语言（`zh`/`en`/`ja`/`auto`） | `auto` |
| `--translate <代码>` | 翻译目标语言（`zh`/`en`/`ja` 等） | 不翻译 |
| `--bilingual` | 输出双语字幕 | 否 |
| `--format <格式>` | 输出格式（`srt`/`vtt`/`ass`/`json`） | `srt` |
| `--engine <引擎>` | 转录引擎（`whisper`/`gemini`/`auto`） | `auto` |
| `--word-align` | 启用词级时间轴对齐（需 LattifAI） | 否 |
| `--output <路径>` | 输出文件路径 | 同输入文件名 |

---

## 依赖安装

```bash
pip install yt-dlp openai-whisper
# 可选：Gemini 转录
pip install google-generativeai
```

---

## 与视频生成技能的集成

字幕生成完成后，可直接传入 Remotion 系列命令：

```bash
# 先生成字幕
/caption video.mp4 --translate zh --format srt

# 再用字幕渲染视频
/video-gen --engine native --template ai-company-intro --subtitles video.srt --render
```
