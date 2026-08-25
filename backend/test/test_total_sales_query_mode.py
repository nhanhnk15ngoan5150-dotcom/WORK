from services.llm_service import understand_question


# 1. 单期总营业额
value_result = understand_question(
    question="最近总营业额是多少？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("value:", value_result)


# 2. 最近营业额变化
trend_result = understand_question(
    question="最近总营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("trend:", trend_result)


# 3. 普通月份总营业额
month_result = understand_question(
    question="五月总营业额是多少？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("month:", month_result)


# 4. 品类查询回归
category_result = understand_question(
    question="五月各品类营业额怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("category:", category_result)