from services.llm_service import understand_question


# 1. 测试总营业额表达
questions = [
    "五月营业额是多少？",
    "五月总营业额是多少？",
    "五月所有门店总营业额是多少？",
    "五月哪个品类门店营业额最高？",
]


# 2. 执行 Understanding
for question in questions:
    result = understand_question(
        question,
        [],
        {},
        []
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
        result
    )