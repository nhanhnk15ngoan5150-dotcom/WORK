from services.llm_service import understand_question


questions = [
    "北京今天天气怎么样？",
    "上海明天天气怎么样？",
    "北京今天会下雨吗？",
    "上海明天有雨吗？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. 天气子意图
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


# 2. 内部能力回归
result = understand_question(
    question="最近总营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("内部回归:", result)