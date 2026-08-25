from agent.langgraph_agent import run_langgraph_agent


# 1. 销售额 value → trend
sales_first = run_langgraph_agent(
    question="最近牛肉卖了多少钱？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销售额第一轮")
print("理解:", sales_first["understanding"])
print("计划:", sales_first["plan"])
print("回答:", sales_first["answer"])
print("上下文:", sales_first["structured_context"])
print("记忆:", sales_first["structured_memory"])


sales_second = run_langgraph_agent(
    question="那变化呢？",
    conversation_history=sales_first["conversation_history"],
    structured_context=sales_first["structured_context"],
    structured_memory=sales_first["structured_memory"]
)

print("\n================")
print("销售额第二轮")
print("理解:", sales_second["understanding"])
print("实体:", sales_second["entities"])
print("计划:", sales_second["plan"])
print("结果:", sales_second["results"])
print("回答:", sales_second["answer"])
print("成功:", sales_second["success"])
print("错误:", sales_second["error"])
print("上下文:", sales_second["structured_context"])


# 2. 销量 value → trend
quantity_first = run_langgraph_agent(
    question="最近可乐卖了多少份？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销量第一轮")
print("理解:", quantity_first["understanding"])
print("计划:", quantity_first["plan"])
print("回答:", quantity_first["answer"])
print("上下文:", quantity_first["structured_context"])


quantity_second = run_langgraph_agent(
    question="那变化呢？",
    conversation_history=quantity_first["conversation_history"],
    structured_context=quantity_first["structured_context"],
    structured_memory=quantity_first["structured_memory"]
)

print("\n================")
print("销量第二轮")
print("理解:", quantity_second["understanding"])
print("实体:", quantity_second["entities"])
print("计划:", quantity_second["plan"])
print("结果:", quantity_second["results"])
print("回答:", quantity_second["answer"])
print("成功:", quantity_second["success"])
print("错误:", quantity_second["error"])
print("上下文:", quantity_second["structured_context"])