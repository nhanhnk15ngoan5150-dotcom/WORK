from agent.langgraph_agent import run_langgraph_agent


# 1. 准备已有成功业务上下文
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


# 2. 执行 Weather 缺地点 + Unsupported
result = run_langgraph_agent(
    question="今天天气怎么样？顺便给我写首诗。",
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


# 3. 锁定没有任务进入执行阶段
assert result["plan"] == []

assert result["results"] == []


# 4. 锁定组合澄清结果
assert result["success"] is False

assert result["error"] is None

assert (
    "天气查询缺少地点信息"
    in result["answer"]
)

assert (
    "超出餐饮经营数据分析能力范围"
    in result["answer"]
)


# 5. 锁定业务记忆不更新
assert (
    result["structured_context"]
    == original_context
)

assert (
    result["structured_memory"]
    == original_memory
)


print("\n================")
print(
    "Unsupported + Clarification Only "
    "LangGraph 契约: PASS"
)