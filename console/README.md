# WorkAgent Console · 需求与产物工作台

> 本目录是 WorkAgent 仓库中的 Web 控制台（`console/`）。仓库根目录存放 harness
> 资产（commands / skills / agents / roles / docs），控制台负责把这些能力交付给售前、
> 产品与内容团队使用。

面向**售前（SA）**、**产品（PM）**与**内容（Content）**团队的 AI 工作台。
对话即入口：先说清楚要做什么，系统自动登记需求，再由所选智能体完成整理与交付。

- 售前：方案 / PPT / 标书 → **沉淀到产物库**，保留地址与版本，可回溯
- 产品：开发需求 → **推送 Linear**，PRD / 原型 / 技术交底书同样归档
- 内容：白皮书 / PR / 文案 → 沉淀到产物库并回写关联需求

前端为单页应用（原生 HTML/CSS/JS，无构建），后端为 Python 标准库
（`http.server` + `sqlite3`），**零第三方依赖**，带登录鉴权与 Docker 部署。

## 快速开始

### 本地运行

```bash
cd console            # 若在仓库根目录
python server/app.py
# 或双击 run.bat（Windows）
```

打开 <http://127.0.0.1:8765/>，使用初始账号登录：

```
用户名：admin
密码：  admin123
```

首次登录后请到「账户设置」修改密码。

### Docker 部署

```bash
cd console                # docker-compose 以仓库根为构建上下文
cp .env.example .env      # 按需修改管理员账号与端口
docker compose up -d --build
```

也可以直接带上下文构建：

```bash
docker build -f console/Dockerfile -t workagent-console .
docker run -d -p 8765:8765 -v workagent-data:/app/data workagent-console
```

数据（SQLite + 产物文件）挂载在 `workagent-data` 卷，容器重建不丢数据。

### 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `WORKAGENT_HOST` | `0.0.0.0` | 监听地址 |
| `WORKAGENT_PORT` | `8765` | 服务端口 |
| `WORKAGENT_ADMIN_USER` | `admin` | 首次启动创建的管理员用户名 |
| `WORKAGENT_ADMIN_PASSWORD` | `admin123` | 首次启动创建的管理员密码 |
| `WORKAGENT_SESSION_HOURS` | `72` | 登录会话有效期（小时） |
| `WORKAGENT_RESET_ADMIN` | — | 设为 `1` 时按上面两个变量重置管理员密码并清空所有会话 |

忘记密码时：

```bash
WORKAGENT_ADMIN_PASSWORD=新密码 WORKAGENT_RESET_ADMIN=1 python server/app.py
```

启动一次后去掉 `WORKAGENT_RESET_ADMIN` 再重启即可。

## 页面说明

| 页面 | 说明 |
|---|---|
| 登录 | 用户名 + 密码；会话保存在本地，过期回到登录页 |
| 数据看板 | KPI、需求与沉淀趋势、产物类型分布、活跃需求、任务双列预览、最近产物 |
| AI 对话 | 顶部选择执行智能体 `/sa` `/pm` `/content`；第一条消息自动登记需求 |
| 任务列表 | 售前 / 产品双列，5 步进度，重试 / 暂停 / 恢复 |
| 产物库 | 生成、下载、预览正文、版本历史；按角色与类型筛选 |
| 工作待办 | 增删改查、按组筛选、完成率统计 |
| Skill 集成 | 上传 Markdown 新增能力，或合并到仓库已有的 27 个 Skill |
| 模型配置 | 模型选择、温度、路由策略，保存到后端 |
| 审计日志 | 登录、需求、产物、Linear 推送、Skill 上传/合并、配置变更全部留痕 |
| 系统集成 | API / 数据库 / 存储 / Linear / 模型服务状态与端点清单 |
| 账户设置 | 修改密码、查看账号信息与部署说明 |

## Skill 能力扩展

在「Skill 集成」页上传 `.md` 文件：

1. **作为新能力添加**：从文件名或 `# 标题` 生成 slug，进入能力库
2. **合并到已有 Skill**：正文追加到目标 Skill 的能力文档，版本号自增，并记录合并历史

支持 YAML frontmatter：

```markdown
---
name: 威胁建模
description: 对架构做 STRIDE 威胁建模并输出缓解建议
---

# 威胁建模

## 输入
- 架构图或组件清单

## 输出
- 威胁清单与缓解措施
```

单个文件上限 2MB。每个 Skill 可点「能力内容」查看当前正文与合并记录。

## 后端接口

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/api/health` | 健康检查（无需登录） |
| POST | `/api/auth/login` | 登录，返回 Bearer token |
| GET | `/api/auth/me` | 当前用户 |
| POST | `/api/auth/logout` | 退出登录 |
| POST | `/api/auth/password` | 修改密码 |
| GET | `/api/bootstrap` | 全量初始化数据 |
| GET | `/api/stats` | 运行统计 |
| GET | `/api/search?q=` | 全局搜索（需求 / 产物 / 任务） |
| GET | `/api/audit?limit=` | 审计日志 |
| GET / POST | `/api/requirements` | 需求列表 / 新建（对话自动调用） |
| GET / PATCH / DELETE | `/api/requirements/{id}` | 读取 / 编辑 / 删除 |
| POST | `/api/requirements/{id}/element` | 保存单项要素 |
| POST | `/api/requirements/{id}/export` | 导出交付包 JSON |
| GET / POST | `/api/artifacts` | 产物列表 / 生成并落盘 |
| GET | `/api/artifacts/{id}/content` | 读取产物正文 |
| GET / PATCH / DELETE | `/api/todos[/{id}]` | 待办增删改 |
| POST | `/api/tasks/{id}/{retry\|pause\|resume\|cancel}` | 任务控制 |
| GET / PATCH | `/api/skills[/{slug}]` | Skill 列表 / 启停 |
| GET | `/api/skills/{slug}/content` | Skill 能力正文与合并记录 |
| POST | `/api/skills/upload` | 上传 Markdown（新增或合并） |
| GET / PUT | `/api/config` | 读取 / 保存模型配置 |
| POST | `/api/mcp/linear/push` | Linear 推送（售前请求返回 400） |
| GET | `/download/{path}` | 下载产物文件 |

除 `/api/health` 与 `/api/auth/*` 外，所有接口都需要
`Authorization: Bearer <token>`。

## 目录结构

```
console/
├── server/
│   ├── app.py            # API、鉴权、静态文件、任务推进器
│   ├── db.py             # 表结构、种子数据、密码哈希、文件落盘
│   └── test_api.py       # 后端回归测试（含鉴权与 Skill 上传）
├── web/
│   └── index.html        # 前端单页（API 适配 + 演示降级）
├── data/                 # 运行期生成，已 gitignore
│   ├── workagent.db
│   └── output/{sa|pm|content}/{REQ}/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── run.bat / run.ps1
└── README.md
```

## 测试

```bash
python server/app.py           # 先启动服务
python server/test_api.py      # 26+ 项断言：鉴权、需求、产物、Skill、审计
```

## 设计约定

- **需求只在对话中产生**：不提供逐项填写表单，避免两套入口
- **售前不走 Linear**：`role=sa` 的推送请求由服务端直接拒绝
- **产物真实落盘**：生成即写入 `data/output/`，可下载、可预览正文
- **能力可扩展**：上传 Markdown 即可新增或补充 Skill，版本自增
- **审计不可省略**：登录与所有写操作都写入 `audit` 表
- **默认安全**：未登录访问任何业务接口返回 401
