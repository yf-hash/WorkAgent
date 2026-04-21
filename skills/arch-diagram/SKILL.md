---
name: arch-diagram
description: >
  云架构图生成技能，基于 mingrammer/diagrams（Python + Graphviz），支持 AWS/GCP/Azure/K8s/
  阿里云/本地部署节点库，从自然语言描述或 IaC 文件生成标准云架构图，输出 Python 代码 +
  渲染 PNG，支持 Cluster 分组、Edge 标签、多云混合、自定义节点图标
user-invocable: false
effort: medium
---

# arch-diagram — 云架构图生成技能

## 能力范围

基于 [mingrammer/diagrams](https://github.com/mingrammer/diagrams) 库，将架构描述转为
标准云图标图表。支持 AWS、GCP、Azure、K8s、阿里云、本地部署六大节点库，
以及 Generic（通用）和 Custom（自定义图标）节点。

---

## 节点库速查

### AWS（diagrams.aws.*）
```python
from diagrams.aws.compute import EC2, Lambda, ECS, EKS, Fargate, Batch
from diagrams.aws.database import RDS, Aurora, DynamoDB, ElastiCache, Redshift
from diagrams.aws.network import CloudFront, ALB, NLB, APIGateway, VPC, Route53
from diagrams.aws.storage import S3, EFS, EBS, Glacier
from diagrams.aws.security import WAF, Shield, Cognito, IAM, KMS
from diagrams.aws.analytics import Kinesis, Glue, Athena, EMR, QuickSight
from diagrams.aws.integration import SQS, SNS, EventBridge, StepFunctions
from diagrams.aws.management import Cloudwatch, CloudTrail, Config, SSM
from diagrams.aws.ml import Sagemaker, Rekognition, Comprehend
```

### GCP（diagrams.gcp.*）
```python
from diagrams.gcp.compute import GCE, GKE, CloudRun, AppEngine, Functions
from diagrams.gcp.database import SQL, Bigtable, Firestore, Spanner, Memorystore
from diagrams.gcp.network import LoadBalancing, CDN, DNS, VPC
from diagrams.gcp.storage import GCS, Filestore
from diagrams.gcp.analytics import BigQuery, Dataflow, Dataproc, PubSub
from diagrams.gcp.ml import AIPlatform, AutoML, NaturalLanguageAPI
```

### Azure（diagrams.azure.*）
```python
from diagrams.azure.compute import VM, AKS, FunctionApps, ContainerInstances
from diagrams.azure.database import SQLDatabases, CosmosDb, CacheForRedis
from diagrams.azure.network import ApplicationGateway, CDNProfiles, LoadBalancers
from diagrams.azure.storage import BlobStorage, DataLakeStorage
from diagrams.azure.security import KeyVaults, ActiveDirectory
from diagrams.azure.analytics import EventHubs, StreamAnalytics, Databricks
```

### Kubernetes（diagrams.k8s.*）
```python
from diagrams.k8s.compute import Pod, Deployment, StatefulSet, DaemonSet, Job
from diagrams.k8s.network import Service, Ingress, NetworkPolicy
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.k8s.rbac import ClusterRole, ServiceAccount
from diagrams.k8s.infra import Node, Namespace
```

### 阿里云（diagrams.alibabacloud.*）
```python
from diagrams.alibabacloud.compute import ECS, FunctionCompute, ContainerService
from diagrams.alibabacloud.database import RDS, PolarDB, Tablestore
from diagrams.alibabacloud.network import SLB, CDN, VPC, APIGateway
from diagrams.alibabacloud.storage import OSS, NAS
```

### 本地部署（diagrams.onprem.*）
```python
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL, PostgreSQL, MongoDB, Redis, Cassandra
from diagrams.onprem.network import Nginx, HAProxy, Traefik, Istio
from diagrams.onprem.monitoring import Grafana, Prometheus, Datadog
from diagrams.onprem.queue import Kafka, RabbitMQ, Celery
from diagrams.onprem.container import Docker, K3S
from diagrams.onprem.vcs import Github, Gitlab
from diagrams.onprem.ci import Jenkins, GithubActions, CircleCI
```

---

## 代码模板

### 基础三层架构
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB, CloudFront

with Diagram("三层 Web 架构", direction="TB", filename="arch_output"):
    cdn = CloudFront("CDN")
    with Cluster("VPC"):
        lb = ALB("负载均衡")
        with Cluster("应用层"):
            web = [EC2("app-1"), EC2("app-2")]
        with Cluster("数据层"):
            db = RDS("PostgreSQL")
    cdn >> lb >> web >> db
```

### K8s 微服务
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PVC

with Diagram("K8s 微服务", direction="LR", filename="k8s_arch"):
    ingress = Ingress("Ingress")
    with Cluster("frontend"):
        fe_svc = Service("fe-svc")
        fe_pod = Deployment("frontend")
    with Cluster("backend"):
        be_svc = Service("be-svc")
        be_pod = Deployment("backend")
    with Cluster("storage"):
        pvc = PVC("data-pvc")
    ingress >> fe_svc >> fe_pod >> be_svc >> be_pod >> pvc
```

### 多云混合
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC
from diagrams.azure.network import VirtualNetworks
from diagrams.onprem.network import Firewall

with Diagram("多云混合架构", direction="LR", filename="multi_cloud"):
    with Cluster("AWS"):
        aws_vpc = VPC("AWS VPC")
    with Cluster("Azure"):
        az_vnet = VirtualNetworks("Azure VNet")
    fw = Firewall("本地防火墙")
    aws_vpc - Edge(label="VPN") - fw - Edge(label="ExpressRoute") - az_vnet
```

---

## 自然语言解析规则

| 关键词 | 映射节点 |
|--------|---------|
| `用户/客户端/浏览器` | Generic User / Client |
| `CDN/内容分发` | CloudFront / CDN |
| `负载均衡/LB/ALB` | ALB / LoadBalancing |
| `API网关` | APIGateway |
| `服务/微服务` | EC2 / GCE / Pod |
| `数据库/DB/MySQL/PG` | RDS / SQL / MySQL |
| `缓存/Redis` | ElastiCache / Redis |
| `队列/MQ/Kafka` | SQS / Kafka |
| `对象存储/OSS/S3` | S3 / GCS / OSS |
| `监控/Prometheus` | Cloudwatch / Prometheus |
| `→/->` | Edge（单向） |
| `↔/<->` | Edge（双向） |
| `..>` | Edge(style="dashed")（异步） |

---

## 图表样式配置

```python
# 默认样式
graph_attr = {"fontsize": "14", "bgcolor": "white"}

# 深色样式
graph_attr = {"fontsize": "14", "bgcolor": "#1a1a2e", "fontcolor": "white"}

# 简约样式
graph_attr = {"fontsize": "12", "bgcolor": "transparent", "pad": "0.5"}
```

---

## 渲染执行

```bash
# 安装依赖
pip install diagrams
# macOS: brew install graphviz
# Linux: apt-get install graphviz
# Windows: winget install graphviz

# 执行渲染
python arch_output.py
# 生成 arch_output.png
```

---

## 与其他技能的协同

- `visio-builder`：将生成的 PNG 嵌入 Visio 文档
- `diagram-suite`：arch-diagram 作为 `arch` 引擎被路由调用
- `html-chart`：复杂交互图表的补充方案
