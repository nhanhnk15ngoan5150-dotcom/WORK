from agent.nodes import (
    validation_node,
    validation_route,
    planner_node,
    executor_node,
    answer_node,
)


# 1. 准备完整任务 + 商品歧义 + Unsupported
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
                "intent": "product_sales",
                "products": ["poke"],
                "time_expression": "六月",
                "metric": "销售额",
                "query_mode": "value",
            },
        ],
        "unsupported": True,
        "unsupported_reason": (
            "当前问题超出餐饮经营数据分析能力范围"
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
            "intent": "product_sales",
            "products": [
                {
                    "input": "poke",
                    "original": "poke",
                    "standard": None,
                    "method": "ambiguous",
                    "confidence": 0.0,
                    "need_clarification": True,
                    "candidates": [
                        "三文鱼poke",
                        "鸡肉poke",
                        "牛肉poke",
                    ],
                }
            ],
            "time_expression": "六月",
            "metric": "销售额",
            "query_mode": "value",
        },
    ],
}


# 2. 执行 Validation
validation_result = validation_node(
    state
)

merged_state = {
    **state,
    **validation_result,
}

print("\n================")
print("Validation:")
print(validation_result)

print(
    "Route:",
    validation_route(
        merged_state
    )
)


# 3. 执行 Planner
planner_result = planner_node(
    merged_state
)

merged_state.update(
    planner_result
)

print("\nPlan:")
print(planner_result)


# 4. 执行 Executor
executor_result = executor_node(
    merged_state
)

merged_state.update(
    executor_result
)

print("\nResults:")
print(executor_result)


# 5. 执行 Answer
answer_result = answer_node(
    merged_state
)

print("\nAnswer:")
print(answer_result)


# 6. 锁定三状态组合
assert (
    validation_result.get(
        "partial_unsupported"
    )
    is True
)

assert (
    validation_result.get(
        "partial_clarification"
    )
    is True
)

assert (
    validation_result.get(
        "validated_entities"
    )
    == [
        state["entities"][0]
    ]
)


# 7. 锁定只有完整任务进入执行
assert (
    validation_route(
        merged_state
    )
    == "planner"
)

assert len(
    planner_result["plan"]
) == 1

assert (
    planner_result["plan"][0]["intent"]
    == "total_sales"
)


# 8. 锁定业务任务正常完成
assert len(
    executor_result["results"]
) == 1

assert (
    executor_result["results"][0]["result"]["success"]
    is True
)


# 9. 锁定最终回答同时保留三类信息
assert (
    answer_result["success"]
    is True
)

assert (
    answer_result["error"]
    == "部分请求超出能力范围"
)

assert (
    "151572"
    in answer_result["answer"]
)

assert (
    "poke"
    in answer_result["answer"]
)

assert (
    "请确认具体商品"
    in answer_result["answer"]
)

assert (
    "超出餐饮经营数据分析能力范围"
    in answer_result["answer"]
)


print("\n================")
print(
    "Combined Entity Partial State "
    "执行链契约: PASS"
)