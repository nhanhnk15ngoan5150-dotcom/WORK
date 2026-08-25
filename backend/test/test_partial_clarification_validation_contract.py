from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 纯天气缺地点
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
        "need_clarification": True,
        "clarification_reason": "天气查询缺少地点信息",
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

pure_result = validation_node(
    pure_state
)

print("\n================")
print("纯 Clarification:")
print(pure_result)
print(
    "Route:",
    validation_route(pure_result)
)


# 2. 完整营业额 + 天气缺地点
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
        "unsupported": False,
        "unsupported_reason": "",
        "need_clarification": True,
        "clarification_reason": "天气查询缺少地点信息",
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

mixed_result = validation_node(
    mixed_state
)

print("\n================")
print("混合 Clarification 修改前:")
print(mixed_result)
print(
    "Route:",
    validation_route(mixed_result)
)


# 3. 锁定纯 Clarification 旧契约
assert pure_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": "天气查询缺少地点信息",
}

assert (
    validation_route(pure_result)
    == "clarification"
)


# 4. 锁定混合 Clarification 任务隔离
assert mixed_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": False,
    "clarification_reason": None,
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
    "Partial Clarification Validation "
    "契约: PASS"
)