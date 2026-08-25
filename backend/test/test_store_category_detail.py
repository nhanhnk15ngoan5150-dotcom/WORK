from agent.langgraph_agent import run_langgraph_agent


# 1. 第一轮查询五月各品类
first = run_langgraph_agent(
    question="五月各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)


# 2. 第二轮与六月比较
second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=first["conversation_history"],
    structured_context=first["structured_context"],
    structured_memory=first["structured_memory"]
)


# 3. 查看五月完整链路
print("\n================")
print("第一轮理解:", first["understanding"])
print("第一轮计划:", first["plan"])
print("第一轮结果:", first["results"])
print("第一轮回答:", first["answer"])


# 4. 查看跨月完整链路
print("\n================")
print("第二轮理解:", second["understanding"])
print("第二轮计划:", second["plan"])
print("第二轮结果:", second["results"])
print("第二轮回答:", second["answer"])
print("第二轮成功:", second["success"])