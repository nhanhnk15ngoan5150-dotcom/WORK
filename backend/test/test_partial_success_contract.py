from agent.executor import execute_plan
from agent.nodes import answer_node
from services.answer_service import generate_final_answer


plan = [
    {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
        "weather_query": "unknown",
    },
    {
        "intent": "total_sales",
        "time_expression": "最近",
        "metric": "营业额",
        "query_mode": "trend",
    },
]


# 1. 执行混合任务
results = execute_plan(
    plan
)

print("\n================")
print("执行结果:")
print(results)


# 2. 生成回答
answer = generate_final_answer(
    results
)

print("\n================")
print("回答:")
print(answer)


# 3. 判断整体状态
state_result = answer_node(
    {
        "results": results
    }
)

print("\n================")
print("Answer Node:")
print(state_result)


# 4. 锁定部分成功契约
assert len(results) == 2

assert (
    results[0]["result"]["success"]
    is False
)

assert (
    results[1]["result"]["success"]
    is True
)

assert (
    state_result["success"]
    is True
)

assert (
    state_result["error"]
    == "部分任务执行失败"
)

assert (
    "151572" in state_result["answer"]
)

print("\n================")
print("部分成功契约: PASS")