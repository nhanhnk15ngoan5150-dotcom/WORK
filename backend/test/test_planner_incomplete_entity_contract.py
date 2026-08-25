from agent.nodes import planner_node


# 1. 普通完整任务
normal_state = {
    "entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        }
    ]
}

normal_result = planner_node(
    normal_state
)

print("\n================")
print("普通完整任务:")
print(normal_result)


# 2. 完整任务 + 缺地点天气任务
mixed_state = {
    "entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        },
        {
            "intent": "weather_info",
            "products": [],
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        },
    ]
}

mixed_result = planner_node(
    mixed_state
)

print("\n================")
print("混合不完整任务修改前:")
print(mixed_result)


# 3. 锁定普通 Planner 旧契约
assert normal_result == {
    "plan": [
        {
            "intent": "total_sales",
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        }
    ],
    "planning_failed": False,
    "planning_error": None,
}


# 4. 锁定当前 Planner 不过滤缺条件任务
assert mixed_result == {
    "plan": [
        {
            "intent": "total_sales",
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        },
        {
            "intent": "weather_info",
            "location": None,
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        },
    ],
    "planning_failed": False,
    "planning_error": None,
}

print("\n================")
print(
    "Planner 不完整任务修改前契约: PASS"
)

# 5. 测试验证后的可执行实体
validated_state = {
    "entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        },
        {
            "intent": "weather_info",
            "products": [],
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "general",
        },
    ],
    "validated_entities": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        }
    ],
}

validated_result = planner_node(
    validated_state
)

print("\n================")
print("验证后可执行任务:")
print(validated_result)


# 6. 锁定 validated_entities 优先级
assert validated_result == {
    "plan": [
        {
            "intent": "total_sales",
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend",
        }
    ],
    "planning_failed": False,
    "planning_error": None,
}

print("\n================")
print(
    "Planner validated_entities 契约: PASS"
)