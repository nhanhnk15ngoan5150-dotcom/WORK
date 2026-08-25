from services.answer_service import _answer_failed_task


# 1. 商品失败
product_item = {
    "task": {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "四月",
        "metric": "销售额",
    },
    "result": {
        "success": False,
        "message": "暂无四月数据",
    },
}

product_answer = _answer_failed_task(
    product_item
)

print("\n================")
print("商品失败:")
print(product_answer)


# 2. 门店品类失败
store_item = {
    "task": {
        "intent": "store_category_sales",
        "time_expression": "四月",
    },
    "result": {
        "success": False,
        "message": "暂无四月数据",
    },
}

store_answer = _answer_failed_task(
    store_item
)

print("\n================")
print("品类失败:")
print(store_answer)


# 3. 总营业额失败
total_item = {
    "task": {
        "intent": "total_sales",
        "time_expression": "四月",
    },
    "result": {
        "success": False,
        "message": "暂无四月数据",
    },
}

total_answer = _answer_failed_task(
    total_item
)

print("\n================")
print("总营业额失败:")
print(total_answer)


# 4. 客单价失败
aov_item = {
    "task": {
        "intent": "avg_order_value_trend",
    },
    "result": {
        "success": False,
        "message": "查询失败",
    },
}

aov_answer = _answer_failed_task(
    aov_item
)

print("\n================")
print("客单价失败:")
print(aov_answer)


# 5. 当前天气失败
weather_item = {
    "task": {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
    },
    "result": {
        "success": False,
        "message": "天气服务暂不可用",
    },
}

weather_answer = _answer_failed_task(
    weather_item
)

print("\n================")
print("天气当前失败:")
print(weather_answer)


# 6. 锁定旧失败回答契约
assert (
    product_answer
    == "四月可乐销售额查询失败：暂无四月数据。"
)

assert (
    store_answer
    == "四月门店品类营业额查询失败：暂无四月数据。"
)

assert (
    total_answer
    == "四月总营业额查询失败：暂无四月数据。"
)

assert (
    aov_answer
    == "客单价趋势查询失败：查询失败。"
)

assert (
    weather_answer
    == "北京今天天气查询失败：天气服务暂不可用。"
)

print("\n================")
print("失败回答契约: PASS")