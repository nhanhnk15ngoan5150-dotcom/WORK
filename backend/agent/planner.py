from services.entity_service import resolve_product_entity


# 1. 兼容旧版 Understanding 输入
def _build_entities_from_understanding(understanding: dict):
    entities = []

    for task in understanding.get("tasks", []):
        resolved_products = []

        for product in task.get("products", []):
            resolved_products.append(
                resolve_product_entity(product)
            )

        entity_task = {
            "intent": task.get("intent"),
            "products": resolved_products,
            "time_expression": task.get("time_expression"),
            "metric": task.get("metric"),
            "query_mode": task.get("query_mode"),
        }

        # 1. 保存天气地点
        location = task.get("location")

        if location:
            entity_task["location"] = location

        # 2. 保存天气查询类型
        weather_query = task.get(
            "weather_query"
        )

        if weather_query:
            entity_task[
                "weather_query"
            ] = weather_query

        # 3. 保存新闻主题
        topic = task.get("topic")

        if topic:
            entity_task["topic"] = topic

        entities.append(
            entity_task
        )

    return entities


# 2. 创建商品销售任务
def _create_product_sales_tasks(task: dict):
    plan = []

    for entity in task.get("products", []):
        plan.append(
            {
                "intent": "product_sales",
                "product": entity.get("standard"),
                "time_expression": task.get("time_expression"),
                "metric": task.get("metric"),
                "query_mode": task.get("query_mode"),
                "entity_method": entity.get("method"),
                "confidence": entity.get("confidence"),
            }
        )

    return plan


# 3. 创建门店品类销售任务
def _create_store_category_task(task: dict):
    return {
        "intent": "store_category_sales",
        "time_expression": task.get("time_expression"),
        "query_mode": task.get("query_mode"),
        "analysis_mode": task.get("analysis_mode"),
    }

# 5. 创建天气查询任务
def _create_weather_info_task(task: dict):
    weather_task = {
        "intent": "weather_info",
        "location": task.get("location"),
        "time_expression": task.get("time_expression"),
        "metric": task.get("metric"),
    }

    # 1. 保存天气查询类型
    weather_query = task.get(
        "weather_query"
    )

    if weather_query:
        weather_task[
            "weather_query"
        ] = weather_query

    return weather_task

def _create_news_info_task(task: dict):
    return {
        "intent": "news_info",
        "topic": task.get("topic"),
        "time_expression": task.get("time_expression"),
        "metric": task.get("metric"),
    }


# 4. 创建总营业额任务
def _create_total_sales_task(task: dict):
    return {
        "intent": "total_sales",
        "time_expression": task.get("time_expression"),
        "metric": task.get("metric"),
        "query_mode": task.get("query_mode"),
    }


# 5. 创建客单价趋势任务
def _create_avg_order_value_task(task: dict):
    return {
        "intent": "avg_order_value_trend",
        "time_expression": task.get("time_expression"),
        "query_mode": task.get("query_mode"),
    }

# 6. 创建执行计划
def create_plan(data: dict):
    entities = data.get("entities")

    if entities is None:
        entities = _build_entities_from_understanding(data)

    plan = []

    for task in entities:
        intent = task.get("intent")

        if intent == "product_sales":
            plan.extend(
                _create_product_sales_tasks(task)
            )

        elif intent == "store_category_sales":
            plan.append(
                _create_store_category_task(task)
            )

        elif intent == "total_sales":
            plan.append(
                _create_total_sales_task(task)
            )

        elif intent == "avg_order_value_trend":
            plan.append(
                _create_avg_order_value_task(task)
            )

        elif intent == "weather_info":
            plan.append(
                _create_weather_info_task(task)
            )

        elif intent == "news_info":
            plan.append(
                _create_news_info_task(task)
            )

    return plan