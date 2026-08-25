from services.llm_service import understand_question
from agent.nodes import entity_node


questions = [
    "北京今天天气怎么样？",
    "最近有什么餐饮行业新闻？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. 外部信息 Entity 透传
for question in questions:
    understanding = understand_question(
        question=question,
        history=[],
        structured_context={},
        structured_memory=[]
    )

    entity_result = entity_node(
        {
            "understanding": understanding
        }
    )

    print("\n================")
    print("问题:", question)
    print("理解:", understanding)
    print("实体:", entity_result["entities"])


# 2. 内部商品 Entity 回归
product_understanding = understand_question(
    question="六月牛肉卖了多少？",
    history=[],
    structured_context={},
    structured_memory=[]
)

product_entity_result = entity_node(
    {
        "understanding": product_understanding
    }
)

print("\n================")
print("商品回归")
print("理解:", product_understanding)
print("实体:", product_entity_result["entities"])