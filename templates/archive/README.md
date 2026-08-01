# templates/archive — 已归档模板

以下模板在 v3.1 templates 索引检查中被标记为"无引用者"，且经确认仓库内没有对应的 command / skill 消费它们，故迁移到本目录归档。

| 模板 | 归档原因 | 恢复方式 |
|---|---|---|
| `brd-template.md` | 无 `/brd` 命令，无 skill 消费 | 如需恢复，mv 回 `../` |
| `mrd-template.md` | 无 `/mrd` 命令，无 skill 消费 | 同上 |
| `requirement-pool-template.md` | 无对应命令 / skill | 同上 |

**归档标准**：v3.1 起，templates/ 顶层只放"至少 1 个 command/skill/agent 引用"的模板。孤儿模板迁到本目录。

**保留原因**：Git 保留完整历史即可，但保留文件方便未来快速恢复。如果 6 个月后仍无使用，考虑彻底删除。

**v3.0 之前的引用**：以下模板在 v3.0 之前可能被文档提到过但从未被程序引用：
- BRD / MRD 是传统 PM 文档类型；WorkAgent 通过 `/prd --mode` 12 种模式覆盖了实际需求，未单独实现 BRD/MRD 生成
- Requirement Pool 是需求池概念；实际需求管理走 Linear / GitHub Issues 等外部工具
