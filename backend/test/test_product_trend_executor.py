from agent.executor import execute_plan


# 1. 最近商品销售额趋势
sales_plan = [
    {
        "intent": "product_sales",
        "product": "牛肉poke",
        "time_expression": "最近",
        "metric": "销售额",
        "query_mode": "trend"
    }
]

sales_result = execute_plan(
    sales_plan
)

print("\n================")
print("销售额 TREND:", sales_result)


# 2. 最近商品销量趋势
quantity_plan = [
    {
        "intent": "product_sales",
        "product": "可乐",
        "time_expression": "最近",
        "metric": "销量",
        "query_mode": "trend"
    }
]

quantity_result = execute_plan(
    quantity_plan
)

print("\n================")
print("销量 TREND:", quantity_result)


# 3. 最近商品销售额普通值
value_plan = [
    {
        "intent": "product_sales",
        "product": "牛肉poke",
        "time_expression": "最近",
        "metric": "销售额",
        "query_mode": "value"
    }
]

value_result = execute_plan(
    value_plan
)

print("\n================")
print("销售额 VALUE:", value_result)