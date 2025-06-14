import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Streamlit page config
st.set_page_config(page_title="Gemini Chat", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Options")
    st.markdown("Customize your chat experience.")
    if st.button("🗑️ Clear Chat History"):
       st.session_state.messages = []
       st.rerun()
    st.markdown("---")
    st.info("Made with ❤️ using Gemini API + Streamlit")

# App Title
st.title("🤖 Gemini Chat Assistant")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask anything...")

if prompt:
    # Add user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Request to Gemini API
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    # API call and response handling
    with st.spinner("Gemini is thinking..."):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses
            gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            gemini_reply = f"⚠️ Failed to get a response: {e}"

    # Show and store assistant reply
    st.chat_message("assistant").markdown(gemini_reply)
    st.session_state.messages.append({"role": "assistant", "content": gemini_reply})
