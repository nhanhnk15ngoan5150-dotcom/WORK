from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.langgraph_agent import run_langgraph_agent

from tools.dashboard_tool import (
    add_months,
    get_dashboard_data,
    get_latest_sales_date,
)
from tools.product_tool import get_product_rank
from tools.store_dashboard_tool import get_store_dashboard_data
from tools.analytics_tool import get_filtered_analytics_data


# 1. 创建 FastAPI 应用
app = FastAPI(
    title="Moneki Restaurant Analysis Agent",
    version="1.0.0",
)


# 2. 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. 定义聊天请求结构
class ChatRequest(BaseModel):
    question: str
    conversation_history: list = Field(
        default_factory=list
    )
    structured_context: dict = Field(
        default_factory=dict
    )
    structured_memory: list = Field(
        default_factory=list
    )


# 4. 健康检查接口
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "restaurant-analysis-agent",
    }


# 5. Dashboard 真实数据接口
@app.get("/api/dashboard")
def dashboard():
    return get_dashboard_data()


# 6. 商品真实数据接口
@app.get("/api/products")
def products():

    # 1. 获取数据库最新有数据月份
    latest_date_text = get_latest_sales_date()

    if not latest_date_text:
        return {
            "success": False,
            "message": "没有查询到商品销售数据",
        }

    month_start = date.fromisoformat(
        latest_date_text
    ).replace(day=1)

    next_month_start = add_months(
        month_start,
        1,
    )

    start_date = month_start.isoformat()
    end_date = next_month_start.isoformat()

    # 2. 查询最新月份商品排行
    result = get_product_rank(
        start_date,
        end_date,
    )

    if not result["success"]:
        return result


    ranking = result["data"]

    total_sales = round(
        sum(
            item["total_sales"]
            for item in ranking
        ),
        2,
    )


    total_quantity = sum(
        item["total_quantity"]
        for item in ranking
    )


    return {
        "success": True,

        "period": {
            "label": (
                f"{month_start.year}年"
                f"{month_start.month}月"
            ),
            "start_date": start_date,
            "end_date": end_date,
        },

        "summary": {
            "total_products": len(ranking),
            "total_sales": total_sales,
            "total_quantity": total_quantity,
            "top_product": ranking[0]["product_name"],
            "top_product_sales": ranking[0]["total_sales"],
        },

        "ranking": ranking,

        "message": "查询成功",
    }


# 7. 门店真实数据接口
@app.get("/api/stores")
def stores():
    return get_store_dashboard_data()


# 8. 前端全局筛选聚合接口
@app.get("/api/analytics")
def analytics(
    store_id: str | None = None,
    category: str | None = None,
    product_id: str | None = None,
    months: int = 1,
):
    return get_filtered_analytics_data(
        store_id=store_id,
        category=category,
        product_id=product_id,
        months=months,
    )

# 7. Agent 聊天接口
@app.post("/api/chat")
def chat(request: ChatRequest):
    result = run_langgraph_agent(
        question=request.question,
        conversation_history=request.conversation_history,
        structured_context=request.structured_context,
        structured_memory=request.structured_memory
    )

    return result