from stock_review import review_stock_position, review_stock_position_structured


def analyze_portfolio(symbols):
    """分析指定股票组合的仓位情况。"""
    print("=== 投资组合复盘报告 ===\n")

    total_pnl = 0.0
    total_investment = 0.0

    for symbol in symbols:
        try:
            insights = review_stock_position_structured(symbol)
            print(insights["report"])

            total_pnl += insights["total_pnl"]
            total_investment += insights["cost"] * insights["shares"]

            print("\n" + "=" * 60 + "\n")

        except Exception as e:
            print(f"分析 {symbol} 时出错: {e}")
            print("\n" + "=" * 60 + "\n")

    # 显示投资组合汇总
    print("【投资组合汇总】")
    print(f"- 总投资金额: ${total_investment:.2f}")
    print(f"- 总盈亏金额: ${total_pnl:.2f}")
    if total_investment > 0:
        print(f"- 总收益率: {(total_pnl / total_investment) * 100:.2f}%")

    # 提供投资建议
    print("\n【投资建议】")
    if total_pnl > 0:
        print("✅ 整体投资表现良好，建议继续持有盈利仓位")
    else:
        print("⚠️ 整体投资出现亏损，建议重新评估投资策略")

    print("\n=== 复盘完成 ===")


if __name__ == "__main__":
    # 分析用户指定的股票
    user_portfolio = ["AAPL", "TSLA"]
    analyze_portfolio(user_portfolio)
