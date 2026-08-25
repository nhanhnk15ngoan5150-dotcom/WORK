from agent.planner import create_plan


# 1. 测试销售额任务
sales_amount_data = {
    "entities": [
        {
            "intent": "product_sales",
            "products": [
                {
                    "standard": "可乐",
                    "method": "exact",
                    "confidence": 1.0
                }
            ],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}


# 2. 测试销量任务
sales_quantity_data = {
    "entities": [
        {
            "intent": "product_sales",
            "products": [
                {
                    "standard": "可乐",
                    "method": "exact",
                    "confidence": 1.0
                }
            ],
            "time_expression": "六月",
            "metric": "销量"
        }
    ]
}


# 3. 测试双指标任务
double_metric_data = {
    "entities": [
        {
            "intent": "product_sales",
            "products": [
                {
                    "standard": "鸡肉poke",
                    "method": "alias",
                    "confidence": 0.95
                }
            ],
            "time_expression": "五月",
            "metric": "销售额"
        },
        {
            "intent": "product_sales",
            "products": [
                {
                    "standard": "鸡肉poke",
                    "method": "alias",
                    "confidence": 0.95
                }
            ],
            "time_expression": "五月",
            "metric": "销量"
        }
    ]
}


print(
    "销售额:",
    create_plan(
        sales_amount_data
    )
)

print(
    "销量:",
    create_plan(
        sales_quantity_data
    )
)

print(
    "双指标:",
    create_plan(
        double_metric_data
    )
)