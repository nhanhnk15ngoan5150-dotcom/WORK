from agent.langgraph_agent import run_langgraph_agent


# 1. 各品类趋势
trend_result = run_langgraph_agent(
    question="最近各品类营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("DETAIL TREND")
print("理解:", trend_result["understanding"])
print("实体:", trend_result["entities"])
print("计划:", trend_result["plan"])
print("结果:", trend_result["results"])
print("回答:", trend_result["answer"])


# 2. 各品类单期
detail_result = run_langgraph_agent(
    question="最近各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("DETAIL VALUE")
print("理解:", detail_result["understanding"])
print("实体:", detail_result["entities"])
print("计划:", detail_result["plan"])
print("结果:", detail_result["results"])
print("回答:", detail_result["answer"])


# 3. 最高品类单期
top_result = run_langgraph_agent(
    question="最近哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("TOP VALUE")
print("理解:", top_result["understanding"])
print("实体:", top_result["entities"])
print("计划:", top_result["plan"])
print("结果:", top_result["results"])
print("回答:", top_result["answer"])