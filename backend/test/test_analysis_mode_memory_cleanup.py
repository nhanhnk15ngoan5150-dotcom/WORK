from agent.langgraph_agent import run_langgraph_agent


# 1. 商品记忆不应出现 analysis_mode=None
product_result = run_langgraph_agent(
    question="六月可乐卖了多少份？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("商品记忆:", product_result["structured_memory"])


# 2. 品类记忆必须保留 analysis_mode
category_result = run_langgraph_agent(
    question="最近各品类营业额变化怎么样？",
    conversation_history=[],
    structured_context={},
    structured_memory=[]
)

print("\n================")
print("品类记忆:", category_result["structured_memory"])