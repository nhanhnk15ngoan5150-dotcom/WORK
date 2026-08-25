from services.llm_service import understand_question


# 1. 测试销售额
result_1 = understand_question(
    "六月可乐卖了多少钱？",
    [],
    {},
    []
)

print(
    "\n销售额:",
    result_1
)


# 2. 测试销量
result_2 = understand_question(
    "六月可乐卖了多少份？",
    [],
    {},
    []
)

print(
    "\n销量:",
    result_2
)


# 3. 测试当前指标覆盖历史指标
result_3 = understand_question(
    "卖了多少份？",
    [],
    {
        "intent": "product_sales",
        "products": [
            "可乐"
        ],
        "time_expression": "六月",
        "metric": "销售额"
    },
    []
)

print(
    "\n指标覆盖:",
    result_3
)


# 4. 测试销量上下文继承
result_4 = understand_question(
    "那牛肉呢？",
    [],
    {
        "intent": "product_sales",
        "products": [
            "可乐"
        ],
        "time_expression": "六月",
        "metric": "销量"
    },
    []
)

print(
    "\n销量继承:",
    result_4
)


# 5. 测试同一句同时查询金额和数量
result_5 = understand_question(
    "五月鸡肉卖了多少钱，多少份？",
    [],
    {},
    []
)

print(
    "\n双指标:",
    result_5
)


# 6. 回归原有“卖了多少”语义
result_6 = understand_question(
    "六月牛肉卖了多少？",
    [],
    {},
    []
)

print(
    "\n原功能回归:",
    result_6
)