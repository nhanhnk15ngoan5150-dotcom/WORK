from services.answer_service import generate_final_answer


# 1. 构造五月 detail 结果
detail_results = [
    {
        "task": {
            "intent": "store_category_sales",
            "time_expression": "五月",
            "query_mode": "detail"
        },
        "result": {
            "success": True,
            "data": [
                {
                    "category": "日料",
                    "total_sales": 28779.0
                },
                {
                    "category": "拉面",
                    "total_sales": 28638.0
                },
                {
                    "category": "点心",
                    "total_sales": 27646.0
                },
                {
                    "category": "三明治",
                    "total_sales": 27377.0
                },
                {
                    "category": "轻食",
                    "total_sales": 27314.0
                }
            ],
            "top_category": {
                "category": "日料",
                "total_sales": 28779.0
            }
        }
    }
]


# 2. 构造五月 top 结果
top_results = [
    {
        "task": {
            "intent": "store_category_sales",
            "time_expression": "五月",
            "query_mode": "top"
        },
        "result": {
            "success": True,
            "data": [
                {
                    "category": "日料",
                    "total_sales": 28779.0
                }
            ],
            "top_category": {
                "category": "日料",
                "total_sales": 28779.0
            }
        }
    }
]


# 3. 输出回答
print(
    "detail:",
    generate_final_answer(
        detail_results
    )
)

print(
    "top:",
    generate_final_answer(
        top_results
    )
)