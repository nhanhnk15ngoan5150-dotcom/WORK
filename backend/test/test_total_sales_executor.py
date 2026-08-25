from agent.executor import execute_plan


# 1. 五月总营业额
may_plan = [
    {
        "intent": "total_sales",
        "time_expression": "五月",
        "metric": "营业额"
    }
]


# 2. 六月总营业额
june_plan = [
    {
        "intent": "total_sales",
        "time_expression": "六月",
        "metric": "营业额"
    }
]


# 3. 四月超出数据范围
april_plan = [
    {
        "intent": "total_sales",
        "time_expression": "四月",
        "metric": "营业额"
    }
]


# 4. 最近总营业额
recent_plan = [
    {
        "intent": "total_sales",
        "time_expression": "最近",
        "metric": "营业额"
    }
]


print(
    "五月:",
    execute_plan(
        may_plan
    )
)

print(
    "六月:",
    execute_plan(
        june_plan
    )
)

print(
    "四月:",
    execute_plan(
        april_plan
    )
)

print(
    "最近:",
    execute_plan(
        recent_plan
    )
)