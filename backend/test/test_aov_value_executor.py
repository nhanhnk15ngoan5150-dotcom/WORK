from agent.executor import _execute_avg_order_value_trend


# 1. 五月客单价
may_result = _execute_avg_order_value_trend(
    {
        "intent": "avg_order_value_trend",
        "time_expression": "五月",
        "query_mode": "value",
    }
)

print("\n================")
print("五月 VALUE")
print(may_result)


# 2. 六月客单价
june_result = _execute_avg_order_value_trend(
    {
        "intent": "avg_order_value_trend",
        "time_expression": "六月",
        "query_mode": "value",
    }
)

print("\n================")
print("六月 VALUE")
print(june_result)


# 3. 最近客单价趋势
recent_result = _execute_avg_order_value_trend(
    {
        "intent": "avg_order_value_trend",
        "time_expression": "最近",
        "query_mode": "trend",
    }
)

print("\n================")
print("最近 TREND")
print(recent_result)


# 4. 旧调用兼容
legacy_result = _execute_avg_order_value_trend(
    {
        "intent": "avg_order_value_trend",
        "time_expression": "最近",
    }
)

print("\n================")
print("旧调用兼容")
print(legacy_result)