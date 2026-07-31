---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
description: AI 视频智能剪辑 — 自动检测并剪除停顿/重复/口误/卡顿，支持人工审核模式，FFmpeg精准剪切
argument-hint: "<video_filepath> [--mode auto|review] [--silence-threshold <dB>] [--min-silence <ms>] [--dict <filepath>] [--asr whisper|volcano]"
---

# /videocut

AI 驱动的口播视频智能剪辑，自动去除停顿、重复、口误片段。

> 参考：[Ceeon/videocut-skills](https://github.com/Ceeon/videocut-skills)

## 用法

```
/videocut <视频文件路径> [选项]
```

## 示例

```bash
# 基础剪辑（人工审核模式）
/videocut lecture.mp4

# 全自动剪辑，无需确认
/videocut podcast.mp4 --mode auto

# 自定义静音阈值（更激进地去除停顿）
/videocut interview.mp4 --silence-threshold -35 --min-silence 1000

# 使用自定义术语词典（避免专业词汇误判）
/videocut tech-talk.mp4 --dict terms.json

# 高精度转录（Volcano Engine ASR）
/videocut keynote.mp4 --asr volcano --mode review
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--mode auto` | 全自动剪辑，无需人工确认 | — |
| `--mode review` | 启动 Web UI 人工审核后再剪辑 | 默认 |
| `--silence-threshold <dB>` | 静音检测阈值 | `-40dB` |
| `--min-silence <ms>` | 最短静音时长（低于此值不剪） | `1500ms` |
| `--dict <filepath>` | 自定义术语词典 JSON | — |
| `--asr <引擎>` | `whisper`（本地）/ `volcano`（需API Key） | `whisper` |
| `--output <路径>` | 输出视频路径 | `<原文件名>-cut.mp4` |
| `--keep-cuts` | 保留 cuts.json 供后续调整 | 否 |

## 检测类型

| 类型 | 说明 |
|------|------|
| 静音段 | 超过阈值的无声停顿 |
| 重复片段 | 同一句话说了多遍 |
| 口误 | 说错后自我纠正的片段 |
| 卡顿词 | 填充词密集段（嗯、那个、就是） |
| 语义重复 | 前后两段表达相同内容 |

## 执行流程

1. 加载 `skills/videocut/SKILL.md` 完整规范
2. FFmpeg 提取音频轨道
3. ASR 转录（Whisper / Volcano Engine）
4. Claude 语义分析，生成 `cuts.json`
5. `--mode review`：启动 Web UI 人工审核
6. FFmpeg 精准剪切，合并保留片段
7. 输出剪辑后视频 + 剪辑报告

## 依赖

```bash
# FFmpeg（必须）
# macOS: brew install ffmpeg
# Windows: 下载并加入 PATH

pip install openai-whisper
```

## 相关命令

- `/caption` — 为视频生成字幕
- `/video-gen --engine native|prompt2video|vidosy` — 生成动态视频
- `/pdf2video` — 文档转视频
