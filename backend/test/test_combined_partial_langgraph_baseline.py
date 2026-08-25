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


# 2. 执行三种状态混合请求
result = run_langgraph_agent(
    question=(
        "最近总营业额变化怎么样？"
        "另外今天天气怎么样？"
        "顺便给我写首诗。"
    ),
    conversation_history=[],
    structured_context=original_context,
    structured_memory=original_memory,
)


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

print("\n更新后 Context:")
print(result["structured_context"])

print("\n更新后 Memory:")
print(result["structured_memory"])

# 3. 锁定支持任务正常执行
assert result["success"] is True

assert (
    result["error"]
    == "部分请求超出能力范围"
)


# 4. 锁定支持任务和异常任务都被正确识别
assert any(
    task.get("intent") == "total_sales"
    for task in result["understanding"].get(
        "tasks",
        []
    )
)

assert any(
    task.get("intent") == "weather_info"
    for task in result["understanding"].get(
        "tasks",
        []
    )
)

assert (
    result["understanding"].get(
        "unsupported"
    )
    is True
)


# 5. 锁定缺条件 Weather 不进入执行计划
assert len(
    result["plan"]
) == 1

assert (
    result["plan"][0]["intent"]
    == "total_sales"
)

assert all(
    task.get("intent") != "weather_info"
    for task in result["plan"]
)


# 6. 锁定最终回答
assert (
    "151572"
    in result["answer"]
)

assert (
    "超出餐饮经营数据分析能力范围"
    in result["answer"]
)

assert (
    "天气查询缺少地点信息"
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
    "Combined Partial LangGraph "
    "全链路契约: PASS"
)