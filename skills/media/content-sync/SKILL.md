---
name: content-sync
description: >
  内容多平台分发技能。一键将文章/笔记/图文同步发布到30+内容平台，支持微信公众号、知乎、
  掘金、小红书、抖音、B站、Twitter/X、LinkedIn等。支持 Wechatsync MCP 集成和 PostBot SDK。
  触发关键词：内容分发、多平台发布、同步发布、一键发布、wechatsync、postbot、内容同步、跨平台发布
user-invocable: false
effort: medium
argument-hint: "<filepath|url> [--platforms <平台列表>] [--mode draft|publish] [--convert-md]"
harness:
  execute:
    preset: media-heavy
  constrain:
    profile: shell-restricted
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: medium
---

# 内容多平台分发技能

> 参考：
> - [wechatsync/Wechatsync](https://github.com/wechatsync/Wechatsync) — MCP集成 + JS SDK，支持29+平台
> - [gitcoffee-os/postbot](https://github.com/gitcoffee-os/postbot) — 30+平台，支持视频/音频/图文

## 核心能力

- 文章/图文/视频/音频多格式分发
- 30+ 平台一键同步
- Markdown → 平台富文本自动转换
- 图片自动上传至各平台图床
- 草稿模式（先存草稿，人工确认后发布）
- Wechatsync MCP 集成（Claude Desktop/Code 直接调用）

---

## 支持平台

### 中文平台
| 平台 | 内容类型 | 集成方式 |
|------|---------|---------|
| 微信公众号 | 图文 | Wechatsync |
| 知乎 | 文章/回答 | Wechatsync |
| 掘金 | 技术文章 | Wechatsync |
| CSDN | 技术博客 | Wechatsync / COSE |
| 小红书 | 图文/笔记 | PostBot |
| 抖音 | 视频/图文 | PostBot |
| B站 | 视频/专栏 | PostBot |
| 微博 | 短文/图片 | PostBot |
| 头条号 | 文章 | PostBot |
| 百家号 | 文章 | PostBot |

### 国际平台
| 平台 | 内容类型 | 集成方式 |
|------|---------|---------|
| Twitter/X | 推文/长文 | PostBot |
| LinkedIn | 文章/动态 | PostBot |
| Medium | 文章 | Wechatsync |
| Dev.to | 技术文章 | COSE |
| Hashnode | 技术博客 | PostBot |
| YouTube | 视频 | PostBot |
| TikTok | 短视频 | PostBot |

---

## 两种集成路径

### 路径一：Wechatsync（推荐，有MCP集成）

```
文章 URL 或 Markdown 文件
  → Wechatsync JS SDK
  → 网页内容 → Markdown 转换
  → 图片自动处理（上传至各平台图床）
  → 同步至目标平台（草稿/直接发布）
```

MCP 工具调用（Claude Desktop/Code）：
```
wechatsync_sync_article(url, platforms, mode)
wechatsync_get_accounts()
wechatsync_check_status(task_id)
```

### 路径二：PostBot（更广平台覆盖）

```
内容（文字/图片/视频/音频）
  → PostBot 本地服务
  → 浏览器自动化
  → 多平台并行发布
```

---

## 执行流程

```
Step 1: 内容准备
  URL → 抓取网页内容 → Markdown 转换
  .md 文件 → 直接读取
  .docx/.pdf → 转换为 Markdown

Step 2: 内容适配
  → 检测各平台字数限制（微博140字/知乎无限制等）
  → 长文自动截断 + 添加"阅读原文"链接
  → 图片上传至各平台图床
  → 标签/话题自动提取

Step 3: 平台发布
  → 草稿模式：存入各平台草稿箱，人工审核后发布
  → 直接发布：立即发布（需平台授权）

Step 4: 状态报告
  → 各平台发布状态（成功/失败/草稿）
  → 发布链接汇总
```

---

## 内容适配规则

```
微信公众号：
  - 保留完整 Markdown 格式
  - 图片必须上传至微信图床
  - 不支持外链，自动转为脚注

知乎/掘金：
  - 支持 Markdown 直接粘贴
  - 代码块保留高亮

小红书：
  - 纯文字 + 图片组合
  - 自动提取关键词作为话题标签
  - 字数建议 300-1000 字

Twitter/X：
  - 超过280字自动拆分为线程
  - 图片最多4张
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--platforms <列表>` | 目标平台，逗号分隔（`wechat,zhihu,juejin`） | 交互选择 |
| `--mode draft` | 存草稿，不直接发布 | 默认 |
| `--mode publish` | 直接发布（需平台授权） | — |
| `--convert-md` | 强制将内容转为 Markdown 再分发 | 自动检测 |
| `--tags <标签>` | 手动指定标签/话题 | 自动提取 |
| `--title <标题>` | 覆盖原标题 | 原标题 |

---

## 依赖配置

```bash
# Wechatsync CLI
npm install -g @wechatsync/cli

# PostBot（本地服务）
git clone https://github.com/gitcoffee-os/postbot
npm install && npm start
```

平台账号授权：首次使用需在浏览器中完成各平台登录授权，凭证本地存储，不上传云端。
