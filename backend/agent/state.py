from typing import TypedDict


# 1. 定义 Agent 全流程状态
class AgentState(TypedDict, total=False):
    question: str

    conversation_history: list
    structured_context: dict
    structured_memory: list

    understanding: dict
    entities: list
    plan: list
    results: list

    answer: str

    need_clarification: bool
    clarification_reason: str | None

    unsupported: bool
    unsupported_reason: str | None

    # 2. 部分能力范围外状态
    partial_unsupported: bool
    partial_unsupported_reason: str | None

    # 3. 部分澄清状态
    partial_clarification: bool
    partial_clarification_reason: str | None

    # 4. 验证通过的可执行实体
    validated_entities: list

    planning_failed: bool
    planning_error: str | None

    error: str | None
    success: bool