from agent.langgraph_agent import run_langgraph_agent


# 1. 最近总营业额
current_result = run_langgraph_agent(
    question="最近总营业额是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近总营业额是多少？")
print("理解:", current_result["understanding"])
print("计划:", current_result["plan"])
print("结果:", current_result["results"])
print("回答:", current_result["answer"])
print("成功:", current_result["success"])
print("错误:", current_result["error"])


# 2. 最近总营业额变化
trend_result = run_langgraph_agent(
    question="最近总营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近总营业额变化怎么样？")
print("理解:", trend_result["understanding"])
print("计划:", trend_result["plan"])
print("结果:", trend_result["results"])
print("回答:", trend_result["answer"])
print("成功:", trend_result["success"])
print("错误:", trend_result["error"])