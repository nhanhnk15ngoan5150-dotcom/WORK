from agent.nodes import (
    validation_node,
    validation_route,
)


# 1. 准备纯商品无法匹配任务
pure_state = {
    "understanding": {
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["不存在商品"],
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
                    "input": "不存在商品",
                    "original": "不存在商品",
                    "standard": None,
                    "method": "none",
                    "confidence": 0.2,
                    "need_clarification": False,
                    "candidates": [],
                }
            ],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "trend",
        }
    ],
}


# 2. 准备完整任务 + 商品无法匹配任务
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
                "products": ["不存在商品"],
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
                    "input": "不存在商品",
                    "original": "不存在商品",
                    "standard": None,
                    "method": "none",
                    "confidence": 0.2,
                    "need_clarification": False,
                    "candidates": [],
                }
            ],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "trend",
        },
    ],
}


# 3. 执行纯商品无法匹配
pure_result = validation_node(
    pure_state
)

print("\n================")
print("纯商品无法匹配:")
print(pure_result)
print(
    "Route:",
    validation_route(pure_result)
)


# 4. 执行完整任务 + 商品无法匹配
mixed_result = validation_node(
    mixed_state
)

print("\n================")
print("完整任务 + 商品无法匹配:")
print(mixed_result)
print(
    "Route:",
    validation_route(mixed_result)
)


expected_reason = (
    "没有找到与“不存在商品”对应的商品，"
    "请确认商品名称。"
)


# 5. 锁定纯商品无法匹配旧契约
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


# 6. 锁定 Mixed 商品无法匹配任务隔离
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
    "Unresolved Product 契约: PASS"
)