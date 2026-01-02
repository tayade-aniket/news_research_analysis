import streamlit as st

USERS = {"admin": "admin123", "user": "user123"}

def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in USERS and USERS[user] == pwd:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.clear()
    st.rerun()
