from agent.langgraph_agent import run_langgraph_agent


# 1. 最近各品类营业额变化
detail_result = run_langgraph_agent(
    question="最近各品类营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近各品类营业额变化怎么样？")
print("理解:", detail_result["understanding"])
print("实体:", detail_result["entities"])
print("计划:", detail_result["plan"])
print("结果:", detail_result["results"])
print("回答:", detail_result["answer"])
print("成功:", detail_result["success"])
print("错误:", detail_result["error"])


# 2. 最近最高品类
top_result = run_langgraph_agent(
    question="最近哪个品类营业额最高？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近哪个品类营业额最高？")
print("理解:", top_result["understanding"])
print("实体:", top_result["entities"])
print("计划:", top_result["plan"])
print("结果:", top_result["results"])
print("回答:", top_result["answer"])
print("成功:", top_result["success"])
print("错误:", top_result["error"])