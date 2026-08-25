from services.llm_service import understand_question


# 1. 锁定普通成功上下文继承
product_context = {
    "intent": "product_sales",
    "time_expression": "六月",
    "metric": "销售额",
    "query_mode": "value",
    "products": ["牛肉poke"],
}

product_memory = [
    {
        "question": "牛肉六月卖的怎么样？",
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["牛肉poke"],
                "time_expression": "六月",
                "metric": "销售额",
                "query_mode": "value",
            }
        ],
    }
]

product_result = understand_question(
    question="那五月呢？",
    history=[
        {
            "role": "user",
            "content": "牛肉六月卖的怎么样？",
        },
        {
            "role": "assistant",
            "content": "六月牛肉poke销售额为13692元。",
        },
    ],
    structured_context=product_context,
    structured_memory=product_memory,
)

print("\n================")
print("普通上下文继承:")
print(product_result)


# 2. 锁定 clarification 后话题优先
clarification_history = [
    {
        "role": "user",
        "content": "牛肉六月卖的怎么样？",
    },
    {
        "role": "assistant",
        "content": "六月牛肉poke销售额为13692元。",
    },
    {
        "role": "user",
        "content": "那五月呢？",
    },
    {
        "role": "assistant",
        "content": "五月牛肉poke销售额为13104元。",
    },
    {
        "role": "user",
        "content": "今天天气怎么样？",
    },
    {
        "role": "assistant",
        "content": "天气查询缺少地点信息",
    },
]

clarification_context = {
    "intent": "product_sales",
    "time_expression": "五月",
    "metric": "销售额",
    "query_mode": "value",
    "products": ["牛肉poke"],
}

clarification_memory = [
    {
        "question": "牛肉六月卖的怎么样？",
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["牛肉poke"],
                "time_expression": "六月",
                "metric": "销售额",
                "query_mode": "value",
            }
        ],
    },
    {
        "question": "那五月呢？",
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["牛肉poke"],
                "time_expression": "五月",
                "metric": "销售额",
                "query_mode": "value",
            }
        ],
    },
]

clarification_result = understand_question(
    question="那明天呢？",
    history=clarification_history,
    structured_context=clarification_context,
    structured_memory=clarification_memory,
)

print("\n================")
print("Clarification 后连续追问:")
print(clarification_result)


# 3. 锁定旧商品继承契约
product_task = product_result["tasks"][0]

assert product_task["intent"] == "product_sales"
assert product_task["products"] == ["牛肉poke"]
assert product_task["time_expression"] == "五月"
assert product_task["metric"] == "销售额"
assert product_result["need_clarification"] is False


# 4. 锁定未完成天气话题契约
weather_task = clarification_result["tasks"][0]

assert weather_task["intent"] == "weather_info"
assert weather_task["products"] == []
assert weather_task["location"] == ""
assert weather_task["time_expression"] == "明天"
assert weather_task["metric"] == "天气"
assert weather_task["weather_query"] == "general"

assert clarification_result["unsupported"] is False
assert clarification_result["need_clarification"] is True

print("\n================")
print("话题切换 Clarification 契约: PASS")