# Stock Reviewer MCP Server

一个基于 FastMCP 的股票持仓复盘工具，提供智能的股票投资建议评估和盈亏分析。

## 项目概述

Stock Reviewer 是一个 Model Context Protocol (MCP) 服务器，专门用于股票投资复盘分析。它能够：
- 分析股票持仓的盈亏情况
- 评估历史投资建议的准确性
- 提供智能的复盘结论
- 支持多只股票的持仓管理

## 功能特性

### 🎯 核心功能
- **持仓复盘**: 对指定股票进行全面的盈亏分析
- **建议评估**: 智能判断历史投资建议的准确性
- **实时行情**: 模拟实时股票价格数据
- **多股票支持**: 支持管理多个股票的持仓信息

### 📊 分析维度
- 成本均价 vs 当前市价
- 盈亏金额和百分比计算
- 持仓数量统计
- 目标价达成情况
- 投资建议准确性评估

## 项目结构

```
gemimc/
├── stock_review.py     # 主程序文件，包含 MCP 服务器逻辑
├── run_mcp.bat        # Windows 批处理启动脚本
└── README.md          # 项目说明文档
```

## 快速开始

### 环境要求
- Python 3.8+
- FastMCP 库
- Windows 系统（或兼容的 Python 环境）

### 安装依赖
```bash
pip install fastmcp
```

### 运行方式

#### 方式一：使用批处理文件（推荐）
```bash
run_mcp.bat
```

#### 方式二：直接运行 Python 脚本
```bash
python stock_review.py
```

## 使用方法

### 调用股票复盘工具
```python
# 示例调用
result = review_stock_position("AAPL")
print(result)
```

### 支持的股票代码
当前模拟数据库中包含以下股票：
- **AAPL** (苹果): 成本价 $150.0，目标价 $180.0
- **TSLA** (特斯拉): 成本价 $240.0，目标价 $300.0  
- **BABA** (阿里巴巴): 成本价 $100.0，目标价 $80.0

### 输出示例
```
--- 股票复盘报告: AAPL ---
【持仓情况】
- 成本均价: $150.0
- 当前市价: $220.0
- 持仓数量: 100
- 盈亏金额: $7000.00 (46.67%)

【建议回顾】
- 历史建议: BUY (目标价: $180.0)
- 复盘结论: ✅ 建议准确：买入后上涨，策略成功。
---------------------------
```

## 技术架构

### 核心组件
1. **MCP 服务器**: 基于 FastMCP 框架构建
2. **模拟数据库**: 内存中的持仓数据存储
3. **行情接口**: 模拟实时价格数据
4. **复盘引擎**: 智能建议评估算法

### 智能复盘逻辑
- **BUY 建议**: 检查当前价格是否高于成本价
- **SELL 建议**: 检查当前价格是否低于成本价  
- **HOLD 建议**: 中性评估，持续观察

## 配置说明

### 持仓数据库
在 `stock_review.py` 中修改 `PORTFOLIO_DB` 来添加或更新持仓信息：
```python
PORTFOLIO_DB = {
    "股票代码": {
        "cost": 成本价,
        "shares": 持仓数量, 
        "advice": "BUY/HOLD/SELL",
        "target": 目标价
    }
}
```

### 行情数据
在 `CURRENT_MARKET_DATA` 中更新实时价格数据。

## 扩展开发

### 添加真实数据源
```python
# 替换模拟数据为真实 API 调用
import yfinance as yf

def get_real_price(symbol):
    stock = yf.Ticker(symbol)
    return stock.info['currentPrice']
```

### 集成数据库
```python
# 使用 SQLite 或 PostgreSQL 替代内存存储
import sqlite3
conn = sqlite3.connect('portfolio.db')
```

## 故障排除

### 常见问题
1. **模块未找到**: 确保已安装 `fastmcp` 库
2. **股票未找到**: 检查股票代码是否在数据库中
3. **价格获取失败**: 验证行情数据配置

### 日志查看
运行时会输出 MCP 服务器状态信息，可用于调试。

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题或建议，请通过项目 Issues 页面联系。
