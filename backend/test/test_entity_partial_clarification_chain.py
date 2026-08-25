from agent.nodes import (
    validation_node,
    planner_node,
    executor_node,
    answer_node,
)


def run_chain(state):
    # 1. 执行 Validation
    validation_result = validation_node(
        state
    )

    merged_state = {
        **state,
        **validation_result,
    }

    # 2. 执行 Planner
    planner_result = planner_node(
        merged_state
    )

    merged_state.update(
        planner_result
    )

    # 3. 执行 Executor
    executor_result = executor_node(
        merged_state
    )

    merged_state.update(
        executor_result
    )

    # 4. 执行 Answer
    answer_result = answer_node(
        merged_state
    )

    return {
        "validation": validation_result,
        "planner": planner_result,
        "executor": executor_result,
        "answer": answer_result,
    }


# 5. 完整营业额 + 商品歧义
ambiguous_state = {
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

ambiguous_result = run_chain(
    ambiguous_state
)

print("\n================")
print("商品歧义链路:")
print("Validation:", ambiguous_result["validation"])
print("Plan:", ambiguous_result["planner"])
print("Results:", ambiguous_result["executor"])
print("Answer:", ambiguous_result["answer"])


# 6. 完整营业额 + 商品无法匹配
unresolved_state = {
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

unresolved_result = run_chain(
    unresolved_state
)

print("\n================")
print("商品无法匹配链路:")
print("Validation:", unresolved_result["validation"])
print("Plan:", unresolved_result["planner"])
print("Results:", unresolved_result["executor"])
print("Answer:", unresolved_result["answer"])


# 7. 锁定商品歧义下游链路
assert (
    ambiguous_result["planner"]["plan"][0]["intent"]
    == "total_sales"
)

assert len(
    ambiguous_result["planner"]["plan"]
) == 1

assert (
    ambiguous_result["answer"]["success"]
    is True
)

assert (
    ambiguous_result["answer"]["error"]
    == "部分请求需要补充条件"
)

assert (
    "151572"
    in ambiguous_result["answer"]["answer"]
)

assert (
    "牛肉poke、鸡肉poke"
    in ambiguous_result["answer"]["answer"]
)


# 8. 锁定商品无法匹配下游链路
assert (
    unresolved_result["planner"]["plan"][0]["intent"]
    == "total_sales"
)

assert len(
    unresolved_result["planner"]["plan"]
) == 1

assert (
    unresolved_result["answer"]["success"]
    is True
)

assert (
    unresolved_result["answer"]["error"]
    == "部分请求需要补充条件"
)

assert (
    "151572"
    in unresolved_result["answer"]["answer"]
)

assert (
    "不存在商品"
    in unresolved_result["answer"]["answer"]
)


print("\n================")
print(
    "Entity Partial Clarification "
    "执行链契约: PASS"
)