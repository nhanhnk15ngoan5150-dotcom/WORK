from services.llm_service import understand_question


questions = [
    "北京今天天气怎么样？",
    "上海明天天气怎么样？",
    "最近有什么餐饮行业新闻？",
    "最近有什么食品安全新闻？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. 外部信息 Understanding
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


# 2. 能力外问题回归
unsupported_result = understand_question(
    question="帮我写一首诗。",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("能力外回归: 帮我写一首诗。")
print("理解:", unsupported_result)


# 3. 内部能力回归
regressions = [
    "最近总营业额变化怎么样？",
    "最近订单量变化怎么样？",
    "最近牛肉销售额变化怎么样？",
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
    print("内部回归:", question)
    print("理解:", result)