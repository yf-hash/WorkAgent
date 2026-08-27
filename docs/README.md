# docs — 元文档

WorkAgent 三条端到端流水线的元文档目录。

| 文档 | 用途 |
|---|---|
| [PM_HARNESS.md](PM_HARNESS.md) | PM 端到端 6 模块流水线总览（内部产品：M2 澄清 → M3 方案 → M4 原型 → M5 PRD → M6 技术规格 → M7 归档）+ 竞品分析工程化横向能力 |
| [SA_HARNESS.md](SA_HARNESS.md) | SA 端到端 7 模块流水线总览（对外售前：M1 输入 → M2 调研 → M3 方案拆解 → M4 总体方案 → M5 POC/实施/RFP → M6 报价 → M7 归档） |
| [CONTENT_HARNESS.md](CONTENT_HARNESS.md) | Content 端到端 5 模块流水线总览（内容创作：M1 网关 → M2 素材 → M3 生成 → M4 校验 → M5 归档 + 多格式导出，八大文体） |

顶层框架文档 [`../HARNESS_FRAMEWORK.md`](../HARNESS_FRAMEWORK.md) 保留在仓库根，作为 harness 五能力分层锚点。

## 何时用 PM / SA / Content？

| 输入 | 用 |
|---|---|
| 内部产品经理接收的需求想法 / 用户反馈 | `/pm` 或 `/pm-pipeline` |
| 竞品分析 / 差异化定位 | `/pm-competitive` |
| 销售转述的一句话客户信息 | `/sa` 或 `/sa-pipeline` |
| RFP 招标文件 | `/sa-pipeline --stage-5 rfp` |
| 客户 POC 立项 | `/sa-pipeline --stage-5 poc` |
| 写产品推广文 / 白皮书 / PR 稿 / PPT / 推文 / 科普文 | `/content` |
| 基于 PM/SA 项目出对外物料（自动关联素材） | `/content --project {path} --writeback` |
| 内部产品 PRD | `/prd --mode full` |
| 客户方案汇报 | `/sa-quote`（含 PPT 大纲 + 话术）or `/content --style ppt` |

## 跨流水线协作

```
                        WorkAgent
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
      /pm                  /sa                /content
    (内部 PRD)           (对外方案)           (内容传播)
       │                    │                    │
       └───────素材──────► /content ◄──────素材──┘
                            │
                            ▼
                   产出可回写到 PM/SA
                   {project}/_content/
```

**典型协作**：
1. PM 项目上线 → Content 出 PR 稿 + 推广文 → 回写到 PM 项目
2. SA 中标 → Content 出解决方案白皮书 → 回写到 SA 项目
3. PM 竞品分析 → 输出作为 Content 差异化推广文的输入
4. 一个项目同时拥有 PRD、规格书、方案、对外宣传物料

详见 [`../README.md`](../README.md)。
