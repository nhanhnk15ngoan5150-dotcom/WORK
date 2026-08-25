from services.answer_service import generate_final_answer


# 1. 构造五月和六月品类结果
results = [
    {
        "task": {
            "intent": "store_category_sales",
            "time_expression": "五月"
        },
        "result": {
            "success": True,
            "top_category": {
                "category": "日料",
                "total_sales": 28779.0
            }
        }
    },
    {
        "task": {
            "intent": "store_category_sales",
            "time_expression": "六月"
        },
        "result": {
            "success": True,
            "top_category": {
                "category": "点心",
                "total_sales": 27939.0
            }
        }
    }
]


# 2. 生成比较回答
print(
    generate_final_answer(
        results
    )
)