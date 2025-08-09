# app.py
import streamlit as st
import wikipedia
from gtts import gTTS
import io
import datetime
import os
import re
from typing import List, Dict

# -------------------
# Page setup
# -------------------
st.set_page_config(page_title="Classic Real-World Chatbot", page_icon="💬", layout="centered")
st.title("💬 Classic Real-World Chatbot")

USER_AVATAR = "🧑"
BOT_AVATAR = "🤖"

# Load persistent history
HISTORY_FILE = "chat_history.txt"
if "messages" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_lines = f.readlines()
        st.session_state.messages = [eval(line.strip()) for line in history_lines if line.strip()]
    else:
        st.session_state.messages: List[Dict] = []

# -------------------
# Core functions
# -------------------
def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for m in st.session_state.messages:
            f.write(str(m) + "\n")

def add_message(role, content, meta=None):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "meta": meta or {}
    })
    save_history()

def wikipedia_lookup(query, sentences=2):
    try:
        results = wikipedia.search(query)
        if not results:
            return "Sorry, I couldn't find anything.", None
        summary = wikipedia.summary(results[0], sentences=sentences, auto_suggest=False)
        url = wikipedia.page(results[0], auto_suggest=False).url
        return summary, url
    except wikipedia.DisambiguationError as e:
        opts = ", ".join(e.options[:5])
        return f"Your query is ambiguous. Did you mean: {opts}?", None
    except:
        return "Error fetching from Wikipedia.", None

def text_to_speech(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def handle_tools(query):
    # Tool: Date/Time
    if re.search(r"(time|date|day) now", query.lower()):
        return datetime.datetime.now().strftime("Current date/time: %Y-%m-%d %H:%M:%S")

    # Tool: Calculator
    if re.match(r"^\d+(\s*[\+\-\*/]\s*\d+)+$", query):
        try:
            return f"Result: {eval(query)}"
        except:
            return "Invalid calculation."

    return None  # no local tool used

# -------------------
# Sidebar
# -------------------
with st.sidebar:
    st.header("Settings")
    wiki_sentences = st.slider("Wikipedia sentences", 1, 8, 2)
    voice_enabled = st.checkbox("Enable voice output", True)
    voice_lang = st.selectbox("Voice language", ["en", "hi", "kn", "ta", "te", "ml"], 0)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.experimental_rerun()

# -------------------
# Chat UI
# -------------------
uploaded = st.file_uploader("Upload a text file for local search", type=["txt"])
upload_text = ""
if uploaded:
    upload_text = uploaded.read().decode("utf-8")

query = st.text_input("Type your message:")

if query:
    add_message("user", query)
    st.session_state["bot_typing"] = True
    st.experimental_rerun()

if st.session_state.get("bot_typing"):
    last_query = st.session_state.messages[-1]["content"]

    # Tool check first
    tool_result = handle_tools(last_query)
    if tool_result:
        bot_reply = tool_result
        wiki_url = None
    else:
        # File search
        if upload_text and last_query.lower() in upload_text.lower():
            bot_reply = "I found this in your file:\n" + "\n".join(
                line for line in upload_text.splitlines() if last_query.lower() in line.lower()
            )[:500]
            wiki_url = None
        else:
            # Wikipedia
            bot_reply, wiki_url = wikipedia_lookup(last_query, sentences=wiki_sentences)

    add_message("bot", bot_reply, {"wiki_url": wiki_url})
    st.session_state["bot_typing"] = False
    st.experimental_rerun()

# -------------------
# Display conversation
# -------------------
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    avatar = USER_AVATAR if is_user else BOT_AVATAR
    align = "right" if is_user else "left"
    st.markdown(
        f"<div style='text-align:{align}; border:1px solid #ccc; padding:8px; "
        f"border-radius:10px; margin:5px; background-color:{'#e0f7fa' if is_user else '#f1f8e9'}'>"
        f"<b>{avatar} [{msg['time']}]</b><br>{msg['content']}</div>",
        unsafe_allow_html=True
    )
    if not is_user and msg.get("meta", {}).get("wiki_url"):
        st.markdown(f"[Read more here]({msg['meta']['wiki_url']})")
    if not is_user and voice_enabled:
        if st.button("🔊", key=f"voice_{msg['time']}"):
            st.audio(text_to_speech(msg["content"], voice_lang), format="audio/mp3")
