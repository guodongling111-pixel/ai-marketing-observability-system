import streamlit as st
import json
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI Game Marketing Dashboard",
    layout="wide"
)

# 标题
st.title("🎮 Game Marketing Multi-Agent Dashboard")

st.markdown("---")

# 基础状态栏
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Game", "Impact")

with col2:
    st.metric("System Status", "Running")

with col3:
    st.metric(
        "Last Updated",
        datetime.now().strftime("%H:%M:%S")
    )

st.markdown("---")

# Workflow 状态
st.subheader("🤖 Agent Workflow Status")

workflow_cols = st.columns(4)

agent_data = [
    {
        "name": "Sentiment Agent",
        "status": "Success",
        "duration": "2.1s",
        "tokens": 420
    },
    {
        "name": "Trend Agent",
        "status": "Success",
        "duration": "1.8s",
        "tokens": 380
    },
    {
        "name": "Marketing Agent",
        "status": "Success",
        "duration": "2.5s",
        "tokens": 510
    },
    {
        "name": "Manager Agent",
        "status": "Success",
        "duration": "1.2s",
        "tokens": 250
    }
]

for i, agent in enumerate(agent_data):

    with workflow_cols[i]:

        st.markdown(f"""
        ### 🤖 {agent['name']}

        - Status: ✅ {agent['status']}
        - Duration: ⏱ {agent['duration']}
        - Tokens: 🔥 {agent['tokens']}
        """)

# 读取最终报告
# =========================
# Sentiment Report
# =========================

sentiment_path = "outputs/reports/sentiment_report.json"

if os.path.exists(sentiment_path):

    try:

        with open(
            sentiment_path,
            "r",
            encoding="utf-8"
        ) as f:

            sentiment_report = json.load(f)

        st.subheader("😊 Sentiment Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Overall Sentiment")

            st.success(
                sentiment_report.get(
                    "overall_sentiment",
                    "Unknown"
                )
            )

            st.markdown("### Positive Topics")

            for item in sentiment_report.get(
                "positive_topics",
                []
            ):

                st.info(
                    f"{item['topic']} - {item['emotion']}"
                )

        with col2:

            st.markdown("### Negative Topics")

            for item in sentiment_report.get(
                "negative_topics",
                []
            ):

                st.error(
                    f"{item['topic']} - {item['emotion']}"
                )

            st.markdown("### Hot Characters")

            for item in sentiment_report.get(
                "hot_characters",
                []
            ):

                st.warning(
                    f"{item['character']} ({item['attention_level']})"
                )

    except Exception as e:

        st.error(
            f"Sentiment Report Failed: {e}"
        )

st.markdown("---")

# =========================
# Trend Report
# =========================

trend_path = "outputs/reports/trend_report.json"

if os.path.exists(trend_path):

    try:

        with open(
            trend_path,
            "r",
            encoding="utf-8"
        ) as f:

            trend_report = json.load(f)

        st.subheader("📈 Trend Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🔥 Hot Topics")

            for topic in trend_report.get(
                "hot_topics",
                []
            ):

                st.info(str(topic))

            st.markdown("### 📈 Rising Topics")

            for topic in trend_report.get(
                "rising_topics",
                []
            ):

                st.success(str(topic))

        with col2:

            st.markdown("### 📉 Declining Topics")

            for topic in trend_report.get(
                "declining_topics",
                []
            ):

                st.error(str(topic))

            st.markdown("### 🧠 Insights")

            st.warning(
                trend_report.get(
                    "insights",
                    ""
                )
            )

    except Exception as e:

        st.error(
            f"Trend Report Failed: {e}"
        )

st.markdown("---")

# =========================
# Marketing Report
# =========================

marketing_path = "outputs/reports/marketing_report.json"

if os.path.exists(marketing_path):
    try:
        with open(marketing_path, "r", encoding="utf-8") as f:
            marketing_report = json.load(f)

        st.subheader("🚀 Marketing Generation")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📕 Xiaohongshu Titles")
            for title in marketing_report.get(
                "xiaohongshu_titles",
                []
            ):
                st.success(title)

            st.markdown("### 🎵 Douyin Copywriting")
            st.info(
                marketing_report.get(
                    "douyin_copywriting",
                    ""
                )
            )

        with col2:
            st.markdown("### 📺 Bilibili Titles")
            for title in marketing_report.get(
                "bilibili_titles",
                []
            ):
                st.warning(title)

            st.markdown("### 🚀 Marketing Angles")
            for angle in marketing_report.get(
                "marketing_angles",
                []
            ):
                st.markdown(f"- {angle}")

    except Exception as e:
        st.error(
            f"Marketing Report Failed: {e}"
        )

st.markdown("---")

# =========================
# Manager Report
# =========================

manager_path = "outputs/reports/manager_report.json"
if os.path.exists(manager_path):

    try:

        with open(
            manager_path,
            "r",
            encoding="utf-8"
        ) as f:

            manager_report = json.load(f)

        st.subheader("🧠 Manager Review")

        # =====================
        # Workflow Status
        # =====================

        status = manager_report.get(
            "workflow_status",
            "unknown"
        )

        if status == "approved":

            st.success("✅ Workflow Approved")

        elif status == "issue_found":

            st.error("⚠ Issues Found")

        else:

            st.warning("Unknown Status")

        col1, col2 = st.columns(2)

        # =====================
        # Validation Result
        # =====================

        with col1:

            st.markdown("### Validation Result")

            validation = manager_report.get(
                "validation_result",
                []
            )

            for item in validation:

                st.info(str(item))

        # =====================
        # Manager Feedback
        # =====================

        with col2:

            st.markdown("### Manager Feedback")

            feedback = manager_report.get(
                "manager_feedback",
                []
            )

            for item in feedback:

                st.warning(str(item))

        # =====================
        # Risk Summary
        # =====================

        st.markdown("### 🚨 Risk Summary")

        st.error(
            manager_report.get(
                "risk_summary",
                "No risk summary"
            )
        )

    except Exception as e:

        st.error(
            f"Manager Report Failed: {e}"
        )


st.markdown("---")

# =========================
# Audit / System Errors
# =========================

badcase_path = "outputs/audit/badcase.json"

if os.path.exists(badcase_path):

    with open(badcase_path, "r", encoding="utf-8") as f:
        badcases = json.load(f)

    st.subheader("🚨 System Error Center")

    if len(badcases) == 0:

        st.success("✅ No System Errors")

    else:

        for case in badcases:

            with st.expander(
                f"⚠ {case.get('agent', 'unknown')}"
            ):

                st.error(
                    case.get(
                        "error_type",
                        "unknown_error"
                    )
                )

                st.markdown(
                    f"""
                    **Error Detail**

                    {case.get('error', '')}
                    """
                )

                st.code(
                    case.get(
                        "raw_output",
                        ""
                    )
                )