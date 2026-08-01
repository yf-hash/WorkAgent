---
name: remotion-native
description: >
  Remotion 原生引擎（React/TypeScript 组件）视频生成技能。提供 3 个内置模板（赛博朋克/科技深蓝/字幕语音长版），
  支持字幕自动生成（src/captions.ts）、TTS 旁白（edge/azure/openai）、Remotion Studio 预览 / MP4 渲染。
  触发词：Remotion 原生、Remotion 模板、自定义动画、React 视频、字幕生成、TTS 旁白
user-invocable: false
effort: high
argument-hint: "[--template <name>] [--style <style>] [--duration <seconds>] [--preview|--render] [--subtitles] [--tts]"
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

# Remotion Native — 原生 React 视频生成

> 单一职责：用 Remotion 原生 React 组件生成视频。
> 不做：提示词转视频（→ `remotion-prompt2video`）、JSON 场景配置（→ `remotion-vidosy`）、PDF/PPT 转视频（→ `pdf2video`）

## 核心能力

- 模板视频生成（3 个内置模板）
- 新建 Remotion 项目脚手架
- 字幕自动生成（`src/captions.ts`）
- TTS 旁白生成（edge/azure/openai）
- Remotion Studio 预览 / MP4 渲染

## 内置模板

| 模板 | 时长 | 风格 |
|---|---|---|
| `ai-native-company-intro` | 31s | 赛博朋克·紫色霓虹 |
| `plugin-ai-intro` | 20s | 科技感·深蓝渐变 |
| `ai-company-intro` | 150s | 科技感·字幕+语音 |

## 字幕流程

`voice-script.md` → 自动计算帧时间轴 → `captions.ts` → `SubtitleOverlay` 渲染

## TTS 流程

脚本文本 → 语音生成（voice.mp3）→ Remotion `<Audio />` 挂载 → 与字幕对齐

## 渲染配置

| 参数 | 推荐 |
|---|---|
| 编码 | h264 |
| crf | 18（高质）/ 23（均衡） |
| 分辨率 | 1920×1080 或 1600×900 |
| 依赖 | FFmpeg，`npm install -g @remotion/cli` |

## 适用场景

- 企业介绍视频
- 产品演示视频
- 需要自定义 React 动画的场景
- 内置模板可直接使用的快速产出
