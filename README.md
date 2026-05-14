# 🤖 Game-Insight-Agent: 知识库驱动的多 Agent 营销决策系统

### 🏗️ 系统定位

AI-powered Multi-Agent Workflow System for **原神 (Genshin Impact) 社区营销运营**。  
目标：通过玩家评论分析、社区热点发现和自动生成营销文案，实现游戏运营智能化与 AI 驱动的决策闭环。

---

## 🌟 核心价值

* **Multi-Agent Workflow**：各 Agent 专注不同任务，协作完成完整营销链路
* **Data Augmentation**：原始 CSV → 增强 CSV → 决策支撑
* **Knowledge Base Alignment**：统一业务逻辑，输出符合二次元游戏话语（氪金、保底、谷子等）
* **Audit System + Manager Agent**：
  * **Audit System**：监控系统级错误（工具调用、失败重试、输出格式异常）
  * **Manager Agent**：分析大模型逻辑链条，通过子 Agent report 检查输出完整性和一致性
* **Platform Adaptation**：支持小红书、抖音、B站国内社区，后续可扩展海外平台

---

## 🏗️ 系统架构

```text
                    Manager Agent
                           ↓
        ┌─────────────┬─────────────┐
        ↓             ↓             ↓
Sentiment Agent   Trend Agent   Marketing Agent
                           ↓
                   Audit System (Bad Case Logs)
                           ↓
                  Final Marketing Report
```

**流程说明：**

1. **Crawler** → 采集原始评论 CSV
2. **Sentiment Agent + Knowledge Base** → 玩家情绪报告
3. **Trend Agent + Knowledge Base** → 增广 CSV + 趋势报告
4. **Marketing Agent + Knowledge Base** → 平台定制化营销文案（含二次元游戏话语）
5. **Audit System** → 检查系统级错误：工具调用、失败重试次数、输出格式异常
6. **Manager Agent** → 分析大模型逻辑链条，通过子 Agent report 检查输出完整性和一致性
7. **Manager Agent** → 输出最终运营报告及 Bad Case 日志

---

## 📂 Agent 模块

| Agent           | 功能                                                                  |
| --------------- | ------------------------------------------------------------------- |
| Sentiment Agent | 玩家情绪分析：正负情绪、抱怨/赞美、高频角色、舆情风险                                         |
| Trend Agent     | 社区热点发现：热门角色、关键词、争议话题、传播潜力                                           |
| Marketing Agent | 自动生成小红书、B站、抖音短视频文案，知识库驱动二次元话语（氪金、保底、谷子等）                            |
| Audit System    | 系统级错误监控：工具调用、失败重试、输出格式异常                                            |
| Manager Agent   | 调度 Agent，分析大模型逻辑链条，收集各 Agent report 检查输出完整性与一致性，输出最终报告与 Bad Case 日志 |

---

## 🔗 核心理念

### 1. 数据增广 (Dynamic Value Augmentation)

* 原始 CSV 是“食材”，经过 Trend & Sentiment Agent 处理后，加入价值分析列 → 半成品数据集
* 为 Marketing Agent 提供决策锚点，实现量化支撑

### 2. 知识库驱动 (Knowledge Base Alignment)

* Agent 执行前对照统一 KB
* 保证语义对齐、逻辑一致、业务规范遵循
* 输出符合二次元游戏语境和平台风格

### 3. 系统级监控与逻辑链条审查

* **Audit System**：自动检查工具调用是否成功、失败重试次数、输出格式异常
* **Manager Agent**：分析 LLM 逻辑链条，通过收集各子 Agent report 检查输出完整性和一致性
* 最终形成 Bad Case 日志，供团队快速定位问题并优化系统

---

## 🛠️ 技术栈

| 模块              | 技术                             |
| --------------- | ------------------------------ |
| Multi-Agent     | CrewAI                         |
| LLM             | Doubao API / OpenAI            |
| Workflow        | CrewAI Hierarchical Process    |
| 数据处理            | pandas                         |
| 可视化 & Dashboard | Streamlit / plotly / wordcloud |
| 评论数据            | 小红书 / 抖音 / B站 CSV + Selenium   |

---

## 🗂️ 项目目录结构

```text
teyvat-marketing-agent/
├── agents/
│   ├── sentiment_prompt.txt
│   ├── trend_prompt.txt
│   └── marketing_prompt.txt
├── workflows/
│   └── crew.py
├── data/
│   └── genshin_comments.csv
├── outputs/
│   ├── report.json
│   └── wordcloud.png
├── dashboard/
│   └── app.py
├── utils/
│   ├── llm.py
│   └── data_loader.py
├── requirements.txt
└── README.md
```

> **说明**：`agents/` 目录仅存放 prompt 文件，实际逻辑由 Manager Agent 调用 workflow 执行

---

## 💡 README亮点总结

* **Multi-Agent Workflow** + **Knowledge Base Alignment**
* **动态 CSV 增强**，实现 AI Feature Engineering
* **系统级监控 + 逻辑链条审查**，保证流程稳定
* **可视化 Dashboard**支持运营决策落地
* 输出内容符合二次元游戏语境，适配国内平台营销
