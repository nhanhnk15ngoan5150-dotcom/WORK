from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 纯不支持请求
pure_state = {
    "understanding": {
        "tasks": [],
        "unsupported": True,
        "unsupported_reason": "当前问题超出餐饮经营数据分析能力范围",
        "need_clarification": False,
        "clarification_reason": "",
    },
    "entities": [],
}

pure_result = validation_node(
    pure_state
)

print("\n================")
print("纯 Unsupported:")
print(pure_result)
print(
    "Route:",
    validation_route(pure_result)
)


# 2. 混合支持和不支持请求
mixed_state = {
    "understanding": {
        "tasks": [
            {
                "intent": "total_sales",
                "products": [],
                "time_expression": "最近",
                "metric": "营业额",
                "query_mode": "trend",
            }
        ],
        "unsupported": True,
        "unsupported_reason": "当前问题超出餐饮经营数据分析能力范围",
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
        }
    ],
}

mixed_result = validation_node(
    mixed_state
)

print("\n================")
print("混合 Unsupported 修改前:")
print(mixed_result)
print(
    "Route:",
    validation_route(mixed_result)
)


# 3. 锁定纯 Unsupported 旧契约
assert pure_result == {
    "unsupported": True,
    "unsupported_reason": "当前问题超出餐饮经营数据分析能力范围",
    "need_clarification": False,
    "clarification_reason": None,
}

assert (
    validation_route(pure_result)
    == "unsupported"
)


# 4. 锁定当前混合请求被整体拦截
assert mixed_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": False,
    "clarification_reason": None,
    "partial_unsupported": True,
    "partial_unsupported_reason": (
        "当前问题超出餐饮经营数据分析能力范围"
    ),
}

assert (
    validation_route(mixed_result)
    == "planner"
)

print("\n================")
print("Unsupported Validation 契约: PASS")