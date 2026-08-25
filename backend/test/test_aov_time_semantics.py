from agent.langgraph_agent import run_langgraph_agent


questions = [
    "五月客单价是多少？",
    "五月和六月客单价对比一下",
    "六月客单价比五月高还是低？",
    "最近客单价怎么样？",
]


# 1. 客单价时间语义诊断
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