from services.answer_service import _answer_weather_info


# 1. 旧行为：今天普通天气
today_general = {
    "task": {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
    },
    "result": {
        "success": True,
        "location_name": "北京市",
        "weather": "晴",
        "temperature": "32",
        "humidity": "64",
        "wind_direction": "西南",
        "wind_power": "≤3",
    },
}

today_answer = _answer_weather_info(
    today_general
)

print("\n================")
print("今天 general:")
print(today_answer)


# 2. 旧行为：明天普通天气
tomorrow_general = {
    "task": {
        "intent": "weather_info",
        "location": "上海",
        "time_expression": "明天",
        "metric": "天气",
    },
    "result": {
        "success": True,
        "location_name": "上海市",
        "day_weather": "多云",
        "night_weather": "多云",
        "day_temperature": "32",
        "night_temperature": "27",
        "day_wind_direction": "东",
        "day_wind_power": "1-3",
    },
}

tomorrow_answer = _answer_weather_info(
    tomorrow_general
)

print("\n================")
print("明天 general:")
print(tomorrow_answer)


# 3. 当前缺口：今天 rain 收到 forecast
today_rain = {
    "task": {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
        "weather_query": "rain",
    },
    "result": {
        "success": True,
        "location_name": "北京市",
        "day_weather": "多云",
        "night_weather": "多云",
        "day_temperature": "32",
        "night_temperature": "25",
        "day_wind_direction": "南",
        "day_wind_power": "1-3",
    },
}

rain_answer = _answer_weather_info(
    today_rain
)

print("\n================")
print("今天 rain 当前行为:")
print(rain_answer)


# 4. 锁定旧契约
assert (
    today_answer
    == "北京市今天晴，当前温度32℃，湿度64%，西南风≤3级。"
)

assert (
    tomorrow_answer
    == "上海市明天白天多云，夜间多云，最高32℃，最低27℃，东风1-3级。"
)

print("\n================")
print("旧 Weather Answer 契约: PASS")


# 5. 新行为：今天 rain + forecast
rain_forecast = {
    "task": {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
        "weather_query": "rain",
    },
    "result": {
        "success": True,
        "location_name": "北京市",
        "day_weather": "多云",
        "night_weather": "多云",
        "day_temperature": "32",
        "night_temperature": "25",
    },
}

rain_forecast_answer = _answer_weather_info(
    rain_forecast
)

print("\n================")
print("今天 rain + forecast:")
print(rain_forecast_answer)


# 6. 兼容行为：今天 rain + live
rain_live = {
    "task": {
        "intent": "weather_info",
        "location": "北京",
        "time_expression": "今天",
        "metric": "天气",
        "weather_query": "rain",
    },
    "result": {
        "success": True,
        "location_name": "北京市",
        "weather": "晴",
        "temperature": "32",
        "humidity": "64",
        "wind_direction": "西南",
        "wind_power": "≤3",
    },
}

rain_live_answer = _answer_weather_info(
    rain_live
)

print("\n================")
print("今天 rain + live 兼容:")
print(rain_live_answer)


# 7. 验证新增能力与旧兼容
assert (
    rain_forecast_answer
    == "北京市今天预报白天多云，夜间多云，当前预报暂未显示降雨。"
)

assert (
    rain_live_answer
    == "北京市今天晴，当前温度32℃，湿度64%，西南风≤3级。"
)

print("\n================")
print("Weather Rain Answer 契约: PASS")