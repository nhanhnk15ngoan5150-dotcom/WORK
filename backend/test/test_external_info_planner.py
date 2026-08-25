from services.llm_service import understand_question
from agent.nodes import entity_node
from agent.planner import create_plan


questions = [
    "北京今天天气怎么样？",
    "最近有什么餐饮行业新闻？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. 正常 Entity → Planner 路径
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

    plan = create_plan(
        {
            "entities": entity_result["entities"]
        }
    )

    print("\n================")
    print("问题:", question)
    print("理解:", understanding)
    print("实体:", entity_result["entities"])
    print("计划:", plan)


# 2. Understanding → Planner 兼容路径
weather_understanding = understand_question(
    question="上海明天天气怎么样？",
    history=[],
    structured_context={},
    structured_memory=[]
)

weather_plan = create_plan(
    weather_understanding
)

print("\n================")
print("天气兼容路径")
print("理解:", weather_understanding)
print("计划:", weather_plan)


news_understanding = understand_question(
    question="最近有什么食品安全新闻？",
    history=[],
    structured_context={},
    structured_memory=[]
)

news_plan = create_plan(
    news_understanding
)

print("\n================")
print("新闻兼容路径")
print("理解:", news_understanding)
print("计划:", news_plan)