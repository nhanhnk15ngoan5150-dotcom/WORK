from pathlib import Path
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from dotenv import load_dotenv


# 1. 加载环境变量
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(
    BASE_DIR / ".env"
)

AMAP_API_KEY = os.getenv(
    "AMAP_API_KEY"
)

DISTRICT_URL = (
    "https://restapi.amap.com/v3/config/district"
)

WEATHER_URL = (
    "https://restapi.amap.com/v3/weather/weatherInfo"
)


def _request_json(
    url: str,
    params: dict
):
    query = urlencode(
        params
    )

    request = Request(
        f"{url}?{query}",
        headers={
            "User-Agent": "moneki-agent/1.0"
        }
    )

    try:
        with urlopen(
            request,
            timeout=10
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except HTTPError as exc:
        return {
            "success": False,
            "message": (
                f"高德服务请求失败："
                f"HTTP {exc.code}"
            ),
        }

    except URLError as exc:
        return {
            "success": False,
            "message": (
                f"高德服务连接失败："
                f"{exc.reason}"
            ),
        }

    except Exception as exc:
        return {
            "success": False,
            "message": (
                f"高德服务异常："
                f"{exc}"
            ),
        }


def resolve_weather_location(
    location: str
):
    if not location:
        return {
            "success": False,
            "message": "缺少天气查询地点",
        }

    if not AMAP_API_KEY:
        return {
            "success": False,
            "message": "未配置 AMAP_API_KEY",
        }

    # 1. 查询行政区编码
    data = _request_json(
        DISTRICT_URL,
        {
            "key": AMAP_API_KEY,
            "keywords": location,
            "subdistrict": 0,
            "extensions": "base",
            "output": "JSON",
        }
    )

    if data.get("success") is False:
        return data

    if str(
        data.get("status")
    ) != "1":
        return {
            "success": False,
            "message": (
                "高德行政区查询失败："
                f"{data.get('info') or '未知错误'}"
            ),
        }

    districts = data.get(
        "districts",
        []
    )

    if not districts:
        return {
            "success": False,
            "message": (
                f"没有找到地点："
                f"{location}"
            ),
        }

    district = districts[0]

    return {
        "success": True,
        "input_location": location,
        "location_name": (
            district.get("name")
            or location
        ),
        "adcode": district.get(
            "adcode"
        ),
        "citycode": district.get(
            "citycode"
        ),
        "level": district.get(
            "level"
        ),
        "center": district.get(
            "center"
        ),
    }


def _get_live_weather(
    location_result: dict
):
    # 1. 查询实况天气
    data = _request_json(
        WEATHER_URL,
        {
            "key": AMAP_API_KEY,
            "city": location_result["adcode"],
            "extensions": "base",
            "output": "JSON",
        }
    )

    if data.get("success") is False:
        return data

    if str(
        data.get("status")
    ) != "1":
        return {
            "success": False,
            "message": (
                "高德天气查询失败："
                f"{data.get('info') or '未知错误'}"
            ),
        }

    lives = data.get(
        "lives",
        []
    )

    if not lives:
        return {
            "success": False,
            "message": "没有查询到实况天气",
        }

    live = lives[0]

    return {
        "success": True,
        "source": "高德开放平台",
        "input_location": (
            location_result["input_location"]
        ),
        "location_name": (
            live.get("city")
            or location_result["location_name"]
        ),
        "adcode": location_result["adcode"],
        "date": live.get(
            "reporttime"
        ),
        "weather": live.get(
            "weather"
        ),
        "temperature": live.get(
            "temperature"
        ),
        "wind_direction": live.get(
            "winddirection"
        ),
        "wind_power": live.get(
            "windpower"
        ),
        "humidity": live.get(
            "humidity"
        ),
        "message": "查询成功",
    }


def _get_forecast_weather(
    location_result: dict,
    day_index: int
):
    # 1. 查询预报天气
    data = _request_json(
        WEATHER_URL,
        {
            "key": AMAP_API_KEY,
            "city": location_result["adcode"],
            "extensions": "all",
            "output": "JSON",
        }
    )

    if data.get("success") is False:
        return data

    if str(
        data.get("status")
    ) != "1":
        return {
            "success": False,
            "message": (
                "高德天气查询失败："
                f"{data.get('info') or '未知错误'}"
            ),
        }

    forecasts = data.get(
        "forecasts",
        []
    )

    if not forecasts:
        return {
            "success": False,
            "message": "没有查询到天气预报",
        }

    casts = forecasts[0].get(
        "casts",
        []
    )

    if day_index >= len(casts):
        return {
            "success": False,
            "message": "天气预报数据不足",
        }

    cast = casts[
        day_index
    ]

    return {
        "success": True,
        "source": "高德开放平台",
        "input_location": (
            location_result["input_location"]
        ),
        "location_name": (
            forecasts[0].get("city")
            or location_result["location_name"]
        ),
        "adcode": location_result["adcode"],
        "date": cast.get(
            "date"
        ),
        "week": cast.get(
            "week"
        ),
        "day_weather": cast.get(
            "dayweather"
        ),
        "night_weather": cast.get(
            "nightweather"
        ),
        "day_temperature": cast.get(
            "daytemp"
        ),
        "night_temperature": cast.get(
            "nighttemp"
        ),
        "day_wind_direction": cast.get(
            "daywind"
        ),
        "night_wind_direction": cast.get(
            "nightwind"
        ),
        "day_wind_power": cast.get(
            "daypower"
        ),
        "night_wind_power": cast.get(
            "nightpower"
        ),
        "message": "查询成功",
    }


def get_weather(
    location: str,
    time_expression: str,
    weather_query: str = "general"
):
    # 1. 验证时间表达
    supported_times = {
        "今天",
        "今日",
        "明天",
        "明日",
    }

    if time_expression not in supported_times:
        return {
            "success": False,
            "message": (
                f"当前天气工具暂不支持时间表达："
                f"{time_expression}"
            ),
        }

    # 2. 验证天气查询类型
    supported_queries = {
        "general",
        "rain",
    }

    if weather_query not in supported_queries:
        return {
            "success": False,
            "message": (
                f"当前天气工具暂不支持查询类型："
                f"{weather_query}"
            ),
        }

    # 3. 解析地点
    location_result = (
        resolve_weather_location(
            location
        )
    )

    if not location_result.get(
        "success"
    ):
        return location_result

    # 4. 降雨查询使用天气预报
    if weather_query == "rain":
        day_index = (
            0
            if time_expression in {
                "今天",
                "今日",
            }
            else 1
        )

        return _get_forecast_weather(
            location_result,
            day_index=day_index
        )

    # 5. 今天普通查询使用实况天气
    if time_expression in {
        "今天",
        "今日",
    }:
        return _get_live_weather(
            location_result
        )

    # 6. 明天普通查询使用天气预报
    return _get_forecast_weather(
        location_result,
        day_index=1
    )