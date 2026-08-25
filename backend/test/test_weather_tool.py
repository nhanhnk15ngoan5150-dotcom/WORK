from tools.weather_tool import (
    resolve_weather_location,
    get_weather,
)


# 1. 北京地点解析
beijing = resolve_weather_location(
    "北京"
)

print("\n================")
print("北京地点:", beijing)


# 2. 北京今天天气
beijing_today = get_weather(
    "北京",
    "今天"
)

print("\n================")
print("北京今天:", beijing_today)


# 3. 上海明天天气
shanghai_tomorrow = get_weather(
    "上海",
    "明天"
)

print("\n================")
print("上海明天:", shanghai_tomorrow)


# 4. 不存在地点
unknown_location = get_weather(
    "完全不存在的城市XYZ",
    "今天"
)

print("\n================")
print("未知地点:", unknown_location)


# 5. 暂不支持时间
unsupported_time = get_weather(
    "北京",
    "下个月"
)

print("\n================")
print("未知时间:", unsupported_time)