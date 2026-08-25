from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备商品歧义 + Unsupported
state = {
    "understanding": {
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["poke"],
                "time_expression": "六月",
                "metric": "销售额",
                "query_mode": "value",
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
            "intent": "product_sales",
            "products": [
                {
                    "original": "poke",
                    "input": "poke",
                    "standard": None,
                    "need_clarification": True,
                    "candidates": [
                        "牛肉poke",
                        "鸡肉poke",
                    ],
                }
            ],
            "time_expression": "六月",
            "metric": "销售额",
            "query_mode": "value",
        }
    ],
}


# 2. 执行当前 Validation
result = validation_node(
    state
)

print("\n================")
print("商品歧义 + Unsupported:")
print(result)

print(
    "Route:",
    validation_route(result)
)


# 3. 锁定商品澄清 + Unsupported 组合状态
assert result == {
    "unsupported": False,
    "unsupported_reason": None,
    "need_clarification": True,
    "clarification_reason": (
        "“poke”可能对应多个商品："
        "牛肉poke、鸡肉poke，请确认具体商品。；"
        "当前问题包含超出餐饮经营数据分析能力范围的请求（写诗）"
    ),
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
    "Entity Clarification + Unsupported "
    "契约: PASS"
)