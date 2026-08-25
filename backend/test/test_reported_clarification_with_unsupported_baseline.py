from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备 LLM 已正确报告 Clarification + Unsupported
state = {
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
            "当前问题超出餐饮经营数据分析能力范围"
        ),
        "need_clarification": True,
        "clarification_reason": (
            "天气查询缺少地点信息"
        ),
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


# 2. 执行当前 Validation
result = validation_node(
    state
)

print("\n================")
print("Clarification + Unsupported:")
print(result)

print(
    "Route:",
    validation_route(result)
)


# 3. 锁定 Clarification + Unsupported 组合状态
assert result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "天气查询缺少地点信息；"
        "当前问题超出餐饮经营数据分析能力范围"
    ),
    "partial_unsupported": True,
    "partial_unsupported_reason": (
        "当前问题超出餐饮经营数据分析能力范围"
    ),
}

assert (
    validation_route(result)
    == "clarification"
)


print("\n================")
print(
    "Reported Clarification + Unsupported "
    "契约: PASS"
)