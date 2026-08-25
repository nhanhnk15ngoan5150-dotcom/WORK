from services.answer_service import generate_final_answer


# 1. 构造五月和六月总营业额
results = [
    {
        "task": {
            "intent": "total_sales",
            "time_expression": "五月",
            "metric": "营业额"
        },
        "result": {
            "success": True,
            "total_sales": 139754.0
        }
    },
    {
        "task": {
            "intent": "total_sales",
            "time_expression": "六月",
            "metric": "营业额"
        },
        "result": {
            "success": True,
            "total_sales": 132820.0
        }
    }
]


# 2. 生成比较回答
print(
    generate_final_answer(
        results
    )
)