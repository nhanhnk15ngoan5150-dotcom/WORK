from agent.langgraph_agent import run_langgraph_agent


# 1. 准备完整链路测试问题
questions = [
    "五月营业额是多少？",
    "五月总营业额是多少？",
    "五月所有门店总营业额是多少？",
    "五月哪个品类门店营业额最高？",
    "最近总营业额是多少？",
    "四月总营业额是多少？",
]


# 2. 独立执行每个问题
for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    print(
        "\n================"
    )

    print(
        "问题:",
        question
    )

    print(
        "理解:",
        result.get("understanding")
    )

    print(
        "实体:",
        result.get("entities")
    )

    print(
        "计划:",
        result.get("plan")
    )

    print(
        "结果:",
        result.get("results")
    )

    print(
        "回答:",
        result.get("answer")
    )

    print(
        "成功:",
        result.get("success")
    )

    print(
        "错误:",
        result.get("error")
    )