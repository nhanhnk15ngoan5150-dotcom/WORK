from agent.langgraph_agent import run_langgraph_agent


# 1. 准备已有业务上下文
original_context = {
    "intent": "product_sales",
    "time_expression": "五月",
    "metric": "销售额",
    "query_mode": "value",
    "products": ["可乐"],
}

original_memory = [
    {
        "question": "五月可乐销售额是多少？",
        "tasks": [
            {
                "intent": "product_sales",
                "products": ["可乐"],
                "time_expression": "五月",
                "metric": "销售额",
                "query_mode": "value",
            }
        ],
    }
]


# 2. 执行纯能力范围外请求
result = run_langgraph_agent(
    question="帮我写一首关于夏天的诗。",
    conversation_history=[],
    structured_context=original_context,
    structured_memory=original_memory,
)


print("\n================")
print("理解:")
print(result["understanding"])

print("\n计划:")
print(result["plan"])

print("\n结果:")
print(result["results"])

print("\n回答:")
print(result["answer"])

print("\n成功:")
print(result["success"])

print("\n错误:")
print(result["error"])

print("\nContext:")
print(result["structured_context"])

print("\nMemory:")
print(result["structured_memory"])


# 3. 锁定纯 Unsupported 全链路
assert result["understanding"]["unsupported"] is True

assert result["plan"] == []

assert result["results"] == []

assert result["success"] is False

assert result["error"] is None

assert (
    result["structured_context"]
    == original_context
)

assert (
    result["structured_memory"]
    == original_memory
)

print("\n================")
print("纯 Unsupported LangGraph 契约: PASS")