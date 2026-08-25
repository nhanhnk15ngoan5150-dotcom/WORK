from services.answer_service import (
    _answer_avg_order_value_comparison,
)


# 1. 五月到六月客单价比较
items = [
    {
        "task": {
            "intent": "avg_order_value_trend",
            "time_expression": "五月",
            "query_mode": "value",
        },
        "result": {
            "success": True,
            "avg_order_value": 36.72,
        },
    },
    {
        "task": {
            "intent": "avg_order_value_trend",
            "time_expression": "六月",
            "query_mode": "value",
        },
        "result": {
            "success": True,
            "avg_order_value": 35.17,
        },
    },
]

answer = _answer_avg_order_value_comparison(
    items
)

print("\n================")
print("回答:", answer)


# 2. 单任务不能生成跨期比较
single_answer = _answer_avg_order_value_comparison(
    items[:1]
)

print("\n================")
print("单任务:", single_answer)