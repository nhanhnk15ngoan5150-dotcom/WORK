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


# 2. 执行支持 + 不支持混合请求
result = run_langgraph_agent(
    question="最近总营业额变化怎么样？顺便给我写首诗。",
    conversation_history=[],
    structured_context=original_context,
    structured_memory=original_memory,
)


print("\n================")
print("理解:")
print(result["understanding"])

print("\n计划:")
print(result["plan"])

print("\n回答:")
print(result["answer"])

print("\n成功:")
print(result["success"])

print("\n错误:")
print(result["error"])

print("\n更新后 Context:")
print(result["structured_context"])

print("\n更新后 Memory:")
print(result["structured_memory"])


# 3. 锁定 Mixed Unsupported 状态
assert result["success"] is True

assert (
    result["error"]
    == "部分请求超出能力范围"
)

assert (
    "151572" in result["answer"]
)

assert (
    "当前问题超出餐饮经营数据分析能力范围"
    in result["answer"]
)


# 4. 锁定业务上下文不更新
assert (
    result["structured_context"]
    == original_context
)

assert (
    result["structured_memory"]
    == original_memory
)


print("\n================")
print("Mixed Unsupported Memory 隔离契约: PASS")