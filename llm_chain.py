import os
import joblib
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from news_service import fetch_news

# Load env variables
load_dotenv()

# Safety check
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("❌ GROQ_API_KEY not found. Check .env file.")

# Load saved config
config = joblib.load("news_llm_config.joblib")

# Initialize Groq LLM
llm = ChatGroq(
    model=config["model_name"],
    temperature=config["temperature"],
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Prompt
prompt = PromptTemplate(
    template=config["prompt_template"],
    input_variables=["query", "news", "tone", "length"]
)

chain = prompt | llm


# 🔍 VALIDATION FUNCTION (ADD THIS BELOW CHAIN)
def validate_summary(query, summary):
    validation_prompt = f"""
You are a fact-checking AI.

User Query:
{query}

Generated Summary:
{summary}

Check:
1. Relevance (High/Medium/Low)
2. Hallucination risk (Yes/No)
3. Missing important facts (Yes/No)

Give a short validation report.
"""
    response = llm.invoke(validation_prompt)
    return response.content


# 🧠 MAIN FUNCTION (REPLACE OLD ONE)
def generate_summary(query, tone, length):
    news_text = fetch_news(query)

    response = chain.invoke({
        "query": query,
        "news": news_text,
        "tone": tone,
        "length": length
    })

    summary = response.content
    validation = validate_summary(query, summary)

    # ⬅️ RETURN BOTH
    return summary, validation
