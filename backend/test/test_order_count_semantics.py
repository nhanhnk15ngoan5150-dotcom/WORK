from agent.langgraph_agent import run_langgraph_agent


questions = [
    "五月有多少订单？",
    "六月订单量是多少？",
    "最近订单量怎么样？",
    "最近订单量变化怎么样？",
    "五月和六月订单数对比一下",
]


# 1. 订单量语义诊断
for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result["understanding"])
    print("实体:", result["entities"])
    print("计划:", result["plan"])
    print("结果:", result["results"])
    print("回答:", result["answer"])
    print("成功:", result["success"])
    print("错误:", result["error"])