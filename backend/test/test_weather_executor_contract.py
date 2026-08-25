import agent.executor as executor


calls = []


# 1. 模拟天气工具
def fake_get_weather(*args):
    calls.append(args)

    return {
        "success": True,
        "args": args,
    }


executor.get_weather = (
    fake_get_weather
)


# 2. 旧任务：没有 weather_query
calls.clear()

legacy_task = {
    "intent": "weather_info",
    "location": "北京",
    "time_expression": "今天",
    "metric": "天气",
}

legacy_result = (
    executor._execute_weather_info(
        legacy_task
    )
)

print("\n================")
print("旧 Weather Task:")
print("结果:", legacy_result)
print("调用:", calls)


# 3. 当前 general 任务
calls.clear()

general_task = {
    "intent": "weather_info",
    "location": "北京",
    "time_expression": "今天",
    "metric": "天气",
    "weather_query": "general",
}

general_result = (
    executor._execute_weather_info(
        general_task
    )
)

print("\n================")
print("General Task 当前行为:")
print("结果:", general_result)
print("调用:", calls)


# 4. 当前 rain 任务
calls.clear()

rain_task = {
    "intent": "weather_info",
    "location": "北京",
    "time_expression": "今天",
    "metric": "天气",
    "weather_query": "rain",
}

rain_result = (
    executor._execute_weather_info(
        rain_task
    )
)

print("\n================")
print("Rain Task 当前行为:")
print("结果:", rain_result)
print("调用:", calls)


# 5. 验证旧契约和新增能力
assert legacy_result["args"] == (
    "北京",
    "今天",
)

assert general_result["args"] == (
    "北京",
    "今天",
)

assert rain_result["args"] == (
    "北京",
    "今天",
    "rain",
)

print("\n================")
print(
    "Weather Executor 新契约: PASS"
)

# 6. 非法天气查询类型
calls.clear()

unknown_task = {
    "intent": "weather_info",
    "location": "北京",
    "time_expression": "今天",
    "metric": "天气",
    "weather_query": "unknown",
}

unknown_result = (
    executor._execute_weather_info(
        unknown_task
    )
)

print("\n================")
print("Unknown Task:")
print("结果:", unknown_result)
print("调用:", calls)

assert unknown_result["args"] == (
    "北京",
    "今天",
    "unknown",
)