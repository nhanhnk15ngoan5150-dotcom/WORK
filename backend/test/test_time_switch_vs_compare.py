from agent.langgraph_agent import run_langgraph_agent


# 1. 定义两轮测试函数
def run_two_rounds(
    first_question,
    second_question
):
    first = run_langgraph_agent(
        question=first_question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    second = run_langgraph_agent(
        question=second_question,
        conversation_history=first["conversation_history"],
        structured_context=first["structured_context"],
        structured_memory=first["structured_memory"]
    )

    print("\n================")
    print("第一轮:", first_question)
    print("第一轮回答:", first["answer"])
    print("第二轮:", second_question)
    print("第二轮理解:", second["understanding"])
    print("第二轮计划:", second["plan"])
    print("第二轮回答:", second["answer"])


# 2. 普通时间切换
run_two_rounds(
    "五月可乐卖了多少钱？",
    "那六月呢？"
)


# 3. 普通重新查看
run_two_rounds(
    "五月可乐卖了多少钱？",
    "再看看六月。"
)


# 4. 明确修改时间
run_two_rounds(
    "五月可乐卖了多少钱？",
    "改成六月。"
)


# 5. 明确时间比较
run_two_rounds(
    "五月可乐卖了多少钱？",
    "和六月比呢？"
)