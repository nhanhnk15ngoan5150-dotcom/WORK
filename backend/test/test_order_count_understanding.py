from services.llm_service import understand_question


questions = [
    "五月有多少订单？",
    "六月订单量是多少？",
    "最近订单量怎么样？",
    "最近订单量变化怎么样？",
    "五月和六月订单数对比一下",
    "六月订单量比五月高还是低？",
]


# 1. 订单数语义
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
    "五月营业额是多少？",
    "六月可乐卖了多少份？",
    "最近客单价怎么样？",
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