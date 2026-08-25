from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备纯商品歧义任务
pure_state = {
    "understanding": {
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["poke"],
                "time_expression": "最近",
                "metric": "销售额",
                "query_mode": "trend",
            }
        ],
        "unsupported": False,
        "unsupported_reason": "",
        "need_clarification": False,
        "clarification_reason": "",
    },
    "entities": [
        {
            "intent": "product_sales",
            "products": [
                {
                    "input": "poke",
                    "original": "poke",
                    "standard": None,
                    "method": "ambiguous",
                    "confidence": 0.6,
                    "need_clarification": True,
                    "candidates": [
                        "牛肉poke",
                        "鸡肉poke",
                    ],
                }
            ],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "trend",
        }
    ],
}


# 2. 准备完整任务 + 商品歧义任务
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
                "intent": "product_sales",
                "products": ["poke"],
                "time_expression": "最近",
                "metric": "销售额",
                "query_mode": "trend",
            },
        ],
        "unsupported": False,
        "unsupported_reason": "",
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
            "intent": "product_sales",
            "products": [
                {
                    "input": "poke",
                    "original": "poke",
                    "standard": None,
                    "method": "ambiguous",
                    "confidence": 0.6,
                    "need_clarification": True,
                    "candidates": [
                        "牛肉poke",
                        "鸡肉poke",
                    ],
                }
            ],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "trend",
        },
    ],
}


# 3. 执行 Pure Entity Clarification
pure_result = validation_node(
    pure_state
)

print("\n================")
print("纯商品歧义:")
print(pure_result)
print(
    "Route:",
    validation_route(pure_result)
)


# 4. 执行 Mixed Entity Clarification
mixed_result = validation_node(
    mixed_state
)

print("\n================")
print("完整任务 + 商品歧义:")
print(mixed_result)
print(
    "Route:",
    validation_route(mixed_result)
)


expected_reason = (
    "“poke”可能对应多个商品："
    "牛肉poke、鸡肉poke，请确认具体商品。"
)


# 5. 锁定纯商品歧义旧契约
assert pure_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": expected_reason,
}

assert (
    validation_route(pure_result)
    == "clarification"
)


# 6. 锁定 Mixed 商品歧义任务隔离
assert mixed_result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": False,
    "clarification_reason": None,
    "partial_clarification": True,
    "partial_clarification_reason": expected_reason,
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
    "Entity Clarification 契约: PASS"
)