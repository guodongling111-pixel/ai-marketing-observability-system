import pandas as pd
import os  # 放在最前面
import json



from crewai import Task, Crew
from agents.sentiment_agent import sentiment_agent
from agents.marketing_agent import marketing_agent
from agents.trend_agent import trend_agent
from agents.manager_agent import manager_agent

# 自动创建 outputs 文件夹
os.makedirs("outputs", exist_ok=True)

# 读取评论数据
df = pd.read_csv("data/genshin_comments.csv")
comments = "\n".join(df["comment"].tolist())


# 定义任务
sentiment_task = Task(
    description="""
你是一名专业的《原神》社区舆情分析师。

请分析以下玩家评论：

""" + comments + """

请完成：

1. 玩家整体情绪
2. 高频抱怨
3. 高频赞美
4. 当前舆情风险
5. 玩家最关注角色

【情绪分类规则】

1. positive_topics 只能包含：
- 喜欢
- 满意
- 赞美
- 震撼
- 优秀
- 期待
- 认可

2. negative_topics 只能包含：
- 不满
- 抱怨
- 生气
- 坐牢
- 氪金压力
- 无聊
- 削弱
- 失望

3. 不允许：
- 正向情绪放入 negative_topics
- 负向情绪放入 positive_topics

4. 示例：

评论：
"丝柯克建模太强了"

应归类为：
positive_topics

评论：
"剧情节奏太拖了"

应归类为：
negative_topics

【重要要求】

1. 只能输出合法 JSON
2. 不要输出 markdown
3. 不要输出 ```json
4. 不要输出解释
5. 所有 key 必须使用双引号
6. 输出必须可被 json.loads() 解析

输出格式如下：

{
  "overall_sentiment": "",
  "negative_topics": [
    {
      "topic": "",
      "emotion": ""
    }
  ],
  "positive_topics": [
    {
      "topic": "",
      "emotion": ""
    }
  ],
  "risk_alerts": [
    {
      "risk": "",
      "suggestion": ""
    }
  ],
  "hot_characters": [
    {
      "character": "",
      "attention_level": ""
    }
  ]
}
""",
    expected_output="JSON analysis of player sentiment.",
    agent=sentiment_agent
)

trend_task = Task(
    description=f"""
你将收到《原神》玩家评论 + 情绪分析结果。

【玩家评论】

{comments}

请分析：

1. 当前最热话题
2. 正在上升的讨论点
3. 正在下降的讨论点
4. 热门角色变化
5. 可用于营销的潜在热点

【分析要求】

1. 基于玩家评论 + 情绪分析结果进行趋势判断
2. rising_topics 必须是热度正在增加的话题
3. declining_topics 必须是热度正在下降的话题
4. marketing_opportunities 必须具有实际营销价值

【严格格式要求】

1. 禁止输出 ```json
2. 禁止输出 markdown code block
3. 只能输出纯 JSON
4. 输出第一字符必须是 {{
5. 输出最后字符必须是 }}
6. 不允许输出解释
7. 所有 key 必须使用双引号

输出 JSON：

{{
  "hot_topics": [],
  "rising_topics": [],
  "declining_topics": [],
  "hot_characters": [],
  "insights": "",
  "marketing_opportunities": []
}}
""",

    expected_output="Trend analysis JSON.",

    agent=trend_agent,

    context=[sentiment_task]
)

marketing_task = Task(
    description=f"""
你将收到《原神》玩家社区趋势分析报告。

请基于该报告：

1. 生成3个小红书爆款标题
2. 生成1段抖音短视频文案
3. 生成3个B站视频标题
4. 提供3个适合当前社区热点的营销方向

【趋势分析报告】

{trend_task}

【生成要求】

1. 小红书标题必须具有爆款感
2. 抖音文案必须适合短视频传播
3. B站标题必须具有二次元社区风格
4. marketing_angles 必须具有真实运营价值

【严格格式要求】

1. 禁止输出 ```json
2. 禁止输出 markdown code block
3. 只能输出纯 JSON
4. 输出第一字符必须是 {{
5. 输出最后字符必须是 }}
6. 不允许输出解释
7. 所有 key 必须使用双引号
8. 所有字符串必须使用英文双引号
9. 不允许使用中文引号
10. 每个 JSON 字段后必须有英文逗号（最后一个除外）
11. 输出前必须检查 JSON 是否合法
12. 输出必须可被 json.loads() 解析

输出格式：

{{
  "xiaohongshu_titles": [],
  "douyin_copywriting": "",
  "bilibili_titles": [],
  "marketing_angles": []
}}
""",

    expected_output="Marketing copywriting JSON.",

    agent=marketing_agent,

    context=[trend_task]
)

manager_task = Task(
    description="""
你将收到三个 Agent 的输出：

1. sentiment_agent 输出
2. trend_agent 输出
3. marketing_agent 输出

请作为「AI社区舆情审计员」，完成以下任务：

---

# 🧪 一、重点检查（核心规则）

请重点检查以下问题：

## 1. sentiment vs trend 是否一致
- sentiment 中的负面话题，trend 是否识别为 declining_topics
- sentiment 中的正面话题，trend 是否出现在 hot_topics

## 2. trend 逻辑合理性
- rising_topics 是否真的来自“正向或热度增强内容”
- declining_topics 是否对应“负面或热度下降内容”
- 是否存在明显遗漏高频话题

## 3. marketing 合理性
- marketing_angles 是否基于 trend 输出
- 是否出现与用户情绪无关的营销建议

## 4. JSON 结构检查
- 是否存在空字段
- 是否有 markdown
- 是否 JSON 不合法
- 是否字段缺失

---

# ⚠️ 二、异常判定规则

如果出现以下情况标记 risk：

- sentiment 与 trend 明显冲突
- marketing 完全不依赖 trend
- 输出出现空数组过多
- 情绪分类明显错误

---

# 📊 三、输出要求

必须输出 JSON：

{
  "agent_reviews": {
    "sentiment_agent": "",
    "trend_agent": "",
    "marketing_agent": ""
  },
  "issues_found": [],
  "consistency_check": "",
  "overall_risk": "",
  "final_summary": ""
}

---

【强制要求】
1. 只能输出 JSON
2. 禁止 markdown
3. 禁止 ```json
4. 所有 key 使用双引号
""",
    agent=manager_agent,
    context=[sentiment_task, trend_task, marketing_task],
    expected_output="Manager audit JSON"
)

# 创建 Crew
crew = Crew(
    agents=[
    sentiment_agent,
    trend_agent,
    marketing_agent,
    manager_agent
    ],
    tasks=[
    sentiment_task,
    trend_task,
    marketing_task,
    manager_task
    ],
    verbose=True
)

# 启动工作流
result = crew.kickoff()

print("\n===== FINAL RESULT =====\n")
print(result)

# 保存 sentiment report
with open(
    "outputs/reports/sentiment_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        json.loads(sentiment_task.output.raw),
        f,
        ensure_ascii=False,
        indent=2
    )

# 保存 trend report
with open(
    "outputs/reports/trend_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        json.loads(trend_task.output.raw),
        f,
        ensure_ascii=False,
        indent=2
    )

# 保存 marketing report
with open(
    "outputs/reports/marketing_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        json.loads(marketing_task.output.raw),
        f,
        ensure_ascii=False,
        indent=2
    )

# 保存 manager report
with open(
    "outputs/reports/manager_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        json.loads(manager_task.output.raw),
        f,
        ensure_ascii=False,
        indent=2
    )

# 保存 final report
with open(
    "outputs/reports/final_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        json.loads(str(result)),
        f,
        ensure_ascii=False,
        indent=2
    )

# 转字符串
raw_result = str(result)

# 自动补全 JSON
if not raw_result.strip().endswith("}"):
    raw_result += "\n}"

# 保存 JSON 
# 尝试解析 JSON
try:
    parsed_result = json.loads(str(result))

    

    # 🚨 关键修复点
    if "marketing_angles" in parsed_result:
        parsed_result["marketing_angles"] = parsed_result["marketing_angles"][:2]

    with open("outputs/reports/final_report.json", "w", encoding="utf-8") as f:
     json.dump(parsed_result, f, ensure_ascii=False, indent=2)

    print("\nJSON report saved successfully!")

except Exception as e:
    print("\nJSON parsing failed!")
    print(e)

    # 保存原始输出方便 debug,badcase tracking
    with open("outputs/raw_output.txt", "w", encoding="utf-8") as f:
        f.write(str(result))

    print("\nRaw output saved to outputs/raw_output.txt")

    # 保存 badcase
    badcase = {
        "error": str(e),
        "input": comments,
        "output": str(result),
        "error_type": "json_parse_error",
        "raw_output": raw_result
    }

    with open("outputs/audit/badcase.json", "r", encoding="utf-8") as f:
        badcases = json.load(f)

        badcases.append(badcase)

    with open("outputs/audit/badcase.json", "w", encoding="utf-8") as f:
        json.dump(badcases, f, ensure_ascii=False, indent=2)