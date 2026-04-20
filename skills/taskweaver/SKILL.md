# TaskWeaver - Code-First AI Agent

## 概述
微软开源的代码优先 AI Agent 框架，通过编写 Python 代码来执行复杂的数据分析和自动化任务。

## 核心能力
- **代码生成与执行** - 自动生成并执行 Python 代码
- **插件系统** - 支持自定义插件扩展功能
- **数据分析** - 处理和分析结构化数据
- **任务规划** - 将复杂任务分解为子任务
- **状态管理** - 维护对话上下文和执行状态
- **错误处理** - 自动检测和修复代码错误

## 架构特点

### Code-First 设计
- 将自然语言转换为可执行的 Python 代码
- 代码在隔离的沙箱环境中执行
- 支持复杂的数据处理和计算逻辑

### 插件机制
```python
# 示例插件结构
from taskweaver.plugin import Plugin

class DataAnalysisPlugin(Plugin):
    def __call__(self, data_path: str, analysis_type: str):
        # 插件逻辑
        return result
```

## 前置要求

### 安装 TaskWeaver
```bash
# 安装
pip install taskweaver

# 初始化项目
taskweaver init my_project
cd my_project

# 启动
taskweaver start
```

### 配置文件
```yaml
# taskweaver_config.yaml
llm:
  api_type: "openai"
  api_key: "your-api-key"
  model: "gpt-4"

execution:
  code_verification: true
  max_retry: 3
  
plugins:
  - name: "data_analysis"
    enabled: true
```

## 使用场景
1. **数据分析** - 自动化数据清洗、分析、可视化
2. **报表生成** - 定期生成数据报表
3. **工作流自动化** - 自动化重复性任务
4. **API 集成** - 调用外部 API 获取和处理数据
5. **文件处理** - 批量处理文件（Excel、CSV、JSON 等）

## 工作流程

### 1. 任务规划
TaskWeaver 将复杂任务分解为多个步骤：

```
用户：分析销售数据，找出销售额最高的产品类别

TaskWeaver 规划：
1. 读取销售数据文件
2. 数据清洗和预处理
3. 按产品类别分组统计
4. 排序并找出最高值
5. 生成可视化图表
```

### 2. 代码生成
为每个步骤生成 Python 代码：

```python
# Step 1: 读取数据
import pandas as pd
df = pd.read_csv('sales_data.csv')

# Step 2: 数据清洗
df = df.dropna()
df['amount'] = df['amount'].astype(float)

# Step 3: 分组统计
category_sales = df.groupby('category')['amount'].sum()

# Step 4: 排序
top_category = category_sales.sort_values(ascending=False).head(1)

# Step 5: 可视化
import matplotlib.pyplot as plt
category_sales.plot(kind='bar')
plt.title('Sales by Category')
plt.savefig('sales_chart.png')
```

### 3. 代码执行
在沙箱环境中执行代码，捕获输出和错误

### 4. 结果验证
验证执行结果，必要时重试或调整

### 5. 输出交付
返回分析结果、图表、文件等

## 核心功能

### 1. 数据处理
```python
# 自动生成数据处理代码
# 用户：读取 data.csv，删除重复行，保存为 cleaned_data.csv

import pandas as pd
df = pd.read_csv('data.csv')
df = df.drop_duplicates()
df.to_csv('cleaned_data.csv', index=False)
print(f"处理完成，共 {len(df)} 行数据")
```

### 2. 数据分析
```python
# 用户：计算每月的平均销售额和增长率

import pandas as pd
df = pd.read_csv('sales.csv')
df['date'] = pd.to_datetime(df['date'])
monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].mean()
growth_rate = monthly.pct_change() * 100
result = pd.DataFrame({
    'avg_sales': monthly,
    'growth_rate': growth_rate
})
print(result)
```

### 3. 数据可视化
```python
# 用户：绘制销售趋势折线图

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sales.csv')
df['date'] = pd.to_datetime(df['date'])
daily_sales = df.groupby('date')['amount'].sum()

plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values)
plt.title('Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sales_trend.png')
```

### 4. API 调用
```python
# 用户：获取今天的天气信息

import requests
response = requests.get('https://api.weather.com/v1/current', 
                       params={'city': 'Beijing'})
weather = response.json()
print(f"温度: {weather['temp']}°C")
print(f"天气: {weather['condition']}")
```

## 自定义插件

### 创建插件
```python
# plugins/excel_processor.py
from taskweaver.plugin import Plugin
import pandas as pd

class ExcelProcessor(Plugin):
    """处理 Excel 文件的插件"""
    
    def __call__(self, file_path: str, operation: str):
        """
        Args:
            file_path: Excel 文件路径
            operation: 操作类型 (read/write/merge)
        """
        if operation == 'read':
            df = pd.read_excel(file_path)
            return df.to_dict()
        elif operation == 'merge':
            # 合并多个 Excel 文件
            pass
        
        return {"status": "success"}
```

### 注册插件
```yaml
# taskweaver_config.yaml
plugins:
  - name: "excel_processor"
    module: "plugins.excel_processor"
    class: "ExcelProcessor"
    enabled: true
```

## 最佳实践

### 1. 清晰的任务描述
❌ 不好：处理数据
✅ 好：读取 sales.csv，计算每个产品的总销售额，按降序排列，保存为 summary.csv

### 2. 提供上下文信息
- 文件路径和格式
- 数据结构说明
- 期望的输出格式
- 特殊处理要求

### 3. 分步执行复杂任务
```
复杂任务：生成销售分析报告

分解为：
1. 读取和清洗数据
2. 计算关键指标
3. 生成图表
4. 创建 PDF 报告
```

### 4. 错误处理
```python
# TaskWeaver 自动添加错误处理
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("文件不存在，请检查路径")
except Exception as e:
    print(f"读取失败: {str(e)}")
```

## 安全注意事项

### 1. 代码沙箱
- 代码在隔离环境中执行
- 限制文件系统访问
- 限制网络访问（可配置）

### 2. 代码审查
```yaml
# 启用代码验证
execution:
  code_verification: true
  allowed_modules:
    - pandas
    - numpy
    - matplotlib
  blocked_operations:
    - os.system
    - subprocess
    - eval
```

### 3. 数据安全
- 不处理敏感数据
- 使用数据脱敏
- 限制文件访问权限

## 输出格式

### 标准输出
```markdown
## 任务执行结果

**任务描述**：
[用户的任务需求]

**执行步骤**：
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**生成的代码**：
```python
[Python 代码]
```

**执行结果**：
[输出内容、图表、文件等]

**总结**：
[任务完成情况和关键发现]
```

## 常见问题

### 代码执行失败
- 检查依赖包是否安装
- 验证文件路径是否正确
- 查看错误日志
- 调整代码验证规则

### 性能问题
- 减少数据量
- 优化算法
- 使用并行处理
- 增加超时时间

### 插件不工作
- 检查插件配置
- 验证插件代码
- 查看插件日志
- 重启 TaskWeaver

## 相关资源
- GitHub: https://github.com/microsoft/TaskWeaver
- 文档: https://microsoft.github.io/TaskWeaver/
- 示例: https://github.com/microsoft/TaskWeaver/tree/main/examples
- 论文: https://arxiv.org/abs/2311.17541
