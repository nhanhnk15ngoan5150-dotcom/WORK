from agent.langgraph_agent import run_langgraph_agent


# 1. 准备20轮问题
questions = [
    "五月牛肉卖了多少？",
    "六月三文鱼卖了多少？",
    "五月绿茶卖了多少？",
    "六月可乐卖了多少？",
    "五月鸡肉卖了多少？",
    "六月柚子茶卖了多少？",
    "五月抹茶拿铁卖了多少？",
    "六月毛豆卖了多少？",
    "五月炸鸡块卖了多少？",
    "六月味增汤卖了多少？",
    "五月煎饺卖了多少？",
    "六月小笼包卖了多少？",
    "五月灌汤包卖了多少？",
    "六月吞拿鱼三明治卖了多少？",
    "五月照烧三明治卖了多少？",
    "六月照烧鸡饭卖了多少？",
    "五月味增拉面卖了多少？",
    "六月豚骨拉面卖了多少？",
    "最近客单价怎么样？",
    "回到最开始牛肉那个查询，改成六月。",
]


# 2. 初始化上下文
conversation_history = []
structured_context = {}
structured_memory = []


# 3. 连续执行20轮
for index, question in enumerate(
    questions,
    start=1
):
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
        f"\n========== 第{index}轮 =========="
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
        "计划:",
        result["plan"]
    )

    print(
        "回答:",
        result["answer"]
    )

    print(
        "原始历史轮数:",
        len(conversation_history) // 2
    )

    print(
        "结构化记忆轮数:",
        len(structured_memory)
    )