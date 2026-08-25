from agent.nodes import (
    validation_node,
    planner_node,
    executor_node,
    answer_node,
)


# 1. 准备支持 + Unsupported + Clarification 混合状态
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
                "intent": "weather_info",
                "products": [],
                "location": "",
                "time_expression": "今天",
                "metric": "天气",
                "weather_query": "general",
            },
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


# 2. 执行 Validation
validation_result = validation_node(
    state
)

merged_state = {
    **state,
    **validation_result,
}


# 3. 执行 Planner
planner_result = planner_node(
    merged_state
)

merged_state.update(
    planner_result
)


# 4. 执行 Executor
executor_result = executor_node(
    merged_state
)

merged_state.update(
    executor_result
)


# 5. 执行 Answer
answer_result = answer_node(
    merged_state
)


print("\n================")
print("Validation:")
print(validation_result)

print("\nPlan:")
print(planner_result)

print("\nResults:")
print(executor_result)

print("\nAnswer:")
print(answer_result)


# 6. 观察组合状态下游行为
print("\npartial_unsupported:")
print(
    merged_state.get(
        "partial_unsupported"
    )
)

print("\npartial_clarification:")
print(
    merged_state.get(
        "partial_clarification"
    )
)

# 6. 锁定组合 Partial 状态
assert validation_result[
    "partial_unsupported"
] is True

assert validation_result[
    "partial_clarification"
] is True

assert (
    validation_result[
        "partial_unsupported_reason"
    ]
    == "当前问题超出餐饮经营数据分析能力范围"
)

assert (
    validation_result[
        "partial_clarification_reason"
    ]
    == "天气查询缺少地点信息"
)


# 7. 锁定只执行完整业务任务
assert len(
    planner_result["plan"]
) == 1

assert (
    planner_result[
        "plan"
    ][0]["intent"]
    == "total_sales"
)

assert all(
    task.get("intent")
    != "weather_info"
    for task in planner_result["plan"]
)


# 8. 锁定组合状态回答
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
    "当前问题超出餐饮经营数据分析能力范围"
    in answer_result["answer"]
)

assert (
    "天气查询缺少地点信息"
    in answer_result["answer"]
)


print("\n================")
print(
    "Combined Partial State "
    "执行链契约: PASS"
)