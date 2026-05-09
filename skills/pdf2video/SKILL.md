---
name: pdf2video
description: >
  PDF/PPT 文档转动态视频技能。解析 PDF 或 PPT 文件，自动提取内容并生成 Remotion 动画视频。
  支持 stack/focus/zoom/fan 四种场景动画类型，自动生成标题系统、底部信息栏、背景音乐。
  触发关键词：pdf转视频、ppt转视频、文档转视频、pdf2video、幻灯片视频、文档动画
user-invocable: false
effort: high
argument-hint: "<filepath.pdf|.pptx> [--scene-type stack|focus|zoom|fan] [--music] [--duration <seconds>] [--render]"
---

# PDF/PPT 转动态视频技能

> 参考：[DangJin/pdf2video](https://github.com/DangJin/pdf2video)

## 核心能力

- PDF / PPTX 文件解析，提取文字与图像内容
- 四种场景动画类型自动路由
- 标题系统（打字机效果）
- 底部信息栏（进度/页码/来源）
- 背景音乐（淡入淡出）
- 1920×1080 30fps MP4 输出
- JSON 场景配置中间格式（可手动调整）

---

## 四种场景动画类型

| 类型 | 效果 | 适用内容 |
|------|------|---------|
| `stack` | 内容块逐层堆叠出现 | 列表、要点、步骤说明 |
| `focus` | 聚焦高亮关键内容，其余模糊 | 数据对比、重点强调 |
| `zoom` | 内容从中心缩放出现 | 标题页、封面、过渡页 |
| `fan` | 内容扇形展开 | 图表、关系图、分类展示 |

---

## 执行流程

```
Step 1: 文件解析
  PDF → pdfplumber 提取文字/图像/布局
  PPTX → python-pptx 提取幻灯片内容

Step 2: 内容分析
  → 识别标题、正文、图表、数据
  → 按页/幻灯片分割场景
  → 为每个场景选择最优动画类型

Step 3: 生成 scenes.json
  → 场景列表（id/duration/type/content/title）
  → 音频配置（背景音乐/旁白）
  → 全局配置（分辨率/帧率/风格）

Step 4: Remotion 渲染
  → 加载 scenes.json
  → 生成 React 组件
  → 渲染输出 MP4
```

---

## scenes.json 结构

```json
{
  "config": {
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "style": "corporate|tech|minimal|academic"
  },
  "audio": {
    "background": { "src": "./music.mp3", "volume": 0.2, "fadeOut": 3 }
  },
  "scenes": [
    {
      "id": "scene-1",
      "type": "zoom",
      "duration": 4,
      "title": "文档标题",
      "content": [],
      "footer": { "text": "来源：原始文档", "showProgress": true }
    },
    {
      "id": "scene-2",
      "type": "stack",
      "duration": 6,
      "title": "第一章：背景",
      "content": [
        { "text": "要点一", "delay": 0.5 },
        { "text": "要点二", "delay": 1.0 },
        { "text": "要点三", "delay": 1.5 }
      ]
    },
    {
      "id": "scene-3",
      "type": "focus",
      "duration": 5,
      "title": "核心数据",
      "content": [
        { "highlight": "增长 47%", "context": "相比去年同期" }
      ]
    }
  ]
}
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--scene-type` | 强制所有场景使用同一动画类型 | 自动选择 |
| `--music` | 添加背景音乐 | 无 |
| `--duration <秒>` | 每页默认时长 | 5 |
| `--style` | `corporate` / `tech` / `minimal` / `academic` | `corporate` |
| `--render` | 直接渲染输出 MP4 | 仅生成配置 |
| `--preview` | 启动 Remotion Studio 预览 | — |
| `--output <路径>` | 输出文件路径 | `./output.mp4` |

---

## 依赖

```bash
pip install pdfplumber python-pptx
npm install -g @remotion/cli
```

---

## 输出结构

```
output/
  scenes.json          # 场景配置（可手动调整后重新渲染）
  output.mp4           # 最终视频
  frames/              # 关键帧截图（可选）
```
