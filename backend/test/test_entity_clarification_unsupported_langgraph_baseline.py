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


# 2. 执行商品歧义 + Unsupported
result = run_langgraph_agent(
    question="六月poke销售额是多少？顺便给我写首诗。",
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

# 4. 锁定商品歧义实体
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


# 5. 锁定异常任务不进入执行阶段
assert result["plan"] == []

assert result["results"] == []


# 6. 锁定最终组合澄清
assert result["success"] is False

assert result["error"] is None

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


# 7. 锁定业务记忆不更新
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
    "Entity Clarification + Unsupported "
    "LangGraph 契约: PASS"
)