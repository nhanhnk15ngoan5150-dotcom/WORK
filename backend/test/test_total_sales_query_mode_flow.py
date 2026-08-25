from agent.langgraph_agent import run_langgraph_agent


# 1. 单期总营业额
value_result = run_langgraph_agent(
    question="最近总营业额是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("VALUE")
print("理解:", value_result["understanding"])
print("实体:", value_result["entities"])
print("计划:", value_result["plan"])
print("结果:", value_result["results"])
print("回答:", value_result["answer"])


# 2. 最近营业额趋势
trend_result = run_langgraph_agent(
    question="最近总营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("TREND")
print("理解:", trend_result["understanding"])
print("实体:", trend_result["entities"])
print("计划:", trend_result["plan"])
print("结果:", trend_result["results"])
print("回答:", trend_result["answer"])