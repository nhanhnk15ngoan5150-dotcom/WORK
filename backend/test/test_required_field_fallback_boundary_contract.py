from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. Weather 条件完整
normal_weather_state = {
    "understanding": {
        "tasks": [
            {
                "intent": "weather_info",
                "products": [],
                "location": "北京",
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
            "location": "北京",
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        }
    ],
}


# 2. Weather 缺地点，LLM 已正确要求澄清
reported_missing_state = {
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


# 3. Weather 缺地点，LLM 漏报澄清
missed_missing_state = {
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


# 4. Weather 缺地点 + Unsupported，LLM 漏报澄清
unsupported_missing_state = {
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
        "unsupported": True,
        "unsupported_reason": (
            "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
        ),
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


normal_result = validation_node(
    normal_weather_state
)

reported_result = validation_node(
    reported_missing_state
)

missed_result = validation_node(
    missed_missing_state
)

unsupported_missing_result = validation_node(
    unsupported_missing_state
)


# 5. 打印修改前边界
print("\n================")
print("Weather 条件完整:")
print(normal_result)
print("Route:", validation_route(normal_result))

print("\n================")
print("Weather 缺地点，LLM 已正确澄清:")
print(reported_result)
print("Route:", validation_route(reported_result))

print("\n================")
print("Weather 缺地点，LLM 漏报:")
print(missed_result)
print("Route:", validation_route(missed_result))

print("\n================")
print("Weather 缺地点 + Unsupported，LLM 漏报:")
print(unsupported_missing_result)
print(
    "Route:",
    validation_route(
        unsupported_missing_result
    )
)


# 6. 锁定正常 Weather 旧契约
assert normal_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": False,
    "clarification_reason": None,
}

assert (
    validation_route(normal_result)
    == "planner"
)


# 7. 锁定 LLM 正确澄清旧契约
assert reported_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "天气查询缺少地点信息"
    ),
}

assert (
    validation_route(reported_result)
    == "clarification"
)


# 8. 锁定 LLM 漏报兜底
assert missed_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "天气查询缺少地点信息"
    ),
}

assert (
    validation_route(missed_result)
    == "clarification"
)


# 9. 锁定 Unsupported + 缺条件组合澄清
assert unsupported_missing_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "天气查询缺少地点信息；"
        "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
    ),
    "partial_unsupported": True,
    "partial_unsupported_reason": (
        "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
    ),
}

assert (
    validation_route(
        unsupported_missing_result
    )
    == "clarification"
)


print("\n================")
print(
    "Required Field Fallback "
    "边界契约: PASS"
)