from services.llm_service import understand_question
from services.entity_service import resolve_product_entity
from services.answer_service import generate_final_answer

from agent.planner import create_plan
from agent.executor import execute_plan


# 1. 理解用户问题
def understanding_node(state):
    understanding = understand_question(
        state["question"],
        state.get("conversation_history", []),
        state.get("structured_context", {}),
        state.get("structured_memory", [])
    )

    return {
        "understanding": understanding
    }


# 2. 解析业务实体
def entity_node(state):
    entities = []

    for task in state["understanding"].get("tasks", []):
        resolved_products = []

        for product in task.get("products", []):
            entity = resolve_product_entity(product)

            entity["original"] = product

            resolved_products.append(
                entity
            )

        # * 构造实体任务
        entity_task = {
            "intent": task.get("intent"),
            "products": resolved_products,
            "time_expression": task.get("time_expression"),
            "metric": task.get("metric"),
        }

        # * 仅保存有效查询模式
        query_mode = task.get("query_mode")

        if query_mode is not None:
            entity_task["query_mode"] = query_mode

        # * 仅保存有效分析模式
        analysis_mode = task.get("analysis_mode")

        if analysis_mode is not None:
            entity_task["analysis_mode"] = analysis_mode

        # * 保存天气地点
        location = task.get("location")

        if location:
            entity_task["location"] = location

        # * 保存天气查询类型
        weather_query = task.get("weather_query")

        if weather_query:
            entity_task["weather_query"] = weather_query

        # * 保存新闻主题
        topic = task.get("topic")

        if topic:
            entity_task["topic"] = topic

        entities.append(entity_task)

    return {
        "entities": entities
    }


# 3. 验证理解和实体结果
def validation_node(state):
    understanding = state.get(
        "understanding",
        {}
    )

    # 1. 区分纯能力外和部分能力外请求
    if understanding.get("unsupported"):
        tasks = understanding.get(
            "tasks",
            []
        )

        # 1.1 纯能力范围外请求
        if not tasks:
            return {
                "unsupported": True,
                "unsupported_reason": understanding.get(
                    "unsupported_reason"
                ) or "当前问题超出餐饮经营数据分析能力范围",
                "need_clarification": False,
                "clarification_reason": None
            }

        # 1.2 有可执行任务时继续后续验证
        partial_unsupported = True
        partial_unsupported_reason = (
                understanding.get(
                    "unsupported_reason"
                )
                or "部分请求超出餐饮经营数据分析能力范围"
        )

    else:
        partial_unsupported = False
        partial_unsupported_reason = None

    # 2. 处理 Understanding 歧义
    if understanding.get("need_clarification"):
        entities = state.get(
            "entities",
            []
        )

        executable_entities = []
        incomplete_entities = []

        # 2.1 识别缺少必要条件的任务
        for entity in entities:
            if (
                    entity.get("intent")
                    == "weather_info"
                    and not entity.get("location")
            ):
                incomplete_entities.append(
                    entity
                )
            else:
                executable_entities.append(
                    entity
                )

        # 2.2 全部任务都需要澄清
        if (
                incomplete_entities
                and not executable_entities
        ):
            # 2.2.1 同时存在部分能力范围外请求
            if partial_unsupported:
                clarification_reason = (
                        understanding.get(
                            "clarification_reason"
                        )
                        or "请补充更明确的查询条件。"
                )

                return {
                    "unsupported": False,
                    "unsupported_reason": None,
                    "need_clarification": True,
                    "clarification_reason": (
                        f"{clarification_reason}；"
                        f"{partial_unsupported_reason}"
                    ),
                    "partial_unsupported": True,
                    "partial_unsupported_reason": (
                        partial_unsupported_reason
                    )
                }

            # 2.2.2 保持纯澄清旧契约
            return {
                "unsupported": False,
                "unsupported_reason": None,
                "need_clarification": True,
                "clarification_reason": understanding.get(
                    "clarification_reason"
                ) or "请补充更明确的查询条件。"
            }
        # 2.3 部分任务需要澄清
        if (
                incomplete_entities
                and executable_entities
        ):
            partial_clarification = True
            partial_clarification_reason = (
                    understanding.get(
                        "clarification_reason"
                    )
                    or "部分任务缺少必要查询条件。"
            )
            validated_entities = (
                executable_entities
            )

        # 2.4 无法进行任务级隔离时保持旧行为
        else:
            return {
                "unsupported": False,
                "unsupported_reason": None,
                "need_clarification": True,
                "clarification_reason": understanding.get(
                    "clarification_reason"
                ) or "请补充更明确的查询条件。"
            }

    else:
        partial_clarification = False
        partial_clarification_reason = None
        validated_entities = None

        # 2.5 兜底检查天气必要字段
        fallback_incomplete_entities = []
        fallback_executable_entities = []

        for entity in state.get(
            "entities",
            []
        ):
            if (
                entity.get("intent")
                == "weather_info"
                and not entity.get("location")
            ):
                fallback_incomplete_entities.append(
                    entity
                )
            else:
                fallback_executable_entities.append(
                    entity
                )

        # 2.5.1 有其他可执行任务
        if (
            fallback_incomplete_entities
            and fallback_executable_entities
        ):
            partial_clarification = True
            partial_clarification_reason = (
                "天气查询缺少地点信息"
            )
            validated_entities = (
                fallback_executable_entities
            )

        # 2.5.2 纯天气缺地点
        elif (
            fallback_incomplete_entities
            and not partial_unsupported
        ):
            return {
                "unsupported": False,
                "unsupported_reason": None,
                "need_clarification": True,
                "clarification_reason": (
                    "天气查询缺少地点信息"
                )
            }

        # 2.5.3 缺条件任务 + 部分能力范围外
        elif (
            fallback_incomplete_entities
            and partial_unsupported
            and not fallback_executable_entities
        ):
            clarification_reason = (
                "天气查询缺少地点信息；"
                f"{partial_unsupported_reason}"
            )

            return {
                "unsupported": False,
                "unsupported_reason": None,
                "need_clarification": True,
                "clarification_reason": (
                    clarification_reason
                ),
                "partial_unsupported": True,
                "partial_unsupported_reason": (
                    partial_unsupported_reason
                )
            }

    tasks = understanding.get(
        "tasks",
        []
    )

    # 3. 没有可执行任务
    if not tasks:
        return {
            "unsupported": False,
            "unsupported_reason": None,
            "need_clarification": True,
            "clarification_reason": "没有识别到可执行的经营分析任务"
        }


    # 4. 确定需要继续验证的实体
    if validated_entities is not None:
        entities_to_validate = (
            validated_entities
        )
    else:
        entities_to_validate = state.get(
            "entities",
            []
        )

    # 5. 检查实体解析结果
    entity_validated_entities = []
    entity_clarification_reasons = []

    for task in entities_to_validate:
        task_clarification_reason = None
        task_unresolved_products = []

        for product in task.get("products", []):
            original = product.get(
                "original"
            ) or product.get(
                "input"
            )

            # 5.1 Entity 存在多个候选
            if product.get("need_clarification"):
                candidates = product.get(
                    "candidates",
                    []
                )

                if candidates:
                    candidate_text = "、".join(
                        candidates[:5]
                    )

                    task_clarification_reason = (
                        f"“{original}”可能对应多个商品："
                        f"{candidate_text}，请确认具体商品。"
                    )
                else:
                    task_clarification_reason = (
                        f"“{original}”存在商品匹配歧义，请确认具体商品。"
                    )

                break

            # 5.2 Entity 无法匹配
            if not product.get("standard"):
                task_unresolved_products.append(
                    original
                )

        # 5.3 生成商品无法匹配提示
        if (
            not task_clarification_reason
            and task_unresolved_products
        ):
            names = "、".join(
                task_unresolved_products
            )

            task_clarification_reason = (
                f"没有找到与“{names}”对应的商品，"
                f"请确认商品名称。"
            )

        # 5.4 暂停需要澄清的任务
        if task_clarification_reason:
            entity_clarification_reasons.append(
                task_clarification_reason
            )
            continue

        entity_validated_entities.append(
            task
        )

    # 6. 处理商品实体澄清
    if entity_clarification_reasons:
        entity_reason = "；".join(
            entity_clarification_reasons
        )

        # 6.1 全部任务都存在商品澄清
        if not entity_validated_entities:
            # 6.1.1 同时存在部分能力范围外请求
            if partial_unsupported:
                return {
                    "unsupported": False,
                    "unsupported_reason": None,
                    "need_clarification": True,
                    "clarification_reason": (
                        f"{entity_reason}；"
                        f"{partial_unsupported_reason}"
                    ),
                    "partial_unsupported": True,
                    "partial_unsupported_reason": (
                        partial_unsupported_reason
                    )
                }

            # 6.1.2 保持纯商品澄清旧契约
            return {
                "unsupported": False,
                "unsupported_reason": None,
                "need_clarification": True,
                "clarification_reason": entity_reason
            }

        # 6.2 部分任务存在商品歧义
        partial_clarification = True

        if partial_clarification_reason:
            if (
                    entity_reason
                    not in partial_clarification_reason
            ):
                partial_clarification_reason = (
                    f"{partial_clarification_reason}；"
                    f"{entity_reason}"
                )
        else:
            partial_clarification_reason = (
                entity_reason
            )

        validated_entities = (
            entity_validated_entities
        )


    # 7. 验证通过
    result = {
        "unsupported": False,
        "unsupported_reason": None,
        "need_clarification": False,
        "clarification_reason": None
    }

    # 8. 保存部分能力范围外状态
    if partial_unsupported:
        result["partial_unsupported"] = True
        result["partial_unsupported_reason"] = (
            partial_unsupported_reason
        )

    # 9. 保存部分澄清状态
    if partial_clarification:
        result["partial_clarification"] = True
        result["partial_clarification_reason"] = (
            partial_clarification_reason
        )
        result["validated_entities"] = (
            validated_entities
        )

    return result


# 4. 生成执行计划
def planner_node(state):
    # 1. 优先使用验证后的可执行实体
    validated_entities = state.get(
        "validated_entities"
    )

    if validated_entities is None:
        entities = state.get(
            "entities",
            []
        )
    else:
        entities = validated_entities

    # 2. 创建执行计划
    plan = create_plan(
        {
            "entities": entities
        }
    )

    # 3. 处理规划失败
    if not plan:
        return {
            "plan": [],
            "planning_failed": True,
            "planning_error": "未生成可执行计划"
        }

    # 4. 返回执行计划
    return {
        "plan": plan,
        "planning_failed": False,
        "planning_error": None
    }

# 5. 执行任务
def executor_node(state):
    results = execute_plan(
        state["plan"]
    )

    return {
        "results": results
    }


# 6. 生成最终回答
def answer_node(state):
    results = state.get(
        "results",
        []
    )

    answer = generate_final_answer(
        results
    )

    successful_count = sum(
        1
        for item in results
        if item.get(
            "result",
            {}
        ).get(
            "success",
            False
        )
    )

    failed_count = (
        len(results)
        - successful_count
    )

    # 1. 全部成功
    if results and failed_count == 0:
        success = True
        error = None

    # 2. 部分成功
    elif successful_count > 0:
        success = True
        error = "部分任务执行失败"

    # 3. 全部失败或无结果
    else:
        success = False
        error = "全部任务执行失败"

    # 4. 处理部分能力范围外请求
    if state.get(
        "partial_unsupported",
        False
    ):
        reason = state.get(
            "partial_unsupported_reason"
        ) or "部分请求超出餐饮经营数据分析能力范围"

        if answer:
            answer = (
                f"{answer}\n"
                f"{reason}"
            )
        else:
            answer = reason

        # 5. 阻止部分处理轮次写入业务记忆
        if success and error is None:
            error = "部分请求超出能力范围"

    # 6. 处理部分需要澄清请求
    if state.get(
        "partial_clarification",
        False
    ):
        reason = state.get(
            "partial_clarification_reason"
        ) or "部分请求需要补充更明确的查询条件。"

        if answer:
            answer = (
                f"{answer}\n"
                f"{reason}"
            )
        else:
            answer = reason

        # 7. 阻止部分澄清轮次写入业务记忆
        if success and error is None:
            error = "部分请求需要补充条件"

    return {
        "answer": answer,
        "success": success,
        "error": error
    }


# 7. 生成澄清回答
def clarification_node(state):
    reason = state.get(
        "clarification_reason"
    )

    return {
        "answer": reason or "请补充更明确的查询条件。",
        "success": False,
        "error": None
    }


# 8. 生成能力范围外回答
def unsupported_node(state):
    reason = state.get(
        "unsupported_reason"
    )

    return {
        "answer": (
            reason
            or "当前问题超出餐饮经营数据分析能力范围。"
        ),
        "success": False,
        "error": None
    }

# 9. 判断验证后的路由
def validation_route(state):
    if state.get(
        "unsupported",
        False
    ):
        return "unsupported"

    if state.get(
        "need_clarification",
        False
    ):
        return "clarification"

    return "planner"


# 10. 生成规划失败回答
def planning_failed_node(state):
    error = state.get(
        "planning_error"
    )

    return {
        "answer": (
            error
            or "系统暂时无法生成可执行分析计划。"
        ),
        "success": False,
        "error": error or "规划失败"
    }

# 11. 判断 Planner 结果
def planner_route(state):
    if state.get(
        "planning_failed",
        False
    ):
        return "planning_failed"

    return "executor"