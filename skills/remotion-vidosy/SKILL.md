---
name: remotion-vidosy
description: >
  Vidosy JSON 场景配置驱动视频生成引擎。无需写 React 代码，纯 JSON 配置场景、背景（视频/图片/纯色）、
  文字/图片元素、动画、分层音频（背景音乐+旁白）、TTS 语音、Zod schema 验证。适合多场景产品演示。
  触发词：vidosy、JSON 场景配置、无代码视频、配置驱动视频、多场景演示
user-invocable: false
effort: medium
---

# Remotion Vidosy — JSON 场景配置视频生成

> 单一职责：用 JSON 配置生成视频，不写 React 代码。
> 不做：自定义 React 动画（→ `remotion-native`）、提示词全链路（→ `remotion-prompt2video`）

> 参考：[aaurelions/vidosy](https://github.com/aaurelions/vidosy)

## 核心优势

- 无需编写 React 代码，纯 JSON 配置驱动
- 支持多媒体背景（视频/图片/纯色）
- 分层音频（背景音乐 + 旁白，支持淡入淡出）
- 每场景独立旁白文本
- Zod schema 验证，配置错误即时提示

## 场景配置结构

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

## 元素类型

| type | 用途 |
|---|---|
| `text` | 文字（含字体/颜色/字重/动画）|
| `image` | 静态图片 |
| `video` | 嵌入视频片段 |
| `shape` | 矩形/圆形装饰元素 |

## 动画类型

| 动画 | 效果 |
|---|---|
| `fadeIn` | 渐显 |
| `slideUp` / `slideDown` / `slideLeft` / `slideRight` | 滑入 |
| `zoomIn` / `zoomOut` | 缩放 |
| `bounce` | 弹跳 |

## 质量预设

- `high`：1920×1080，crf 18
- `balanced`：1920×1080，crf 23
- `fast`：1280×720，crf 28

## 适用场景

- 多场景企业宣传片
- 产品功能逐步展示
- 数据可视化视频
- 培训/教学视频

## 依赖

```bash
npm install -g @remotion/cli
# Vidosy 自带 Zod schema 验证
```
