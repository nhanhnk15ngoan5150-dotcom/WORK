from agent.langgraph_agent import run_langgraph_agent


# 1. 测试最近商品销售额
sales_result = run_langgraph_agent(
    question="最近牛肉卖了多少钱？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近牛肉卖了多少钱？")
print("理解:", sales_result["understanding"])
print("计划:", sales_result["plan"])
print("结果:", sales_result["results"])
print("回答:", sales_result["answer"])
print("成功:", sales_result["success"])
print("错误:", sales_result["error"])


# 2. 测试最近商品销量
quantity_result = run_langgraph_agent(
    question="最近可乐卖了多少份？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("问题: 最近可乐卖了多少份？")
print("理解:", quantity_result["understanding"])
print("计划:", quantity_result["plan"])
print("结果:", quantity_result["results"])
print("回答:", quantity_result["answer"])
print("成功:", quantity_result["success"])
print("错误:", quantity_result["error"])