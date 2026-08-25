from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 纯天气缺地点，但 Understanding 漏报 Clarification
pure_state = {
    "understanding": {
        "tasks": [
            {
                "intent": "weather_info",
                "products": [],
                "location": "",
                "time_expression": "今天",
                "metric": "天气",
                "weather_query": "general",
            }
        ],
        "unsupported": False,
        "unsupported_reason": "",
        "need_clarification": False,
        "clarification_reason": "",
    },
    "entities": [
        {
            "intent": "weather_info",
            "products": [],
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        }
    ],
}


# 2. Supported + Unsupported + 天气缺地点
mixed_state = {
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
            "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
        ),
        "need_clarification": False,
        "clarification_reason": "",
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


# 3. 执行当前 Validation
pure_result = validation_node(
    pure_state
)

mixed_result = validation_node(
    mixed_state
)


print("\n================")
print("纯 Weather 漏报 Clarification:")
print(pure_result)
print(
    "Route:",
    validation_route(pure_result)
)


print("\n================")
print("组合状态漏报 Clarification:")
print(mixed_result)
print(
    "Route:",
    validation_route(mixed_result)
)


# 4. 锁定纯 Weather 必要字段兜底
assert pure_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "天气查询缺少地点信息"
    ),
}

assert (
    validation_route(pure_result)
    == "clarification"
)


assert mixed_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": False,
    "clarification_reason": None,
    "partial_unsupported": True,
    "partial_unsupported_reason": (
        "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
    ),
    "partial_clarification": True,
    "partial_clarification_reason": (
        "天气查询缺少地点信息"
    ),
    "validated_entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        }
    ],
}

assert (
    validation_route(mixed_result)
    == "planner"
)


print("\n================")
print(
    "Required Field Fallback 契约: PASS"
)