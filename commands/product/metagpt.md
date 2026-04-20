---
name: metagpt
description: 使用 MetaGPT 多 Agent 软件公司模拟，从需求到代码一键生成完整项目（PRD→架构设计→代码→测试）
user-invocable: true
argument-hint: "<项目需求描述> [--roles pm|architect|engineer|qa] [--output <输出目录>] [--mode full|prd|design|code|review]"
---

# /metagpt — 多 Agent 软件项目生成（MetaGPT）

加载技能：`skills/metagpt/SKILL.md`

**前置条件**：需要安装 MetaGPT（`pip install metagpt`）并配置 LLM API Key

## 触发条件
用户需要快速生成软件项目原型、产品需求文档、系统架构设计、完整代码实现，或对现有项目进行代码审查和文档生成。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<需求描述>` | 项目需求（越详细越好，必填） | — |
| `--roles` | 参与的角色（逗号分隔） | `pm,architect,engineer` |
| `--output` | 输出目录 | `./workspace` |
| `--mode` | 执行模式 | `full` |

### 执行模式说明
| `--mode` 值 | 执行内容 | 适用场景 |
|------------|---------|---------|
| `full` | PRD → 架构 → 代码 → 测试 | 完整项目生成 |
| `prd` | 仅生成产品需求文档 | 需求文档化 |
| `design` | PRD + 架构设计 | 技术方案评审 |
| `code` | 仅代码生成（需提供设计文档） | 快速实现 |
| `review` | 代码审查 | 质量检查 |

### 角色说明
| 角色 | 职责 | 输出 |
|------|------|------|
| `pm` | 产品经理 | PRD、功能列表 |
| `architect` | 架构师 | 系统设计、数据模型、API 设计 |
| `pm_mgr` | 项目经理 | 任务分解、工作计划 |
| `engineer` | 工程师 | 代码实现 |
| `qa` | 测试工程师 | 测试用例、测试代码 |

## 执行流程

```
Step 1: 需求分析（Product Manager）
  → 解析用户输入的需求描述
  → 生成标准化 PRD 文档
  → 定义功能列表和优先级

Step 2: 系统设计（Architect）
  → 设计系统架构（分层/微服务/模块化）
  → 定义数据模型和数据库 Schema
  → 设计 RESTful API 接口规范
  → 选择技术栈

Step 3: 代码实现（Engineer）
  → 按架构设计生成代码文件
  → 实现业务逻辑
  → 生成配置文件和 Dockerfile

Step 4: 测试生成（QA Engineer，按需）
  → 生成单元测试和集成测试
  → 覆盖主要业务场景

Step 5: 文档生成
  → 生成 README.md
  → 生成 API 文档
  → 生成部署说明
```

## 输出结构

```
workspace/
├── docs/
│   ├── prd.md              # 产品需求文档
│   ├── system_design.md    # 系统架构设计
│   └── api.md              # API 文档
├── src/
│   ├── frontend/           # 前端代码（如有）
│   ├── backend/            # 后端代码
│   └── database/           # 数据库初始化脚本
├── tests/                  # 测试代码
├── docker-compose.yml      # 容器编排（如适用）
└── README.md               # 项目说明
```

## 需求描述最佳实践

```
✅ 好的需求描述示例：

开发一个在线书店 Web 应用：
1. 用户功能：注册/登录、浏览图书、搜索、购物车、下单、查看订单
2. 管理功能：图书管理（增删改查）、订单管理、用户管理
3. 技术栈：Vue 3 + Spring Boot + MySQL
4. 认证：JWT Token
5. 支付：接入支付宝沙箱
6. 部署：Docker 容器化

❌ 不好的需求描述：
做一个网站
```

## 输出格式

```markdown
## 项目生成完成

**项目**：[项目名称]
**技术栈**：[前端框架] + [后端框架] + [数据库]

**生成内容**：
| 文件 | 说明 |
|------|------|
| `docs/prd.md` | 产品需求文档 |
| `docs/system_design.md` | 系统架构设计 |
| `src/backend/` | 后端代码（[N] 个文件） |
| `src/frontend/` | 前端代码（[N] 个文件） |
| `tests/` | 测试代码（[N] 个测试用例） |

**快速启动**：
```bash
# 安装依赖
npm install && pip install -r requirements.txt

# 启动开发环境
docker-compose up -d

# 运行测试
npm test && pytest
```

**架构亮点**：
- [设计决策 1]
- [设计决策 2]

**下一步建议**：
1. 检查并调整环境变量配置
2. 运行测试验证功能
3. 根据实际需求调整业务逻辑
```

## 使用示例

```
/metagpt 开发一个待办事项管理 API，支持增删改查和状态筛选，使用 Python FastAPI + SQLite
/metagpt 开发一个博客系统 --roles pm,architect --mode design
/metagpt 仅生成 PRD：一个企业内部知识库系统 --mode prd
/metagpt 对 src/backend/ 目录进行代码审查 --mode review
/metagpt 在现有博客项目基础上添加评论功能 --output ./workspace/blog
```

## 注意事项
- 需求描述越详细，生成质量越高
- 大型项目（10+ 模块）建议先用 `--mode prd` 确认需求再全量生成
- 生成的代码需要人工审查，特别是安全相关逻辑
- API Key 成本：完整项目生成约消耗 10k-50k tokens
