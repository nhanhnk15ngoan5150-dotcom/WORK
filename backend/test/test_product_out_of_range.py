from agent.executor import execute_plan


# 1. 四月销售额
april_sales = [
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "四月",
        "metric": "销售额",
    }
]


# 2. 四月销量
april_quantity = [
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "四月",
        "metric": "销量",
    }
]


# 3. 正常五月查询
may_sales = [
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "五月",
        "metric": "销售额",
    }
]


print(
    "四月销售额:",
    execute_plan(april_sales)
)

print(
    "四月销量:",
    execute_plan(april_quantity)
)

print(
    "五月销售额:",
    execute_plan(may_sales)
)