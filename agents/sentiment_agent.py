from crewai import Agent

sentiment_agent = Agent(
    role="Tears of Themis Community Sentiment Specialist",

    goal="""
    Analyze player emotions and dissatisfaction patterns
    in Tears of Themis Impact discussions.
    """,

    backstory="""
    You are an experienced game community analyst
    specializing in Chinese gaming communities such as
    Xiaohongshu, Douyin and Bilibili.
    """,

    verbose=True,

    llm="qwen2.5:7b"
)