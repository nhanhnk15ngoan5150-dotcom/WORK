from services.llm_service import understand_question


# 1. 连续测试普通商品销售额语义
for index in range(5):
    result = understand_question(
        question="六月牛肉卖了多少？",
        history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("轮次:", index + 1)
    print("理解:", result)