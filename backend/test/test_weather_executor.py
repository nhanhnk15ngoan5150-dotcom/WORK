from agent.executor import execute_plan


# 1. 北京今天
today_plan = [
    {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
    }
]

today_result = execute_plan(
    today_plan
)

print("\n================")
print("北京今天:")
print(today_result)


# 2. 上海明天
tomorrow_plan = [
    {
        "intent": "weather_info",
        "location": "上海",
        "time_expression": "明天",
        "metric": "天气",
    }
]

tomorrow_result = execute_plan(
    tomorrow_plan
)

print("\n================")
print("上海明天:")
print(tomorrow_result)


# 3. 不支持时间
unsupported_plan = [
    {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "下个月",
        "metric": "天气",
    }
]

unsupported_result = execute_plan(
    unsupported_plan
)

print("\n================")
print("不支持时间:")
print(unsupported_result)


# 4. 天气 + 内部经营混合执行
mixed_plan = [
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
    }
]

mixed_result = execute_plan(
    mixed_plan
)

print("\n================")
print("混合执行:")
print(mixed_result)