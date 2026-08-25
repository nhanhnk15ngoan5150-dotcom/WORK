from services.answer_service import generate_final_answer


# 1. 五月总营业额
may_results = [
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
    }
]


# 2. 六月总营业额
june_results = [
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


# 3. 最近总营业额
recent_results = [
    {
        "task": {
            "intent": "total_sales",
            "time_expression": "最近",
            "metric": "营业额"
        },
        "result": {
            "success": True,
            "total_sales": 151572.0
        }
    }
]


# 4. 四月超出数据范围
april_results = [
    {
        "task": {
            "intent": "total_sales",
            "time_expression": "四月",
            "metric": "营业额"
        },
        "result": {
            "success": False,
            "message": (
                "当前数据范围为"
                "2026-05-01至2026-07-31，"
                "暂无四月数据"
            )
        }
    }
]


# 5. 执行测试
print(
    "五月:",
    generate_final_answer(
        may_results
    )
)

print(
    "六月:",
    generate_final_answer(
        june_results
    )
)

print(
    "最近:",
    generate_final_answer(
        recent_results
    )
)

print(
    "四月:",
    generate_final_answer(
        april_results
    )
)