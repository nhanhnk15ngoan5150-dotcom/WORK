from services.time_service import parse_time_expression

from tools.product_tool import (
    get_product_sales,
    get_product_quantity,
)
from tools.store_tool import get_store_category_sales
from tools.sales_tool import (
    get_sales_summary,
    compare_avg_order_value,
)

from tools.weather_tool import get_weather


# 1. 执行商品销售任务
def _execute_product_sales(task):
    time_result = parse_time_expression(
        task.get("time_expression")
    )

    # 1. 数据时间范围之外
    if time_result.get("mode") == "out_of_range":
        return {
            "success": False,
            "message": (
                "当前数据范围为"
                f"{time_result.get('available_start')}"
                "至"
                f"{time_result.get('available_end')}，"
                f"暂无{task.get('time_expression')}数据"
            )
        }

    # 2. 无法识别时间
    if time_result.get("mode") == "unknown":
        return {
            "success": False,
            "message": "无法识别查询时间"
        }

    metric = task.get(
        "metric"
    ) or "销售额"

    query_mode = task.get(
        "query_mode"
    ) or "value"

    # 3. 最近商品趋势
    if (
        time_result.get("mode") == "compare"
        and query_mode == "trend"
    ):
        if metric == "销量":
            current_result = get_product_quantity(
                product_name=task.get("product"),
                start_date=time_result["current_start"],
                end_date=time_result["current_end"]
            )

            previous_result = get_product_quantity(
                product_name=task.get("product"),
                start_date=time_result["previous_start"],
                end_date=time_result["previous_end"]
            )

        elif metric == "销售额":
            current_result = get_product_sales(
                product_name=task.get("product"),
                start_date=time_result["current_start"],
                end_date=time_result["current_end"]
            )

            previous_result = get_product_sales(
                product_name=task.get("product"),
                start_date=time_result["previous_start"],
                end_date=time_result["previous_end"]
            )

        else:
            return {
                "success": False,
                "message": f"暂不支持的商品指标: {metric}"
            }

        if (
            not current_result.get("success")
            or not previous_result.get("success")
        ):
            return {
                "success": False,
                "message": "商品趋势查询失败"
            }

        return {
            "success": True,
            "comparison": True,
            "current": current_result,
            "previous": previous_result,
            "message": "查询成功"
        }

    # 4. 最近单期查询
    if time_result.get("mode") == "compare":
        start_date = time_result["current_start"]
        end_date = time_result["current_end"]

    # 5. 普通时间查询
    else:
        start_date = time_result["start_date"]
        end_date = time_result["end_date"]

    # 6. 销量
    if metric == "销量":
        return get_product_quantity(
            product_name=task.get("product"),
            start_date=start_date,
            end_date=end_date
        )

    # 7. 销售额
    if metric == "销售额":
        return get_product_sales(
            product_name=task.get("product"),
            start_date=start_date,
            end_date=end_date
        )

    return {
        "success": False,
        "message": f"暂不支持的商品指标: {metric}"
    }


# 2. 执行门店品类营业额任务
def _execute_store_category_sales(task):
    time_expression = task.get(
        "time_expression"
    ) or ""

    time_result = parse_time_expression(
        time_expression
    )

    # 1. 时间超出数据范围
    if time_result.get("mode") == "out_of_range":
        available_start = time_result.get(
            "available_start"
        )

        available_end = time_result.get(
            "available_end"
        )

        return {
            "success": False,
            "message": (
                f"当前数据范围为"
                f"{available_start}至{available_end}，"
                f"暂无{time_expression}数据"
            )
        }

    # 2. 无法识别时间
    if time_result.get("mode") == "unknown":
        return {
            "success": False,
            "message": "无法识别查询时间"
        }

    # 3. 最近时间
    if time_result.get("mode") == "compare":
        analysis_mode = task.get("analysis_mode") or "value"

        # 3.1 最近趋势比较
        if analysis_mode == "trend":
            current_result = get_store_category_sales(
                time_result["current_start"],
                time_result["current_end"]
            )

            previous_result = get_store_category_sales(
                time_result["previous_start"],
                time_result["previous_end"]
            )

            if (
                    not current_result.get("success")
                    or not previous_result.get("success")
            ):
                return {
                    "success": False,
                    "message": "品类营业额趋势查询失败"
                }

            return {
                "success": True,
                "comparison": True,
                "current": current_result,
                "previous": previous_result,
                "message": "查询成功"
            }

        # 3.2 最近单期查询
        return get_store_category_sales(
            time_result["current_start"],
            time_result["current_end"]
        )

    # 4. 普通时间范围
    return get_store_category_sales(
        time_result["start_date"],
        time_result["end_date"]
    )


# 3. 执行总营业额任务
def _execute_total_sales(task):
    time_result = parse_time_expression(
        task.get("time_expression")
    )

    # 1. 数据时间范围之外
    if time_result.get("mode") == "out_of_range":
        return {
            "success": False,
            "message": (
                "当前数据范围为"
                f"{time_result.get('available_start')}"
                "至"
                f"{time_result.get('available_end')}，"
                f"暂无{task.get('time_expression')}数据"
            )
        }

    # 2. 无法识别时间
    if time_result.get("mode") == "unknown":
        return {
            "success": False,
            "message": "无法识别查询时间"
        }

    query_mode = task.get(
        "query_mode"
    ) or "value"

    # 3. 最近营业额趋势
    if (
        time_result.get("mode") == "compare"
        and query_mode == "trend"
    ):
        current_result = get_sales_summary(
            start_date=time_result["current_start"],
            end_date=time_result["current_end"]
        )

        previous_result = get_sales_summary(
            start_date=time_result["previous_start"],
            end_date=time_result["previous_end"]
        )

        if (
            not current_result.get("success")
            or not previous_result.get("success")
        ):
            return {
                "success": False,
                "message": "营业额趋势查询失败"
            }

        return {
            "success": True,
            "comparison": True,
            "current": current_result,
            "previous": previous_result,
            "message": "查询成功"
        }

    # 4. 最近单期营业额
    if time_result.get("mode") == "compare":
        return get_sales_summary(
            start_date=time_result["current_start"],
            end_date=time_result["current_end"]
        )

    # 5. 明确月份或全部数据
    return get_sales_summary(
        start_date=time_result["start_date"],
        end_date=time_result["end_date"]
    )


# 4. 执行客单价趋势任务
def _execute_avg_order_value_trend(task: dict):
    time_expression = task.get(
        "time_expression"
    ) or ""

    time_result = parse_time_expression(
        time_expression
    )

    query_mode = task.get(
        "query_mode"
    ) or "trend"

    # 1. 时间超出数据范围
    if time_result.get("mode") == "out_of_range":
        available_start = time_result.get(
            "available_start"
        )

        available_end = time_result.get(
            "available_end"
        )

        return {
            "success": False,
            "message": (
                f"当前数据范围为"
                f"{available_start}至{available_end}，"
                f"暂无{time_expression}数据"
            )
        }

    # 2. 无法识别时间
    if time_result.get("mode") == "unknown":
        return {
            "success": False,
            "message": "无法识别查询时间"
        }

    # 3. 客单价单期值
    if query_mode == "value":
        if time_result.get("mode") == "compare":
            start_date = time_result[
                "current_start"
            ]
            end_date = time_result[
                "current_end"
            ]
        else:
            start_date = time_result[
                "start_date"
            ]
            end_date = time_result[
                "end_date"
            ]

        result = get_sales_summary(
            start_date,
            end_date
        )

        if not result.get("success"):
            return {
                "success": False,
                "message": "客单价查询失败"
            }

        return result

    # 4. 客单价趋势
    if query_mode == "trend":
        if time_result.get("mode") != "compare":
            return {
                "success": False,
                "message": "客单价趋势需要可对比的时间范围"
            }

        return compare_avg_order_value(
            current_start=time_result["current_start"],
            current_end=time_result["current_end"],
            previous_start=time_result["previous_start"],
            previous_end=time_result["previous_end"]
        )

    # 5. 不支持的查询模式
    return {
        "success": False,
        "message": "不支持的客单价查询模式"
    }

# 5. 执行天气查询任务
def _execute_weather_info(task: dict):
    location = task.get(
        "location"
    ) or ""

    time_expression = task.get(
        "time_expression"
    ) or ""

    weather_query = task.get(
        "weather_query"
    )

    # 1. 保持旧普通天气调用兼容
    if not weather_query or weather_query == "general":
        return get_weather(
            location,
            time_expression
        )

    # 2. 透传天气子查询类型
    return get_weather(
        location,
        time_expression,
        weather_query
    )

# 6. 执行单个任务
def _execute_task(task: dict):
    intent = task.get("intent")

    if intent == "product_sales":
        return _execute_product_sales(
            task
        )

    if intent == "store_category_sales":
        return _execute_store_category_sales(
            task
        )

    if intent == "total_sales":
        return _execute_total_sales(
            task
        )

    if intent == "avg_order_value_trend":
        return _execute_avg_order_value_trend(
            task
        )

    if intent == "weather_info":
        return _execute_weather_info(
            task
        )

    return {
        "success": False,
        "message": f"暂不支持的任务类型: {intent}"
    }


# 7. 执行计划
def execute_plan(plan: list):
    results = []

    for task in plan:
        try:
            result = _execute_task(
                task
            )

        except Exception as exc:
            result = {
                "success": False,
                "message": "任务执行失败",
                "error": str(exc)
            }

        results.append(
            {
                "task": task,
                "result": result
            }
        )

    return results