import os
import sys
import json
import yaml
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

# =========================
# Runtime Logging
# =========================

os.makedirs(
    "outputs/logs",
    exist_ok=True
)

log_file = open(
    "outputs/logs/agentruntime.log",
    "a",
    encoding="utf-8"
)

sys.stdout = log_file
sys.stderr = log_file

from datetime import datetime

print(
    f"\n\n===== NEW RUN {datetime.now()} =====\n"
)

# =========================
# Crew Imports
# =========================

from crewai import Task, Crew

from agents.sentiment_agent import sentiment_agent
from agents.marketing_agent import marketing_agent
from agents.trend_agent import trend_agent
from agents.manager_agent import manager_agent





# --- 新增：读取配置文件逻辑 ---
def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    current_task_key = config.get('current_task', 'eggy_party') # 默认选蛋仔
    return config['tasks'][current_task_key]

# 加载当前选中的游戏配置
game_params = load_config()
GAME_NAME = game_params['game_name']
POSITIVE_EXAMPLE = game_params['positive_example']
NEGATIVE_EXAMPLE = game_params['negative_example']

# 自动创建 outputs 文件夹
os.makedirs("outputs", exist_ok=True)

# 读取评论数据
df = pd.read_csv("data/comments.csv")
comments = "\n".join(df["comment"].tolist())


# 定义任务
# 0. 先在项目头部定义配置变量（以后改这里即可）
GAME_NAME = "未定事件簿"
# 针对不同游戏的示例：未定用“左然卡面”，原神用“丝柯克建模”
POSITIVE_EXAMPLE = "左然这幅私语卡面绝了，眼神拉丝！" 
NEGATIVE_EXAMPLE = "这次异常调查的掉率也太低了吧，体力根本不够用。"

# 1. 泛化后的 sentiment_task
sentiment_task = Task(
    description=f"""
你是一名专业的《{GAME_NAME}》社区舆情分析师。

请分析以下玩家评论：

""" + comments + f"""

请完成：
1. 玩家整体情绪
2. 高频抱怨点（如：掉率、体力机制、剧情逻辑等）
3. 高频赞美点（如：卡面画质、配音表现、人设细节等）
4. 当前舆情风险（如：玩家退游倾向、集体维权风险）
5. 玩家最关注的角色（请准确识别游戏中的核心人物）

【情绪分类规则】

1. positive_topics 只能包含：
- 喜欢、满意、赞美、震撼、优秀、期待、认可、心动、还原

2. negative_topics 只能包含：
- 不满、抱怨、生气、坐牢、氪金压力、无聊、削弱、失望、人设崩坏

3. 不允许：
- 正向情绪放入 negative_topics
- 负向情绪放入 positive_topics

4. 示例：
评论："{POSITIVE_EXAMPLE}"
应归类为：positive_topics

评论："{NEGATIVE_EXAMPLE}"
应归类为：negative_topics

【重要要求】
1. 只能输出合法 JSON
2. 不要输出 markdown 格式代码块
3. 不要输出 ```json 或任何前导文本
4. 不要输出任何解释文字
5. 所有 key 必须使用英文双引号
6. 确保输出能被 json.loads() 直接解析

输出格式如下：
{{
  "overall_sentiment": "",
  "negative_topics": [
    {{
      "topic": "",
      "emotion": ""
    }}
  ],
  "positive_topics": [
    {{
      "topic": "",
      "emotion": ""
    }}
  ],
  "risk_alerts": [
    {{
      "risk": "",
      "suggestion": ""
    }}
  ],
  "hot_characters": [
    {{
      "character": "",
      "attention_level": ""
    }}
  ]
}}
""",
    expected_output=f"JSON analysis of {GAME_NAME} player sentiment.",
    agent=sentiment_agent
)

trend_task = Task(
    description=f"""
你将收到《{GAME_NAME}》玩家评论 + 情绪分析结果。

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
你将收到《{GAME_NAME}》玩家社区趋势分析报告。

请基于该报告：

1. 生成3个小红书爆款标题
2. 生成1段抖音短视频文案
3. 生成3个B站视频标题
4. 提供3个适合当前社区热点的营销方向

【趋势分析报告】

{{trend_task}}

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

# --- 1. 强制保存原始输出 (保命符，最先执行) ---
raw_final_string = str(result)
os.makedirs("outputs/audit", exist_ok=True)

with open("outputs/raw_output.txt", "w", encoding="utf-8") as f:
    f.write(raw_final_string)
print("\n[System] Raw output secured in outputs/raw_output.txt")

# --- 2. 尝试解析并清理 JSON ---
try:
    # 自动补全可能缺失的反括号
    processed_result = raw_final_string.strip()
    if not processed_result.endswith("}"):
        processed_result += "}"
    
    # 关键修复：去掉大模型可能自带的 markdown 标记
    processed_result = processed_result.replace("```json", "").replace("```", "").strip()
    
    parsed_result = json.loads(processed_result)

    # 业务逻辑：截取营销方向
    if "marketing_angles" in parsed_result:
        parsed_result["marketing_angles"] = parsed_result["marketing_angles"][:2]

    with open("outputs/reports/final_report.json", "w", encoding="utf-8") as f:
        json.dump(parsed_result, f, ensure_ascii=False, indent=2)

    print("✅ Final report saved successfully!")

except Exception as e:
    print(f"❌ JSON Parsing Failed: {e}")
    
    # --- 3. 安全追加 Badcase (防崩处理) ---
    badcase_path = "outputs/audit/badcase.json"
    
    # 获取现有 badcases，如果文件不存在或损坏则初始化为空列表
    current_badcases = []
    if os.path.exists(badcase_path):
        try:
            with open(badcase_path, "r", encoding="utf-8") as f:
                current_badcases = json.load(f)
        except Exception:
            current_badcases = []

    # 追加当前 badcase
    current_badcases.append({
        "error": str(e),
        "game": GAME_NAME,
        "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "raw_output": raw_final_string
    })

    # 写入文件
    try:
        with open(badcase_path, "w", encoding="utf-8") as f:
            json.dump(current_badcases, f, ensure_ascii=False, indent=2)
        print(f"⚠️ Badcase tracking updated in {badcase_path}")
    except Exception as final_e:
        print(f"致命错误：连 Badcase 都存不进去! {final_e}")