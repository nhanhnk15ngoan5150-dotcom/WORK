from agent.langgraph_agent import run_langgraph_agent


# 1. 测试多意图独立时间作用域
questions = [
    "五月牛肉卖了多少，总营业额是多少？",
    "五月总营业额是多少，哪个品类门店营业额最高？",
]


for question in questions:
    result = run_langgraph_agent(
        question=question,
        conversation_history=[],
        structured_context={},
        structured_memory=[]
    )

    print("\n================")
    print("问题:", question)
    print("理解:", result.get("understanding"))
    print("计划:", result.get("plan"))
    print("回答:", result.get("answer"))
    print("成功:", result.get("success"))


# 2. 测试总营业额时间继承
conversation_history = []
structured_context = {}
structured_memory = []

first = run_langgraph_agent(
    question="五月总营业额是多少？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

conversation_history = first["conversation_history"]
structured_context = first["structured_context"]
structured_memory = first["structured_memory"]

second = run_langgraph_agent(
    question="那六月呢？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

print("\n================")
print("总营业额上下文第一轮:", first["answer"])
print("总营业额上下文第二轮理解:", second["understanding"])
print("总营业额上下文第二轮:", second["answer"])


# 3. 测试商品条件不能泄漏到总营业额
conversation_history = []
structured_context = {}
structured_memory = []

first = run_langgraph_agent(
    question="五月牛肉卖了多少？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

conversation_history = first["conversation_history"]
structured_context = first["structured_context"]
structured_memory = first["structured_memory"]

second = run_langgraph_agent(
    question="那总营业额呢？",
    conversation_history=conversation_history,
    structured_context=structured_context,
    structured_memory=structured_memory
)

print("\n================")
print("商品转总营业额第一轮:", first["answer"])
print("商品转总营业额第二轮理解:", second["understanding"])
print("商品转总营业额第二轮计划:", second["plan"])
print("商品转总营业额第二轮:", second["answer"])
print("第二轮结构化上下文:", second["structured_context"])