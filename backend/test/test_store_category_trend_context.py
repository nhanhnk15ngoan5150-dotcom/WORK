from agent.langgraph_agent import run_langgraph_agent


# 1. detail value → trend
detail_first = run_langgraph_agent(
    question="最近各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("DETAIL 第一轮")
print("理解:", detail_first["understanding"])
print("回答:", detail_first["answer"])
print("上下文:", detail_first["structured_context"])
print("记忆:", detail_first["structured_memory"])


detail_second = run_langgraph_agent(
    question="那变化呢？",
    conversation_history=detail_first["conversation_history"],
    structured_context=detail_first["structured_context"],
    structured_memory=detail_first["structured_memory"]
)

print("\n================")
print("DETAIL 第二轮")
print("理解:", detail_second["understanding"])
print("实体:", detail_second["entities"])
print("计划:", detail_second["plan"])
print("结果:", detail_second["results"])
print("回答:", detail_second["answer"])
print("成功:", detail_second["success"])
print("错误:", detail_second["error"])
print("上下文:", detail_second["structured_context"])


# 2. top value → trend
top_first = run_langgraph_agent(
    question="最近哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("TOP 第一轮")
print("理解:", top_first["understanding"])
print("回答:", top_first["answer"])
print("上下文:", top_first["structured_context"])
print("记忆:", top_first["structured_memory"])


top_second = run_langgraph_agent(
    question="那变化呢？",
    conversation_history=top_first["conversation_history"],
    structured_context=top_first["structured_context"],
    structured_memory=top_first["structured_memory"]
)

print("\n================")
print("TOP 第二轮")
print("理解:", top_second["understanding"])
print("实体:", top_second["entities"])
print("计划:", top_second["plan"])
print("结果:", top_second["results"])
print("回答:", top_second["answer"])
print("成功:", top_second["success"])
print("错误:", top_second["error"])
print("上下文:", top_second["structured_context"])