from typing import Any, Dict

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # 便于在未安装 mcp 的环境下本地测试
    class FastMCP:  # type: ignore
        def __init__(self, *_args, **_kwargs):
            pass

        def tool(self):
            def decorator(func):
                return func
            return decorator

        def run(self):
            raise RuntimeError("缺少 mcp 依赖，无法启动服务端")

# 初始化 MCP 服务端
mcp = FastMCP("StockReviewer")

# --- 模拟数据 ---
# 实际场景中，这里应该连接 SQLite, PostgreSQL 或读取 Excel/CSV
# 格式: {代码: {成本, 持仓数量, 当时建议, 目标价}}
PORTFOLIO_DB: Dict[str, Dict[str, Any]] = {
    "AAPL": {"cost": 150.0, "shares": 100, "advice": "BUY", "target": 180.0},
    "TSLA": {"cost": 240.0, "shares": 50, "advice": "HOLD", "target": 300.0},
    "BABA": {"cost": 100.0, "shares": 200, "advice": "SELL", "target": 80.0},
}

# --- 模拟实时行情 ---
# 实际场景中，这里应该调用 Yahoo Finance (yfinance) 或 Alpha Vantage API
CURRENT_MARKET_DATA: Dict[str, float] = {
    "AAPL": 220.0,  # 涨了
    "TSLA": 180.0,  # 跌了
    "BABA": 75.0,   # 跌了（建议卖出是对的）
}


def _build_insights(symbol: str) -> Dict[str, Any]:
    """聚合持仓、行情并计算衍生指标，返回结构化结果。"""
    normalized = symbol.upper()
    position = PORTFOLIO_DB.get(normalized)
    if not position:
        raise ValueError(f"未在持仓数据库中找到股票 {normalized}")

    current_price = CURRENT_MARKET_DATA.get(normalized)
    if current_price is None:
        raise ValueError(f"无法获取 {normalized} 的当前市场价格")

    cost = position["cost"]
    shares = position["shares"]
    advice = position["advice"]
    target = position["target"]

    if cost is None or cost <= 0:
        raise ValueError(f"{normalized} 的成本价无效（必须大于 0）")
    if shares is None or shares < 0:
        raise ValueError(f"{normalized} 的持仓数量无效（必须为非负整数）")

    profit_per_share = current_price - cost
    total_pnl = profit_per_share * shares
    pnl_percentage = (profit_per_share / cost) * 100
    target_gap = current_price - target
    target_progress_pct = (current_price / target) * 100 if target else None

    verdict = ""
    if advice == "BUY":
        verdict = "📈 买入建议验证：价格高于成本" if current_price > cost else "❗ 买入建议受挫：价格低于成本"
    elif advice == "SELL":
        verdict = "✅ 卖出建议验证：价格低于成本" if current_price < cost else "⚠️ 卖出建议失效：价格继续上涨"
    elif advice == "HOLD":
        verdict = "ℹ️ 持有建议：维持观察"
    else:
        verdict = f"⚠️ 未知建议类型：{advice}"

    status = "profit" if total_pnl > 0 else "loss" if total_pnl < 0 else "flat"

    return {
        "symbol": normalized,
        "cost": cost,
        "shares": shares,
        "current_price": current_price,
        "advice": advice,
        "target": target,
        "profit_per_share": profit_per_share,
        "total_pnl": total_pnl,
        "pnl_percentage": pnl_percentage,
        "target_gap": target_gap,
        "target_progress_pct": target_progress_pct,
        "status": status,
        "verdict": verdict,
    }


def _format_report(insights: Dict[str, Any]) -> str:
    """将结构化结果转换为可读报告文本。"""
    progress_text = (
        f"{insights['target_progress_pct']:.2f}%" if insights["target_progress_pct"] is not None else "N/A"
    )
    status_flag = {"profit": "🟢 盈利", "loss": "🔴 亏损", "flat": "⚪ 持平"}.get(insights["status"], "")

    report = f"""
--- 股票复盘报告: {insights['symbol']} ---
【持仓情况】
- 成本均价: ${insights['cost']}
- 当前市价: ${insights['current_price']}
- 持仓数量: {insights['shares']}
- 盈亏金额: ${insights['total_pnl']:.2f} ({insights['pnl_percentage']:.2f}%)
- 仓位状态: {status_flag}

【目标追踪】
- 目标价: ${insights['target']}
- 当前与目标差额: ${insights['target_gap']:.2f}
- 目标完成度: {progress_text}

【建议回顾】
- 历史建议: {insights['advice']}
- 复盘结论: {insights['verdict']}
----------------------------
    """
    return report.strip()


@mcp.tool()
def review_stock_position(symbol: str) -> str:
    """
    对指定股票代码进行持仓复盘，返回可读文本报告。
    输入股票代码（如 AAPL），返回盈亏分析及对历史建议的评估。
    """
    insights = _build_insights(symbol)
    return _format_report(insights)


@mcp.tool()
def review_stock_position_structured(symbol: str) -> Dict[str, Any]:
    """
    返回结构化的持仓复盘结果，便于程序化消费。
    响应包含成本、持仓、盈亏、目标进度、状态以及文本报告。
    """
    insights = _build_insights(symbol)
    insights["report"] = _format_report(insights)
    return insights


if __name__ == "__main__":
    # 本地运行服务端
    mcp.run()
