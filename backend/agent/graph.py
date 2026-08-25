from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.nodes import (
    understanding_node,
    entity_node,
    validation_node,
    planner_node,
    executor_node,
    answer_node,
    clarification_node,
    unsupported_node,
    planning_failed_node,
    validation_route,
    planner_route,
)


# 1. 创建工作流
workflow = StateGraph(
    AgentState
)


# 2. 注册节点
workflow.add_node(
    "understanding",
    understanding_node
)

workflow.add_node(
    "entity",
    entity_node
)

workflow.add_node(
    "validation",
    validation_node
)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "executor",
    executor_node
)

workflow.add_node(
    "answer",
    answer_node
)

workflow.add_node(
    "clarification",
    clarification_node
)

workflow.add_node(
    "unsupported",
    unsupported_node
)

workflow.add_node(
    "planning_failed",
    planning_failed_node
)


# 3. 连接基础流程
workflow.add_edge(
    START,
    "understanding"
)

workflow.add_edge(
    "understanding",
    "entity"
)

workflow.add_edge(
    "entity",
    "validation"
)


# 4. 添加 Validation 条件分支
workflow.add_conditional_edges(
    "validation",
    validation_route,
    {
        "planner": "planner",
        "clarification": "clarification",
        "unsupported": "unsupported",
    }
)


# 5. 添加 Planner 条件分支
workflow.add_conditional_edges(
    "planner",
    planner_route,
    {
        "executor": "executor",
        "planning_failed": "planning_failed",
    }
)


# 6. 连接执行流程
workflow.add_edge(
    "executor",
    "answer"
)

workflow.add_edge(
    "answer",
    END
)

workflow.add_edge(
    "clarification",
    END
)

workflow.add_edge(
    "unsupported",
    END
)

workflow.add_edge(
    "planning_failed",
    END
)


# 7. 编译 Graph
graph = workflow.compile()