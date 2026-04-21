---
name: arch-diagram
description: >
  云架构图生成命令，基于 mingrammer/diagrams（Python + Graphviz），支持 AWS/GCP/Azure/
  K8s/阿里云/本地部署多云架构可视化，输出 Python 代码 + 渲染 PNG，适合基础设施文档、
  架构评审和 IaC 可视化，支持自动安装依赖和多云混合架构
user-invocable: true
argument-hint: "<架构描述> [--provider aws|gcp|azure|k8s|alibaba|onprem|multi] [--mode generate|code|render|update] [--style default|dark|minimal] [--output png|pdf|code] [--direction TB|LR|BT|RL]"
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# /arch-diagram — 云架构图生成

加载技能：`skills/arch-diagram/SKILL.md`

## 触发条件
需要绘制云基础设施架构图、可视化 IaC 代码结构、生成多云混合架构图、
为架构评审文档配图，或将自然语言描述的系统架构转为标准云图标图表时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<架构描述>` | 自然语言描述 或 已有 Python/YAML/Terraform 文件路径（必填） | — |
| `--provider` | 云服务商 | `auto` |
| `--mode` | 执行模式 | `generate` |
| `--style` | 图表样式 | `default` |
| `--output` | 输出格式 | `png` |
| `--direction` | 布局方向 | `TB` |

### 云服务商（--provider）
| 值 | 服务商 | 支持的节点库 |
|----|--------|------------|
| `aws` | Amazon Web Services | EC2/S3/RDS/Lambda/VPC/EKS/CloudFront 等 200+ |
| `gcp` | Google Cloud Platform | GCE/GCS/BigQuery/GKE/Cloud Run 等 |
| `azure` | Microsoft Azure | VM/Blob/AKS/Functions/CosmosDB 等 |
| `k8s` | Kubernetes | Pod/Deployment/Service/Ingress/PV 等 |
| `alibaba` | 阿里云 | ECS/OSS/RDS/ACK/SLB 等 |
| `onprem` | 本地部署 | 服务器/数据库/负载均衡/防火墙 等 |
| `multi` | 多云混合 | 自动混合多个服务商节点 |
| `auto` | 自动识别 | 从描述中推断服务商 |

### 执行模式（--mode）
| 值 | 说明 |
|----|------|
| `generate` | 生成 Python 代码 + 自动渲染 PNG |
| `code` | 仅输出 diagrams Python 代码（不渲染） |
| `render` | 渲染已有 .py 文件 |
| `update` | 读取已有架构图代码并按描述修改 |

### 布局方向（--direction）
| 值 | 说明 |
|----|------|
| `TB` | 从上到下（默认，适合层次架构） |
| `LR` | 从左到右（适合流水线/数据流） |
| `BT` | 从下到上 |
| `RL` | 从右到左 |

---

## 执行流程

```
Step 1: 依赖检查
  → 检测 diagrams 库：pip show diagrams
  → 检测 Graphviz：dot -V
  → 缺失时提示安装命令

Step 2: 架构解析
  → 识别服务商（--provider auto 时从描述推断）
  → 提取组件列表：计算/存储/网络/安全/监控
  → 识别组件间关系：单向/双向/虚线（异步）
  → 识别分组：VPC/Cluster/Region/Zone

Step 3: 代码生成
  → 导入对应 provider 的节点类
  → 用 Cluster/Group 定义分组边界
  → 用 Edge/>> 定义连接关系和标签
  → 设置 graph_attr（方向/字体/背景色）

Step 4: 渲染输出
  → generate/render 模式：执行 python arch.py 生成 PNG
  → code 模式：输出代码块 + 渲染说明
  → 输出文件路径和节点统计
```

---

## 安装依赖

```bash
# 安装 diagrams 库
pip install diagrams

# 安装 Graphviz（渲染引擎）
# macOS
brew install graphviz
# Ubuntu/Debian
apt-get install graphviz
# Windows
winget install graphviz
```

---

## 使用示例

```bash
# AWS 三层 Web 架构
/arch-diagram 用户→CloudFront→ALB→EC2集群→RDS+ElastiCache --provider aws

# K8s 微服务架构
/arch-diagram Ingress→Service→Pod(前端/后端/Worker)→PVC --provider k8s

# GCP 数据管道
/arch-diagram Pub/Sub→Dataflow→BigQuery→Looker --provider gcp --direction LR

# 多云混合架构
/arch-diagram AWS VPC + Azure AD + 本地数据中心通过 VPN 互联 --provider multi

# 仅生成代码不渲染
/arch-diagram 微服务架构：API网关→认证/订单/支付服务→MySQL --mode code

# 从 Terraform 文件生成架构图
/arch-diagram main.tf --provider aws --mode generate

# 更新已有架构图
/arch-diagram arch.py --mode update 在现有架构中增加 WAF 和 CloudWatch 监控

# 阿里云架构
/arch-diagram SLB→ECS集群→RDS→OSS --provider alibaba --style dark
```

---

## 输出示例

```python
# 生成的 diagrams 代码示例
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import CloudFront, ALB, VPC

with Diagram("Web Architecture", direction="TB", filename="arch"):
    cdn = CloudFront("CDN")
    with Cluster("VPC"):
        lb = ALB("Load Balancer")
        with Cluster("App Tier"):
            web = [EC2("web-1"), EC2("web-2")]
        with Cluster("Data Tier"):
            db = RDS("PostgreSQL")
            cache = ElastiCache("Redis")
    cdn >> lb >> web >> db
    web >> cache
```

---

## 与其他命令的协同

```
/arch-diagram → /diagram       → 轻量架构图用 PlantUML/Mermaid
/arch-diagram → /visio         → 导出为 Visio 格式供企业使用
/arch-diagram → /illustrate    → 将架构图嵌入技术文章
/arch-diagram → /prd           → 为 PRD 技术方案章节配架构图
@diagram-architect             → 统一图表编排，自动选择最优工具
```
