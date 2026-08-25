from agent.langgraph_agent import run_langgraph_agent


# 1. detail 模式
detail = run_langgraph_agent(
    question="五月各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("detail 理解:", detail["understanding"])
print("detail 上下文:", detail["structured_context"])
print("detail 结构化记忆:", detail["structured_memory"])


# 2. top 模式
top = run_langgraph_agent(
    question="五月哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("top 理解:", top["understanding"])
print("top 上下文:", top["structured_context"])
print("top 结构化记忆:", top["structured_memory"])