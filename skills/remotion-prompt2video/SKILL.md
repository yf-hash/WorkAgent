---
name: remotion-prompt2video
description: >
  提示词 → 短视频全链路引擎。流程：Claude 生成脚本 → timeline.json → 图像生成（DALL-E/SD）→
  语音合成（ElevenLabs/edge-tts）→ Remotion 合成渲染 → MP4。适合 15-60 秒 TikTok/Instagram/视频号风格短视频。
  触发词：提示词转视频、prompt 转视频、短视频生成、TikTok 风格、AI 一键视频
user-invocable: false
effort: high
---

# Remotion Prompt2Video — 提示词全链路视频生成

> 单一职责：从一句话提示词 → 完整短视频。
> 不做：自定义 React 动画（→ `remotion-native`）、JSON 场景配置（→ `remotion-vidosy`）

> 参考：[remotion-dev/template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video)

## 流程

```
用户提示词
  → Claude 生成视频脚本（场景列表）
  → 生成 timeline.json（场景/时长/旁白/视觉描述）
  → 图像生成（DALL-E / Stable Diffusion）
  → 语音合成（ElevenLabs / edge-tts）
  → Remotion 合成渲染 → MP4 输出
```

## timeline.json 结构

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

## 风格预设

| 预设 | 适用 |
|---|---|
| `corporate` | 企业介绍、产品发布 |
| `cinematic` | 品牌故事、营销短片 |
| `minimal` | 单点信息传达 |
| `tech` | 技术产品、AI 工具 |

## 适用场景

- 短视频内容（15-60 秒）
- 产品功能介绍
- 营销宣传片
- 社交媒体内容（TikTok/Instagram/视频号）

## 依赖

```bash
# 图像生成
export OPENAI_API_KEY=...   # DALL-E
# 或本地 Stable Diffusion

# 语音合成
export ELEVEN_API_KEY=...   # ElevenLabs
# 或 edge-tts（免费）

# 渲染
npm install -g @remotion/cli
```

## 渲染建议

- 质量预设 `high`：1920×1080，crf 18
- 短视频通常 1080×1920（9:16 竖屏）
- 单条视频成本估算：图像 N × $0.04 + 语音 ~$0.30 + 渲染本地
