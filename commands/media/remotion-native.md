---
name: remotion-native
description: Remotion 原生 React 视频生成（3 个内置模板 + 字幕 + TTS + 预览/渲染）。
user-invocable: true
argument-hint: "[--template <name>] [--style <style>] [--duration <seconds>] [--preview|--render] [--subtitles] [--tts]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /remotion-native — Remotion 原生引擎

加载技能：`skills/remotion-native/SKILL.md`

## 用法

```bash
/remotion-native --template ai-native-company-intro --render
/remotion-native --template plugin-ai-intro --tts --subtitles --preview
```

## 与其他视频命令的边界

| 场景 | 推荐 |
|---|---|
| 自定义 React 动画 + 模板 | **本命令** |
| 提示词一键生成短视频 | `/remotion-prompt2video` |
| JSON 配置多场景视频 | `/remotion-vidosy` |
| PDF/PPT 转动态视频 | `/pdf2video` |
