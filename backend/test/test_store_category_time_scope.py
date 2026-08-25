from services.llm_service import understand_question


# 1. 准备时间作用域测试
questions = [
    "五月总营业额是多少，哪个品类门店营业额最高？",
    "五月总营业额是多少，六月哪个品类营业额最高？",
    "五月总营业额是多少，同时看看当月哪个品类营业额最高？",
    "六月牛肉和三文鱼卖了多少，哪个品类门店营业额最高？",
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