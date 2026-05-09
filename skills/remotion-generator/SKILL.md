---
name: remotion-generator
description: >
  Remotion 动态视频生成技能。支持三种引擎：① Remotion 原生（React/TypeScript组件）
  ② template-prompt-to-video（提示词→脚本→图像→语音→视频全链路）
  ③ Vidosy（JSON场景配置驱动，无需写React代码）。
  支持字幕时间轴、TTS语音旁白、预览与MP4渲染，适用于企业介绍、产品演示、短视频、汇报视频。
  触发关键词：remotion、视频生成、动态视频、字幕生成、tts旁白、mp4渲染、prompt转视频、场景视频、vidosy
user-invocable: false
effort: high
argument-hint: "[--engine native|prompt2video|vidosy] [--template <name>] [--style <style>] [--duration <seconds>] [--preview|--render] [--subtitles] [--tts]"
---

# Remotion 视频生成技能

## 三引擎架构

| 引擎 | 适用场景 | 技术栈 | 参考项目 |
|------|---------|--------|---------|
| `native` | 企业介绍、产品演示、自定义动画 | React/TypeScript + Remotion | remotion-dev/remotion |
| `prompt2video` | 提示词一键生成短视频（TikTok/Instagram风格） | OpenAI脚本 + 图像生成 + ElevenLabs语音 + Remotion渲染 | remotion-dev/template-prompt-to-video |
| `vidosy` | JSON场景配置驱动，无需写React代码 | JSON → Vidosy → Remotion渲染 | aaurelions/vidosy |

## 引擎一：native（Remotion 原生）

### 核心能力
- 模板视频生成（3个内置模板）
- 新建 Remotion 项目脚手架
- 字幕自动生成（`src/captions.ts`）
- TTS 旁白生成（edge/azure/openai）
- Remotion Studio 预览 / MP4 渲染

### 内置模板
- `ai-native-company-intro`（31s，赛博朋克·紫色霓虹）
- `plugin-ai-intro`（20s，科技感·深蓝渐变）
- `ai-company-intro`（150s，科技感·字幕+语音）

### 字幕流程
`voice-script.md` → 自动计算帧时间轴 → `captions.ts` → `SubtitleOverlay` 渲染

### TTS 流程
脚本文本 → 语音生成（voice.mp3）→ Remotion `<Audio />` 挂载 → 与字幕对齐

---

## 引擎二：prompt2video（提示词→视频全链路）

> 参考：[remotion-dev/template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video)

### 流程
```
用户提示词
  → Claude 生成视频脚本（场景列表）
  → 生成 timeline.json（场景/时长/旁白/视觉描述）
  → 图像生成（DALL-E / Stable Diffusion）
  → 语音合成（ElevenLabs / edge-tts）
  → Remotion 合成渲染 → MP4 输出
```

### timeline.json 结构
```json
{
  "scenes": [
    {
      "id": "scene-1",
      "duration": 3,
      "narration": "旁白文本",
      "visual": "视觉描述（用于图像生成）",
      "text_overlay": "屏幕显示文字（可选）"
    }
  ],
  "total_duration": 30,
  "style": "corporate|cinematic|minimal|tech"
}
```

### 适用场景
- 短视频内容（15-60秒）
- 产品功能介绍
- 营销宣传片
- 社交媒体内容（TikTok/Instagram/视频号）

---

## 引擎三：vidosy（JSON场景配置）

> 参考：[aaurelions/vidosy](https://github.com/aaurelions/vidosy)

### 核心优势
- 无需编写 React 代码，纯 JSON 配置驱动
- 支持多媒体背景（视频/图片/纯色）
- 分层音频（背景音乐 + 旁白，支持淡入淡出）
- 每场景独立旁白文本
- Zod schema 验证，配置错误即时提示

### vidosy 场景配置结构
```json
{
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "scenes": [
    {
      "duration": 5,
      "background": {
        "type": "color|image|video",
        "value": "#1a1a2e | ./bg.jpg | ./bg.mp4"
      },
      "narration": "本场景旁白文字",
      "elements": [
        {
          "type": "text",
          "content": "标题文字",
          "style": { "fontSize": 64, "color": "#ffffff", "fontWeight": "bold" },
          "position": { "x": "center", "y": "center" },
          "animation": "fadeIn|slideUp|zoomIn"
        },
        {
          "type": "image",
          "src": "./logo.png",
          "position": { "x": 100, "y": 50 },
          "size": { "width": 200, "height": 80 }
        }
      ]
    }
  ],
  "audio": {
    "background": { "src": "./music.mp3", "volume": 0.3, "fadeOut": 2 },
    "narration": { "provider": "edge-tts", "voice": "zh-CN-YunxiNeural" }
  }
}
```

### 质量预设
- `high`：1920×1080，crf 18
- `balanced`：1920×1080，crf 23
- `fast`：1280×720，crf 28

### 适用场景
- 多场景企业宣传片
- 产品功能逐步展示
- 数据可视化视频
- 培训/教学视频

---

## 引擎选择策略

```
用户输入分析：
  有提示词，无素材 → prompt2video
  有JSON配置或多场景需求，无需自定义动画 → vidosy
  需要自定义React动画/有内置模板需求 → native
  有PDF/PPT需转视频 → 调用 pdf2video skill
```

---

## 渲染建议（通用）

- 编码：h264
- crf：18（高质）/ 23（均衡）
- 分辨率：1920×1080 或 1600×900
- 需 FFmpeg 才能 render
- 安装：`npm install -g @remotion/cli`
