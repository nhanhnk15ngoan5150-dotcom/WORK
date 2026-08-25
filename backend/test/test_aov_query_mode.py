from services.llm_service import understand_question


questions = [
    "五月客单价是多少？",
    "五月和六月客单价对比一下",
    "六月客单价比五月高还是低？",
    "最近客单价怎么样？",
    "最近客单价变化怎么样？",
]


# 1. 客单价 query_mode 语义
for question in questions:
    result = understand_question(
        question=question,
        history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result)


# 2. 已有能力回归
regressions = [
    "最近总营业额变化怎么样？",
    "最近牛肉销售额变化怎么样？",
    "最近各品类营业额变化怎么样？",
]

for question in regressions:
    result = understand_question(
        question=question,
        history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("回归:", question)
    print("理解:", result)