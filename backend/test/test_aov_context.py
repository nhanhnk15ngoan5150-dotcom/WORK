from agent.langgraph_agent import run_langgraph_agent


# 1. 时间切换：五月 → 六月
switch_first = run_langgraph_agent(
    question="五月客单价是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("时间切换第一轮")
print("理解:", switch_first["understanding"])
print("回答:", switch_first["answer"])
print("上下文:", switch_first["structured_context"])
print("记忆:", switch_first["structured_memory"])


switch_second = run_langgraph_agent(
    question="那六月呢？",
    conversation_history=switch_first["conversation_history"],
    structured_context=switch_first["structured_context"],
    structured_memory=switch_first["structured_memory"]
)

print("\n================")
print("时间切换第二轮")
print("理解:", switch_second["understanding"])
print("实体:", switch_second["entities"])
print("计划:", switch_second["plan"])
print("结果:", switch_second["results"])
print("回答:", switch_second["answer"])
print("上下文:", switch_second["structured_context"])
print("成功:", switch_second["success"])
print("错误:", switch_second["error"])


# 2. 明确比较：五月 → 和六月比
compare_first = run_langgraph_agent(
    question="五月客单价是多少？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

compare_second = run_langgraph_agent(
    question="和六月比呢？",
    conversation_history=compare_first["conversation_history"],
    structured_context=compare_first["structured_context"],
    structured_memory=compare_first["structured_memory"]
)

print("\n================")
print("跨月比较第二轮")
print("理解:", compare_second["understanding"])
print("实体:", compare_second["entities"])
print("计划:", compare_second["plan"])
print("结果:", compare_second["results"])
print("回答:", compare_second["answer"])
print("上下文:", compare_second["structured_context"])
print("成功:", compare_second["success"])
print("错误:", compare_second["error"])