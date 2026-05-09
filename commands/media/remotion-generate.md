---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
description: 使用 Remotion 框架生成专业动态视频，三引擎路由：native模板/prompt2video全链路/vidosy场景配置，支持字幕/TTS/MP4渲染
argument-hint: "[--engine native|prompt2video|vidosy] [--template <name>] [--style <style>] [--duration <seconds>] [--preview] [--render] [--subtitles [script]] [--tts <provider>] [--tts-voice <voice>]"
---

# /remotion-generate

基于 [Remotion](https://github.com/remotion-dev/remotion) 框架，三引擎智能路由，将内容生成为专业动态视频并输出 MP4。

## 用法

```
/remotion-generate [选项] [内容描述|配置文件]
```

## 示例

```bash
# 引擎一：native — 使用内置模板直接渲染
/remotion-generate --template ai-native-company-intro --render

# 引擎一：native — 根据描述新建项目并预览
/remotion-generate --style cyberpunk --duration 30 "云起无垠 AI 平台产品介绍"

# 引擎一：native — 字幕 + 语音一键生成并渲染
/remotion-generate --template ai-company-intro --subtitles voice-script.md --tts edge --render

# 引擎二：prompt2video — 提示词全自动生成短视频
/remotion-generate --engine prompt2video --duration 30 "介绍我们的AI写作工具，面向内容创作者"
/remotion-generate --engine prompt2video --style cinematic --tts elevenlabs "产品发布宣传片"

# 引擎三：vidosy — JSON场景配置驱动
/remotion-generate --engine vidosy scenes.json --render
/remotion-generate --engine vidosy --quality high "生成一个5场景的企业介绍视频"
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--engine <引擎>` | `native` / `prompt2video` / `vidosy`（不指定则自动路由） | 自动 |
| `--template <名称>` | 内置模板（native引擎）：`ai-native-company-intro` / `plugin-ai-intro` / `ai-company-intro` | — |
| `--style <风格>` | `cyberpunk` / `tech` / `minimal` / `corporate` / `cinematic` | `tech` |
| `--duration <秒>` | 视频时长 | 20 |
| `--preview` | 生成项目后启动预览，不渲染 | — |
| `--render` | 直接渲染输出 MP4 | — |
| `--crf <0-51>` | 画质（18=高质量，23=均衡） | 18 |
| `--quality <预设>` | `high`(crf18) / `balanced`(crf23) / `fast`(720p,crf28) | `balanced` |
| `--subtitles [脚本]` | 从脚本文件自动生成字幕 | — |
| `--tts <provider>` | `edge`（免费）/ `azure` / `openai` / `elevenlabs` | — |
| `--tts-voice <音色>` | TTS 音色 | `zh-CN-YunxiNeural` |
| `--tts-speed <倍速>` | 语速（0.5–2.0） | 0.9 |

## 引擎说明

### 引擎一：native（Remotion 原生）
适合：企业介绍、产品演示、自定义动画、有内置模板需求

| 模板 | 时长 | 风格 | 场景 |
|------|------|------|------|
| `ai-native-company-intro` | 31秒 | 赛博朋克·紫色霓虹 | 企业介绍 |
| `plugin-ai-intro` | 20秒 | 科技感·深蓝渐变 | 产品发布 |
| `ai-company-intro` | 150秒 | 科技感·字幕 | 完整企业介绍（含字幕+语音） |

### 引擎二：prompt2video（提示词→视频全链路）
适合：短视频内容（15-60秒）、营销宣传、社交媒体内容

流程：提示词 → Claude生成脚本 → timeline.json → 图像生成 → 语音合成 → Remotion渲染 → MP4

参考：[remotion-dev/template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video)

### 引擎三：vidosy（JSON场景配置）
适合：多场景视频、无需写React代码、配置驱动生成

流程：JSON场景配置 → Vidosy验证 → Remotion渲染 → MP4

参考：[aaurelions/vidosy](https://github.com/aaurelions/vidosy)

## 自动路由逻辑

```
输入分析：
  指定 --template 或 --engine native → native
  指定 --engine prompt2video 或仅有文字描述 → prompt2video
  指定 .json 配置文件 或 --engine vidosy → vidosy
  输入为 PDF/PPT → 建议使用 /pdf2video
```

## 执行流程

1. 加载 `skills/remotion-generator/SKILL.md` 完整规范
2. 路由引擎（native / prompt2video / vidosy）
3. **native**：识别模板或生成 React/TypeScript 场景组件
4. **prompt2video**：生成 timeline.json → 图像 → 语音 → 合成
5. **vidosy**：生成/验证 vidosy.json → Remotion 渲染
6. （可选）生成 `src/captions.ts` 字幕数据
7. （可选）调用 TTS 生成 `public/voice.mp3` 语音
8. `--preview`：启动 Remotion Studio 预览
9. `--render`：执行 `npm run build` 输出 MP4

## 相关命令

- `/pdf2video` — PDF/PPT 文档转动态视频
- `/caption` — 为已有视频生成多语言字幕
- `/videocut` — AI 视频剪辑（去除停顿/口误）
