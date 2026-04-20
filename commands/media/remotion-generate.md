---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
description: 使用 Remotion 框架生成专业动态视频，支持企业介绍/产品宣传/字幕/TTS语音合成
argument-hint: "[--template <name>] [--style <style>] [--duration <seconds>] [--preview] [--render] [--subtitles [script]] [--tts <provider>] [--tts-voice <voice>]"
---

# /remotion-generate

基于 [Remotion](https://github.com/remotion-dev/remotion) 框架，将内容生成为专业动态视频并输出 MP4。

## 用法

```
/remotion-generate [选项] [内容描述]
```

## 示例

```bash
# 使用内置模板直接渲染
/remotion-generate --template ai-native-company-intro --render

# 根据描述新建项目并预览
/remotion-generate --style cyberpunk --duration 30 "云起无垠 AI 平台产品介绍"

# 字幕 + 语音一键生成并渲染
/remotion-generate --template ai-company-intro --subtitles voice-script.md --tts edge --render
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--template <名称>` | 内置模板：`ai-native-company-intro` / `plugin-ai-intro` / `ai-company-intro` | — |
| `--style <风格>` | `cyberpunk` / `tech` / `minimal` / `corporate` | `tech` |
| `--duration <秒>` | 视频时长 | 20 |
| `--preview` | 生成项目后启动预览，不渲染 | — |
| `--render` | 直接渲染输出 MP4 | — |
| `--crf <0-51>` | 画质（18=高质量，23=均衡） | 18 |
| `--subtitles [脚本]` | 从脚本文件自动生成字幕 | — |
| `--tts <provider>` | `edge`（免费）/ `azure` / `openai` | — |
| `--tts-voice <音色>` | TTS 音色 | `zh-CN-YunxiNeural` |
| `--tts-speed <倍速>` | 语速（0.5–2.0） | 0.9 |

## 内置模板

| 模板 | 时长 | 风格 | 场景 |
|------|------|------|------|
| `ai-native-company-intro` | 31秒 | 赛博朋克·紫色霓虹 | 企业介绍 |
| `plugin-ai-intro` | 20秒 | 科技感·深蓝渐变 | 产品发布 |
| `ai-company-intro` | 150秒 | 科技感·字幕 | 完整企业介绍（含字幕+语音） |

## 执行流程

1. 加载 `skills/remotion-generator/SKILL.md` 完整规范
2. 识别模板或从内容描述创建新项目
3. 生成 React/TypeScript 场景组件
4. （可选）解析脚本文件，生成 `src/captions.ts` 字幕数据
5. （可选）调用 TTS 生成 `public/voice.mp3` 语音
6. `--preview`：启动 Remotion Studio 预览
7. `--render`：执行 `npm run build` 输出 MP4

## 相关命令

- `/video preview` — 预览已有 Remotion 项目
