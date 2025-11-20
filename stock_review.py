from mcp.server.fastmcp import FastMCP
from typing import Dict

# 初始化 MCP 服务器
mcp = FastMCP("StockReviewer")

# --- 模拟数据库 ---
# 实际场景中，这里应该连接 SQLite, PostgreSQL 或读取 Excel/CSV
# 格式: {代码: {成本价, 持仓数量, 当时建议, 目标价}}
PORTFOLIO_DB = {
    "AAPL": {"cost": 150.0, "shares": 100, "advice": "BUY", "target": 180.0},
    "TSLA": {"cost": 240.0, "shares": 50, "advice": "HOLD", "target": 300.0},
    "BABA": {"cost": 100.0, "shares": 200, "advice": "SELL", "target": 80.0},
}

# --- 模拟实时行情 ---
# 实际场景中，这里应该调用 Yahoo Finance (yfinance) 或 Alpha Vantage API
CURRENT_MARKET_DATA = {
    "AAPL": 220.0,  # 涨了
    "TSLA": 180.0,  # 跌了
    "BABA": 75.0,   # 跌了（建议卖出是对的）
}

@mcp.tool()
def review_stock_position(symbol: str) -> str:
    """
    对指定股票代码进行持仓复盘。
    输入股票代码（如 AAPL），返回盈亏分析及对历史建议的评估。
    """
    symbol = symbol.upper()
    
    # 1. 获取持仓数据
    position = PORTFOLIO_DB.get(symbol)
    if not position:
        return f"错误: 未在持仓数据库中找到股票 {symbol}。"

    # 2. 获取当前价格
    current_price = CURRENT_MARKET_DATA.get(symbol)
    if not current_price:
        return f"错误: 无法获取 {symbol} 的当前市场价格。"

    # 3. 计算基础数据
    cost = position['cost']
    shares = position['shares']
    advice = position['advice']
    target = position['target']
    
    profit_per_share = current_price - cost
    total_pnl = profit_per_share * shares
    pnl_percentage = (profit_per_share / cost) * 100

    # 4. 智能复盘逻辑（评估建议是否准确）
    review_verdict = ""
    if advice == "BUY":
        if current_price > cost:
            review_verdict = "✅ 建议准确：买入后上涨，策略成功。"
        else:
            review_verdict = "❌ 建议失效：买入后被套。"
    elif advice == "SELL":
        if current_price < cost:
            review_verdict = "✅ 建议准确：卖出/看空正确，规避了下跌。"
        else:
            review_verdict = "❌ 建议失效：卖飞了，价格后续上涨。"
    elif advice == "HOLD":
        review_verdict = "ℹ️ 建议观察：当前价格波动属于持有范围内。"

    # 5. 格式化输出报告
    report = f"""
--- 股票复盘报告: {symbol} ---
【持仓情况】
- 成本均价: ${cost}
- 当前市价: ${current_price}
- 持仓数量: {shares}
- 盈亏金额: ${total_pnl:.2f} ({pnl_percentage:.2f}%)

【建议回顾】
- 历史建议: {advice} (目标价: ${target})
- 复盘结论: {review_verdict}
---------------------------
    """
    return report.strip()

if __name__ == "__main__":
    # 本地运行服务器
    mcp.run()