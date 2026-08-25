from agent.langgraph_agent import run_langgraph_agent


# 1. 趋势模式写入结构化记忆
trend_result = run_langgraph_agent(
    question="最近各品类营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("趋势理解:", trend_result["understanding"])
print("趋势上下文:", trend_result["structured_context"])
print("趋势记忆:", trend_result["structured_memory"])


# 2. 普通模式写入结构化记忆
value_result = run_langgraph_agent(
    question="最近哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("普通理解:", value_result["understanding"])
print("普通上下文:", value_result["structured_context"])
print("普通记忆:", value_result["structured_memory"])