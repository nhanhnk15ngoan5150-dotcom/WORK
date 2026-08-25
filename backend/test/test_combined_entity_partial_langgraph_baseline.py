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


# 2. 执行完整任务 + 商品歧义 + Unsupported
result = run_langgraph_agent(
    question=(
        "最近总营业额变化怎么样？"
        "另外六月poke销售额是多少？"
        "顺便给我写首诗。"
    ),
    conversation_history=[],
    structured_context=original_context,
    structured_memory=original_memory,
)


# 3. 输出真实全链路结果
print("\n================")
print("理解:")
print(result["understanding"])

print("\n实体:")
print(result["entities"])

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

# 4. 锁定三类任务被正确识别
intents = [
    task.get("intent")
    for task in result["understanding"].get(
        "tasks",
        []
    )
]

assert "total_sales" in intents
assert "product_sales" in intents

assert (
    result["understanding"].get(
        "unsupported"
    )
    is True
)


# 5. 锁定商品实体进入澄清
product_entities = [
    product
    for entity in result["entities"]
    if entity.get("intent") == "product_sales"
    for product in entity.get("products", [])
]

assert product_entities

assert any(
    product.get("need_clarification") is True
    for product in product_entities
)

assert any(
    product.get("standard") is None
    for product in product_entities
)


# 6. 锁定只有完整任务进入执行
assert len(
    result["plan"]
) == 1

assert (
    result["plan"][0]["intent"]
    == "total_sales"
)

assert all(
    task.get("intent") != "product_sales"
    for task in result["plan"]
)

assert len(
    result["results"]
) == 1

assert (
    result["results"][0]["task"]["intent"]
    == "total_sales"
)


# 7. 锁定最终组合回答
assert result["success"] is True

assert (
    result["error"]
    == "部分请求超出能力范围"
)

assert (
    "151572"
    in result["answer"]
)

assert (
    "poke"
    in result["answer"]
)

assert (
    "请确认具体商品"
    in result["answer"]
)

assert (
    "超出餐饮经营数据分析能力范围"
    in result["answer"]
)


# 8. 锁定业务记忆不更新
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
    "Combined Entity Partial LangGraph "
    "全链路契约: PASS"
)