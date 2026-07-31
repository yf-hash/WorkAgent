---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
description: 内容多平台一键分发 — 同步发布到微信/知乎/掘金/小红书/抖音/B站/Twitter等30+平台，支持草稿模式
argument-hint: "<filepath|url> [--platforms <平台列表>] [--mode draft|publish] [--tags <标签>] [--title <标题>]"
---

# /sync

将文章或内容一键同步发布到多个内容平台。

> 参考：
> - [wechatsync/Wechatsync](https://github.com/wechatsync/Wechatsync) — MCP集成，29+平台
> - [gitcoffee-os/postbot](https://github.com/gitcoffee-os/postbot) — 30+平台，支持视频/音频

## 用法

```
/sync <文件路径或URL> [选项]
```

## 示例

```bash
# 同步到默认平台（微信+知乎+掘金）
/sync article.md

# 指定平台列表
/sync article.md --platforms wechat,zhihu,juejin,csdn

# 草稿模式（存草稿，人工确认后发布）
/sync article.md --platforms wechat,xiaohongshu --mode draft

# 从 URL 抓取并同步
/sync https://mp.weixin.qq.com/s/xxx --platforms zhihu,juejin

# 添加标签
/sync article.md --platforms juejin,csdn --tags "AI,Claude,写作"

# 同步视频内容
/sync video.mp4 --platforms douyin,bilibili,youtube
```

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--platforms <列表>` | 目标平台，逗号分隔 | 交互选择 |
| `--mode draft` | 存草稿，不直接发布（推荐） | 默认 |
| `--mode publish` | 直接发布（需平台授权） | — |
| `--tags <标签>` | 手动指定标签，逗号分隔 | 自动提取 |
| `--title <标题>` | 覆盖原标题 | 原标题 |
| `--convert-md` | 强制转为 Markdown 再分发 | 自动检测 |

## 支持平台

**中文平台**：`wechat`（微信公众号）`zhihu`（知乎）`juejin`（掘金）`csdn` `xiaohongshu`（小红书）`douyin`（抖音）`bilibili`（B站）`weibo`（微博）`toutiao`（头条）`baijiahao`（百家号）

**国际平台**：`twitter` `linkedin` `medium` `devto` `hashnode` `youtube` `tiktok`

## 执行流程

1. 加载 `skills/media/content-sync/SKILL.md` 完整规范
2. 内容准备（URL抓取 / 文件读取 / 格式转换）
3. 平台适配（字数截断/图片上传/标签提取）
4. 分发到各平台（草稿/直接发布）
5. 输出发布状态报告（各平台链接汇总）

## 依赖配置

```bash
npm install -g @wechatsync/cli
# 首次使用需在浏览器完成各平台登录授权
```

## 相关命令

- `/article-writer` — 先写文章，再用 /sync 分发
- `/humanize --mode scan` → `/humanize --mode soul` — 先去AI味，再用 /sync 分发
- `/polish` — 先润色，再用 /sync 分发
