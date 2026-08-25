import tools.weather_tool as weather_tool


calls = []


# 1. 模拟地点解析
def fake_resolve_weather_location(location):
    return {
        "success": True,
        "input_location": location,
        "location_name": location,
        "adcode": "TEST",
    }


# 2. 模拟实况查询
def fake_live_weather(location_result):
    calls.append(
        ("live", None)
    )

    return {
        "success": True,
        "mode": "live",
    }


# 3. 模拟预报查询
def fake_forecast_weather(
    location_result,
    day_index
):
    calls.append(
        ("forecast", day_index)
    )

    return {
        "success": True,
        "mode": "forecast",
        "day_index": day_index,
    }


weather_tool.resolve_weather_location = (
    fake_resolve_weather_location
)

weather_tool._get_live_weather = (
    fake_live_weather
)

weather_tool._get_forecast_weather = (
    fake_forecast_weather
)


# 4. 旧行为：今天普通天气
calls.clear()

result = weather_tool.get_weather(
    "北京",
    "今天"
)

print("\n================")
print("旧行为 今天 general:")
print("结果:", result)
print("调用:", calls)


# 5. 旧行为：明天普通天气
calls.clear()

result = weather_tool.get_weather(
    "上海",
    "明天"
)

print("\n================")
print("旧行为 明天 general:")
print("结果:", result)
print("调用:", calls)


# 6. 新行为：今天降雨
calls.clear()

result = weather_tool.get_weather(
    "北京",
    "今天",
    "rain"
)

print("\n================")
print("新行为 今天 rain:")
print("结果:", result)
print("调用:", calls)


# 7. 新行为：明天降雨
calls.clear()

result = weather_tool.get_weather(
    "上海",
    "明天",
    "rain"
)

print("\n================")
print("新行为 明天 rain:")
print("结果:", result)
print("调用:", calls)


# 8. 非法查询类型
calls.clear()

result = weather_tool.get_weather(
    "北京",
    "今天",
    "unknown"
)

print("\n================")
print("非法查询类型:")
print("结果:", result)
print("调用:", calls)