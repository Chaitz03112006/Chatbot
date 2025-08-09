# app.py
import streamlit as st
import wikipedia
from gtts import gTTS
import io
import datetime
from typing import List, Dict, Optional

# -------------------
# Page config & utils
# -------------------
st.set_page_config(page_title="Classic Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Classic Chatbot — Wikipedia + Voice")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages: List[Dict] = []  # each item: {"role": "user"/"bot", "content": str, "meta": {...}}

# Helper: add message
def add_message(role: str, content: str, meta: Optional[dict] = None):
    if meta is None:
        meta = {}
    st.session_state.messages.append({"role": role, "content": content, "meta": meta})

# -------------------
# Sidebar (settings)
# -------------------
with st.sidebar:
    st.header("Settings")
    wiki_sentences = st.slider("Wikipedia summary sentences", 1, 8, 2)
    voice_enabled = st.checkbox("Enable voice button", value=True)
    voice_lang = st.selectbox("Voice language", ["en", "hi", "kn", "ta", "te", "ml"], index=0)
    persona = st.selectbox("Persona", ["Friendly", "Formal", "Concise"], index=0)
    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# -------------------
# File upload for context
# -------------------
st.markdown("#### Upload contextual text (optional)")
uploaded = st.file_uploader("Upload a .txt file to add as context (optional)", type=["txt"])
upload_context = ""
if uploaded:
    try:
        upload_context = uploaded.read().decode("utf-8")
        st.success(f"Loaded {uploaded.name} ({len(upload_context.splitlines())} lines)")
    except Exception:
        st.error("Couldn't read file. Please upload plain text .txt")

# -------------------
# Core functions
# -------------------
def get_wikipedia_summary(query: str, sentences: int = 2):
    """Searches Wikipedia and returns summary + URL"""
    results = wikipedia.search(query)
    if not results:
        return "Sorry, I couldn't find anything on that topic.", None
    page_title = results[0]
    try:
        summary = wikipedia.summary(page_title, sentences=sentences, auto_suggest=False, redirect=True)
        page = wikipedia.page(page_title, auto_suggest=False, redirect=True)
        return summary, page.url
    except wikipedia.DisambiguationError as e:
        options = e.options[:7]
        opt_str = "Ambiguous query. Possible options:\n" + "\n".join(f"- {o}" for o in options)
        return opt_str, None
    except wikipedia.PageError:
        return "Sorry, I couldn't find a page matching your query.", None
    except Exception as ex:
        return f"Something went wrong with Wikipedia: {ex}", None

def text_to_speech_bytes(text: str, lang: str = "en"):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# -------------------
# User input UI
# -------------------
st.markdown("### Chat")
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Ask me anything:", key="user_input_field")
with col2:
    if st.button("Send"):
        pass  # handled below

if st.session_state.get("user_input_field"):
    raw = st.session_state.user_input_field.strip()
    if raw:
        st.session_state.user_input_field = ""  # clear box
        prompt_parts = [raw]
        if upload_context:
            prompt_parts.append("\n\nExtra context:\n" + upload_context[:5000])
        prompt_text = "\n\n".join(prompt_parts)

        add_message("user", raw)

        # Get Wikipedia result
        wiki_summary, wiki_url = get_wikipedia_summary(raw, sentences=wiki_sentences)

        # Persona effect: simple style tweak
        if persona == "Friendly":
            wiki_summary = f"Here's what I found 😊:\n\n{wiki_summary}"
        elif persona == "Formal":
            wiki_summary = f"According to Wikipedia:\n\n{wiki_summary}"
        elif persona == "Concise":
            wiki_summary = wiki_summary.strip().split(".")[0] + "."

        meta = {"wiki_url": wiki_url} if wiki_url else {}
        add_message("bot", wiki_summary, meta=meta)

# -------------------
# Display conversation
# -------------------
st.markdown("---")
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
        if msg.get("meta", {}).get("wiki_url"):
            st.markdown(f"[Read more on Wikipedia]({msg['meta']['wiki_url']})")
        if voice_enabled:
            if st.button("🔊 Play Voice", key=f"voice_{i}"):
                try:
                    audio_bytes = text_to_speech_bytes(msg["content"], lang=voice_lang)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error(f"Voice error: {e}")

# -------------------
# Transcript controls
# -------------------
st.markdown("---")
if st.button("Download transcript"):
    txt = ""
    for m in st.session_state.messages:
        prefix = "You:" if m["role"] == "user" else "Bot:"
        txt += f"{prefix} {m['content']}\n\n"
    st.download_button(
        "Click to download",
        data=txt,
        file_name=f"chat_transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
