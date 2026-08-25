from agent.langgraph_agent import run_langgraph_agent


# 1. 初始化上下文
conversation_history = []
structured_context = {}
structured_memory = []


# 2. 第一轮查询五月可乐
first = run_langgraph_agent(
    question="五月可乐卖了多少钱？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

conversation_history = first[
    "conversation_history"
]
structured_context = first[
    "structured_context"
]
structured_memory = first[
    "structured_memory"
]


# 3. 第二轮要求与六月比较
second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)


print("\n================")
print("第一轮回答:", first["answer"])
print("第一轮上下文:", first["structured_context"])

print("\n第二轮理解:", second["understanding"])
print("第二轮计划:", second["plan"])
print("第二轮结果:", second["results"])
print("第二轮回答:", second["answer"])


# 4. 测试多商品跨月变化
conversation_history = []
structured_context = {}
structured_memory = []

first = run_langgraph_agent(
    question="五月牛肉和鸡肉卖了多少？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

conversation_history = first[
    "conversation_history"
]
structured_context = first[
    "structured_context"
]
structured_memory = first[
    "structured_memory"
]

second = run_langgraph_agent(
    question="再看看六月。",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

conversation_history = second[
    "conversation_history"
]
structured_context = second[
    "structured_context"
]
structured_memory = second[
    "structured_memory"
]

third = run_langgraph_agent(
    question="这两个月变化怎么样？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)


print("\n================")
print("多商品第一轮:", first["answer"])
print("多商品第二轮:", second["answer"])
print("第三轮理解:", third["understanding"])
print("第三轮计划:", third["plan"])
print("第三轮回答:", third["answer"])