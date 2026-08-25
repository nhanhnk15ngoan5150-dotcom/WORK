import agent.nodes as nodes


# 1. 保存原回答函数
original_generate_final_answer = (
    nodes.generate_final_answer
)


def fake_generate_final_answer(results):
    return "业务回答"


try:
    # 2. 使用固定回答隔离 Answer Node 状态逻辑
    nodes.generate_final_answer = (
        fake_generate_final_answer
    )

    # 3. 普通全部成功
    normal_success = nodes.answer_node(
        {
            "results": [
                {
                    "result": {
                        "success": True
                    }
                }
            ]
        }
    )

    print("\n================")
    print("普通全部成功:")
    print(normal_success)

    # 4. 当前部分澄清行为
    partial_clarification = nodes.answer_node(
        {
            "results": [
                {
                    "result": {
                        "success": True
                    }
                }
            ],
            "partial_clarification": True,
            "partial_clarification_reason": (
                "天气查询缺少地点信息"
            ),
        }
    )

    print("\n================")
    print("部分澄清修改前:")
    print(partial_clarification)

finally:
    # 5. 恢复原回答函数
    nodes.generate_final_answer = (
        original_generate_final_answer
    )


# 6. 锁定普通成功旧契约
assert normal_success == {
    "answer": "业务回答",
    "success": True,
    "error": None,
}


# 7. 锁定当前 Partial Clarification 缺口
assert partial_clarification == {
    "answer": (
        "业务回答\n"
        "天气查询缺少地点信息"
    ),
    "success": True,
    "error": "部分请求需要补充条件",
}

print("\n================")
print(
    "Answer Node Partial Clarification "
    "契约: PASS"
)