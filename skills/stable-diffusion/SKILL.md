---
name: stable-diffusion
description: >
  Stable Diffusion 图像生成知识库。触发词：AI绘图、文生图、图生图、SD、
  Stable Diffusion、创意图像、封面图、插图、写实风格、艺术风格、提示词。
user-invocable: false
effort: medium
---

# Stable Diffusion Image Generator

## 概述
通过 Stable Diffusion WebUI API 生成 AI 图像，支持文生图、图生图、图像修复等功能。

## 核心能力
- **文生图（Text-to-Image）** - 根据文本描述生成图像
- **图生图（Image-to-Image）** - 基于参考图生成新图像
- **图像修复（Inpainting）** - 修复或替换图像局部区域
- **图像放大（Upscaling）** - 提升图像分辨率
- **风格迁移** - 应用不同艺术风格
- **批量生成** - 一次生成多张图像

## 前置要求

### 本地部署
需要先部署 Stable Diffusion WebUI：
```bash
# 克隆仓库
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 启动 WebUI（启用 API）
./webui.sh --api --listen
# Windows: webui-user.bat --api --listen
```

### API 配置
默认 API 地址：`http://127.0.0.1:7860`

## 使用场景
1. **文章配图** - 为文章生成插图、封面图
2. **PPT 配图** - 生成演讲用的视觉素材
3. **概念设计** - 快速可视化创意想法
4. **营销素材** - 生成广告图、海报
5. **产品原型** - 生成产品概念图

## 工作流程

### 1. 需求分析
- 理解图像需求（主题、风格、尺寸、用途）
- 确定生成方式（文生图/图生图）
- 规划提示词策略

### 2. 提示词工程（Prompt Engineering）

#### 提示词结构
```
[主体] + [细节描述] + [风格] + [质量标签] + [技术参数]
```

#### 示例提示词
```
正向提示词（Prompt）:
a professional business person working on laptop, modern office, 
natural lighting, photorealistic, high quality, 8k, detailed

负向提示词（Negative Prompt）:
low quality, blurry, distorted, ugly, bad anatomy, watermark, 
text, signature
```

#### 提示词最佳实践
- **具体明确** - 详细描述想要的内容
- **风格关键词** - photorealistic, anime, oil painting, watercolor
- **质量标签** - high quality, masterpiece, 8k, detailed
- **排除不需要的** - 使用负向提示词排除
- **权重控制** - 使用 `(keyword:1.2)` 增强，`(keyword:0.8)` 减弱

### 3. 参数配置

#### 基础参数
- **Steps（采样步数）** - 20-50，越高质量越好但越慢
- **CFG Scale（提示词相关性）** - 7-12，控制对提示词的遵循程度
- **Sampler（采样器）** - Euler a, DPM++ 2M Karras（推荐）
- **Size（尺寸）** - 512x512, 768x768, 1024x1024

#### 高级参数
- **Seed（随机种子）** - 固定种子可复现结果
- **Batch Size（批次大小）** - 一次生成多张
- **Denoising Strength（去噪强度）** - 图生图时使用，0.3-0.7

### 4. API 调用示例

#### 文生图 API
```python
import requests
import json
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

payload = {
    "prompt": "a beautiful landscape, mountains, sunset, photorealistic",
    "negative_prompt": "low quality, blurry",
    "steps": 30,
    "cfg_scale": 7,
    "width": 768,
    "height": 768,
    "sampler_name": "DPM++ 2M Karras",
    "seed": -1
}

response = requests.post(url, json=payload)
result = response.json()

# 保存图像
image_data = base64.b64decode(result['images'][0])
with open('output.png', 'wb') as f:
    f.write(image_data)
```

#### 图生图 API
```python
url = "http://127.0.0.1:7860/sdapi/v1/img2img"

# 读取参考图
with open('reference.png', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()

payload = {
    "init_images": [image_base64],
    "prompt": "same image but in anime style",
    "negative_prompt": "low quality",
    "steps": 30,
    "denoising_strength": 0.5,
    "cfg_scale": 7
}

response = requests.post(url, json=payload)
```

### 5. 输出交付
- 生成图像文件（PNG 格式）
- 提供生成参数记录
- 说明使用建议

## 常用风格关键词

### 艺术风格
- `photorealistic` - 照片级真实
- `anime style` - 动漫风格
- `oil painting` - 油画
- `watercolor` - 水彩
- `sketch` - 素描
- `digital art` - 数字艺术
- `3d render` - 3D 渲染
- `pixel art` - 像素艺术

### 场景氛围
- `cinematic lighting` - 电影级光效
- `dramatic lighting` - 戏剧性光效
- `soft lighting` - 柔和光线
- `golden hour` - 黄金时刻
- `moody atmosphere` - 情绪化氛围
- `vibrant colors` - 鲜艳色彩

### 质量标签
- `masterpiece` - 杰作
- `best quality` - 最佳质量
- `high resolution` - 高分辨率
- `8k` - 8K 分辨率
- `detailed` - 细节丰富
- `sharp focus` - 清晰对焦

## 最佳实践

1. **迭代优化** - 从简单提示词开始，逐步细化
2. **参考种子** - 保存好的结果的种子值，便于微调
3. **批量测试** - 同时生成多张，选择最佳结果
4. **合理分辨率** - 从 512x512 开始，满意后再放大
5. **负向提示词** - 始终使用负向提示词排除低质量元素

## 常见问题

### 图像质量差
- 增加 Steps（30-50）
- 调整 CFG Scale（7-12）
- 添加质量标签到提示词
- 使用更好的采样器

### 不符合预期
- 细化提示词描述
- 增加权重 `(keyword:1.3)`
- 调整 CFG Scale
- 尝试不同的 Seed

### 生成速度慢
- 减少 Steps
- 降低分辨率
- 使用更快的采样器（Euler a）
- 检查 GPU 性能

## 输出格式

### 标准输出
```markdown
## 生成图像

**提示词**：
[正向提示词]

**负向提示词**：
[负向提示词]

**参数**：
- Steps: 30
- CFG Scale: 7
- Size: 768x768
- Sampler: DPM++ 2M Karras
- Seed: [种子值]

**图像文件**：`[文件路径]`

**使用建议**：
[针对具体用途的建议]
```

## 注意事项
- 需要本地部署 Stable Diffusion WebUI 或使用云服务
- 生成时间取决于硬件性能（GPU）
- 注意版权和使用限制
- 避免生成不当内容
- 保存好的提示词和参数供复用

## 相关资源
- Stable Diffusion WebUI: https://github.com/AUTOMATIC1111/stable-diffusion-webui
- API 文档: http://127.0.0.1:7860/docs
- 提示词指南: https://prompthero.com/
- 模型下载: https://civitai.com/
