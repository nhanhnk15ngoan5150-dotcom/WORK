from services.llm_service import understand_question


# 1. 准备品类查询模式测试
questions = [
    "五月哪个品类营业额最高？",
    "五月各品类营业额怎么样？",
    "五月所有品类营业额分别是多少？",
    "五月营业额最高的品类是什么？",
]


# 2. 执行 Understanding
for question in questions:
    result = understand_question(
        question,
        [],
        {},
        []
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result)