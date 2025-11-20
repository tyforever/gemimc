"""
轻量级自检脚本，验证 stock_review 的核心路径与错误分支。
直接运行：python test_stock_review.py
"""
from stock_review import (
    CURRENT_MARKET_DATA,
    PORTFOLIO_DB,
    review_stock_position,
    review_stock_position_structured,
)


def check_structured_success():
    insights = review_stock_position_structured("AAPL")
    assert insights["symbol"] == "AAPL"
    assert insights["status"] == "profit"
    assert "report" in insights and "AAPL" in insights["report"]
    print("[OK] AAPL 结构化结果校验通过")


def check_sell_verdict():
    insights = review_stock_position_structured("BABA")
    assert insights["verdict"].startswith("✅")
    assert insights["status"] == "loss"  # 当前价格低于成本
    print("[OK] BABA 卖出建议判定校验通过")


def check_text_report():
    report = review_stock_position("TSLA")
    assert "TSLA" in report and "盈亏金额" in report
    print("[OK] 文本报告输出校验通过")


def check_missing_symbol():
    try:
        review_stock_position("MSFT")
    except ValueError as e:
        assert "未在持仓数据库中找到股票" in str(e)
        print("[OK] 未知股票错误处理校验通过")
    else:
        raise AssertionError("缺少股票时报错预期未触发")


def check_invalid_cost():
    PORTFOLIO_DB["ZERO"] = {"cost": 0, "shares": 10, "advice": "BUY", "target": 10}
    CURRENT_MARKET_DATA["ZERO"] = 0.1
    try:
        review_stock_position("ZERO")
    except ValueError as e:
        assert "成本价无效" in str(e)
        print("[OK] 成本为 0 的错误处理校验通过")
    else:
        raise AssertionError("成本为 0 时应报错")
    finally:
        PORTFOLIO_DB.pop("ZERO", None)
        CURRENT_MARKET_DATA.pop("ZERO", None)


if __name__ == "__main__":
    check_structured_success()
    check_sell_verdict()
    check_text_report()
    check_missing_symbol()
    check_invalid_cost()
    print("\n全部检查完成")
