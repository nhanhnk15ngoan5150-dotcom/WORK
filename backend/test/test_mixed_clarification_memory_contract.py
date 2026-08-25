from agent.langgraph_agent import run_langgraph_agent


# 1. 准备已有成功业务上下文
original_context = {
    "intent": "product_sales",
    "time_expression": "五月",
    "metric": "销售额",
    "query_mode": "value",
    "products": ["可乐"],
}

original_memory = [
    {
        "question": "五月可乐销售额是多少？",
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["可乐"],
                "time_expression": "五月",
                "metric": "销售额",
                "query_mode": "value",
            }
        ],
    }
]


# 2. 执行完整任务 + 缺条件任务
result = run_langgraph_agent(
    question="最近总营业额变化怎么样？另外今天天气怎么样？",
    conversation_history=[],
    structured_context=original_context,
    structured_memory=original_memory,
)


print("\n================")
print("理解:")
print(result["understanding"])

print("\n计划:")
print(result["plan"])

print("\n结果:")
print(result["results"])

print("\n回答:")
print(result["answer"])

print("\n成功:")
print(result["success"])

print("\n错误:")
print(result["error"])

print("\n更新后 Context:")
print(result["structured_context"])

print("\n更新后 Memory:")
print(result["structured_memory"])


# 3. 锁定 Partial Clarification 状态
assert result["success"] is True

assert (
    result["error"]
    == "部分请求需要补充条件"
)

assert (
    "151572"
    in result["answer"]
)

assert (
    "天气查询缺少地点信息"
    in result["answer"]
)


# 4. 锁定缺条件天气没有进入执行计划
assert len(result["plan"]) == 1

assert (
    result["plan"][0]["intent"]
    == "total_sales"
)

assert all(
    task.get("intent") != "weather_info"
    for task in result["plan"]
)


# 5. 锁定业务 Context 不更新
assert (
    result["structured_context"]
    == original_context
)


# 6. 锁定业务 Memory 不更新
assert (
    result["structured_memory"]
    == original_memory
)


print("\n================")
print(
    "Mixed Clarification Memory "
    "隔离契约: PASS"
)