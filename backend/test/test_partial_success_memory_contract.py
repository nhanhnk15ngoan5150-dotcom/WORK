import copy

import agent.langgraph_agent as agent


# 1. 保存原 Graph
original_graph = agent.graph


class FakeGraph:
    def invoke(self, state):
        return {
            "success": True,
            "error": "部分任务执行失败",
            "answer": (
                "最近一期总营业额为151572元。\n"
                "北京今天天气查询失败。"
            ),
            "understanding": {
                "tasks": [
                    {
                        "intent": "weather_info",
                        "location": "北京",
                        "time_expression": "今天",
                        "metric": "天气",
                    },
                    {
                        "intent": "total_sales",
                        "time_expression": "最近",
                        "metric": "营业额",
                        "query_mode": "trend",
                    },
                ]
            },
            "entities": [],
            "plan": [],
            "results": [],
            "need_clarification": False,
            "unsupported": False,
            "planning_failed": False,
        }


# 2. 准备原有业务记忆
original_context = {
    "intent": "total_sales",
    "time_expression": "五月",
    "metric": "营业额",
}

original_memory = [
    {
        "question": "五月营业额是多少？",
        "tasks": [
            {
                "intent": "total_sales",
                "time_expression": "五月",
                "metric": "营业额",
            }
        ],
    }
]

context_before = copy.deepcopy(
    original_context
)

memory_before = copy.deepcopy(
    original_memory
)


try:
    # 3. 模拟部分成功 Graph
    agent.graph = FakeGraph()

    result = agent.run_langgraph_agent(
        question=(
            "北京今天天气怎么样？"
            "顺便看看最近营业额。"
        ),
        conversation_history=[],
        structured_context=original_context,
        structured_memory=original_memory,
    )

finally:
    # 4. 恢复原 Graph
    agent.graph = original_graph


print("\n================")
print("成功:", result["success"])
print("错误:", result["error"])
print(
    "更新后 Context:",
    result["structured_context"]
)
print(
    "更新后 Memory:",
    result["structured_memory"]
)


# 5. 锁定部分成功记忆契约
assert result["success"] is True

assert (
    result["error"]
    == "部分任务执行失败"
)

assert (
    result["structured_context"]
    == context_before
)

assert (
    result["structured_memory"]
    == memory_before
)

print("\n================")
print(
    "部分成功 Memory 隔离契约: PASS"
)