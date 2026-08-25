from agent.langgraph_agent import run_langgraph_agent


# 1. 测试 detail 模式跨月继承
first = run_langgraph_agent(
    question="五月各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=first["conversation_history"],
    structured_context=first["structured_context"],
    structured_memory=first["structured_memory"]
)

print("\n================")
print("detail 第一轮理解:", first["understanding"])
print("detail 第一轮上下文:", first["structured_context"])
print("detail 第二轮理解:", second["understanding"])


# 2. 测试 top 模式跨月继承
first = run_langgraph_agent(
    question="五月哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=first["conversation_history"],
    structured_context=first["structured_context"],
    structured_memory=first["structured_memory"]
)

print("\n================")
print("top 第一轮理解:", first["understanding"])
print("top 第一轮上下文:", first["structured_context"])
print("top 第二轮理解:", second["understanding"])