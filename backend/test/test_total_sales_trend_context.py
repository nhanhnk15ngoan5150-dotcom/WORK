from agent.langgraph_agent import run_langgraph_agent


# 1. 第一轮查询最近总营业额
first_result = run_langgraph_agent(
    question="最近总营业额是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("第一轮问题: 最近总营业额是多少？")
print("第一轮理解:", first_result["understanding"])
print("第一轮计划:", first_result["plan"])
print("第一轮回答:", first_result["answer"])
print("第一轮上下文:", first_result["structured_context"])
print("第一轮记忆:", first_result["structured_memory"])


# 2. 第二轮切换为趋势查询
second_result = run_langgraph_agent(
    question="那变化呢？",
    conversation_history=first_result["conversation_history"],
    structured_context=first_result["structured_context"],
    structured_memory=first_result["structured_memory"]
)

print("\n================")
print("第二轮问题: 那变化呢？")
print("第二轮理解:", second_result["understanding"])
print("第二轮计划:", second_result["plan"])
print("第二轮结果:", second_result["results"])
print("第二轮回答:", second_result["answer"])
print("第二轮成功:", second_result["success"])
print("第二轮错误:", second_result["error"])
print("第二轮上下文:", second_result["structured_context"])