from agent.langgraph_agent import run_langgraph_agent


def run_round(
    question,
    history,
    context,
    memory,
):
    result = run_langgraph_agent(
        question=question,
        conversation_history=history,
        structured_context=context,
        structured_memory=memory,
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result["understanding"])
    print("Context:", result["structured_context"])
    print("Memory:", result["structured_memory"])
    print("回答:", result["answer"])
    print("成功:", result["success"])
    print("错误:", result["error"])

    return (
        result["conversation_history"],
        result["structured_context"],
        result["structured_memory"],
    )


# 1. 测试有明确城市的话题切换
print("\n\n######## 场景一：明确城市 ########")

history = []
context = {}
memory = []

for question in [
    "牛肉六月卖的怎么样？",
    "那五月呢？",
    "北京今天天气怎么样？",
    "那明天呢？",
    "牛肉七月呢？",
    "那六月呢？",
]:
    history, context, memory = run_round(
        question,
        history,
        context,
        memory,
    )


# 2. 测试天气缺少城市后的连续追问
print("\n\n######## 场景二：天气缺少城市 ########")

history = []
context = {}
memory = []

for question in [
    "牛肉六月卖的怎么样？",
    "那五月呢？",
    "今天天气怎么样？",
    "那明天呢？",
]:
    history, context, memory = run_round(
        question,
        history,
        context,
        memory,
    )