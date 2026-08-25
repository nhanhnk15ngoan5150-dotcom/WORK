from services.llm_service import understand_question

from agent.planner import create_plan

from agent.executor import execute_plan

from services.answer_service import generate_final_answer



def run_agent(
    question:str,
    history:list=None
):


    if history is None:

        history = []



    # 1. 理解用户问题
    understanding = understand_question(
        question,
        history
    )



    # 2. 任务规划
    plan = create_plan(
        understanding
    )



    # 3. 执行任务
    results = execute_plan(
        plan
    )



    # 4. 生成回答
    answer = generate_final_answer(
        results
    )


    return {

        "question":question,

        "understanding":understanding,

        "plan":plan,

        "results":results,

        "answer":answer

    }