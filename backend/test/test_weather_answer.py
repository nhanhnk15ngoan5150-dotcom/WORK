from agent.langgraph_agent import run_langgraph_agent


questions = [
    "北京今天天气怎么样？",
    "上海明天天气怎么样？",
    "北京今天会下雨吗？顺便看看最近总营业额变化怎么样？",
]


# 1. Weather Answer 端到端
for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result["understanding"])
    print("实体:", result["entities"])
    print("计划:", result["plan"])
    print("结果:", result["results"])
    print("回答:", result["answer"])
    print("成功:", result["success"])
    print("错误:", result["error"])