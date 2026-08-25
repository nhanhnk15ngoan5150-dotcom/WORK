from agent.executor import execute_plan


# 1. 准备执行计划
plan = [
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "六月",
        "metric": "销售额",
    },
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "六月",
        "metric": "销量",
    },
]


# 2. 执行计划
results = execute_plan(
    plan
)


# 3. 查看结果
for item in results:
    print(
        item
    )