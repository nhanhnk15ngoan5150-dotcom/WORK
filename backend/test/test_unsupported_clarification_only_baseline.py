from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备 Unsupported + Weather 缺地点
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


# 2. 执行 Validation
result = validation_node(
    state
)

print("\n================")
print("Validation:")
print(result)

print(
    "Route:",
    validation_route(result)
)


# 3. 锁定无可执行任务时的组合澄清
expected_reason = (
    "天气查询缺少地点信息；"
    "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
)

assert result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": expected_reason,
    "partial_unsupported": True,
    "partial_unsupported_reason": (
        "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
    ),
}

assert (
    validation_route(result)
    == "clarification"
)


print("\n================")
print(
    "Unsupported + Clarification Only "
    "Validation 契约: PASS"
)