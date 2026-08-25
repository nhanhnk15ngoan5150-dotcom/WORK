from agent.langgraph_agent import run_langgraph_agent


# 1. 准备时间范围测试
questions = [
    "四月哪个品类门店营业额最高？",
    "五月哪个品类门店营业额最高？",
    "七月哪个品类门店营业额最高？",
    "八月哪个品类门店营业额最高？",
]


# 2. 执行完整 LangGraph
for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result.get("understanding"))
    print("计划:", result.get("plan"))
    print("结果:", result.get("results"))
    print("回答:", result.get("answer"))
    print("成功:", result.get("success"))
    print("错误:", result.get("error"))