from agent.langgraph_agent import run_langgraph_agent


# 1. 第一轮查询五月品类营业额
first = run_langgraph_agent(
    question="五月哪个品类门店营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)


# 2. 第二轮要求与六月比较
second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=first["conversation_history"],
    structured_context=first["structured_context"],
    structured_memory=first["structured_memory"]
)


# 3. 查看完整链路
print("\n================")
print("第一轮理解:", first["understanding"])
print("第一轮计划:", first["plan"])
print("第一轮结果:", first["results"])
print("第一轮回答:", first["answer"])
print("第一轮上下文:", first["structured_context"])

print("\n第二轮理解:", second["understanding"])
print("第二轮计划:", second["plan"])
print("第二轮结果:", second["results"])
print("第二轮回答:", second["answer"])
print("第二轮成功:", second["success"])
print("第二轮错误:", second["error"])