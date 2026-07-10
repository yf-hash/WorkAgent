---
name: product-deploy
description: >
  产品部署及配置手册生成器（单一职责）— 面向实施工程师的可公开 Word 文档。
  含环境准备、安装步骤、初始化配置、高可用部署、升级回滚、运维监控六大章节。
  仅做部署手册一件事，终端用户操作请用 /product-manual。
user-invocable: true
argument-hint: "<产品名称> [--version v1.0] [--deploy-mode standalone|cluster|container|cloud]"
---

# /product-deploy — 产品部署及配置手册生成器

加载技能：`skills/product-writer-router/SKILL.md` + 结构模板 `templates/product/deploy.md`
配套核验：`skills/doc-auditor/SKILL.md`（生成后自动调用）

## 触发条件
需要为实施工程师 / 运维提供"如何安装、配置、升级、监控产品"的指引文档时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<产品名称>` | 产品全称（必填） | — |
| `--version` | 当前版本号 | `v1.0` |
| `--deploy-mode` | 主要部署模式（单机 / 集群 / 容器 / 云） | `standalone` |
| `--out` | 输出路径 | `./outputs/` |

## 使用示例

```
/product-deploy 数据安全网关 --version v2.0 --deploy-mode cluster
/product-deploy 智能运维平台 --deploy-mode container
```

## 执行流程

```
Step 1: 信息采集
  → 必问：支持的 OS / 数据库 / 中间件 / 浏览器
  → 主要部署模式（单机 / 集群 / 容器 / 云）
  → 资源最小配置 / 推荐配置
  → 关键配置文件清单
  → 升级路径（哪些版本可直接升、哪些要中转）

Step 2: 结构填充
  → 加载 templates/product/deploy.md 中的六章标准结构
  → 命令行操作必须用代码块呈现
  → 关键配置项用表格说明（项 / 默认值 / 说明 / 必填）

Step 3: 命名与版式
  → 文件名：[产品名]【版本号】部署及配置手册_版本号.docx
  → 密级：可公开

Step 4: 14 项自查（doc-auditor 自动调用）
  → 重点核查：C2 完整性（环境准备 / 升级 / 回滚是否覆盖）

Step 5: 输出
  → 部署手册 + 自查报告
  → 建议下一步：兼容性文档（/product-compat）
```

## 与其他命令的边界

| 选择 | 用本命令 | 用其他 |
|------|---------|-------|
| `/product-deploy` vs `/product-manual` | 实施工程师安装 | 终端用户日常使用 |
| `/product-deploy` vs `/product-compat` | 部署步骤 | 兼容平台矩阵 |
