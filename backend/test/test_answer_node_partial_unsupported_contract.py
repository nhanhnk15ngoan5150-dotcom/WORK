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

    # 3. 全部任务成功
    all_success = nodes.answer_node(
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
    print("全部成功:")
    print(all_success)

    # 4. 部分执行失败
    partial_failure = nodes.answer_node(
        {
            "results": [
                {
                    "result": {
                        "success": True
                    }
                },
                {
                    "result": {
                        "success": False
                    }
                },
            ]
        }
    )

    print("\n================")
    print("部分执行失败:")
    print(partial_failure)

    # 5. 全部任务失败
    all_failed = nodes.answer_node(
        {
            "results": [
                {
                    "result": {
                        "success": False
                    }
                }
            ]
        }
    )

    print("\n================")
    print("全部执行失败:")
    print(all_failed)

    # 6. 当前部分能力外行为
    partial_unsupported = nodes.answer_node(
        {
            "results": [
                {
                    "result": {
                        "success": True
                    }
                }
            ],
            "partial_unsupported": True,
            "partial_unsupported_reason": (
                "部分请求超出餐饮经营数据分析能力范围"
            ),
        }
    )

    print("\n================")
    print("部分能力外修改前:")
    print(partial_unsupported)

finally:
    # 7. 恢复原回答函数
    nodes.generate_final_answer = (
        original_generate_final_answer
    )


# 8. 锁定 Answer Node 旧契约
assert all_success == {
    "answer": "业务回答",
    "success": True,
    "error": None,
}

assert partial_failure == {
    "answer": "业务回答",
    "success": True,
    "error": "部分任务执行失败",
}

assert all_failed == {
    "answer": "业务回答",
    "success": False,
    "error": "全部任务执行失败",
}


# 9. 锁定当前 Partial Unsupported 缺口
assert partial_unsupported == {
    "answer": (
        "业务回答\n"
        "部分请求超出餐饮经营数据分析能力范围"
    ),
    "success": True,
    "error": "部分请求超出能力范围",
}

print("\n================")
print(
    "Answer Node Partial Unsupported "
    "契约: PASS"
)