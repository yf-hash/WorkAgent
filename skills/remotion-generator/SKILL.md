---
name: remotion-generator
description: >
  Remotion 动态视频生成技能。基于模板或文本描述生成 React/TypeScript 视频项目，
  支持字幕时间轴、TTS语音旁白、预览与MP4渲染，适用于企业介绍、产品演示、汇报视频。
  触发关键词：remotion、视频生成、动态视频、字幕生成、tts旁白、mp4渲染
user-invocable: false
effort: high
argument-hint: "[--template <name>] [--style <style>] [--duration <seconds>] [--preview|--render] [--subtitles] [--tts]"
---

# Remotion 视频生成技能

## 核心能力

- 模板视频生成（3个内置模板）
- 新建 Remotion 项目脚手架
- 字幕自动生成（`src/captions.ts`）
- TTS 旁白生成（edge/azure/openai）
- Remotion Studio 预览 / MP4 渲染

## 模板

- ai-native-company-intro（31s）
- plugin-ai-intro（20s）
- ai-company-intro（150s）

## 字幕流程

`voice-script.md` → 自动计算帧时间轴 → `captions.ts` → `SubtitleOverlay` 渲染

## TTS 流程

脚本文本 → 语音生成（voice.mp3）→ Remotion `<Audio />` 挂载 → 与字幕对齐

## 渲染建议

- 编码：h264
- crf：18（高质）/23（均衡）
- 分辨率：1920x1080 或 1600x900
- 需 FFmpeg 才能 render
