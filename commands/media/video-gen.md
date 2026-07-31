---
name: video-gen
description: Remotion 视频生成统一入口（native / prompt2video / vidosy 三引擎）。原生 React 模板、提示词一键、JSON 场景配置。
user-invocable: true
argument-hint: "[--engine native|prompt2video|vidosy] [各引擎参数]"
allowed-tools: [Read, Write, Edit, Bash]
---

# /video-gen — Remotion 视频生成

## 一句话

Remotion 三引擎一个入口。用 `--engine` 分派。

## 用法

```bash
# native：Remotion 原生 React 模板（3 内置模板 + 字幕 + TTS）
/video-gen --engine native --template ai-native-company-intro --render
/video-gen --engine native --template plugin-ai-intro --tts --subtitles --preview

# prompt2video：提示词一键短视频（15-60 秒 TikTok/视频号）
/video-gen --engine prompt2video "介绍我们的 AI 写作助手" --style tech --duration 30

# vidosy：JSON 场景配置驱动（多场景 / 数据可视化 / 培训片）
/video-gen --engine vidosy ./scenes.json --quality high
```

## 分派规则

| `--engine` | 加载技能 | 场景 |
|---|---|---|
| `native` | `skills/remotion-native/SKILL.md` | 自定义 React 动画、内置模板、精细控制 |
| `prompt2video` | `skills/remotion-prompt2video/SKILL.md` | 15-60 秒 TikTok/Instagram/视频号短视频 |
| `vidosy` | `skills/remotion-vidosy/SKILL.md` | 多场景企业宣传、产品功能逐步展示、培训片 |

## 与其他视频命令的边界

| 场景 | 用 |
|---|---|
| Remotion 生成视频 | **本命令** |
| PDF/PPT → 视频 | `/pdf2video` |
| 视频字幕 | `/caption` |
| AI 视频剪辑 | `/videocut` |

## 迁移说明（v2.8）

旧命令 `/remotion-native` / `/remotion-prompt2video` / `/remotion-vidosy` 已合并至本命令，用 `--engine <name>` 替代。3 个 skill 未变。
