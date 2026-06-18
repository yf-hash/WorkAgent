---
name: remotion-prompt2video
description: 提示词 → 短视频全链路（脚本 → timeline.json → 图像生成 → 语音合成 → MP4）。
user-invocable: true
argument-hint: "<提示词> [--style corporate|cinematic|minimal|tech] [--duration <seconds>]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /remotion-prompt2video — 提示词全链路视频生成

加载技能：`skills/remotion-prompt2video/SKILL.md`

## 用法

```bash
/remotion-prompt2video "介绍我们的 AI 写作助手产品" --style tech --duration 30
```

## 适用

15-60 秒 TikTok/Instagram/视频号风格短视频。
