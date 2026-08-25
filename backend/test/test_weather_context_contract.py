from services.context_service import (
    update_structured_context,
    append_structured_memory,
)


# 1. 锁定商品 Context 旧契约
product_understanding = {
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["牛肉"],
            "time_expression": "六月",
            "metric": "销售额",
            "query_mode": "value",
        }
    ]
}

product_entities = [
    {
        "intent": "product_sales",
        "products": [
            {
                "standard": "牛肉poke",
            }
        ],
        "time_expression": "六月",
        "metric": "销售额",
        "query_mode": "value",
    }
]

product_context = update_structured_context(
    {},
    product_understanding,
    product_entities,
)

product_memory = append_structured_memory(
    [],
    "牛肉六月卖的怎么样？",
    product_understanding,
    product_entities,
)

print("\n================")
print("商品 Context:")
print(product_context)

print("\n商品 Memory:")
print(product_memory)


# 2. 锁定 Weather 修改前契约
weather_understanding = {
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "北京",
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        }
    ]
}

weather_entities = [
    {
        "intent": "weather_info",
        "products": [],
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
        "weather_query": "general",
    }
]

weather_context = update_structured_context(
    {},
    weather_understanding,
    weather_entities,
)

weather_memory = append_structured_memory(
    [],
    "北京今天天气怎么样？",
    weather_understanding,
    weather_entities,
)

print("\n================")
print("Weather Context 修改前:")
print(weather_context)

print("\nWeather Memory 修改前:")
print(weather_memory)


# 3. 商品旧契约必须保持
assert product_context == {
    "intent": "product_sales",
    "time_expression": "六月",
    "metric": "销售额",
    "query_mode": "value",
    "products": ["牛肉poke"],
}

assert product_memory == [
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


# 4. 锁定当前 Weather 缺字段行为
assert weather_context == {
    "intent": "weather_info",
    "time_expression": "今天",
    "metric": "天气",
    "query_mode": None,
    "products": [],
    "location": "北京",
    "weather_query": "general",
}

assert weather_memory == [
    {
        "question": "北京今天天气怎么样？",
        "tasks": [
            {
                "intent": "weather_info",
                "products": [],
                "time_expression": "今天",
                "metric": "天气",
                "query_mode": None,
                "location": "北京",
                "weather_query": "general",
            }
        ],
    }
]

print("\n================")
print("Weather Context 修改前契约: PASS")