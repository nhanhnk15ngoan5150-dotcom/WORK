# 1. 生成商品销售回答
def _answer_product_sales(items: list):
    sentences = []
    sales_records = []
    quantity_records = []

    for item in items:
        task = item["task"]
        result = item["result"]

        if not result.get("success"):
            continue

        product = task.get("product")
        time_expression = task.get(
            "time_expression"
        ) or ""

        metric = task.get(
            "metric"
        ) or "销售额"

        #  最近商品趋势
        if (
            task.get("query_mode") == "trend"
            and result.get("comparison")
        ):
            current = result.get(
                "current",
                {}
            )

            previous = result.get(
                "previous",
                {}
            )

            # 销量趋势
            if metric == "销量":
                current_value = current.get(
                    "total_quantity",
                    0
                )

                previous_value = previous.get(
                    "total_quantity",
                    0
                )

                diff = (
                    current_value
                    - previous_value
                )

                trend = (
                    "增加"
                    if diff >= 0
                    else "减少"
                )

                sentence = (
                    f"最近一期{product}销量为"
                    f"{current_value:.0f}份，"
                    f"上一期为{previous_value:.0f}份，"
                    f"{trend}{abs(diff):.0f}份"
                )

                if previous_value != 0:
                    change_rate = (
                        diff
                        / previous_value
                        * 100
                    )

                    sentence += (
                        f"，变化率为"
                        f"{abs(change_rate):.2f}%"
                    )

                sentences.append(
                    sentence
                )

                continue

            # 销售额趋势
            if metric == "销售额":
                current_value = current.get(
                    "total_sales",
                    0
                )

                previous_value = previous.get(
                    "total_sales",
                    0
                )

                diff = (
                    current_value
                    - previous_value
                )

                trend = (
                    "增加"
                    if diff >= 0
                    else "减少"
                )

                sentence = (
                    f"最近一期{product}销售额为"
                    f"{current_value:.0f}元，"
                    f"上一期为{previous_value:.0f}元，"
                    f"{trend}{abs(diff):.0f}元"
                )

                if previous_value != 0:
                    change_rate = (
                        diff
                        / previous_value
                        * 100
                    )

                    sentence += (
                        f"，变化率为"
                        f"{abs(change_rate):.2f}%"
                    )

                sentences.append(
                    sentence
                )

                continue

        # 销量
        if metric == "销量":
            quantity = result.get(
                "total_quantity",
                0
            )

            sentences.append(
                f"{time_expression}{product}"
                f"销量为{quantity:.0f}份"
            )

            quantity_records.append(
                {
                    "product": product,
                    "time": time_expression,
                    "quantity": quantity,
                }
            )

            continue

        # 销售额
        sales = result.get(
            "total_sales",
            0
        )

        sentences.append(
            f"{time_expression}{product}"
            f"销售额为{sales:.0f}元"
        )

        sales_records.append(
            {
                "product": product,
                "time": time_expression,
                "sales": sales,
            }
        )

    if not sentences:
        return None

    answer = "，".join(
        sentences
    ) + "。"

    # 2. 销售额比较
    if sales_records:
        sales_times = list(
            dict.fromkeys(
                item["time"]
                for item in sales_records
            )
        )

        sales_products = list(
            dict.fromkeys(
                item["product"]
                for item in sales_records
            )
        )

        # 同一时间多个商品
        if (
            len(sales_times) == 1
            and len(sales_records) > 1
        ):
            ranked = sorted(
                sales_records,
                key=lambda x: x["sales"],
                reverse=True
            )

            top = ranked[0]
            second = ranked[1]

            diff = (
                top["sales"]
                - second["sales"]
            )

            answer += (
                f"其中{top['product']}销售额最高，"
                f"高出{second['product']}{diff:.0f}元。"
            )

        # 多个时间按商品比较变化
        elif len(sales_times) > 1:
            for product in sales_products:
                product_records = [
                    item
                    for item in sales_records
                    if item["product"] == product
                ]

                if len(product_records) < 2:
                    continue

                first = product_records[0]
                last = product_records[-1]

                diff = (
                    last["sales"]
                    - first["sales"]
                )

                trend = (
                    "增加"
                    if diff >= 0
                    else "减少"
                )

                answer += (
                    f"{product}从{first['time']}的"
                    f"{first['sales']:.0f}元变为"
                    f"{last['time']}的"
                    f"{last['sales']:.0f}元，"
                    f"{trend}{abs(diff):.0f}元"
                )

                if first["sales"] != 0:
                    change_rate = (
                        diff
                        / first["sales"]
                        * 100
                    )

                    answer += (
                        f"，变化率为"
                        f"{abs(change_rate):.2f}%"
                    )

                answer += "。"

    # 3. 销量比较
    if quantity_records:
        quantity_times = list(
            dict.fromkeys(
                item["time"]
                for item in quantity_records
            )
        )

        quantity_products = list(
            dict.fromkeys(
                item["product"]
                for item in quantity_records
            )
        )

        # 同一时间多个商品
        if (
            len(quantity_times) == 1
            and len(quantity_records) > 1
        ):
            ranked = sorted(
                quantity_records,
                key=lambda x: x["quantity"],
                reverse=True
            )

            top = ranked[0]
            second = ranked[1]

            diff = (
                top["quantity"]
                - second["quantity"]
            )

            answer += (
                f"其中{top['product']}销量最高，"
                f"比{second['product']}多{diff:.0f}份。"
            )

        # 多个时间按商品比较变化
        elif len(quantity_times) > 1:
            for product in quantity_products:
                product_records = [
                    item
                    for item in quantity_records
                    if item["product"] == product
                ]

                if len(product_records) < 2:
                    continue

                first = product_records[0]
                last = product_records[-1]

                diff = (
                    last["quantity"]
                    - first["quantity"]
                )

                trend = (
                    "增加"
                    if diff >= 0
                    else "减少"
                )

                answer += (
                    f"{product}从{first['time']}的"
                    f"{first['quantity']:.0f}份变为"
                    f"{last['time']}的"
                    f"{last['quantity']:.0f}份，"
                    f"{trend}{abs(diff):.0f}份"
                )

                if first["quantity"] != 0:
                    change_rate = (
                        diff
                        / first["quantity"]
                        * 100
                    )

                    answer += (
                        f"，变化率为"
                        f"{abs(change_rate):.2f}%"
                    )

                answer += "。"

    return answer


# 2. 生成门店品类回答
def _answer_store_category_sales(item: dict):
    task = item.get(
        "task",
        {}
    )

    result = item.get(
        "result",
        {}
    )

    if not result.get("success"):
        return None

    time_expression = task.get(
        "time_expression"
    ) or ""

    query_mode = task.get(
        "query_mode"
    )

    # 1. 最近品类趋势
    if (
        task.get("analysis_mode") == "trend"
        and result.get("comparison")
    ):
        previous_result = result.get(
            "previous",
            {}
        )

        current_result = result.get(
            "current",
            {}
        )

        comparison_items = [
            {
                "task": {
                    "time_expression": "上一期",
                    "query_mode": query_mode,
                },
                "result": previous_result,
            },
            {
                "task": {
                    "time_expression": "最近一期",
                    "query_mode": query_mode,
                },
                "result": current_result,
            },
        ]

        comparison_answer = (
            _answer_store_category_comparison(
                comparison_items
            )
        )

        if comparison_answer:
            return comparison_answer

    # 2. 各品类明细
    if query_mode == "detail":
        data = result.get(
            "data",
            []
        )

        if not data:
            return "没有查询到门店品类营业额数据。"

        details = [
            f"{item.get('category')} "
            f"{item.get('total_sales', 0):.0f}元"
            for item in data
        ]

        detail_text = "、".join(
            details
        )

        if time_expression:
            return (
                f"{time_expression}各品类营业额："
                f"{detail_text}。"
            )

        return (
            f"各品类营业额："
            f"{detail_text}。"
        )

    # 3. 最高品类
    top_category = result.get(
        "top_category"
    )

    if not top_category:
        return "没有查询到门店品类营业额数据。"

    category = top_category.get(
        "category"
    )

    category_sales = top_category.get(
        "total_sales",
        0
    )

    if time_expression:
        return (
            f"{time_expression}门店品类中，"
            f"{category}营业额最高，"
            f"为{category_sales:.0f}元。"
        )

    return (
        f"门店品类中，{category}营业额最高，"
        f"为{category_sales:.0f}元。"
    )


# 3. 生成门店品类比较回答
def _answer_store_category_comparison(items: list):
    valid_items = []

    for item in items:
        task = item.get(
            "task",
            {}
        )

        result = item.get(
            "result",
            {}
        )

        if not result.get("success"):
            continue

        valid_items.append(
            {
                "time": task.get(
                    "time_expression"
                ) or "",
                "query_mode": task.get(
                    "query_mode"
                ),
                "result": result,
            }
        )

    if len(valid_items) < 2:
        return None

    times = list(
        dict.fromkeys(
            item["time"]
            for item in valid_items
        )
    )

    if len(times) < 2:
        return None

    first = valid_items[0]
    last = valid_items[-1]

    # 1. 各品类明细比较
    if (
        first["query_mode"] == "detail"
        and last["query_mode"] == "detail"
    ):
        first_data = first["result"].get(
            "data",
            []
        )

        last_data = last["result"].get(
            "data",
            []
        )

        if not first_data or not last_data:
            return None

        first_sales = {
            item.get("category"): item.get(
                "total_sales",
                0
            )
            for item in first_data
            if item.get("category")
        }

        last_sales = {
            item.get("category"): item.get(
                "total_sales",
                0
            )
            for item in last_data
            if item.get("category")
        }

        categories = list(
            dict.fromkeys(
                list(first_sales.keys())
                + list(last_sales.keys())
            )
        )

        comparisons = []

        for category in categories:
            first_value = first_sales.get(
                category,
                0
            )

            last_value = last_sales.get(
                category,
                0
            )

            diff = (
                last_value
                - first_value
            )

            trend = (
                "增加"
                if diff >= 0
                else "减少"
            )

            sentence = (
                f"{category}从"
                f"{first['time']}的{first_value:.0f}元"
                f"变为{last['time']}的{last_value:.0f}元，"
                f"{trend}{abs(diff):.0f}元"
            )

            if first_value != 0:
                change_rate = (
                    diff
                    / first_value
                    * 100
                )

                sentence += (
                    f"，变化率为"
                    f"{abs(change_rate):.2f}%"
                )

            comparisons.append(
                sentence + "。"
            )

        if not comparisons:
            return None

        return "".join(
            comparisons
        )

    # 2. 最高品类比较
    first_top = first["result"].get(
        "top_category"
    )

    last_top = last["result"].get(
        "top_category"
    )

    if not first_top or not last_top:
        return None

    first_category = first_top.get(
        "category"
    )

    last_category = last_top.get(
        "category"
    )

    first_sales = first_top.get(
        "total_sales",
        0
    )

    last_sales = last_top.get(
        "total_sales",
        0
    )

    diff = (
        last_sales
        - first_sales
    )

    trend = (
        "增加"
        if diff >= 0
        else "减少"
    )

    # 最高品类发生变化
    if first_category != last_category:
        answer = (
            f"最高营业额品类从"
            f"{first['time']}的{first_category}"
            f"变为{last['time']}的{last_category}，"
            f"最高品类营业额从"
            f"{first_sales:.0f}元变为"
            f"{last_sales:.0f}元，"
            f"{trend}{abs(diff):.0f}元"
        )

    # 最高品类保持不变
    else:
        answer = (
            f"{first['time']}和{last['time']}"
            f"最高营业额品类均为{first_category}，"
            f"营业额从{first_sales:.0f}元变为"
            f"{last_sales:.0f}元，"
            f"{trend}{abs(diff):.0f}元"
        )

    if first_sales != 0:
        change_rate = (
            diff
            / first_sales
            * 100
        )

        answer += (
            f"，变化率为"
            f"{abs(change_rate):.2f}%"
        )

    return answer + "。"

# 4. 生成总营业额回答
def _answer_total_sales(item: dict):
    task = item.get(
        "task",
        {}
    )

    result = item.get(
        "result",
        {}
    )

    if not result.get("success"):
        return None

    time_expression = task.get(
        "time_expression"
    ) or ""

    query_mode = task.get(
        "query_mode"
    ) or "value"

    metric = task.get(
        "metric"
    ) or "营业额"

    # 1. 订单数
    if metric == "订单数":
        if (
            query_mode == "trend"
            and result.get("comparison")
        ):
            current = result.get(
                "current",
                {}
            )

            previous = result.get(
                "previous",
                {}
            )

            current_orders = current.get(
                "order_count",
                0
            )

            previous_orders = previous.get(
                "order_count",
                0
            )

            diff = (
                current_orders
                - previous_orders
            )

            trend = (
                "增加"
                if diff >= 0
                else "减少"
            )

            answer = (
                f"最近一期订单数为"
                f"{current_orders}单，"
                f"上一期为"
                f"{previous_orders}单，"
                f"{trend}{abs(diff)}单"
            )

            if previous_orders != 0:
                change_rate = (
                    diff
                    / previous_orders
                    * 100
                )

                answer += (
                    f"，变化率为"
                    f"{abs(change_rate):.2f}%"
                )

            return answer + "。"

        order_count = result.get(
            "order_count",
            0
        )

        if time_expression == "最近":
            return (
                f"最近一期订单数为"
                f"{order_count}单。"
            )

        if time_expression:
            return (
                f"{time_expression}订单数为"
                f"{order_count}单。"
            )

        return (
            f"订单数为"
            f"{order_count}单。"
        )

    # 2. 最近营业额趋势
    if (
        query_mode == "trend"
        and result.get("comparison")
    ):
        current = result.get(
            "current",
            {}
        )

        previous = result.get(
            "previous",
            {}
        )

        current_sales = current.get(
            "total_sales",
            0
        )

        previous_sales = previous.get(
            "total_sales",
            0
        )

        diff = (
            current_sales
            - previous_sales
        )

        trend = (
            "增加"
            if diff >= 0
            else "减少"
        )

        answer = (
            f"最近一期总营业额为"
            f"{current_sales:.0f}元，"
            f"上一期为"
            f"{previous_sales:.0f}元，"
            f"{trend}{abs(diff):.0f}元"
        )

        if previous_sales != 0:
            change_rate = (
                diff
                / previous_sales
                * 100
            )

            answer += (
                f"，变化率为"
                f"{abs(change_rate):.2f}%"
            )

        return answer + "。"

    # 3. 单期总营业额
    total_sales = result.get(
        "total_sales",
        0
    )

    if time_expression == "最近":
        return (
            f"最近一期总营业额为"
            f"{total_sales:.0f}元。"
        )

    if time_expression:
        return (
            f"{time_expression}总营业额为"
            f"{total_sales:.0f}元。"
        )

    return (
        f"总营业额为"
        f"{total_sales:.0f}元。"
    )


# 5. 生成总营业额比较回答
def _answer_total_sales_comparison(items: list):
    records = []

    # 1. 收集有效结果
    for item in items:
        task = item.get(
            "task",
            {}
        )

        result = item.get(
            "result",
            {}
        )

        if not result.get("success"):
            continue

        records.append(
            {
                "time": task.get(
                    "time_expression"
                ) or "",
                "metric": task.get(
                    "metric"
                ) or "营业额",
                "result": result,
            }
        )

    if len(records) < 2:
        return None

    times = list(
        dict.fromkeys(
            item["time"]
            for item in records
        )
    )

    if len(times) < 2:
        return None

    # 2. 防止不同指标被错误比较
    metrics = list(
        dict.fromkeys(
            item["metric"]
            for item in records
        )
    )

    if len(metrics) != 1:
        return None

    metric = metrics[0]
    first = records[0]
    last = records[-1]

    # 3. 订单数跨时间比较
    if metric == "订单数":
        first_value = first["result"].get(
            "order_count",
            0
        )

        last_value = last["result"].get(
            "order_count",
            0
        )

        diff = (
            last_value
            - first_value
        )

        trend = (
            "增加"
            if diff >= 0
            else "减少"
        )

        answer = (
            f"订单数从{first['time']}的"
            f"{first_value}单变为"
            f"{last['time']}的"
            f"{last_value}单，"
            f"{trend}{abs(diff)}单"
        )

        if first_value != 0:
            change_rate = (
                diff
                / first_value
                * 100
            )

            answer += (
                f"，变化率为"
                f"{abs(change_rate):.2f}%"
            )

        return answer + "。"

    # 4. 总营业额跨时间比较
    first_value = first["result"].get(
        "total_sales",
        0
    )

    last_value = last["result"].get(
        "total_sales",
        0
    )

    diff = (
        last_value
        - first_value
    )

    trend = (
        "增加"
        if diff >= 0
        else "减少"
    )

    answer = (
        f"总营业额从{first['time']}的"
        f"{first_value:.0f}元变为"
        f"{last['time']}的"
        f"{last_value:.0f}元，"
        f"{trend}{abs(diff):.0f}元"
    )

    if first_value != 0:
        change_rate = (
            diff
            / first_value
            * 100
        )

        answer += (
            f"，变化率为"
            f"{abs(change_rate):.2f}%"
        )

    return answer + "。"


# 6. 生成客单价趋势回答
def _answer_avg_order_value_trend(item: dict):
    task = item.get(
        "task",
        {}
    )

    result = item.get(
        "result",
        {}
    )

    if not result.get("success"):
        return None

    query_mode = task.get(
        "query_mode"
    ) or "trend"

    time_expression = task.get(
        "time_expression"
    ) or ""

    # 1. 客单价单期值
    if query_mode == "value":
        avg_order_value = result.get(
            "avg_order_value",
            0
        )

        if time_expression:
            return (
                f"{time_expression}客单价为"
                f"{avg_order_value:.2f}元。"
            )

        return (
            f"客单价为"
            f"{avg_order_value:.2f}元。"
        )

    # 2. 客单价趋势
    current = result.get(
        "current_avg_order_value",
        0
    )

    previous = result.get(
        "previous_avg_order_value",
        0
    )

    change = result.get(
        "change",
        0
    )

    change_rate = result.get(
        "change_rate",
        0
    )

    trend = result.get(
        "trend",
        ""
    )

    return (
        f"当前客单价为{current:.2f}元，"
        f"上一期为{previous:.2f}元，"
        f"{trend}{abs(change):.2f}元，"
        f"变化率为{abs(change_rate):.2f}%。"
    )


def _answer_avg_order_value_comparison(items: list):
    valid_items = []

    # 1. 收集客单价单期结果
    for item in items:
        task = item.get(
            "task",
            {}
        )

        result = item.get(
            "result",
            {}
        )

        if (
            task.get("query_mode") != "value"
            or not result.get("success")
        ):
            continue

        valid_items.append(
            {
                "time": task.get(
                    "time_expression"
                ) or "",
                "value": result.get(
                    "avg_order_value",
                    0
                ),
            }
        )

    # 2. 至少需要两个时间
    if len(valid_items) < 2:
        return None

    times = list(
        dict.fromkeys(
            item["time"]
            for item in valid_items
        )
    )

    if len(times) < 2:
        return None

    first = valid_items[0]
    last = valid_items[-1]

    diff = (
        last["value"]
        - first["value"]
    )

    trend = (
        "增加"
        if diff >= 0
        else "减少"
    )

    answer = (
        f"客单价从"
        f"{first['time']}的{first['value']:.2f}元"
        f"变为{last['time']}的{last['value']:.2f}元，"
        f"{trend}{abs(diff):.2f}元"
    )

    # 3. 计算变化率
    if first["value"] != 0:
        change_rate = (
            diff
            / first["value"]
            * 100
        )

        answer += (
            f"，变化率为"
            f"{abs(change_rate):.2f}%"
        )

    return answer + "。"

# 7. 生成天气信息回答
def _answer_weather_info(item: dict):
    task = item.get(
        "task",
        {}
    )

    result = item.get(
        "result",
        {}
    )

    if not result.get("success"):
        return None

    location = (
        result.get("location_name")
        or task.get("location")
        or ""
    )

    time_expression = (
        task.get("time_expression")
        or ""
    )

    # 1. 生成降雨查询回答
    weather_query = (
        task.get("weather_query")
        or "general"
    )

    day_weather = result.get(
        "day_weather"
    )

    night_weather = result.get(
        "night_weather"
    )

    if (
        weather_query == "rain"
        and (
            day_weather
            or night_weather
        )
    ):
        day_weather = (
            day_weather
            or "未知"
        )

        night_weather = (
            night_weather
            or "未知"
        )

        has_rain = (
            "雨" in day_weather
            or "雨" in night_weather
        )

        answer = (
            f"{location}{time_expression}"
            f"预报白天{day_weather}，"
            f"夜间{night_weather}"
        )

        if has_rain:
            answer += "，有降雨天气"
        else:
            answer += "，当前预报暂未显示降雨"

        return answer + "。"

    # 2. 今天实况天气
    if time_expression in {
        "今天",
        "今日",
    }:
        weather = (
            result.get("weather")
            or "天气情况未知"
        )

        temperature = result.get(
            "temperature"
        )

        humidity = result.get(
            "humidity"
        )

        wind_direction = result.get(
            "wind_direction"
        ) or ""

        wind_power = result.get(
            "wind_power"
        ) or ""

        answer = (
            f"{location}{time_expression}"
            f"{weather}"
        )

        if temperature not in {
            None,
            "",
        }:
            answer += (
                f"，当前温度"
                f"{temperature}℃"
            )

        if humidity not in {
            None,
            "",
        }:
            answer += (
                f"，湿度"
                f"{humidity}%"
            )

        if wind_direction or wind_power:
            answer += (
                f"，{wind_direction}风"
                f"{wind_power}级"
            )

        return answer + "。"

    # 3. 明天天气预报
    day_weather = (
        result.get("day_weather")
        or "未知"
    )

    night_weather = (
        result.get("night_weather")
        or "未知"
    )

    day_temperature = result.get(
        "day_temperature"
    )

    night_temperature = result.get(
        "night_temperature"
    )

    day_wind_direction = (
        result.get("day_wind_direction")
        or ""
    )

    day_wind_power = (
        result.get("day_wind_power")
        or ""
    )

    answer = (
        f"{location}{time_expression}"
        f"白天{day_weather}，"
        f"夜间{night_weather}"
    )

    if day_temperature not in {
        None,
        "",
    }:
        answer += (
            f"，最高{day_temperature}℃"
        )

    if night_temperature not in {
        None,
        "",
    }:
        answer += (
            f"，最低{night_temperature}℃"
        )

    if (
        day_wind_direction
        or day_wind_power
    ):
        answer += (
            f"，{day_wind_direction}风"
            f"{day_wind_power}级"
        )

    return answer + "。"

# 8. 生成失败任务提示
def _answer_failed_task(item: dict):
    task = item.get(
        "task",
        {}
    )

    result = item.get(
        "result",
        {}
    )

    if result.get("success"):
        return None

    intent = task.get("intent")

    message = result.get(
        "message",
        "任务执行失败"
    )

    # 商品查询失败
    if intent == "product_sales":
        product = task.get(
            "product"
        ) or ""

        time_expression = task.get(
            "time_expression"
        ) or ""

        metric = task.get(
            "metric"
        ) or "销售额"

        metric_name = (
            "销量"
            if metric == "销量"
            else "销售额"
        )

        return (
            f"{time_expression}{product}"
            f"{metric_name}查询失败：{message}。"
        )

    # 门店品类查询失败
    if intent == "store_category_sales":
        time_expression = task.get(
            "time_expression"
        ) or ""

        return (
            f"{time_expression}门店品类营业额查询失败："
            f"{message}。"
        )

    # 总营业额查询失败
    if intent == "total_sales":
        time_expression = task.get(
            "time_expression"
        ) or ""

        return (
            f"{time_expression}总营业额查询失败："
            f"{message}。"
        )

    # 客单价查询失败
    if intent == "avg_order_value_trend":
        return (
            f"客单价趋势查询失败："
            f"{message}。"
        )

    # 天气查询失败
    if intent == "weather_info":
        location = task.get(
            "location"
        ) or ""

        time_expression = task.get(
            "time_expression"
        ) or ""

        return (
            f"{location}{time_expression}"
            f"天气查询失败：{message}。"
        )

    return (
        f"任务执行失败："
        f"{message}。"
    )

# 9. 生成最终回答
def generate_final_answer(results: list):
    if not results:
        return "没有查询到相关数据。"

    answers = []

    product_items = [
        item
        for item in results
        if item.get(
            "task",
            {}
        ).get("intent") == "product_sales"
    ]

    if product_items:
        product_answer = _answer_product_sales(
            product_items
        )

        if product_answer:
            answers.append(
                product_answer
            )

    for item in results:
        intent = item.get(
            "task",
            {}
        ).get("intent")

        if intent == "store_category_sales":
            answer = _answer_store_category_sales(
                item
            )

            if answer:
                answers.append(
                    answer
                )

        elif intent == "total_sales":
            answer = _answer_total_sales(
                item
            )

            if answer:
                answers.append(
                    answer
                )

        elif intent == "avg_order_value_trend":
            answer = _answer_avg_order_value_trend(
                item
            )

            if answer:
                answers.append(
                    answer
                )

        elif intent == "weather_info":
            answer = _answer_weather_info(
                item
            )

            if answer:
                answers.append(
                    answer
                )

    # 门店品类跨时间比较
    store_category_items = [
        item
        for item in results
        if item.get(
            "task",
            {}
        ).get("intent") == "store_category_sales"
    ]

    store_category_comparison = (
        _answer_store_category_comparison(
            store_category_items
        )
    )

    if store_category_comparison:
        answers.append(
            store_category_comparison
        )

    # 总营业额跨时间比较
    total_sales_items = [
        item
        for item in results
        if item.get(
            "task",
            {}
        ).get("intent") == "total_sales"
    ]

    total_sales_comparison = (
        _answer_total_sales_comparison(
            total_sales_items
        )
    )

    if total_sales_comparison:
        answers.append(
            total_sales_comparison
        )

    # 客单价跨时间比较
    avg_order_value_items = [
        item
        for item in results
        if item.get(
            "task",
            {}
        ).get("intent") == "avg_order_value_trend"
    ]

    avg_order_value_comparison = (
        _answer_avg_order_value_comparison(
            avg_order_value_items
        )
    )

    if avg_order_value_comparison:
        answers.append(
            avg_order_value_comparison
        )

    # 添加失败任务提示
    for item in results:
        failure_answer = _answer_failed_task(
            item
        )

        if failure_answer:
            answers.append(
                failure_answer
            )

    if not answers:
        return "暂时无法生成查询结果。"

    return "\n".join(
        answers
    )