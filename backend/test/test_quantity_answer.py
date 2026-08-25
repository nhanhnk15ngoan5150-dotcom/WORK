from services.answer_service import generate_final_answer


# 1. 单独测试销量
quantity_results = [
    {
        "task": {
            "intent": "product_sales",
            "product": "可乐",
            "time_expression": "六月",
            "metric": "销量"
        },
        "result": {
            "success": True,
            "total_quantity": 310
        }
    }
]

print(
    "销量:",
    generate_final_answer(
        quantity_results
    )
)


# 2. 测试销售额
sales_results = [
    {
        "task": {
            "intent": "product_sales",
            "product": "可乐",
            "time_expression": "六月",
            "metric": "销售额"
        },
        "result": {
            "success": True,
            "total_sales": 1550
        }
    }
]

print(
    "销售额:",
    generate_final_answer(
        sales_results
    )
)


# 3. 测试同一商品双指标
double_metric_results = [
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
            "product": "鸡肉poke",
            "time_expression": "五月",
            "metric": "销量"
        },
        "result": {
            "success": True,
            "total_quantity": 327
        }
    }
]

print(
    "双指标:",
    generate_final_answer(
        double_metric_results
    )
)


# 4. 测试两个商品销量比较
quantity_compare_results = [
    {
        "task": {
            "intent": "product_sales",
            "product": "牛肉poke",
            "time_expression": "五月",
            "metric": "销量"
        },
        "result": {
            "success": True,
            "total_quantity": 312
        }
    },
    {
        "task": {
            "intent": "product_sales",
            "product": "鸡肉poke",
            "time_expression": "五月",
            "metric": "销量"
        },
        "result": {
            "success": True,
            "total_quantity": 327
        }
    }
]

print(
    "销量比较:",
    generate_final_answer(
        quantity_compare_results
    )
)