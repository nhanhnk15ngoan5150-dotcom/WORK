from services.answer_service import generate_final_answer


# 1. 构造五月和六月两个商品的数据
results = [
    {
        "task": {
            "intent": "product_sales",
            "product": "牛肉poke",
            "time_expression": "五月",
            "metric": "销售额"
        },
        "result": {
            "success": True,
            "total_sales": 13104
        }
    },
    {
        "task": {
            "intent": "product_sales",
            "product": "鸡肉poke",
            "time_expression": "五月",
            "metric": "销售额"
        },
        "result": {
            "success": True,
            "total_sales": 11118
        }
    },
    {
        "task": {
            "intent": "product_sales",
            "product": "牛肉poke",
            "time_expression": "六月",
            "metric": "销售额"
        },
        "result": {
            "success": True,
            "total_sales": 13692
        }
    },
    {
        "task": {
            "intent": "product_sales",
            "product": "鸡肉poke",
            "time_expression": "六月",
            "metric": "销售额"
        },
        "result": {
            "success": True,
            "total_sales": 8908
        }
    }
]


# 2. 生成回答
answer = generate_final_answer(
    results
)

print(
    "回答:",
    answer
)