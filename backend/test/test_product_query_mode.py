from services.llm_service import understand_question


# 1. 商品销售额单期
sales_value = understand_question(
    question="最近牛肉卖了多少钱？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销售额 VALUE:", sales_value)


# 2. 商品销售额趋势
sales_trend = understand_question(
    question="最近牛肉销售额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销售额 TREND:", sales_trend)


# 3. 商品销量单期
quantity_value = understand_question(
    question="最近可乐卖了多少份？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销量 VALUE:", quantity_value)


# 4. 商品销量趋势
quantity_trend = understand_question(
    question="最近可乐销量变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("销量 TREND:", quantity_trend)


# 5. 品类 query_mode 回归
category_result = understand_question(
    question="五月各品类营业额怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("品类回归:", category_result)


# 6. 总营业额 query_mode 回归
total_result = understand_question(
    question="最近总营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("总营业额回归:", total_result)