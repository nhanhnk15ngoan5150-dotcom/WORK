MAX_HISTORY_ROUNDS = 20
MAX_STRUCTURED_ROUNDS = 20


# 1. 裁剪对话历史
def trim_history(history: list):
    max_messages = MAX_HISTORY_ROUNDS * 2

    if len(history) <= max_messages:
        return history

    return history[-max_messages:]


# 2. 添加一轮对话
def append_round(
    history: list,
    user_message: str,
    assistant_message: str
):
    new_history = list(
        history or []
    )

    new_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    new_history.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    return trim_history(
        new_history
    )


# 3. 更新最近业务上下文
def update_structured_context(
    context: dict,
    understanding: dict,
    entities: list
):
    tasks = understanding.get(
        "tasks",
        []
    )

    if not tasks:
        return dict(
            context or {}
        )

    last_task = tasks[-1]

    new_context = {
        "intent": last_task.get("intent"),
        "time_expression": last_task.get("time_expression") or "",
        "metric": last_task.get("metric"),
        "query_mode": last_task.get("query_mode"),
        "products": [],
    }

    # * 仅保存有效分析模式
    analysis_mode = last_task.get("analysis_mode")

    if analysis_mode is not None:
        new_context["analysis_mode"] = analysis_mode

    # * 保存天气上下文
    if last_task.get("intent") == "weather_info":
        location = last_task.get("location")

        if location:
            new_context["location"] = location

        weather_query = last_task.get("weather_query")

        if weather_query:
            new_context["weather_query"] = weather_query

    if entities:
        last_entity_task = entities[-1]

        new_context["products"] = [
            item.get("standard")
            for item in last_entity_task.get(
                "products",
                []
            )
            if item.get("standard")
        ]

        new_context["products"] = [
            item.get("standard")
            for item in last_entity_task.get(
                "products",
                []
            )
            if item.get("standard")
        ]

    return new_context


# 4. 裁剪结构化记忆
def trim_structured_memory(
    memory: list
):
    if len(memory) <= MAX_STRUCTURED_ROUNDS:
        return memory

    return memory[-MAX_STRUCTURED_ROUNDS:]


# 5. 添加结构化业务记忆
def append_structured_memory(
    memory: list,
    question: str,
    understanding: dict,
    entities: list
):
    new_memory = list(
        memory or []
    )

    tasks = understanding.get(
        "tasks",
        []
    )

    if not tasks:
        return trim_structured_memory(
            new_memory
        )

    memory_tasks = []

    for index, task in enumerate(tasks):
        standard_products = []

        if index < len(entities):
            entity_task = entities[index]

            standard_products = [
                item.get("standard")
                for item in entity_task.get(
                    "products",
                    []
                )
                if item.get("standard")
            ]

        # * 构造结构化记忆任务
        memory_task = {
            "intent": task.get("intent"),
            "products": standard_products,
            "time_expression": task.get(
                "time_expression"
            ),
            "metric": task.get("metric"),
            "query_mode": task.get("query_mode"),
        }

        # * 仅保存有效分析模式
        analysis_mode = task.get("analysis_mode")

        if analysis_mode is not None:
            memory_task["analysis_mode"] = analysis_mode

        # * 保存天气结构化记忆
        if task.get("intent") == "weather_info":
            location = task.get("location")

            if location:
                memory_task["location"] = location

            weather_query = task.get("weather_query")

            if weather_query:
                memory_task["weather_query"] = weather_query

        memory_tasks.append(memory_task)

    new_memory.append(
        {
            "question": question,
            "tasks": memory_tasks,
        }
    )

    return trim_structured_memory(
        new_memory
    )