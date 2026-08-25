from agent.langgraph_agent import run_langgraph_agent


# 1. 第一轮建立 detail 品类记忆
result = run_langgraph_agent(
    question="五月各品类营业额怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

conversation_history = result["conversation_history"]
structured_context = result["structured_context"]
structured_memory = result["structured_memory"]

print("\n========== 第1轮 ==========")
print("理解:", result["understanding"])
print("上下文:", structured_context)
print("结构化记忆:", structured_memory[-1])


# 2. 插入18轮其他业务查询
questions = [
    "六月牛肉卖了多少？",
    "五月三文鱼卖了多少？",
    "六月可乐卖了多少？",
    "五月绿茶卖了多少？",
    "六月鸡肉卖了多少？",
    "五月抹茶拿铁卖了多少？",
    "六月毛豆卖了多少？",
    "五月炸鸡块卖了多少？",
    "六月味增汤卖了多少？",
    "五月煎饺卖了多少？",
    "六月小笼包卖了多少？",
    "五月灌汤包卖了多少？",
    "六月吞拿鱼三明治卖了多少？",
    "五月照烧三明治卖了多少？",
    "六月照烧鸡饭卖了多少？",
    "五月味增拉面卖了多少？",
    "六月豚骨拉面卖了多少？",
    "最近客单价怎么样？",
]

for index, question in enumerate(
    questions,
    start=2
):
    result = run_langgraph_agent(
        question=question,
        conversation_history=conversation_history,
        structured_context=structured_context,
        structured_memory=structured_memory
    )

    conversation_history = result["conversation_history"]
    structured_context = result["structured_context"]
    structured_memory = result["structured_memory"]

    print(
        f"第{index}轮完成：",
        question
    )


# 3. 清空原始对话，强制使用结构化记忆
final_result = run_langgraph_agent(
    question="回到最开始那个品类查询，和六月比呢？",
    conversation_history=[],
    structured_context=structured_context,
    structured_memory=structured_memory
)


# 4. 查看远距离恢复结果
print("\n========== 第20轮 ==========")
print("问题: 回到最开始那个品类查询，和六月比呢？")
print("理解:", final_result["understanding"])
print("计划:", final_result["plan"])
print("回答:", final_result["answer"])
print("结构化记忆轮数:", len(final_result["structured_memory"]))