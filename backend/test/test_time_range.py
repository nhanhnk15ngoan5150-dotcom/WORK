from services.time_service import (
    parse_time_expression,
)


# 1. 数据范围之前
print(
    "四月:",
    parse_time_expression(
        "四月"
    )
)


# 2. 正常月份
print(
    "五月:",
    parse_time_expression(
        "五月"
    )
)

print(
    "七月:",
    parse_time_expression(
        "七月"
    )
)


# 3. 数据范围之后
print(
    "八月:",
    parse_time_expression(
        "八月"
    )
)


# 4. 真正无法识别
print(
    "未知:",
    parse_time_expression(
        "十三月"
    )
)