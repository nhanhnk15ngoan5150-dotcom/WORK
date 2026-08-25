from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备支持 + Unsupported + Clarification 混合状态
state = {
    "understanding": {
        "tasks": [
            {
                "intent": "total_sales",
                "products": [],
                "time_expression": "最近",
                "metric": "营业额",
                "query_mode": "trend",
            },
            {
                "intent": "weather_info",
                "products": [],
                "location": "",
                "time_expression": "今天",
                "metric": "天气",
                "weather_query": "general",
            },
        ],
        "unsupported": True,
        "unsupported_reason": (
            "当前问题超出餐饮经营数据分析能力范围"
        ),
        "need_clarification": True,
        "clarification_reason": (
            "天气查询缺少地点信息"
        ),
    },
    "entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        },
        {
            "intent": "weather_info",
            "products": [],
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        },
    ],
}


# 2. 执行 Validation
result = validation_node(
    state
)

print("\n================")
print("组合 Partial 状态:")
print(result)

print(
    "Route:",
    validation_route(result)
)


# 3. 观察当前组合状态
print("\npartial_unsupported:")
print(
    result.get("partial_unsupported")
)

print("\npartial_clarification:")
print(
    result.get("partial_clarification")
)

print("\nvalidated_entities:")
print(
    result.get("validated_entities")
)