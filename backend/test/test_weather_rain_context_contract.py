from services.llm_service import understand_question


# 1. 准备天气降雨上下文
weather_context = {
    "intent": "weather_info",
    "time_expression": "今天",
    "metric": "天气",
    "query_mode": None,
    "products": [],
    "location": "北京",
    "weather_query": "rain",
}

weather_memory = [
    {
        "question": "北京今天会下雨吗？",
        "tasks": [
            {
                "intent": "weather_info",
                "products": [],
                "time_expression": "今天",
                "metric": "天气",
                "query_mode": None,
                "location": "北京",
                "weather_query": "rain",
            }
        ],
    }
]

history = [
    {
        "role": "user",
        "content": "北京今天会下雨吗？",
    },
    {
        "role": "assistant",
        "content": "北京市今天预报白天多云，夜间多云，当前预报暂未显示降雨。",
    },
]


# 2. 测试省略追问
result = understand_question(
    question="那明天呢？",
    history=history,
    structured_context=weather_context,
    structured_memory=weather_memory,
)

print("\n================")
print("Rain 上下文继承:")
print(result)


# 3. 锁定 Rain 继承契约
task = result["tasks"][0]

assert task["intent"] == "weather_info"
assert task["products"] == []
assert task["location"] == "北京"
assert task["time_expression"] == "明天"
assert task["metric"] == "天气"
assert task["weather_query"] == "rain"

assert result["unsupported"] is False
assert result["need_clarification"] is False

print("\n================")
print("Weather Rain 多轮继承契约: PASS")