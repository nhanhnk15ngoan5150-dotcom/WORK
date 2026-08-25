import sqlite3
import json

from pathlib import Path

from services.llm_service import semantic_resolve_product


# 1. 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_FILE = BASE_DIR / "data" / "moneki.db"

ALIAS_FILE = BASE_DIR / "data" / "product_alias.json"


# 2. 加载商品列表
def get_products():
    conn = sqlite3.connect(
        DB_FILE
    )

    cursor = conn.cursor()

    result = cursor.execute(
        """
        SELECT product_name
        FROM products
        """
    ).fetchall()

    conn.close()

    return [
        item[0]
        for item in result
    ]


# 3. 加载商品别名
def get_product_alias():
    if not ALIAS_FILE.exists():
        return {}

    with open(
        ALIAS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        aliases = json.load(f)

    products = set(
        get_products()
    )

    # 过滤无效别名目标
    return {
        alias: standard
        for alias, standard in aliases.items()
        if standard in products
    }


# 4. 文本标准化
def normalize_text(
    text: str
):
    return (
        text
        .replace(" ", "")
        .replace("　", "")
        .lower()
    )


# 5. 获取模糊匹配候选
def _get_fuzzy_candidates(
    user_input: str,
    products: list
):
    input_text = normalize_text(
        user_input
    )

    candidates = []

    for product in products:
        product_text = normalize_text(
            product
        )

        if (
            input_text in product_text
            or product_text in input_text
        ):
            candidates.append(
                product
            )

    return candidates


# 6. 商品实体识别
def resolve_product_entity(
    user_input: str
):
    products = get_products()

    aliases = get_product_alias()

    input_text = normalize_text(
        user_input
    )

    # 精确匹配
    for product in products:
        if input_text == normalize_text(product):
            return {
                "input": user_input,
                "standard": product,
                "method": "exact",
                "confidence": 1.0,
                "need_clarification": False,
                "candidates": [],
            }

    # 别名匹配
    for alias, standard in aliases.items():
        if input_text == normalize_text(alias):
            return {
                "input": user_input,
                "standard": standard,
                "method": "alias",
                "confidence": 0.95,
                "need_clarification": False,
                "candidates": [],
            }

    # 模糊候选匹配
    fuzzy_candidates = _get_fuzzy_candidates(
        user_input,
        products
    )

    if len(fuzzy_candidates) == 1:
        return {
            "input": user_input,
            "standard": fuzzy_candidates[0],
            "method": "fuzzy",
            "confidence": 0.8,
            "need_clarification": False,
            "candidates": fuzzy_candidates,
        }

    # 多个模糊候选交给语义层判断
    semantic_products = (
        fuzzy_candidates
        if fuzzy_candidates
        else products
    )

    semantic_result = semantic_resolve_product(
        user_input,
        semantic_products
    )

    standard_product = semantic_result.get(
        "standard_product"
    )

    confidence = semantic_result.get(
        "confidence",
        0
    )

    need_clarification = semantic_result.get(
        "need_clarification",
        False
    )

    # 高置信度语义匹配
    if (
        standard_product
        and confidence >= 0.8
        and not need_clarification
    ):
        return {
            "input": user_input,
            "standard": standard_product,
            "method": "semantic",
            "confidence": confidence,
            "need_clarification": False,
            "candidates": fuzzy_candidates[:5],
        }

    # 存在歧义
    if need_clarification:
        return {
            "input": user_input,
            "standard": None,
            "method": "ambiguous",
            "confidence": confidence,
            "need_clarification": True,
            "candidates": fuzzy_candidates[:5],
        }

    # 无法识别
    return {
        "input": user_input,
        "standard": None,
        "method": "none",
        "confidence": confidence,
        "need_clarification": False,
        "candidates": [],
    }