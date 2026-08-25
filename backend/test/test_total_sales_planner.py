from agent.planner import create_plan


# 1. 总营业额任务
total_sales_data = {
    "entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额"
        }
    ]
}


# 2. 品类营业额任务
category_sales_data = {
    "entities": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额"
        }
    ]
}


# 3. 执行 Planner
print(
    "总营业额:",
    create_plan(
        total_sales_data
    )
)

print(
    "品类营业额:",
    create_plan(
        category_sales_data
    )
)