from agent.langgraph_agent import run_langgraph_agent


# 1. 准备四轮上下文问题
questions = [
    "六月牛肉卖了多少？",
    "那五月呢？",
    "三文鱼呢？",
    "再看看六月。",
]


# 2. 初始化上下文
conversation_history = []
structured_context = {}
structured_memory = []


# 3. 连续执行四轮
for question in questions:
    result = run_langgraph_agent(
        question,
        conversation_history=conversation_history,
        structured_context=structured_context,
        structured_memory=structured_memory
    )

    conversation_history = result[
        "conversation_history"
    ]

    structured_context = result[
        "structured_context"
    ]

    structured_memory = result[
        "structured_memory"
    ]

    print(
        "\n================"
    )

    print(
        "问题:",
        question
    )

    print(
        "理解:",
        result["understanding"]
    )

    print(
        "结构化上下文:",
        structured_context
    )

    print(
        "结构化记忆轮数:",
        len(structured_memory)
    )

    if structured_memory:
        print(
            "最新结构化记忆:",
            structured_memory[-1]
        )

    print(
        "回答:",
        result["answer"]
    )