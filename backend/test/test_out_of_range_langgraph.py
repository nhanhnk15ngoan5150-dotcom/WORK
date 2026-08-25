from agent.langgraph_agent import run_langgraph_agent


# 1. 四月销售额
result_1 = run_langgraph_agent(
    "四月可乐卖了多少钱？"
)

print(
    "\n================"
)

print(
    "问题:",
    "四月可乐卖了多少钱？"
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


# 2. 四月销量
result_2 = run_langgraph_agent(
    "四月可乐卖了多少份？"
)

print(
    "\n================"
)

print(
    "问题:",
    "四月可乐卖了多少份？"
)

print(
    "理解:",
    result_2["understanding"]
)

print(
    "计划:",
    result_2["plan"]
)

print(
    "结果:",
    result_2["results"]
)

print(
    "回答:",
    result_2["answer"]
)

print(
    "成功:",
    result_2["success"]
)


# 3. 五月正常回归
result_3 = run_langgraph_agent(
    "五月可乐卖了多少钱？"
)

print(
    "\n================"
)

print(
    "问题:",
    "五月可乐卖了多少钱？"
)

print(
    "回答:",
    result_3["answer"]
)

print(
    "成功:",
    result_3["success"]
)