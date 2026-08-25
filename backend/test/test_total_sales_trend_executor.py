from agent.executor import execute_plan


# 1. 最近单期营业额
value_plan = [
    {
        "intent": "total_sales",
        "time_expression": "最近",
        "metric": "营业额",
        "query_mode": "value"
    }
]

value_result = execute_plan(
    value_plan
)

print("\n================")
print("VALUE:", value_result)


# 2. 最近营业额趋势
trend_plan = [
    {
        "intent": "total_sales",
        "time_expression": "最近",
        "metric": "营业额",
        "query_mode": "trend"
    }
]

trend_result = execute_plan(
    trend_plan
)

print("\n================")
print("TREND:", trend_result)