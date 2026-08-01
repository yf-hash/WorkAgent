---
name: videocut
description: >
  AI 视频智能剪辑技能。专为口播/演讲视频设计，自动检测并剪除停顿、重复、口误、卡顿片段。
  基于 ASR 转录 + Claude 语义分析 + FFmpeg 精准剪切，支持人工审核 Web UI。
  触发关键词：视频剪辑、去停顿、去口误、口播剪辑、videocut、自动剪辑、视频精剪
user-invocable: false
effort: high
argument-hint: "<video_filepath> [--mode auto|review] [--silence-threshold <dB>] [--min-silence <ms>] [--output <path>]"
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

# AI 视频智能剪辑技能

> 参考：[Ceeon/videocut-skills](https://github.com/Ceeon/videocut-skills)

## 核心能力

- 语音转录（Volcano Engine ASR / Whisper）
- Claude 语义分析：识别停顿/重复/口误/卡顿
- 自定义术语词典（避免专业词汇误判）
- Web 审核界面（人工确认剪切点）
- FFmpeg 精准帧级剪切
- 输出剪辑后视频 + 剪辑报告

---

## 检测类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **静音段** | 超过阈值的无声片段 | 思考停顿、换气停顿 |
| **重复片段** | 同一句话说了多遍 | "这个这个这个功能" |
| **口误** | 说错后自我纠正 | "我们有三个...不对，四个功能" |
| **卡顿词** | 填充词/语气词密集 | "那个、就是、然后、嗯" |
| **语义重复** | 同一意思反复表达 | 前后两段表达相同内容 |

---

## 执行流程

```
Step 1: 音频提取
  视频文件 → FFmpeg 提取音频轨道（WAV/MP3）

Step 2: 语音转录
  音频 → ASR（Volcano Engine / Whisper）
  → 带精确时间戳的转录文本

Step 3: Claude 语义分析
  转录文本 → Claude 分析
  → 标记需剪除的片段（类型/开始时间/结束时间/原因）
  → 生成剪切清单 cuts.json

Step 4: 人工审核（--mode review）
  启动 Web UI → 展示剪切清单
  → 用户确认/修改/跳过每个剪切点
  → 保存最终剪切决策

Step 5: FFmpeg 剪切
  按 cuts.json 执行精准剪切
  → 合并保留片段
  → 输出剪辑后视频

Step 6: 输出报告
  → 原始时长 vs 剪辑后时长
  → 剪除片段数量与类型统计
  → 剪切详情列表
```

---

## cuts.json 结构

```json
{
  "source": "input.mp4",
  "total_duration": 600.0,
  "cuts": [
    {
      "id": 1,
      "type": "silence",
      "start": 12.3,
      "end": 14.8,
      "duration": 2.5,
      "reason": "静音停顿超过2秒",
      "transcript": ""
    },
    {
      "id": 2,
      "type": "repetition",
      "start": 45.1,
      "end": 48.6,
      "duration": 3.5,
      "reason": "重复表达：'这个功能'出现3次",
      "transcript": "这个功能这个功能这个功能可以帮助"
    },
    {
      "id": 3,
      "type": "mistake",
      "start": 102.0,
      "end": 106.5,
      "duration": 4.5,
      "reason": "口误后自我纠正",
      "transcript": "我们有三个...不对，四个核心模块"
    }
  ],
  "estimated_saved": 45.2
}
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode auto` | 全自动剪辑，无需人工确认 | — |
| `--mode review` | 启动 Web UI 人工审核后再剪辑 | 默认 |
| `--silence-threshold <dB>` | 静音检测阈值 | `-40dB` |
| `--min-silence <ms>` | 最短静音时长（低于此值不剪） | `1500ms` |
| `--dict <filepath>` | 自定义术语词典（避免误判专业词汇） | — |
| `--asr <引擎>` | `volcano`（需API Key）/ `whisper`（本地） | `whisper` |
| `--output <路径>` | 输出视频路径 | `<原文件名>-cut.mp4` |
| `--keep-cuts` | 保留 cuts.json 供后续调整 | 否 |

---

## 术语词典格式

```json
{
  "terms": ["Claude Code", "WorkAgent", "RAG", "LLM", "API"],
  "ignore_patterns": ["嗯+", "那个那个", "就是就是"]
}
```

---

## 依赖安装

```bash
# FFmpeg（必须）
# macOS: brew install ffmpeg
# Windows: 下载 ffmpeg.exe 并加入 PATH

# Whisper（本地ASR）
pip install openai-whisper

# Web UI（审核模式）
npm install
```

---

## 输出结构

```
output/
  <filename>-cut.mp4     # 剪辑后视频
  cuts.json              # 剪切记录
  report.md              # 剪辑报告（时长对比/类型统计）
```
