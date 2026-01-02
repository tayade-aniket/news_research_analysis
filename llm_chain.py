import os
from dotenv import load_dotenv

# ✅ LOAD ENV FIRST
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import config
from news_service import fetch_news

# ✅ DEBUG CHECK (OPTIONAL – REMOVE LATER)
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq LLM
llm = ChatGroq(
    model=config["model_name"],
    temperature=config["temperature"],
    groq_api_key=os.getenv("GROQ_API_KEY")
)

prompt = PromptTemplate(
    template="""
You are a senior financial news analyst.

Query:
{query}

News Articles:
{news}

Tasks:
1. Executive summary
2. Key trends
3. Risks & opportunities
""",
    input_variables=["query", "news"]
)

def generate_summary(query: str) -> str:
    news = fetch_news(query)
    response = llm.invoke(prompt.format(query=query, news=news))
    return response.content

def sentiment_confidence(summary: str) -> str:
    response = llm.invoke(
        f"""
Analyze sentiment (Positive/Neutral/Negative)
and confidence score (0–100%).

Summary:
{summary}
"""
    )
    return response.content
