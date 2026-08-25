from agent.executor import _execute_store_category_sales


# 1. 最近各品类趋势
trend_result = _execute_store_category_sales(
    {
        "intent": "store_category_sales",
        "time_expression": "最近",
        "query_mode": "detail",
        "analysis_mode": "trend",
    }
)

print("\n================")
print("TREND")
print(trend_result)


# 2. 最近各品类单期
value_result = _execute_store_category_sales(
    {
        "intent": "store_category_sales",
        "time_expression": "最近",
        "query_mode": "detail",
        "analysis_mode": "value",
    }
)

print("\n================")
print("VALUE")
print(value_result)


# 3. 越界回归
out_of_range_result = _execute_store_category_sales(
    {
        "intent": "store_category_sales",
        "time_expression": "四月",
        "query_mode": "detail",
        "analysis_mode": "value",
    }
)

print("\n================")
print("OUT OF RANGE")
print(out_of_range_result)