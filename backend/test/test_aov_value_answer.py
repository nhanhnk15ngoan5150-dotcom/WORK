from agent.langgraph_agent import run_langgraph_agent


# 1. 明确月份客单价
may_result = run_langgraph_agent(
    question="五月客单价是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("五月 VALUE")
print("理解:", may_result["understanding"])
print("计划:", may_result["plan"])
print("结果:", may_result["results"])
print("回答:", may_result["answer"])
print("成功:", may_result["success"])
print("错误:", may_result["error"])


# 2. 最近客单价趋势回归
recent_result = run_langgraph_agent(
    question="最近客单价怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("最近 TREND")
print("理解:", recent_result["understanding"])
print("计划:", recent_result["plan"])
print("结果:", recent_result["results"])
print("回答:", recent_result["answer"])
print("成功:", recent_result["success"])
print("错误:", recent_result["error"])