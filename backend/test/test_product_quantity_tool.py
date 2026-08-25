from tools.product_tool import (
    get_product_sales,
    get_product_quantity,
)


# 1. 测试六月可乐销量
quantity_result = get_product_quantity(
    product_name="可乐",
    start_date="2026-06-01",
    end_date="2026-07-01",
)

print(
    "销量:",
    quantity_result
)


# 2. 回归六月可乐销售额
sales_result = get_product_sales(
    product_name="可乐",
    start_date="2026-06-01",
    end_date="2026-07-01",
)

print(
    "销售额:",
    sales_result
)