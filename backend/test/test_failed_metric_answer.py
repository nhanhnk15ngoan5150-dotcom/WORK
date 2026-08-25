
from services.answer_service import generate_final_answer


# 1. 销售额失败
sales_failed = [
    {
        "task": {
            "intent": "product_sales",
            "product": "可乐",
            "time_expression": "四月",
            "metric": "销售额"
        },
        "result": {
            "success": False,
            "message": (
                "当前数据范围为2026-05-01至2026-07-31，"
                "暂无四月数据"
            )
        }
    }
]


# 2. 销量失败
quantity_failed = [
    {
        "task": {
            "intent": "product_sales",
            "product": "可乐",
            "time_expression": "四月",
            "metric": "销量"
        },
        "result": {
            "success": False,
            "message": (
                "当前数据范围为2026-05-01至2026-07-31，"
                "暂无四月数据"
            )
        }
    }
]


print(
    "销售额:",
    generate_final_answer(
        sales_failed
    )
)

print(
    "销量:",
    generate_final_answer(
        quantity_failed
    )
)