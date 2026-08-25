from agent.langgraph_agent import run_langgraph_agent


# 1. 建立最开始的订单数查询
result = run_langgraph_agent(
    question="五月有多少订单？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("第1轮理解:", result["understanding"])
print("第1轮回答:", result["answer"])
print("第1轮上下文:", result["structured_context"])
print("第1轮记忆:", result["structured_memory"])


# 2. 插入18轮其他业务查询
for index in range(18):
    result = run_langgraph_agent(
        question="六月可乐卖了多少份？",
        conversation_history=result["conversation_history"],
        structured_context=result["structured_context"],
        structured_memory=result["structured_memory"]
    )


# 3. 仅依赖结构化记忆恢复订单数查询
final_result = run_langgraph_agent(
    question="回到最开始那个订单查询，和六月比呢？",
    conversation_history=[],
    structured_context={},
    structured_memory=result["structured_memory"]
)

print("\n================")
print("最终理解:", final_result["understanding"])
print("最终实体:", final_result["entities"])
print("最终计划:", final_result["plan"])
print("最终结果:", final_result["results"])
print("最终回答:", final_result["answer"])
print("最终上下文:", final_result["structured_context"])
print("记忆长度:", len(final_result["structured_memory"]))
print("成功:", final_result["success"])
print("错误:", final_result["error"])