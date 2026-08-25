from services.llm_service import understand_question
from agent.nodes import entity_node


questions = [
    "北京今天天气怎么样？",
    "北京今天会下雨吗？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. 天气查询类型 Entity 透传
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


# 2. 内部任务回归
internal_understanding = understand_question(
    question="最近总营业额变化怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

internal_entity = entity_node(
    {
        "understanding": internal_understanding
    }
)

print("\n================")
print("内部回归")
print("理解:", internal_understanding)
print("实体:", internal_entity["entities"])