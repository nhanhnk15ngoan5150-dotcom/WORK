from agent.langgraph_agent import run_langgraph_agent


questions = [
    "最近总营业额变化怎么样？顺便给我写首诗。",
    "最近牛肉销售额怎么样？另外帮我分析一下老板今天心情。",
]


# 1. 测试支持任务和不支持任务混合请求
for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[],
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result["understanding"])
    print("计划:", result["plan"])
    print("结果:", result["results"])
    print("回答:", result["answer"])
    print("成功:", result["success"])
    print("错误:", result["error"])