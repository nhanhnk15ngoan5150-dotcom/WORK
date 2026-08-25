from agent.langgraph_agent import run_langgraph_agent


# 1. 准备测试问题
questions = [
    "哪个品类门店营业额最高？",
    "最近客单价怎么样？",
    "六月牛肉卖了多少？",
    "六月牛肉卖了多少，最近客单价怎么样？",
    "六月牛肉和三文鱼卖了多少，哪个品类门店营业额最高？",
]


# 2. 执行测试
for question in questions:
    result = run_langgraph_agent(
        question
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
        result.get(
            "understanding"
        )
    )

    print(
        "计划:",
        result.get(
            "plan"
        )
    )

    print(
        "回答:",
        result.get(
            "answer"
        )
    )

    print(
        "成功:",
        result.get(
            "success"
        )
    )