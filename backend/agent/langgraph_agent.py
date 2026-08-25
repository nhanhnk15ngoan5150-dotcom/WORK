from agent.graph import graph

from services.context_service import (
    append_round,
    trim_history,
    update_structured_context,
    append_structured_memory,
    trim_structured_memory,
)


# 1. 执行 LangGraph Agent
def run_langgraph_agent(
    question: str,
    conversation_history: list | None = None,
    structured_context: dict | None = None,
    structured_memory: list | None = None
):
    history = trim_history(
        conversation_history or []
    )

    business_context = dict(
        structured_context or {}
    )

    business_memory = trim_structured_memory(
        structured_memory or []
    )

    # 2. 初始化 LangGraph State
    initial_state = {
        "question": question,
        "conversation_history": history,
        "structured_context": business_context,
        "structured_memory": business_memory,
        "success": False,
        "error": None,
    }

    # 3. 执行 LangGraph
    result = graph.invoke(
        initial_state
    )

    answer = result.get(
        "answer",
        ""
    )

    # 4. 更新原始对话历史
    updated_history = append_round(
        history,
        question,
        answer
    )

    # 5. 判断本轮是否允许写入业务记忆
    can_update_memory = (
            result.get(
                "success",
                False
            )
            and result.get(
        "error"
    ) is None
            and not result.get(
        "need_clarification",
        False
    )
            and not result.get(
        "unsupported",
        False
    )
            and not result.get(
        "planning_failed",
        False
    )
    )

    # 6. 更新业务上下文和结构化记忆
    if can_update_memory:
        updated_context = update_structured_context(
            business_context,
            result.get(
                "understanding",
                {}
            ),
            result.get(
                "entities",
                []
            )
        )

        updated_memory = append_structured_memory(
            business_memory,
            question,
            result.get(
                "understanding",
                {}
            ),
            result.get(
                "entities",
                []
            )
        )

    else:
        updated_context = business_context
        updated_memory = business_memory

    # 7. 返回完整结果
    return {
        "success": result.get("success", False),
        "question": question,
        "understanding": result.get("understanding", {}),
        "entities": result.get("entities", []),
        "plan": result.get("plan", []),
        "results": result.get("results", []),
        "answer": answer,
        "conversation_history": updated_history,
        "structured_context": updated_context,
        "structured_memory": updated_memory,
        "error": result.get("error"),
    }