from agent.langgraph_agent import run_langgraph_agent


# 1. 商品销售额趋势
sales_result = run_langgraph_agent(
    question="最近牛肉销售额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销售额 TREND")
print("理解:", sales_result["understanding"])
print("实体:", sales_result["entities"])
print("计划:", sales_result["plan"])
print("结果:", sales_result["results"])
print("回答:", sales_result["answer"])


# 2. 商品销量趋势
quantity_result = run_langgraph_agent(
    question="最近可乐销量变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销量 TREND")
print("理解:", quantity_result["understanding"])
print("实体:", quantity_result["entities"])
print("计划:", quantity_result["plan"])
print("结果:", quantity_result["results"])
print("回答:", quantity_result["answer"])


# 3. 商品普通值查询
value_result = run_langgraph_agent(
    question="最近牛肉卖了多少钱？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销售额 VALUE")
print("理解:", value_result["understanding"])
print("实体:", value_result["entities"])
print("计划:", value_result["plan"])
print("结果:", value_result["results"])
print("回答:", value_result["answer"])