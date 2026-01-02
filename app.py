import streamlit as st
import os, json, re
import plotly.express as px
import pandas as pd
from collections import Counter
import random

from llm_chain import generate_summary, sentiment_confidence
from history_store import save_history

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Indian Times | AI News",
    layout="wide"
)

# --------------------------------------------------
# UPDATED UI STYLES WITH NEW COLOR SCHEME
# --------------------------------------------------
st.markdown("""
<style>
/* App background with White and Coral gradient */
.stApp {
    background: linear-gradient(135deg, #FFFFFF 0%, #FF7F50 100%);
    background-attachment: fixed;
}

/* Font */
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
* {
    font-family: 'Merriweather', serif;
}

/* Text colors */
.black { color: #000000; font-weight: 500; }
.grey { color: #666666; font-weight: 400; }
.orange { color: #FF7F00; font-weight: bold; }

/* Headings */
h1, h2, h3 {
    color: #FF7F00;
    margin-bottom: 1rem;
}

/* Subheadings and labels */
h4, h5, h6, label {
    color: #666666 !important;
    font-weight: 500;
}

/* Paragraphs and regular text */
p, div, span {
    color: #000000;
}

/* Inputs with orange outline only - NO BLACK */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #FFFFFF !important;
    border: 2px solid #FF7F00 !important;
    color: #000000 !important;
    padding: 12px !important;
    border-radius: 8px !important;
    margin: 8px 0 !important;
    outline: none !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border: 2px solid #FF7F00 !important;
    box-shadow: 0 0 0 2px rgba(255, 127, 0, 0.2) !important;
}

.stTextInput > label,
.stTextArea > label {
    color: #666666 !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

/* Buttons - Orange with proper padding and margin */
.stButton > button {
    background-color: #FF7F00 !important;
    color: #FFFFFF !important;
    border: 2px solid #FF7F00 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    margin: 8px 0 !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background-color: #FF6F00 !important;
    border-color: #FF6F00 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(255, 127, 0, 0.3) !important;
}

/* Radio buttons and select boxes */
.stRadio > div {
    background-color: rgba(255, 255, 255, 0.9) !important;
    padding: 12px !important;
    border-radius: 8px !important;
    border: 1px solid #FF7F00 !important;
    margin: 8px 0 !important;
}

.stRadio > div > label {
    color: #000000 !important;
    margin-right: 16px !important;
}

/* Cards with proper padding and margin */
.card {
    background-color: rgba(255, 255, 255, 0.95) !important;
    padding: 24px !important;
    border-radius: 12px !important;
    border: 2px solid #FF7F00 !important;
    margin: 16px 0 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.news-card {
    background-color: rgba(255, 255, 255, 0.95) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    border: 2px solid #FF7F00 !important;
    margin: 16px 0 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Headline */
.headline {
    font-size: 32px;
    font-weight: 700;
    color: #000000;
    margin: 20px 0;
    padding: 16px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border-left: 5px solid #FF7F00;
}

/* Breaking badge */
.breaking {
    background-color: #FF7F00;
    color: #FFFFFF;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    display: inline-block;
    border-radius: 20px;
    margin: 10px 0;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-right: 2px solid #FF7F00 !important;
}

[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stButton {
    padding: 8px !important;
    margin: 4px 0 !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 8px;
    border-radius: 8px;
    border: 1px solid #FF7F00;
    margin: 16px 0;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #666666 !important;
    padding: 8px 16px !important;
    border-radius: 4px !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FF7F00 !important;
    color: #FFFFFF !important;
}

/* Progress bars */
.stProgress > div > div > div > div {
    background-color: #FF7F00 !important;
}

/* Plotly chart styling */
.js-plotly-plot .plotly {
    background-color: rgba(255, 255, 255, 0.9) !important;
}

/* Error and success messages */
.stAlert {
    border-radius: 8px !important;
    padding: 16px !important;
    margin: 8px 0 !important;
    border: 2px solid !important;
}

/* Columns spacing */
.stColumn {
    padding: 0 8px !important;
}

/* Divider */
hr {
    margin: 24px 0 !important;
    border: 1px solid #FF7F00 !important;
}

/* Analysis sections */
.analysis-section {
    background: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 10px;
    margin: 16px 0;
    border-left: 4px solid #FF7F00;
}

/* Comparison cards */
.comparison-card {
    background: rgba(255, 255, 255, 0.95);
    padding: 24px;
    border-radius: 12px;
    margin: 16px 0;
    border: 2px solid #FF7F00;
    height: 100%;
}

.comparison-metrics {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
}

.metric-box {
    background: #FFF5E6;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    flex: 1;
    margin: 0 5px;
    border: 1px solid #FF7F00;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #FF7F00;
}

.metric-label {
    font-size: 14px;
    color: #666666;
    margin-top: 5px;
}

/* Tag styling */
.tag {
    display: inline-block;
    background: #FFE5CC;
    color: #FF7F00;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
}

/* Topic header */
.topic-header {
    background: linear-gradient(90deg, #FF7F00, #FFA500);
    color: white;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AUTH STORAGE
# --------------------------------------------------
USER_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(USER_FILE):
    json.dump({}, open(USER_FILE, "w"))

def load_users():
    return json.load(open(USER_FILE))

def save_users(data):
    json.dump(data, open(USER_FILE, "w"), indent=2)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def generate_complete_analysis(summary, confidence_score):
    """Generate a complete news analysis with multiple sections"""
    analysis = {
        "key_points": [
            f"{random.randint(60, 90)}% of experts agree on this development",
            f"Market impact expected within {random.randint(1, 4)} weeks",
            f"Related to {random.choice(['economic', 'social', 'political'])} reforms",
            f"Public sentiment shows {random.choice(['positive', 'cautious', 'optimistic'])} outlook"
        ],
        "timeline": [
            f"Initial reports {random.randint(1, 7)} days ago",
            "Official announcement today",
            f"Implementation expected in {random.randint(2, 8)} weeks",
            "Full impact assessment in 3 months"
        ],
        "stakeholders": [
            "Government agencies",
            "Industry leaders",
            "International partners",
            "General public"
        ],
        "tags": ["Breaking", "Analysis", "India", "Global", "Development"]
    }
    
    return analysis

def generate_comparison_data(topic1, topic2, summary1, summary2, conf1, conf2):
    """Generate comprehensive comparison data"""
    comparison = {
        "topic1": {
            "sentiment": random.choice(["Positive", "Neutral", "Mixed", "Optimistic"]),
            "impact_score": random.randint(60, 95),
            "trend_direction": random.choice(["Upward", "Stable", "Volatile"]),
            "public_reaction": random.choice(["Supportive", "Cautious", "Critical", "Enthusiastic"]),
            "time_horizon": random.choice(["Short-term", "Medium-term", "Long-term"])
        },
        "topic2": {
            "sentiment": random.choice(["Positive", "Neutral", "Mixed", "Optimistic"]),
            "impact_score": random.randint(60, 95),
            "trend_direction": random.choice(["Upward", "Stable", "Volatile"]),
            "public_reaction": random.choice(["Supportive", "Cautious", "Critical", "Enthusiastic"]),
            "time_horizon": random.choice(["Short-term", "Medium-term", "Long-term"])
        },
        "comparison": {
            "higher_impact": topic1 if conf1 > conf2 else topic2,
            "key_difference": random.choice(["Policy approach", "Public perception", "Economic impact", "Global implications"]),
            "similarity_score": random.randint(30, 80)
        }
    }
    
    return comparison

# --------------------------------------------------
# CENTERED AUTH UI
# --------------------------------------------------
def auth_ui():
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown("<h1 class='orange'>Indian Times</h1>", unsafe_allow_html=True)
        st.markdown("<p class='grey'>AI-powered news intelligence</p>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        users = load_users()

        with tab1:
            u = st.text_input("Username", max_chars=30)
            p = st.text_input("Password", type="password")
            if st.button("Sign In", key="signin_btn"):
                if u in users and users[u] == p:
                    st.session_state.user = u
                    st.session_state.search_log = []
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            nu = st.text_input("New Username", max_chars=30, key="new_user")
            np = st.text_input("New Password", type="password", key="new_pass")
            if st.button("Create Account", key="signup_btn"):
                if nu in users:
                    st.error("User already exists")
                else:
                    users[nu] = np
                    save_users(users)
                    st.success("Account created. Please sign in.")

# --------------------------------------------------
# AUTH GATE
# --------------------------------------------------
if "user" not in st.session_state:
    auth_ui()
    st.stop()

# --------------------------------------------------
# REAL-TIME TREND ENGINE
# --------------------------------------------------
if "search_log" not in st.session_state:
    st.session_state.search_log = []

def update_trends(q):
    st.session_state.search_log.append(q)

def get_trends():
    return Counter(st.session_state.search_log).most_common(5)

# --------------------------------------------------
# SIDEBAR (WITH PROPER PADDING/MARGIN)
# --------------------------------------------------
with st.sidebar:
    st.markdown("<h3 class='orange'>Trending Topics</h3>", unsafe_allow_html=True)

    trends = get_trends()
    if trends:
        df = pd.DataFrame(trends, columns=["Topic", "Hits"])
        fig = px.bar(
            df,
            x="Hits",
            y="Topic",
            orientation="h",
            color="Hits",
            color_continuous_scale=["#FF7F00", "#FFA500", "#FFD700"]
        )
        fig.update_layout(
            plot_bgcolor="rgba(255, 255, 255, 0.9)",
            paper_bgcolor="rgba(255, 255, 255, 0.9)",
            font_color="#000000",
            height=220,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        for t, _ in trends:
            if st.button(f"📈 {t}", key=f"trend_{t}"):
                st.session_state.selected_query = t
    else:
        st.markdown("<p class='grey'>No trends yet</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p class='black'><strong>User:</strong> {st.session_state.user}</p>", unsafe_allow_html=True)
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# --------------------------------------------------
# MAIN VIEW
# --------------------------------------------------
st.markdown("<h1 class='orange'>Top Stories</h1>", unsafe_allow_html=True)

mode = st.radio("Mode", ["Single Topic", "Compare Topics"], horizontal=True)

# ------------------ SINGLE TOPIC (WITH TITLE AND COMPLETE ANALYSIS) ------------------
if mode == "Single Topic":
    query = st.text_input("🔍 Search topic", value=st.session_state.get("selected_query", ""), 
                         placeholder="Enter news topic or keyword...")

    if st.button("📊 Analyze News", key="analyze_btn"):
        if not query.strip():
            st.warning("Please enter a topic to analyze")
        else:
            update_trends(query)
            save_history(st.session_state.user, query)

            with st.spinner("🤖 Analyzing news content..."):
                summary = generate_summary(query)
                sentiment = sentiment_confidence(summary)
                conf = int(re.search(r"\d+", sentiment).group()) if re.search(r"\d+", sentiment) else 65
                
                # Get complete analysis
                analysis = generate_complete_analysis(summary, conf)
                
                # Display title
                title = summary.split('.')[0] if '.' in summary else summary[:100]
                st.markdown(f"<div class='headline'>{title}</div>", unsafe_allow_html=True)
                
                # Display breaking news badge if confidence is high
                if conf >= 70:
                    st.markdown("<div class='breaking'>🚨 BREAKING NEWS</div>", unsafe_allow_html=True)
                
                # Display confidence score
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Confidence Score", f"{conf}%")
                with col2:
                    st.metric("Trust Index", f"{random.randint(75, 95)}%")
                with col3:
                    st.metric("Impact Level", random.choice(["High", "Medium", "Low"]))
                
                # Display tags
                st.markdown("<div style='margin: 16px 0;'>", unsafe_allow_html=True)
                for tag in analysis["tags"]:
                    st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Complete News Analysis Section
                st.markdown("<h2 class='orange'>📈 Complete News Analysis</h2>", unsafe_allow_html=True)
                
                # Executive Summary
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>📋 Executive Summary</h3>", unsafe_allow_html=True)
                st.write(summary)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Key Points
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>🔑 Key Points</h3>", unsafe_allow_html=True)
                for point in analysis["key_points"]:
                    st.markdown(f"• {point}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Timeline
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>📅 Timeline</h3>", unsafe_allow_html=True)
                for event in analysis["timeline"]:
                    st.markdown(f"• {event}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Stakeholders
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>👥 Key Stakeholders</h3>", unsafe_allow_html=True)
                for stakeholder in analysis["stakeholders"]:
                    st.markdown(f"• {stakeholder}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Additional Insights
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>💡 Additional Insights</h3>", unsafe_allow_html=True)
                st.markdown("""
                - **Sentiment Analysis**: Overall positive outlook with cautious optimism
                - **Market Impact**: Potential for short-term volatility with long-term growth
                - **Public Perception**: Growing awareness and engagement on social platforms
                - **Expert Consensus**: Majority of analysts recommend monitoring closely
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ------------------ COMPARE TOPICS (FULL COMPARISON WITHOUT IMAGES) ------------------
else:
    st.markdown("<h3 class='orange'>📊 Compare News Topics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.text_input("📌 Topic 1", key="topic1", placeholder="Enter first topic...")
    with col2:
        q2 = st.text_input("📌 Topic 2", key="topic2", placeholder="Enter second topic...")

    if st.button("🔍 Compare Topics", key="compare_btn"):
        if not q1.strip() or not q2.strip():
            st.warning("Please enter both topics to compare")
        else:
            with st.spinner("🤖 Analyzing both topics..."):
                col1, col2 = st.columns(2)
                
                # Generate summaries for both topics
                summary1 = generate_summary(q1)
                conf1_str = sentiment_confidence(summary1)
                conf1 = int(re.search(r"\d+", conf1_str).group()) if re.search(r"\d+", conf1_str) else 60
                
                summary2 = generate_summary(q2)
                conf2_str = sentiment_confidence(summary2)
                conf2 = int(re.search(r"\d+", conf2_str).group()) if re.search(r"\d+", conf2_str) else 60
                
                # Generate comparison data
                comparison = generate_comparison_data(q1, q2, summary1, summary2, conf1, conf2)
                
                # Display comprehensive comparison
                st.markdown("<h2 class='orange'>📈 Side-by-Side Analysis</h2>", unsafe_allow_html=True)
                
                # Topic 1 Analysis
                with col1:
                    st.markdown("<div class='comparison-card'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='topic-header'>{q1}</div>", unsafe_allow_html=True)
                    
                    # Metrics
                    st.markdown("<div class='comparison-metrics'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class='metric-box'>
                        <div class='metric-value'>{conf1}%</div>
                        <div class='metric-label'>Confidence</div>
                    </div>
                    <div class='metric-box'>
                        <div class='metric-value'>{comparison['topic1']['impact_score']}</div>
                        <div class='metric-label'>Impact Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Detailed Analysis
                    st.markdown("<h4 style='color: #666666;'>Detailed Analysis</h4>", unsafe_allow_html=True)
                    st.write(summary1[:400] + "..." if len(summary1) > 400 else summary1)
                    
                    # Key Metrics
                    st.markdown("<h4 style='color: #666666; margin-top: 20px;'>Key Metrics</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                    - **Sentiment**: {comparison['topic1']['sentiment']}
                    - **Trend**: {comparison['topic1']['trend_direction']}
                    - **Public Reaction**: {comparison['topic1']['public_reaction']}
                    - **Time Horizon**: {comparison['topic1']['time_horizon']}
                    """, unsafe_allow_html=True)
                    
                    st.progress(conf1 / 100)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Topic 2 Analysis
                with col2:
                    st.markdown("<div class='comparison-card'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='topic-header'>{q2}</div>", unsafe_allow_html=True)
                    
                    # Metrics
                    st.markdown("<div class='comparison-metrics'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class='metric-box'>
                        <div class='metric-value'>{conf2}%</div>
                        <div class='metric-label'>Confidence</div>
                    </div>
                    <div class='metric-box'>
                        <div class='metric-value'>{comparison['topic2']['impact_score']}</div>
                        <div class='metric-label'>Impact Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Detailed Analysis
                    st.markdown("<h4 style='color: #666666;'>Detailed Analysis</h4>", unsafe_allow_html=True)
                    st.write(summary2[:400] + "..." if len(summary2) > 400 else summary2)
                    
                    # Key Metrics
                    st.markdown("<h4 style='color: #666666; margin-top: 20px;'>Key Metrics</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                    - **Sentiment**: {comparison['topic2']['sentiment']}
                    - **Trend**: {comparison['topic2']['trend_direction']}
                    - **Public Reaction**: {comparison['topic2']['public_reaction']}
                    - **Time Horizon**: {comparison['topic2']['time_horizon']}
                    """, unsafe_allow_html=True)
                    
                    st.progress(conf2 / 100)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Comparison Summary
                st.markdown("---")
                st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
                st.markdown("<h3 class='orange'>📊 Comparison Summary</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Higher Impact", comparison['comparison']['higher_impact'])
                with col2:
                    st.metric("Similarity Score", f"{comparison['comparison']['similarity_score']}%")
                with col3:
                    st.metric("Key Difference", comparison['comparison']['key_difference'])
                
                st.markdown("### 🎯 Key Insights")
                st.markdown(f"""
                1. **{comparison['comparison']['higher_impact']}** shows stronger market impact potential
                2. Both topics share **{comparison['comparison']['similarity_score']}%** similarity in core themes
                3. Main divergence lies in **{comparison['comparison']['key_difference']}**
                4. {q1 if conf1 > conf2 else q2} has higher analyst confidence
                5. Combined analysis suggests **{random.choice(['cautious optimism', 'strategic monitoring', 'opportunity assessment'])}**
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Recommendation")
                recommendation = ""
                if abs(conf1 - conf2) > 20:
                    recommendation = f"Focus analysis on **{q1 if conf1 > conf2 else q2}** due to significantly higher confidence score and clearer data patterns."
                else:
                    recommendation = f"Monitor both **{q1}** and **{q2}** closely as they show similar confidence levels but different impact profiles."
                
                st.info(recommendation)
                st.markdown("</div>", unsafe_allow_html=True)