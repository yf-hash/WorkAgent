---
name: chat2db
description: >
  Chat2DB AI 数据库助手知识库。触发词：自然语言转SQL、SQL生成、数据库查询、
  Chat2DB、SQL优化、数据库分析、NL2SQL、数据库操作。
user-invocable: false
effort: medium
---

# Chat2DB - AI Database Assistant

## 概述
通过 AI 辅助进行数据库操作，支持自然语言转 SQL、SQL 优化、数据分析等功能。

## 核心能力
- **自然语言转 SQL** - 用自然语言描述需求，自动生成 SQL
- **SQL 优化** - 分析和优化 SQL 查询性能
- **数据分析** - 对查询结果进行智能分析
- **Schema 理解** - 自动理解数据库结构
- **SQL 解释** - 解释复杂 SQL 的含义
- **数据可视化** - 将查询结果转换为图表

## 支持的数据库
- MySQL
- PostgreSQL
- Oracle
- SQL Server
- SQLite
- MongoDB
- Redis
- ClickHouse
- H2
- 更多...

## 前置要求

### 安装 Chat2DB
```bash
# 下载安装包
# https://github.com/chat2db/Chat2DB/releases

# 或使用 Docker
docker pull chat2db/chat2db:latest
docker run -p 10824:10824 chat2db/chat2db:latest
```

### 配置数据库连接
在 Chat2DB 中添加数据库连接信息：
- 主机地址
- 端口
- 数据库名
- 用户名/密码

## 使用场景
1. **数据查询** - 快速查询数据，无需手写 SQL
2. **报表生成** - 生成数据报表和分析
3. **SQL 学习** - 学习 SQL 语法和最佳实践
4. **数据库管理** - 管理数据库结构和数据
5. **性能优化** - 优化慢查询

## 工作流程

### 1. 需求分析
- 理解用户的数据需求
- 确定目标数据库和表
- 明确查询条件和输出格式

### 2. 自然语言转 SQL

#### 示例对话
```
用户：查询最近 7 天销售额超过 1000 的订单

AI 生成 SQL：
SELECT 
    order_id,
    customer_name,
    order_date,
    total_amount
FROM orders
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    AND total_amount > 1000
ORDER BY order_date DESC;
```

#### 复杂查询示例
```
用户：统计每个产品类别的销售额，按销售额降序排列，只显示前 10 名

AI 生成 SQL：
SELECT 
    c.category_name,
    COUNT(o.order_id) as order_count,
    SUM(oi.quantity * oi.price) as total_sales
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
GROUP BY c.category_id, c.category_name
ORDER BY total_sales DESC
LIMIT 10;
```

### 3. SQL 优化

#### 优化前
```sql
SELECT * FROM orders 
WHERE customer_id IN (
    SELECT customer_id FROM customers WHERE city = 'Beijing'
);
```

#### 优化后
```sql
SELECT o.* 
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE c.city = 'Beijing';

-- 优化说明：
-- 1. 避免使用 SELECT *，明确指定字段
-- 2. 使用 JOIN 替代子查询，性能更好
-- 3. 确保 city 字段有索引
```

### 4. 数据分析

#### 分析查询结果
```
查询结果：
| product_name | sales_count | revenue |
|--------------|-------------|---------|
| Product A    | 150         | 45000   |
| Product B    | 120         | 36000   |
| Product C    | 90          | 27000   |

AI 分析：
1. Product A 是销量和营收的双冠军，占总营收的 41.7%
2. 前三名产品贡献了总营收的 100%
3. 建议：重点推广 Product A，同时关注 Product C 的增长潜力
```

### 5. Schema 理解

#### 自动分析表结构
```
表名：orders
字段：
- order_id (INT, PRIMARY KEY) - 订单 ID
- customer_id (INT, FOREIGN KEY) - 客户 ID，关联 customers 表
- order_date (DATE) - 订单日期
- total_amount (DECIMAL) - 订单总额
- status (VARCHAR) - 订单状态

索引：
- PRIMARY KEY (order_id)
- INDEX idx_customer (customer_id)
- INDEX idx_date (order_date)

关系：
- customers (1:N) orders
- orders (1:N) order_items
```

## 常用功能

### 1. 数据查询
```
自然语言：查询今天新增的用户数量
SQL：SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURDATE();
```

### 2. 数据统计
```
自然语言：按月统计 2024 年的订单数量
SQL：
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(*) as order_count
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY month
ORDER BY month;
```

### 3. 数据更新
```
自然语言：将所有待支付订单的状态改为已取消
SQL：
UPDATE orders 
SET status = 'cancelled' 
WHERE status = 'pending_payment';
```

### 4. 数据导出
```
自然语言：导出所有活跃用户的信息到 CSV
操作：执行查询后，使用导出功能保存为 CSV 文件
```

## 最佳实践

### 1. 清晰描述需求
❌ 不好：查询订单
✅ 好：查询最近 30 天金额超过 500 元的已完成订单

### 2. 指定时间范围
❌ 不好：查询销售数据
✅ 好：查询 2024 年 1 月的销售数据

### 3. 明确排序和限制
❌ 不好：查询热门产品
✅ 好：查询销量前 10 的产品，按销量降序排列

### 4. 验证生成的 SQL
- 检查 SQL 逻辑是否正确
- 在测试环境先执行
- 对于 UPDATE/DELETE 操作，先用 SELECT 验证

### 5. 性能考虑
- 避免 SELECT *
- 合理使用索引
- 限制返回行数（LIMIT）
- 避免复杂的子查询

## 安全注意事项

### 1. 权限控制
- 使用只读账号进行查询
- 限制 UPDATE/DELETE 权限
- 敏感操作需要审批

### 2. 数据脱敏
- 查询结果中隐藏敏感信息（手机号、身份证等）
- 使用脱敏函数处理个人信息

### 3. SQL 注入防护
- 使用参数化查询
- 验证用户输入
- 避免动态拼接 SQL

## 输出格式

### 标准输出
```markdown
## SQL 查询

**需求描述**：
[用户的自然语言需求]

**生成的 SQL**：
```sql
[SQL 代码]
```

**执行结果**：
[查询结果表格或说明]

**数据分析**：
[对结果的分析和洞察]

**使用建议**：
[针对具体场景的建议]
```

### SQL 优化输出
```markdown
## SQL 优化

**原始 SQL**：
```sql
[原始 SQL]
```

**优化后 SQL**：
```sql
[优化后的 SQL]
```

**优化说明**：
1. [优化点 1]
2. [优化点 2]
3. [优化点 3]

**性能提升**：
- 执行时间：从 X 秒降至 Y 秒
- 扫描行数：从 X 行降至 Y 行
```

## 常见问题

### 生成的 SQL 不正确
- 更详细地描述需求
- 提供表结构信息
- 给出示例数据
- 手动调整 SQL

### 查询性能慢
- 检查是否有索引
- 优化 JOIN 条件
- 减少返回字段
- 添加 LIMIT 限制

### 无法连接数据库
- 检查网络连接
- 验证连接信息
- 检查防火墙设置
- 确认数据库服务运行

## 相关资源
- Chat2DB 官网: https://chat2db.ai/
- GitHub: https://github.com/chat2db/Chat2DB
- 文档: https://docs.chat2db.ai/
- SQL 教程: https://www.w3schools.com/sql/
