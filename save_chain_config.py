import joblib

config = {
    "model_name": "llama-3.1-8b-instant",
    "temperature": 0.3,
    "prompt_template": """
You are a senior equity research analyst.

Tone: {tone}
Summary Length: {length}

User Query:
{query}

News Articles:
{news}

Tasks:
1. Executive summary
2. Key trends
3. Risks
4. Opportunities
"""
}

joblib.dump(config, "news_llm_config.joblib")
print("✅ Model configuration saved")
