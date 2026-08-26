---
name: marketing-copy
description: >
  产品营销推广内容生成器 — 9 大文体一站式覆盖：公众号软文、小红书种草、
  知乎专业种草、朋友圈文案、短视频脚本、官网/落地页文案、邮件营销（EDM）、
  新闻通稿/PR 稿、客户故事/案例稿。含 ToB / ToC 双语风、AI 安全产品专属话术、
  避雷词清单、CTA 设计、SEO 关键词嵌入。
user-invocable: true
argument-hint: "<产品/主题> [--type wechat|xhs|zhihu|moments|video|landing|edm|pr|case|demo] [--audience tob|toc] [--industry fintech|gov|healthcare|saas|...] [--length short|medium|long] [--cta demo|whitepaper|wechat|purchase]"
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion]
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: one-shot
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /marketing-copy — 产品营销推广内容生成器

加载技能：`skills/writing/marketing-copy/SKILL.md`

## 触发条件
需要生成带营销目的的产品推广内容（区别于个人风格的公众号长文 `/article-writer`、内部资料体系 `/product-*` 系列、客户响应方案 `/proposal`）：
- 给媒体 / 自媒体投放的软文、种草、PR 稿
- 给官网 / 落地页 / 邮件 / 短视频用的文案
- 给销售外推用的客户故事 / 案例稿

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品/主题>` | 产品名 或 推广主题（必填） | — |
| `--type` | 文体类型（见下表，必填） | — |
| `--audience` | 目标读者类型 | `tob` |
| `--industry` | 目标行业 | — |
| `--length` | 篇幅 | `medium` |
| `--cta` | 主 CTA 类型 | — |
| `--platform` | 投放平台（影响调性） | — |
| `--out` | 输出路径 | `./outputs/` |

### 文体类型

| `--type` | 文体 | 适用场景 | 字数 / 时长 |
|----------|------|---------|------------|
| `wechat` | 公众号软文 | 转化引流 / 行业教育 | 2000-4000 字 |
| `xhs` | 小红书种草 | C 端口碑 / IT 决策人种草 | 800-1500 字 |
| `zhihu` | 知乎专业种草 | B 端深度种草 | 2000-5000 字 |
| `moments` | 朋友圈文案 | 创始人 / 销售 IP | 50-200 字 |
| `video` | 短视频脚本 | 抖音 / 视频号 / 小红书 | 60-180 秒 |
| `landing` | 官网 / 落地页文案 | 自然流量 / SEM 落地 | 按页面板块 |
| `edm` | 邮件营销 | 老客唤醒 / 新品发布 | 200-500 字 |
| `pr` | 新闻通稿 / PR 稿 | 媒体投放 / 融资发布 | 800-1500 字 |
| `case` | 客户故事 / 案例稿 | 销售背书 / 案例库 | 1500-3000 字 |
| `demo` | Demo 脚本 | 销售演示 30 分钟标准 | 30 分钟分镜 |

### CTA 类型

| `--cta` | 适用文体 | 设计原则 |
|---------|---------|---------|
| `demo` | wechat / landing / edm / case | 「预约 30 分钟 Demo」（动词 + 价值）|
| `whitepaper` | xhs / zhihu / pr | 「私信「白皮书」获取」 |
| `wechat` | moments / video | 「加微信 / 进群」 |
| `purchase` | landing / edm（C 端）| 「立即购买 / 注册」 |
| `subscribe` | wechat / xhs | 「关注主页 / 公众号」 |

## 使用示例

```
# 公众号软文（B 端教育）
/marketing-copy AI 安全运营平台 --type wechat --audience tob --industry fintech --cta demo

# 小红书种草（B 端 IT 决策人）
/marketing-copy 零信任访问控制 --type xhs --audience tob --industry saas --cta whitepaper

# 官网 Hero + Feature 文案
/marketing-copy 数据安全网关 --type landing --audience tob --industry fintech --cta demo

# 客户故事（媒体投放版本）
/marketing-copy 城商行案例 --type case --industry fintech --length long --cta demo

# 创始人朋友圈
/marketing-copy 新品发布 --type moments --audience tob --cta wechat

# Demo 脚本
/marketing-copy SOC 智能体 --type demo --industry fintech

# 抖音短视频
/marketing-copy 半夜告警没人响应 --type video --audience tob --length short

# PR 稿（融资发布）
/marketing-copy "[公司名] 完成 A 轮融资" --type pr --length medium

# 邮件营销（老客唤醒）
/marketing-copy v2.0 新功能发布 --type edm --audience tob --cta demo
```

## 执行流程

```
Step 1: 信息采集（按 type 分支提问）
  通用必问：
    Q1 一句话产品/活动定位？
    Q2 目标读者画像（行业/角色/痛点）？
    Q3 主 CTA 想让读者做什么？
    Q4 已有素材（数据/客户案例/截图）？

  按 type 追问：
    [wechat/zhihu] 钩子方向：反常识？数据？故事？争议？
    [xhs] 真人感来源：创始人/销售/运营？emoji 风格？
    [video] 视频时长？前 3 秒钩子方案？是否真人入镜？
    [landing] 主关键词 + 长尾关键词？竞品落地页对标？
    [pr] 是否有客户证言？高管金句？指定媒体？
    [case] 客户名 / 数字是否可署名？是否需匿名化？

Step 2: 钩子设计
  → 从钩子库选 3 个候选：
    A. 数据冲击（"我们让 8 小时变成 2 分钟"）
    B. 反常识（"做 SOC，第一件事不是买设备"）
    C. 痛点扎心（"半夜 3 点告警，谁来响应？"）
    D. 故事场景（具体客户场景切入）
  → 给用户 3 选 1，确认后展开

Step 3: 结构填充
  → 加载对应文体的结构框架（marketing-copy SKILL.md）
  → 价值前置：前 3 行 / 3 秒 / 1 屏必须钩住读者
  → 数字 > 形容词：每段至少 1 个具体数字

Step 4: 避雷词扫描
  自动检查并替换：
    ❌ 赋能 → 帮助 / 让 X 能 Y
    ❌ 全栈 → 端到端 / 完整覆盖
    ❌ 闭环 → 完整流程 / 形成回路
    ❌ 在 XX 的时代 → 删除整句
    ❌ 不仅 X，更 X → 拆成两句

Step 5: CTA 强化
  → 动词 + 价值：「预约 30 分钟 Demo」「下载行业白皮书」
  → 一篇内容只有 1 个主 CTA
  → ToB 文体留 1 个备份 CTA（二维码 / 微信号）

Step 6: 四层自检
  ✅ 活人感：无 AI 套话
  ✅ 情感：前 3 行能停下读者
  ✅ 信息：每个数字可查证
  ✅ 结构：CTA 明确，一篇一行动

Step 7: 输出
  → 正文 + 标题 3-5 选 1（ToC / 短视频文体必出多版标题）
  → 替换记录（避雷词替换前后对照）
  → 平台投放建议（最佳时段 / 配图要求 / 互动话术）
```

## 与其他命令的边界

| 选择 | 用前者 | 用后者 |
|------|-------|-------|
| `/marketing-copy` vs `/article-writer` | 带营销目的的推广（CTA 明确）| 公众号长文（个人风格 / 观点输出）|
| `/marketing-copy --type case` vs `/product-case` | 媒体外推 / 公众号发版本 | 官网案例库 / 销售口袋资料 |
| `/marketing-copy` vs `/proposal` | 标准化推广物料 | 一对一客户响应方案 |
| `/marketing-copy --type video` vs `/pdf2video` | 写视频脚本 | 把已有内容渲染成视频 |
| `/marketing-copy --type xhs` vs `/sync` | 写小红书内容 | 把已有内容多平台分发 |
