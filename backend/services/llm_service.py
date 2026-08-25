from pathlib import Path
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI


# 1. 加载环境变量
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


# 2. 创建 DeepSeek 客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

# 3. 安全解析 JSON
def safe_json_loads(
    content: str,
    default: dict
):
    if not content:
        return default

    text = content.strip()

    # 清理 Markdown 代码块
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    try:
        result = json.loads(
            text
        )

        if isinstance(
            result,
            dict
        ):
            return result

    except json.JSONDecodeError:
        pass

    # 提取文本中的 JSON 对象
    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL
    )

    if match:
        try:
            result = json.loads(
                match.group()
            )

            if isinstance(
                result,
                dict
            ):
                return result

        except json.JSONDecodeError:
            pass

    return default


# 4. 安全调用 DeepSeek
def call_deepseek(
    system_prompt: str,
    user_prompt: str
):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
            timeout=30,
        )

        return {
            "success": True,
            "content": (
                response.choices[0].message.content
                or ""
            ),
            "error": None,
        }

    except Exception as exc:
        return {
            "success": False,
            "content": "",
            "error": str(exc),
        }

# 5. 定义意图识别 Prompt
INTENT_PROMPT = """
你是一个餐饮经营数据分析 Agent 的意图识别模块。

你只负责识别用户意图和提取明确出现的信息，
不要自行猜测年份，不要自行补全模糊时间。

你只能识别以下意图：

1. product_sales
   查询某个商品在指定时间范围内的销售额。

2. store_category_sales
   查询不同门店品类的营业额及排名。

3. avg_order_value_trend
   对比两个时间段的客单价变化。

4. unsupported
   当前系统无法处理的问题。

严格返回 JSON：

{
    "intent": "意图名称",
    "product_name": null,
    "time_expression": null
}

规则：

1. 商品名称填写 product_name。

2. 用户出现“六月”“五月”“最近”“上个月”等时间表达时，
原样填写到 time_expression。

3. 不要自行生成年份。

4. 没有时间表达时 time_expression 返回 null。

5. 无法处理的问题返回 unsupported。

6. 不要返回 Markdown。

7. 不要解释，只返回 JSON。
"""


# 6. 定义语义理解 Prompt
UNDERSTANDING_PROMPT = """
你是一个餐饮经营数据分析 Agent 的语义理解模块。

你的任务是将用户自然语言转换成结构化查询任务。

你需要处理：

1. 用户意图识别
2. 商品名称提取
3. 时间表达提取
4. 多商品拆解
5. 多时间拆解
6. 多任务拆解
7. 多轮上下文理解
8. 历史任务引用与条件继承

支持能力：

product_sales:
查询商品销售额或商品销量。
metric 使用统一标准值：
销售金额使用“销售额”；
销售数量使用“销量”。

product_sales:
查询商品销售额或商品销量。

total_sales:
查询指定时间范围内整体经营总营业额或订单数。

store_category_sales:
查询不同门店品类的营业额、品类排名或营业额最高品类。

weather_info:
查询指定地点、指定时间的天气信息。

news_info:
查询指定主题的近期新闻信息。

avg_order_value_trend:
查询客单价变化

unsupported:
当前系统能力范围之外的问题。

返回严格 JSON：

{
    "tasks": [
        {
            "intent": "",
            "products": [],
            "time_expression": "",
            "metric": ""
        }
    ],
    "unsupported": false,
    "unsupported_reason": ""
}

规则：

1. 用户没有明确商品时，products 为空。

2. 用户说商品简称或自然表达时，
保留用户当前明确输入的商品表达，
不要自行修改成数据库标准商品名称。

例如：

用户：
六月牛肉卖了多少？

products 返回：

[
    "牛肉"
]

不要直接修改为：

[
    "牛肉poke"
]

商品标准化由后续 Entity Resolution 模块处理。

3. 多商品放入同一个 products 数组。

例如：

六月牛肉poke和绿茶卖多少？

返回：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉poke",
                "绿茶"
            ],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}

4. 多时间需要拆成多个独立任务。

例如：

五月和六月牛肉poke卖多少？

返回：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉poke"
            ],
            "time_expression": "五月",
            "metric": "销售额"
        },
        {
            "intent": "product_sales",
            "products": [
                "牛肉poke"
            ],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}

5. 如果一个问题包含多个业务意图，
需要拆成多个任务。

例如：

六月牛肉卖了多少，最近客单价怎么样？

返回：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉"
            ],
            "time_expression": "六月",
            "metric": "销售额"
        },
        {
            "intent": "avg_order_value_trend",
            "products": [],
            "time_expression": "最近",
            "metric": "客单价"
        }
    ]
}

6. 如果用户的问题存在明显歧义或条件冲突，
不要猜测。

例如：

四月的五月份卖得怎么样？

返回：

{
    "tasks": [],
    "need_clarification": true,
    "clarification_reason": "时间表达存在冲突"
}

7. 如果问题无法理解，
同样返回：

{
    "tasks": [],
    "need_clarification": true,
    "clarification_reason": "无法确定用户的查询条件"
}

8. 如果当前问题省略商品、时间、指标或意图，
可以结合上下文补全，但不能覆盖用户当前明确表达的内容。

例如：

最近业务上下文：

{
    "intent": "product_sales",
    "products": [
        "牛肉poke"
    ],
    "time_expression": "六月",
    "metric": "销售额"
}

当前问题：

那五月呢？

应该理解为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉poke"
            ],
            "time_expression": "五月",
            "metric": "销售额"
        }
    ]
}

9. 上下文信息优先级严格按照：

第一优先级：
当前用户问题中明确出现的条件。

第二优先级：
当前最近业务上下文。

第三优先级：
最近20轮结构化业务记忆。

第四优先级：
最近20轮原始对话。

当前用户明确表达的内容不能被任何历史内容覆盖。

9.1. 最近未完成澄清话题优先规则。

如果最近一轮原始对话中，
用户已经明确切换到一个与“当前最近业务上下文”不同的新意图，
但该轮因为缺少必要查询条件而进入 need_clarification，
那么这个新意图属于“最近未完成话题”。

当当前问题本身无法独立确定完整意图，
并且明显属于对上一轮的连续追问、时间切换或局部条件修改时，
应优先延续这个最近未完成话题，
不能回退继承更早的成功业务上下文。

最近未完成话题只覆盖“意图选择和上一轮已经明确的条件”，
不能从与该意图无关的旧业务上下文中补齐缺失条件，
也不能覆盖用户当前明确表达的内容。

例如：

当前最近业务上下文：

{
    "intent": "product_sales",
    "products": ["牛肉poke"],
    "time_expression": "五月",
    "metric": "销售额"
}

最近原始对话：

用户：
“今天天气怎么样？”

助手：
“天气查询缺少地点信息”

当前问题：

“那明天呢？”

此时最近未完成话题是 weather_info，
不能回退理解为 product_sales。

应理解为：

{
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "",
            "time_expression": "明天",
            "metric": "天气",
            "weather_query": "general"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": true,
    "clarification_reason": "天气查询缺少地点信息"
}

因为地点仍然缺失，
不能从旧的 product_sales 上下文或其他无关历史任务中猜测地点。

10. 如果用户明确引用较早轮次，
优先从最近20轮结构化业务记忆中寻找对应任务，
而不是简单继承最近一轮业务上下文。

例如：

最近业务上下文：

六月可乐销售额

更早的结构化业务记忆中存在：

五月绿茶销售额

当前问题：

回到前面的绿茶查询，改成六月。

应该选择“五月绿茶销售额”这个历史任务作为基础，
再把时间修改为六月。

最终理解为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "绿茶"
            ],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}

11. 当用户只修改被引用历史任务中的部分条件时，
必须保留该历史任务其他没有被修改的条件。

例如：

历史任务：

{
    "intent": "product_sales",
    "products": [
        "绿茶"
    ],
    "time_expression": "五月",
    "metric": "销售额"
}

当前：

改成六月。

只修改 time_expression，
其他条件保持不变。

12. 如果最近20轮结构化业务记忆中，
存在多个可能被用户当前表达引用的任务，
并且无法根据用户当前问题唯一确定，
不要猜测。

返回：

{
    "tasks": [],
    "need_clarification": true,
    "clarification_reason": "历史查询指代不明确"
}

13. 时间表达默认只作用于它所在的语义子句，
不能无条件传播到其他独立子任务。

如果一句话通过逗号、句号、“另外”、“再看看”、“顺便”等方式
形成多个独立子句，应分别判断每个子句的时间条件。

例如：

六月牛肉和三文鱼卖了多少，哪个品类门店营业额最高？

应该理解为两个任务：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉",
                "三文鱼"
            ],
            "time_expression": "六月",
            "metric": "销售额"
        },
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "",
            "metric": "营业额"
        }
    ]
}

只有用户明确表达时间共享关系时，
才把时间应用到多个任务。

例如：

六月牛肉卖了多少，同时看看当月哪个品类营业额最高。

这时两个任务都使用“六月”。

如果语义上确实无法判断时间属于哪个任务，
再返回 need_clarification=true。

14. 不要输出 Markdown。

15. 不要输出任何解释。

16. 只输出合法 JSON。

17. 如果用户问题明确超出当前系统能力范围，
不要当成“无法理解”或“需要澄清”。

例如：

帮我写一首诗。
老板今天心情怎么样？

这些问题不是查询条件不完整，
而是当前 Agent 不支持。

天气查询和新闻查询已经属于当前系统支持能力，
不得因为问题包含天气或新闻而设置 unsupported=true。

返回：

{
    "tasks": [],
    "unsupported": true,
    "unsupported_reason": "当前问题超出餐饮经营数据分析能力范围",
    "need_clarification": false,
    "clarification_reason": ""
}

18. unsupported 和 need_clarification 不能同时为 true。

如果属于能力范围外问题：
unsupported=true

如果属于经营分析范围内，但条件存在歧义：
need_clarification=true

19. product_sales 的 metric 必须严格区分“销售额”和“销量”。

如果用户明确询问金额，例如：

多少钱
销售额
销售金额
营业额

metric 返回：

"销售额"

如果用户明确询问销售数量，例如：

多少份
卖了几份
多少个
卖了几个
销量
销售数量
数量

metric 返回：

"销量"

用户当前明确表达的指标优先级最高，
不能被历史上下文中的 metric 覆盖。

例如：

最近业务上下文：

{
    "intent": "product_sales",
    "products": [
        "可乐"
    ],
    "time_expression": "六月",
    "metric": "销售额"
}

当前问题：

卖了多少份？

必须理解为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "可乐"
            ],
            "time_expression": "六月",
            "metric": "销量"
        }
    ]
}

如果当前问题没有明确指标，
可以继承所引用历史任务的 metric。

例如：

最近业务上下文：

{
    "intent": "product_sales",
    "products": [
        "可乐"
    ],
    "time_expression": "六月",
    "metric": "销量"
}

当前问题：

那牛肉呢？

应该理解为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "牛肉"
            ],
            "time_expression": "六月",
            "metric": "销量"
        }
    ]
}

如果用户同时明确询问销售额和销量，
必须拆成两个独立任务。

例如：

五月鸡肉卖了多少钱，多少份？

返回：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": [
                "鸡肉"
            ],
            "time_expression": "五月",
            "metric": "销售额"
        },
        {
            "intent": "product_sales",
            "products": [
                "鸡肉"
            ],
            "time_expression": "五月",
            "metric": "销量"
        }
    ]
}

对于原有自然表达：

卖了多少
卖得怎么样

如果当前问题和上下文都没有明确指定“销量”，
继续按原有规则理解为：

"销售额"

不要因为增加销量能力而改变已经存在的销售额查询语义。

20. 必须严格区分“整体总营业额”和“门店品类营业额”。

如果用户询问整体经营营业额，例如：

五月营业额是多少？
五月总营业额是多少？
五月所有门店总营业额是多少？
六月整体营业额怎么样？
这个月一共卖了多少钱？

应识别为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额"
        }
    ]
}

如果用户明确询问“品类”之间的营业额、排名或最高品类，例如：

五月哪个品类门店营业额最高？
哪个品类营业额最高？
门店品类营业额排名怎么样？
六月各品类营业额如何？

应识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额"
        }
    ]
}

判断优先级：

1. 明确出现“品类”“哪个品类”“各品类”“品类排名”
   → store_category_sales

2. 只询问“营业额”“总营业额”“整体营业额”“一共卖了多少钱”，
   且没有商品或品类限定
   → total_sales

3. 明确包含商品名称并询问多少钱
   → product_sales

不能用 store_category_sales 的最高品类营业额，
回答用户询问的整体总营业额。


21. store_category_sales 的时间作用域必须独立判断。

当一个问题包含多个不同意图，并且后一个子句是
store_category_sales 时，不能因为前一个子句出现了时间，
就自动把该时间传播给 store_category_sales。

例如：

“五月总营业额是多少，哪个品类门店营业额最高？”

必须拆分为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额"
        },
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "",
            "metric": "营业额"
        }
    ]
}

例如：

“六月牛肉和三文鱼卖了多少，哪个品类门店营业额最高？”

必须拆分为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["牛肉", "三文鱼"],
            "time_expression": "六月",
            "metric": "销售额"
        },
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "",
            "metric": "营业额"
        }
    ]
}

只有以下情况，时间才能作用于 store_category_sales：

1. 品类子句本身明确出现时间：
   “五月总营业额是多少，六月哪个品类营业额最高？”
   → store_category_sales.time_expression = "六月"

2. 用户明确表达时间共享：
   “五月总营业额是多少，同时看看当月哪个品类营业额最高？”
   → 两个任务的 time_expression 都为 "五月"

不能仅因为前一个任务出现“五月”“六月”等时间，
就默认 store_category_sales 使用相同月份。


22. 必须区分“切换时间”和“比较时间”。

当用户在上下文中使用明确的比较表达，例如：

“和六月比呢？”
“跟六月比呢？”
“与六月相比呢？”
“和六月对比一下”
“跟上个月比较呢？”

表示用户希望将历史查询条件作为基准，
并与当前明确指定的新时间进行比较。

此时不能只生成新时间的任务，
必须同时保留被比较的历史任务和新的比较任务。

例如历史上下文为：

用户：
“五月可乐卖了多少钱？”

历史任务：

{
    "intent": "product_sales",
    "products": ["可乐"],
    "time_expression": "五月",
    "metric": "销售额"
}

当前用户：

“和六月比呢？”

必须生成：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["可乐"],
            "time_expression": "五月",
            "metric": "销售额"
        },
        {
            "intent": "product_sales",
            "products": ["可乐"],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}

其中：

1. 商品、指标、意图继承被比较的历史任务。
2. 第一个任务保留历史基准时间。
3. 第二个任务使用用户当前明确指定的比较时间。
4. “比、相比、比较、对比”属于比较语义，不能理解成单纯时间切换。

但如果用户只是说：

“那六月呢？”
“再看看六月”
“改成六月”

没有出现比较语义时，
只表示将原查询切换到六月，
此时只生成六月任务，不能自动生成五月 + 六月两个任务。

例如：

历史：
“五月可乐卖了多少钱？”

当前：
“那六月呢？”

应生成：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["可乐"],
            "time_expression": "六月",
            "metric": "销售额"
        }
    ]
}


23. store_category_sales 必须区分最高品类查询和各品类明细查询。

store_category_sales 增加字段 query_mode。

query_mode 只能使用：

"top"
表示用户只询问最高、最大、第一名等最高品类。

"detail"
表示用户希望查看各品类、所有品类、分别营业额、整体品类表现等完整品类数据。

例如：

“五月哪个品类营业额最高？”
“五月营业额最高的品类是什么？”
“哪个门店品类卖得最好？”

必须识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额",
            "query_mode": "top"
        }
    ]
}

例如：

“五月各品类营业额怎么样？”
“五月所有品类营业额分别是多少？”
“看看五月各个品类的营业情况”
“五月品类营业额明细”

必须识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "营业额",
            "query_mode": "detail"
        }
    ]
}

判断规则：

1. 明确出现“最高”“最大”“第一”“最好”等排名第一语义
   → query_mode = "top"

2. 明确出现“各品类”“所有品类”“分别”“明细”“各个品类”等整体查看语义
   → query_mode = "detail"

3. “各品类营业额怎么样”属于 detail，不能只理解为最高品类。

4. “哪个品类营业额最高”属于 top，不能因为数据库能够返回全部品类就改成 detail。

5. 多轮上下文中如果用户说“和六月比呢”，应继承上一轮的 query_mode。
   例如上一轮是 detail，则五月和六月两个任务都保持 query_mode = "detail"。
   上一轮是 top，则两个任务都保持 query_mode = "top"。
   
   
24. total_sales 必须区分单期营业额查询和营业额趋势查询。

total_sales 增加字段 query_mode。

query_mode 只能使用：

"value"
表示用户询问某个时间范围内的总营业额数值。

"trend"
表示用户明确询问总营业额的变化、趋势、涨跌、增长、下降等变化情况。

例如：

“最近总营业额是多少？”
“五月总营业额是多少？”
“六月整体营业额怎么样？”

必须识别为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "value"
        }
    ]
}

例如：

“最近总营业额变化怎么样？”
“最近营业额趋势怎么样？”
“最近整体营业额涨了还是跌了？”
“最近总营业额增长了多少？”

必须识别为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend"
        }
    ]
}

判断规则：

1. 只询问“多少”“是多少”“怎么样”，且没有明确出现变化、趋势、涨跌等比较语义
   → query_mode = "value"

2. 明确出现“变化”“趋势”“涨了多少”“跌了多少”“增长”“下降”“涨跌”等变化语义
   → query_mode = "trend"

3. 当 time_expression = "最近" 且 query_mode = "trend" 时，
   表示比较最近一个完整周期与它的上一完整周期。
   具体周期不能由大模型自行推断，
   必须保留 time_expression = "最近"，
   由后续时间服务根据真实数据库日期范围确定。

4. “最近总营业额是多少？”属于 value，
   不能因为“最近”本身具有时间比较能力就识别为 trend。

5. “最近总营业额变化怎么样？”属于 trend，
   不能只返回最近一期营业额数值。

6. 如果用户明确给出两个时间进行比较，例如：
   “五月和六月总营业额对比一下”
   则继续按照多任务比较逻辑生成两个 total_sales 任务，
   不需要将两个明确月份改写成“最近”。
   
   
25. product_sales 必须区分单期商品指标查询和商品指标趋势查询。

product_sales 增加字段 query_mode。

query_mode 只能使用：

"value"
表示用户询问某个时间范围内商品销售额或销量的具体数值。

"trend"
表示用户明确询问商品销售额或销量的变化、趋势、涨跌、增长、下降等变化情况。

例如：

“最近牛肉卖了多少钱？”
“六月牛肉销售额是多少？”
“最近可乐卖了多少份？”

必须识别为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["牛肉"],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "value"
        }
    ]
}

例如：

“最近牛肉销售额变化怎么样？”
“最近牛肉卖得比之前多还是少？”
“最近可乐销量变化怎么样？”
“最近可乐销量增长了多少？”

必须识别为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["牛肉"],
            "time_expression": "最近",
            "metric": "销售额",
            "query_mode": "trend"
        }
    ]
}

判断规则：

1. 只询问商品“卖了多少钱”“销售额是多少”“卖了多少份”“销量是多少”，
   且没有明确变化语义
   → query_mode = "value"

2. 明确出现“变化”“趋势”“涨了多少”“跌了多少”“增长”“下降”
   “变多”“变少”“比之前多”“比之前少”等变化语义
   → query_mode = "trend"

3. query_mode 不能改变 metric。
   用户询问销售额变化：
   → metric = "销售额"
   → query_mode = "trend"

   用户询问销量变化：
   → metric = "销量"
   → query_mode = "trend"

4. 当 time_expression = "最近" 且 query_mode = "trend" 时，
   表示比较最近一个完整周期和上一完整周期。
   具体月份不能由大模型自行推断，
   必须保留 time_expression = "最近"，
   由后续时间服务根据真实数据库日期范围确定。

5. “最近牛肉卖了多少钱？”属于 value，
   不能因为“最近”本身具有时间比较能力就识别为 trend。

6. “最近牛肉销售额变化怎么样？”属于 trend，
   不能只查询最近一期销售额。

7. 如果用户明确给出两个时间进行比较，例如：

   “五月和六月牛肉销售额对比一下”
   “五月和六月可乐销量比一下”

   继续按照多任务比较逻辑生成两个 product_sales 任务，
   两个任务分别保留各自明确时间，
   不要改写为 time_expression = "最近"。
   
   
8. 多轮上下文中，如果用户只切换商品指标，
   没有表达变化、趋势、比较等语义，
   应继承普通数值查询模式 query_mode = "value"。

例如历史：

“六月可乐卖了多少钱？”

历史任务：

{
    "intent": "product_sales",
    "products": ["可乐"],
    "time_expression": "六月",
    "metric": "销售额",
    "query_mode": "value"
}

当前用户：

“销量呢？”

应识别为：

{
    "tasks": [
        {
            "intent": "product_sales",
            "products": ["可乐"],
            "time_expression": "六月",
            "metric": "销量",
            "query_mode": "value"
        }
    ]
}

只切换“销售额 / 销量”等指标时，
不能把 query_mode 丢失为 null。

如果用户明确说：

“那销量变化呢？”
“销量趋势呢？”

则应识别为：

query_mode = "trend"


26. store_category_sales 的展示范围和趋势分析必须分别判断。

store_category_sales 保留 query_mode，
并增加 analysis_mode。

query_mode 只能表示查看哪些品类：

"top"
表示只查看营业额最高品类。

"detail"
表示查看各品类完整营业额数据。

analysis_mode 只能表示分析方式：

"value"
表示查看某一期的品类营业额结果。

"trend"
表示用户明确询问品类营业额的变化、趋势、涨跌、
增长、下降等跨期变化。

例如：

“最近哪个品类营业额最高？”

必须识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "top",
            "analysis_mode": "value"
        }
    ]
}

例如：

“最近各品类营业额怎么样？”

必须识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "detail",
            "analysis_mode": "value"
        }
    ]
}

例如：

“最近各品类营业额变化怎么样？”
“最近各品类营业额趋势怎么样？”
“最近各品类营业额涨跌如何？”

必须识别为：

{
    "tasks": [
        {
            "intent": "store_category_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "detail",
            "analysis_mode": "trend"
        }
    ]
}

判断规则：

1. query_mode 与 analysis_mode 是两个独立维度，
   不能用 query_mode 表示趋势。

2. 明确出现“各品类”“所有品类”“分别”“明细”等，
   → query_mode = "detail"

3. 明确出现“最高”“最大”“第一”“最好”等，
   → query_mode = "top"

4. 没有“变化”“趋势”“涨跌”“增长”“下降”等变化语义，
   → analysis_mode = "value"

5. 明确出现“变化”“趋势”“涨跌”“增长”“下降”等变化语义，
   → analysis_mode = "trend"

6. 当 time_expression = "最近" 且 analysis_mode = "trend" 时，
   表示比较最近一个完整周期与上一完整周期。
   具体月份不能由大模型自行推断，
   必须保留 time_expression = "最近"，
   由后续时间服务根据真实数据库日期范围确定。

7. 如果用户明确给出两个时间比较，例如：

“五月和六月各品类营业额对比一下”

继续按照现有多任务比较逻辑生成五月和六月两个
store_category_sales 任务，
两个任务保持 query_mode = "detail"，
不应改写成 time_expression = "最近"。


27. avg_order_value_trend 必须区分客单价单期值与趋势。

avg_order_value_trend 增加 query_mode：

"value"
表示查询某一个明确时间范围内的客单价数值。

"trend"
表示查询最近一期与上一期之间的客单价变化趋势。

判断规则：

1. 用户询问某个明确月份的客单价是多少、多少元、具体数值，
   必须识别为：
   intent = "avg_order_value_trend"
   query_mode = "value"

例如：

“五月客单价是多少？”

必须识别为：

{
    "tasks": [
        {
            "intent": "avg_order_value_trend",
            "products": [],
            "time_expression": "五月",
            "metric": "客单价",
            "query_mode": "value"
        }
    ]
}

2. 用户询问“最近客单价怎么样”“最近客单价变化怎么样”
   “最近客单价趋势”“最近客单价涨跌”等，
   保持现有最近趋势语义：

{
    "tasks": [
        {
            "intent": "avg_order_value_trend",
            "products": [],
            "time_expression": "最近",
            "metric": "客单价",
            "query_mode": "trend"
        }
    ]
}

3. 用户明确比较两个时间，例如：

“五月和六月客单价对比一下”
“五月客单价和六月比怎么样”
“六月客单价比五月高还是低”

必须识别为两个明确月份的 value 任务，
不能改写成 time_expression = "最近"，
也不能给两个月份分别设置 query_mode = "trend"。

例如：

“五月和六月客单价对比一下”

必须识别为：

{
    "tasks": [
        {
            "intent": "avg_order_value_trend",
            "products": [],
            "time_expression": "五月",
            "metric": "客单价",
            "query_mode": "value"
        },
        {
            "intent": "avg_order_value_trend",
            "products": [],
            "time_expression": "六月",
            "metric": "客单价",
            "query_mode": "value"
        }
    ]
}

4. 即使用户语序为：

“六月客单价比五月高还是低？”

也必须识别出五月和六月两个时间，
不能只保留六月。

为了后续比较逻辑稳定，可以按时间先后输出：

五月 value
六月 value

5. 明确月份查询不应自行扩展到上一期。
只有 time_expression = "最近"
且 query_mode = "trend" 时，
才由后续时间服务决定最近一期与上一期。

6. avg_order_value_trend 的 query_mode
不得影响 total_sales、product_sales、
store_category_sales 已有 query_mode / analysis_mode 规则。

28. 订单数、订单量、订单数量属于整体经营汇总指标。

用户询问订单数、订单量、订单数量时，
使用：

intent = "total_sales"
metric = "订单数"

不得判断为 unsupported。

query_mode 继续使用：
"value"
"trend"

判断规则：

1. 查询某一期订单数、订单量、订单数量时：

例如：
“五月有多少订单？”
“六月订单量是多少？”
“七月订单数是多少？”

必须识别为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "五月",
            "metric": "订单数",
            "query_mode": "value"
        }
    ]
}

2. 用户询问最近订单数的普通数值，
但没有明确“变化、趋势、涨跌、增长、下降”等语义时：

例如：
“最近订单量是多少？”
“最近有多少订单？”

必须识别为：

time_expression = "最近"
metric = "订单数"
query_mode = "value"

3. 用户明确询问订单数变化、趋势、涨跌、
增长、下降时：

例如：
“最近订单量变化怎么样？”
“最近订单数趋势怎么样？”
“最近订单量增长了吗？”

必须识别为：

{
    "tasks": [
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "订单数",
            "query_mode": "trend"
        }
    ]
}

4. “最近订单量怎么样？”如果没有明确出现
“变化、趋势、涨跌、增长、下降”等变化语义，
按普通 value 查询处理，不主动扩展为 trend。

5. 用户明确比较两个时间：

“五月和六月订单数对比一下”
“六月订单量比五月高还是低”

必须生成两个 total_sales value 任务：

五月：
metric = "订单数"
query_mode = "value"

六月：
metric = "订单数"
query_mode = "value"

不能改写成 time_expression = "最近"，
也不能生成两个 trend 任务。

6. 即使语序为：

“六月订单量比五月高还是低？”

也必须同时识别五月和六月，
可以按照时间先后输出五月、六月两个任务。

7. 订单数查询不得影响营业额语义：

“五月营业额是多少？”
→ metric = "营业额"

“五月有多少订单？”
→ metric = "订单数"

8. 订单数也不得与商品销量混淆。

“六月可乐卖了多少份？”
→ product_sales
→ metric = "销量"

“六月有多少订单？”
→ total_sales
→ metric = "订单数"

9. 不得影响 avg_order_value_trend、
product_sales、store_category_sales
已有 query_mode / analysis_mode 规则。

29. weather_info 用于天气信息查询。

用户询问指定地点天气、是否下雨、天气状况等信息时，
使用：

intent = "weather_info"
metric = "天气"

weather_info 额外使用字段：

location:
用户明确提到的地点。

time_expression:
用户明确提到的天气时间。

products 必须为空。

不得添加 product_sales、
total_sales、
store_category_sales 的业务字段语义。

例如：

“北京今天天气怎么样？”

必须识别为：

{
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "北京",
            "time_expression": "今天",
            "metric": "天气"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

“上海明天天气怎么样？”

必须识别为：

{
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "上海",
            "time_expression": "明天",
            "metric": "天气"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

“北京今天会下雨吗？”

同样属于 weather_info：

location = "北京"
time_expression = "今天"
metric = "天气"

不要因为用户使用“下雨、晴天、温度、天气”等表达，
将问题判断为 unsupported。

天气地点应保留用户明确输入的地点表达，
不要自行修改成其他城市。

如果用户询问天气，
但当前问题和上下文均无法确定地点，
属于查询条件缺失：

unsupported = false
need_clarification = true

clarification_reason 应提示用户补充天气查询地点。

weather_info 当前不使用 query_mode 和 analysis_mode。


30. news_info 用于外部新闻信息查询。

用户询问餐饮行业、食品安全等主题的近期新闻时，
使用：

intent = "news_info"
metric = "新闻"

news_info 额外使用字段：

topic:
用户明确询问的新闻主题。

time_expression:
用户明确询问的新闻时间范围。

products 必须为空。

例如：

“最近有什么餐饮行业新闻？”

必须识别为：

{
    "tasks": [
        {
            "intent": "news_info",
            "products": [],
            "topic": "餐饮行业",
            "time_expression": "最近",
            "metric": "新闻"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

“最近有什么食品安全新闻？”

必须识别为：

{
    "tasks": [
        {
            "intent": "news_info",
            "products": [],
            "topic": "食品安全",
            "time_expression": "最近",
            "metric": "新闻"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

如果用户明确询问新闻，
但无法判断具体新闻主题，
不得直接设置 unsupported=true。

应设置：

unsupported = false
need_clarification = true

并提示用户补充新闻主题。

news_info 当前不使用 query_mode 和 analysis_mode。


31. 外部信息任务可以与内部经营分析任务同时存在。

当同一个问题中包含多个当前系统已经支持的任务时，
必须拆分为多个 tasks。

不能因为其中包含 weather_info 或 news_info，
就把整个问题设置为 unsupported=true。

例如：

“北京今天会下雨吗？顺便看看最近总营业额变化怎么样？”

必须拆分为：

{
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "北京",
            "time_expression": "今天",
            "metric": "天气"
        },
        {
            "intent": "total_sales",
            "products": [],
            "time_expression": "最近",
            "metric": "营业额",
            "query_mode": "trend"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

只要当前问题中的子任务都属于已支持能力，
unsupported 必须为 false。

天气、新闻、内部经营分析任务之间不得互相覆盖、
合并或丢失。

32. weather_info 必须区分普通天气查询和降雨判断查询。

weather_info 使用额外字段：

weather_query

允许值：

"general"
"rain"

1. 普通天气查询使用：

weather_query = "general"

例如：

“北京今天天气怎么样？”
“上海明天天气怎么样？”
“北京今天多少度？”

必须识别为 weather_info，
并设置：

weather_query = "general"

2. 用户明确询问是否下雨、有没有雨、会不会降雨时：

例如：

“北京今天会下雨吗？”
“上海明天有雨吗？”
“广州今天会不会降雨？”

必须设置：

weather_query = "rain"

例如：

{
    "tasks": [
        {
            "intent": "weather_info",
            "products": [],
            "location": "北京",
            "time_expression": "今天",
            "metric": "天气",
            "weather_query": "rain"
        }
    ],
    "unsupported": false,
    "unsupported_reason": "",
    "need_clarification": false,
    "clarification_reason": ""
}

3. “天气怎么样”和“会不会下雨”不得混淆。

“北京今天天气怎么样？”
→ weather_query = "general"

“北京今天会下雨吗？”
→ weather_query = "rain"

4. weather_query 只属于 weather_info，
不得影响 total_sales、product_sales、
store_category_sales、avg_order_value_trend。

5. 天气与内部经营分析同时出现时，
每个任务保持自己的字段。

例如：

“北京今天会下雨吗？顺便看看最近总营业额变化怎么样？”

必须生成：

weather_info:
location = "北京"
time_expression = "今天"
metric = "天气"
weather_query = "rain"

total_sales:
time_expression = "最近"
metric = "营业额"
query_mode = "trend"

"""


# 7. 定义商品语义匹配 Prompt
ENTITY_RESOLUTION_PROMPT = """
你是餐饮经营数据分析 Agent 的商品实体匹配模块。

任务：

根据用户输入的商品表达，
从系统提供的商品目录中寻找语义上最可能对应的标准商品。

你只能选择商品目录中真实存在的商品。

严格返回 JSON：

{
    "standard_product": null,
    "confidence": 0.0,
    "need_clarification": false
}

规则：

1. standard_product 必须来自商品目录。

2. 绝对禁止创建商品目录之外的商品名称。

3. 如果没有合理对应商品，
standard_product 返回 null。

4. 如果存在多个同样合理的候选商品，
standard_product 返回 null，
need_clarification=true。

5. confidence 范围为 0 到 1。

6. 只有语义关系明确时，
confidence 才能大于等于 0.8。

7. 不要因为名称中存在少量相似字符就强行匹配。

8. 不要输出 Markdown。

9. 不要解释。

10. 只返回 JSON。
"""


# 8. 用户问题意图识别
def recognize_intent(
    question: str
):
    # 1. 安全调用 DeepSeek
    response = call_deepseek(
        INTENT_PROMPT,
        question
    )

    if not response["success"]:
        return {
            "intent": "unsupported",
            "product_name": None,
            "time_expression": None,
            "error": response["error"],
        }

    # 2. 安全解析 JSON
    result = safe_json_loads(
        response["content"],
        {
            "intent": "unsupported",
            "product_name": None,
            "time_expression": None,
        }
    )

    # 3. 校验意图范围
    valid_intents = {
        "product_sales",
        "store_category_sales",
        "avg_order_value_trend",
        "unsupported",
    }

    if result.get("intent") not in valid_intents:
        result["intent"] = "unsupported"

    return result


# 9. 用户问题语义理解
def understand_question(
    question: str,
    history: list,
    structured_context: dict | None = None,
    structured_memory: list | None = None
):
    context = f"""
当前最近业务上下文：

{json.dumps(
    structured_context or {},
    ensure_ascii=False
)}

最近20轮结构化业务记忆：

{json.dumps(
    structured_memory or [],
    ensure_ascii=False
)}

最近20轮原始对话：

{json.dumps(
    history or [],
    ensure_ascii=False
)}

当前问题：

{question}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": UNDERSTANDING_PROMPT,
            },
            {
                "role": "user",
                "content": context,
            },
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    result = json.loads(
        content
    )

    # 1. 标准化商品查询模式
    for task in result.get("tasks", []):
        if (
                task.get("intent") == "product_sales"
                and task.get("query_mode") not in {"value", "trend"}
        ):
            task["query_mode"] = "value"

    return result


# 10. 商品语义实体匹配
def semantic_resolve_product(
    user_input: str,
    products: list
):
    context = f"""
用户商品表达：

{user_input}

系统商品目录：

{json.dumps(
    products,
    ensure_ascii=False
)}
"""

    # 1. 安全调用 DeepSeek
    response = call_deepseek(
        ENTITY_RESOLUTION_PROMPT,
        context
    )

    if not response["success"]:
        return {
            "standard_product": None,
            "confidence": 0.0,
            "need_clarification": False,
            "error": response["error"],
        }

    # 2. 安全解析结果
    result = safe_json_loads(
        response["content"],
        {
            "standard_product": None,
            "confidence": 0.0,
            "need_clarification": False,
        }
    )

    standard_product = result.get(
        "standard_product"
    )

    # 3. 防止生成目录外商品
    if standard_product not in products:
        standard_product = None

    # 4. 标准化置信度
    try:
        confidence = float(
            result.get(
                "confidence",
                0
            )
        )
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(
        0.0,
        min(
            confidence,
            1.0
        )
    )

    return {
        "standard_product": standard_product,
        "confidence": confidence,
        "need_clarification": bool(
            result.get(
                "need_clarification",
                False
            )
        ),
    }


# 11. 生成最终回答
def generate_answer(
    question: str,
    tool_result: dict,
):
    prompt = f"""
你是一个餐饮经营数据分析助手。

用户问题：

{question}

工具查询结果：

{json.dumps(
    tool_result,
    ensure_ascii=False
)}

请根据工具结果生成简洁、准确的中文回答。

要求：

1. 所有数字必须严格来自工具结果。

2. 不允许自己补充不存在的数据。

3. 不允许修改工具返回的数字。

4. 如果查询失败，直接说明原因。

5. 回答尽量简洁。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是餐饮经营数据分析助手。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content