from services.llm_service import understand_question


# 1. 最近最高品类
top_value = understand_question(
    question="最近哪个品类营业额最高？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("TOP VALUE:", top_value)


# 2. 最近各品类明细
detail_value = understand_question(
    question="最近各品类营业额怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("DETAIL VALUE:", detail_value)


# 3. 最近各品类趋势
detail_trend = understand_question(
    question="最近各品类营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("DETAIL TREND:", detail_trend)


# 4. 明确月份品类回归
month_detail = understand_question(
    question="五月各品类营业额怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("MONTH DETAIL:", month_detail)


# 5. 总营业额趋势回归
total_trend = understand_question(
    question="最近总营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("TOTAL TREND:", total_trend)


# 6. 商品趋势回归
product_trend = understand_question(
    question="最近牛肉销售额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("PRODUCT TREND:", product_trend)