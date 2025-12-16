import streamlit as st
import hashlib
from llm_chain import generate_summary
from filters import get_tone, get_length
from history import save_query, load_history

st.set_page_config(page_title="AI News Analyst", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user": hashlib.sha256("user123".encode()).hexdigest()
}

def login(u, p):
    return USERS.get(u) == hashlib.sha256(p.encode()).hexdigest()

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# ---------------- APP ----------------
st.title("📰 AI-Powered News Analysis")

query = st.text_input("Enter topic or company")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Neutral", "Bullish", "Bearish"])
with col2:
    length = st.selectbox("Summary Length", ["Short", "Medium", "Detailed"])

if st.button("Analyze"):
    if query.strip():
        with st.spinner("Analyzing..."):
            summary, validation = generate_summary(
                query,
                get_tone(tone),
                get_length(length)
            )
            save_query(query, summary)

        st.subheader("🧠 Summary")
        st.markdown(summary)

        st.subheader("✅ Validation")
        st.info(validation)

        st.download_button(
            "📥 Download Summary",
            summary,
            file_name=f"{query}_summary.txt"
        )
    else:
        st.warning("Enter a valid query")

with st.expander("📊 History"):
    for h in reversed(load_history()[-5:]):
        st.markdown(f"**{h['query']}**  \n{h['summary'][:200]}...")
