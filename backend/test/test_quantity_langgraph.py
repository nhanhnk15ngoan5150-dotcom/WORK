from agent.langgraph_agent import run_langgraph_agent


# 1. 单轮销量查询
result_1 = run_langgraph_agent(
    "六月可乐卖了多少份？"
)

print(
    "\n================"
)

print(
    "问题:",
    "六月可乐卖了多少份？"
)

print(
    "理解:",
    result_1["understanding"]
)

print(
    "计划:",
    result_1["plan"]
)

print(
    "结果:",
    result_1["results"]
)

print(
    "回答:",
    result_1["answer"]
)

print(
    "成功:",
    result_1["success"]
)


# 2. 建立销售额上下文
result_2 = run_langgraph_agent(
    "可乐六月份卖的怎么样？"
)

print(
    "\n================"
)

print(
    "第一轮回答:",
    result_2["answer"]
)


# 3. 当前问题覆盖历史 metric
result_3 = run_langgraph_agent(
    "卖了多少份？",
    conversation_history=result_2["conversation_history"],
    structured_context=result_2["structured_context"],
    structured_memory=result_2["structured_memory"]
)

print(
    "第二轮理解:",
    result_3["understanding"]
)

print(
    "第二轮计划:",
    result_3["plan"]
)

print(
    "第二轮回答:",
    result_3["answer"]
)


# 4. 同一句查询销售额和销量
result_4 = run_langgraph_agent(
    "五月鸡肉卖了多少钱，多少份？"
)

print(
    "\n================"
)

print(
    "双指标理解:",
    result_4["understanding"]
)

print(
    "双指标计划:",
    result_4["plan"]
)

print(
    "双指标结果:",
    result_4["results"]
)

print(
    "双指标回答:",
    result_4["answer"]
)

print(
    "双指标成功:",
    result_4["success"]
)