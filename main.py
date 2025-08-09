import streamlit as st
import wikipedia
import requests
from gtts import gTTS
import io
import re
import base64

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(page_title="Motte", page_icon="🌸", layout="wide")

# -------------------
# CUSTOM CSS + JS FOR SAKURA + BACKGROUND MUSIC
# -------------------
sakura_js = """
<script src="https://cdn.jsdelivr.net/npm/sakura-js/dist/sakura.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    var sakura = new Sakura('body');
});
</script>
"""

bg_music_html = """
<audio autoplay loop>
  <source src="https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Podington_Bear/Daydream/Podington_Bear_-_Daydream.mp3" type="audio/mpeg">
</audio>
"""

st.markdown(sakura_js, unsafe_allow_html=True)
st.markdown(bg_music_html, unsafe_allow_html=True)

# -------------------
# SIDEBAR - ABOUT US
# -------------------
with st.sidebar:
    st.header("🌸 About Motte")
    st.write("""
    Motte is your friendly AI-powered chatbot that can answer anything —
    from history to quantum physics, from math problems to health info.
    Uses Wikipedia and WHO data for reliable answers.
    """)
    st.write("**Developer:** You 😎")
    st.write("**Version:** 1.0")
    st.markdown("---")
    st.write("**Quick Topics:**")
    if st.button("Mathematics"):
        st.session_state.query = "Mathematics"
    if st.button("Quantum Physics"):
        st.session_state.query = "Quantum physics"
    if st.button("Space Science"):
        st.session_state.query = "Space science"
    if st.button("Health"):
        st.session_state.query = "Health"

# -------------------
# FUNCTIONS
# -------------------
def fetch_wikipedia_info(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return None, None, None
        page = wikipedia.page(results[0], auto_suggest=False)
        summary = wikipedia.summary(results[0], sentences=3, auto_suggest=False)
        image_url = page.images[0] if page.images else None
        return summary, page.url, image_url
    except Exception as e:
        return f"Error: {e}", None, None

def fetch_who_info(query):
    try:
        # Example: placeholder WHO API call (replace with actual endpoint if available)
        # Here using a dummy WHO facts page as fallback
        url = f"https://www.who.int/news-room/fact-sheets/detail/{query.replace(' ', '-')}"
        r = requests.get(url)
        if r.status_code == 200:
            return f"WHO resource: {url}", url, None
        return None, None, None
    except:
        return None, None, None

def solve_math(expression):
    try:
        result = eval(expression)
        return f"The result is {result}", None, None
    except:
        return None, None, None

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    b64 = base64.b64encode(mp3_fp.read()).decode()
    audio_html = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# -------------------
# MAIN HEADER
# -------------------
st.markdown("<h1 style='text-align:center;'>🌸 Motte</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Ask anything to Motte</h3>", unsafe_allow_html=True)

# -------------------
# USER INPUT
# -------------------
if "query" not in st.session_state:
    st.session_state.query = ""

user_query = st.text_input("Type your question here:", value=st.session_state.query)
if user_query:
    st.session_state.query = ""
    
    # Decide source
    if re.match(r"^[0-9\+\-\*/\.\s]+$", user_query):
        answer, link, image = solve_math(user_query)
    elif any(word in user_query.lower() for word in ["health", "disease", "covid", "virus"]):
        answer, link, image = fetch_who_info(user_query)
        if not answer:
            answer, link, image = fetch_wikipedia_info(user_query)
    else:
        answer, link, image = fetch_wikipedia_info(user_query)

    # Show answer
    if answer:
        st.markdown(f"**Answer:** {answer}")
        if link:
            st.markdown(f"[Read More Here]({link})")
        if image:
            st.image(image, use_container_width=True)
        
        # Auto voice playback
        speak_text(answer)
    else:
        st.warning("Sorry, I couldn't find an answer.")
