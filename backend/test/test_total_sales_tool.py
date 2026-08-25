from tools.sales_tool import get_sales_summary


# 1. 查询五月经营汇总
may_result = get_sales_summary(
    start_date="2026-05-01",
    end_date="2026-06-01"
)


# 2. 查询六月经营汇总
june_result = get_sales_summary(
    start_date="2026-06-01",
    end_date="2026-07-01"
)


# 3. 查看结果
print(
    "五月:",
    may_result
)

print(
    "六月:",
    june_result
)