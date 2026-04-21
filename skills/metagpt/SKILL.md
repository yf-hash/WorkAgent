---
name: metagpt
description: >
  MetaGPT 多 Agent 软件开发框架知识库。触发词：MetaGPT、多Agent协作、软件公司模拟、
  自动软件开发、PRD转代码、多角色Agent、AI软件工程。
user-invocable: false
effort: high
---

# MetaGPT - Multi-Agent Collaboration Framework

## 概述
MetaGPT 是一个多 Agent 协作框架，模拟软件公司的角色分工，通过多个 AI Agent 协作完成复杂的软件开发任务。

## 核心能力
- **多角色协作** - 产品经理、架构师、工程师、QA 等角色协同工作
- **需求分析** - 将用户需求转换为详细的产品需求文档（PRD）
- **系统设计** - 生成系统架构设计和数据结构
- **代码生成** - 自动生成完整的项目代码
- **测试用例** - 生成测试用例和测试代码
- **文档生成** - 生成技术文档和 API 文档

## 角色体系

### 1. Product Manager（产品经理）
- 分析用户需求
- 编写产品需求文档（PRD）
- 定义功能优先级
- 规划产品路线图

### 2. Architect（架构师）
- 设计系统架构
- 选择技术栈
- 定义数据模型
- 设计 API 接口

### 3. Project Manager（项目经理）
- 任务分解
- 资源分配
- 进度跟踪
- 风险管理

### 4. Engineer（工程师）
- 编写代码实现
- 代码审查
- 性能优化
- Bug 修复

### 5. QA Engineer（测试工程师）
- 编写测试用例
- 执行测试
- 缺陷跟踪
- 质量保证

## 前置要求

### 安装 MetaGPT
```bash
# 安装
pip install metagpt

# 或从源码安装
git clone https://github.com/geekan/MetaGPT.git
cd MetaGPT
pip install -e .
```

### 配置
```yaml
# config/config.yaml
llm:
  api_type: "openai"
  api_key: "your-api-key"
  model: "gpt-4"
  
workspace:
  path: "./workspace"
  
roles:
  - ProductManager
  - Architect
  - ProjectManager
  - Engineer
  - QAEngineer
```

## 使用场景
1. **快速原型开发** - 从想法到可运行的原型
2. **项目脚手架** - 生成项目基础结构
3. **需求文档化** - 将模糊需求转换为详细文档
4. **架构设计** - 生成系统架构方案
5. **代码生成** - 自动生成业务代码

## 工作流程

### 1. 需求输入
```python
from metagpt.software_company import SoftwareCompany

company = SoftwareCompany()
company.hire([
    "ProductManager",
    "Architect", 
    "Engineer",
    "QAEngineer"
])

# 输入需求
requirement = """
开发一个待办事项管理应用：
1. 用户可以创建、编辑、删除待办事项
2. 支持设置优先级和截止日期
3. 可以按状态筛选（待办/进行中/已完成）
4. 提供 RESTful API
5. 使用 React 前端 + Node.js 后端
"""

company.start_project(requirement)
```

### 2. 产品经理 - 生成 PRD
```markdown
# 产品需求文档（PRD）

## 功能需求

### 1. 任务管理
- **创建任务**：用户可以创建新的待办事项
- **编辑任务**：修改已有任务的信息
- **删除任务**：删除不需要的任务

### 2. 任务属性
- 优先级：高/中/低
- 截止日期：可选的日期时间
- 状态：待办/进行中/已完成

## 技术要求
- 前端：React + TypeScript
- 后端：Node.js + Express
- 数据库：MongoDB
- API：RESTful 风格
```

### 3. 架构师 - 系统设计
```typescript
// 数据模型
interface Task {
  id: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  status: 'todo' | 'in_progress' | 'done';
  dueDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}

// API 设计
// GET /api/tasks - 获取任务列表
// POST /api/tasks - 创建任务
// GET /api/tasks/:id - 获取单个任务
// PUT /api/tasks/:id - 更新任务
// DELETE /api/tasks/:id - 删除任务
```

### 4. 工程师 - 代码实现
```typescript
// backend/src/models/Task.ts
import mongoose from 'mongoose';

const taskSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: String,
  priority: { 
    type: String, 
    enum: ['high', 'medium', 'low'],
    default: 'medium'
  },
  status: {
    type: String,
    enum: ['todo', 'in_progress', 'done'],
    default: 'todo'
  },
  dueDate: Date
}, { timestamps: true });

export const Task = mongoose.model('Task', taskSchema);
```

### 5. QA 工程师 - 测试用例
```typescript
// backend/tests/tasks.test.ts
describe('Task API', () => {
  it('should create a new task', async () => {
    const response = await request(app)
      .post('/api/tasks')
      .send({ title: 'Test Task', priority: 'high' });
    
    expect(response.status).toBe(201);
    expect(response.body.title).toBe('Test Task');
  });
});
```

## 核心功能

### 1. 一键生成项目
```python
from metagpt.software_company import SoftwareCompany

company = SoftwareCompany()
company.hire(["ProductManager", "Architect", "Engineer"])
company.start_project("开发一个博客系统")

# 输出目录结构：
# workspace/
# ├── docs/
# │   ├── prd.md          # 产品需求文档
# │   ├── design.md       # 系统设计文档
# │   └── api.md          # API 文档
# ├── src/
# │   ├── frontend/       # 前端代码
# │   ├── backend/        # 后端代码
# │   └── database/       # 数据库脚本
# └── tests/              # 测试代码
```

### 2. 增量开发
```python
# 在现有项目基础上添加新功能
company.add_feature("添加用户评论功能")
```

### 3. 代码审查
```python
# 自动代码审查
company.review_code("src/backend/routes/tasks.ts")
```

### 4. 文档生成
```python
# 生成技术文档
company.generate_docs(doc_type="api", output_path="docs/api.md")
```

## 最佳实践

### 1. 清晰的需求描述
```python
# ❌ 不好
requirement = "做一个网站"

# ✅ 好
requirement = """
开发一个在线书店网站：
1. 用户功能：注册、登录、浏览图书、购物车、下单
2. 管理功能：图书管理、订单管理、用户管理
3. 技术栈：Vue 3 + Spring Boot + MySQL
"""
```

### 2. 合理的角色配置
```python
# 小型项目
company.hire(["ProductManager", "Engineer"])

# 中型项目
company.hire(["ProductManager", "Architect", "Engineer", "QAEngineer"])

# 大型项目
company.hire([
    "ProductManager",
    "Architect",
    "ProjectManager",
    "Engineer",
    "Engineer",  # 多个工程师
    "QAEngineer"
])
```

### 3. 迭代开发
```python
company.start_project("开发 MVP 版本")
company.add_feature("添加社交分享功能")
company.optimize("优化数据库查询性能")
```

## 输出格式

### 标准输出
```markdown
## 项目生成结果

**项目名称**：[项目名称]

**生成的文档**：
- 产品需求文档（PRD）
- 系统设计文档
- API 文档

**生成的代码**：
- 前端代码：[路径]
- 后端代码：[路径]
- 测试代码：[路径]

**下一步操作**：
1. 安装依赖：`npm install`
2. 配置环境变量
3. 启动开发服务器：`npm run dev`
4. 运行测试：`npm test`
```

## 常见问题

### 生成的代码不完整
- 提供更详细的需求描述
- 增加工程师角色数量
- 启用迭代模式

### 架构设计不合理
- 明确技术栈要求
- 提供参考架构
- 调整架构师的提示词

### 测试覆盖率低
- 增加 QA 工程师
- 明确测试要求
- 启用测试覆盖率检查

## 相关资源
- GitHub: https://github.com/geekan/MetaGPT
- 文档: https://docs.deepwisdom.ai/main/zh/
- 论文: https://arxiv.org/abs/2308.00352
- 示例: https://github.com/geekan/MetaGPT/tree/main/examples
