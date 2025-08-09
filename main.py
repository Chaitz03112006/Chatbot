import streamlit as st
import wikipedia
import math
import os

# ----------------- CONFIG -----------------
st.set_page_config(page_title="🌸 Motte Chatbot", layout="wide")

# ----------------- SIDEBAR: ABOUT US -----------------
st.sidebar.title("About Us")
st.sidebar.write("""
Welcome to **Motte Chatbot**! 🌸  
Your friendly multi-mode assistant that can:
- 📚 Search Wikipedia
- 🧮 Solve Math problems
- 🩺 Give health tips
- ⚛️ Explain quantum physics  

No external AI APIs — just pure Python magic!
""")

# ----------------- MAIN TITLE -----------------
st.markdown("<h1 style='text-align: center;'>🌸 Motte Chatbot 🌸</h1>", unsafe_allow_html=True)

# ----------------- STATIC FILES -----------------
# Ensure 'static' folder exists with these files
music_file = os.path.join("static", "background.mp3")
petal_image = os.path.join("static", "petal.png")

# Background Music
if os.path.exists(music_file):
    st.markdown(
        f"""
        <audio autoplay loop>
            <source src="{music_file}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# Petal Background
if os.path.exists(petal_image):
    st.markdown(
        f"""
        <style>
        body {{
            background-color: #ffe4e1;
            background-image: url("{petal_image}");
            background-repeat: repeat;
            background-size: 50px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------- MODE SELECTION -----------------
mode = st.radio(
    "Select Motte's Mode:",
    ["📚 Wikipedia", "🧮 Mathematics", "🩺 Health", "⚛️ Quantum Physics"],
    horizontal=True
)

# Mode Greetings
greetings = {
    "📚 Wikipedia": "📚 Motte Encyclopedia at your service.",
    "🧮 Mathematics": "🧮 Motte Calculator is ready for you.",
    "🩺 Health": "🩺 Motte Doctor is here to help.",
    "⚛️ Quantum Physics": "⚛️ Motte Quantum Lab activated."
}
st.markdown(f"**{greetings[mode]}**")

# ----------------- MAIN INPUT -----------------
user_input = st.text_input("Your question:")

# ----------------- MAIN LOGIC -----------------
if st.button("Ask Motte"):
    if mode == "📚 Wikipedia":
        try:
            summary = wikipedia.summary(user_input, sentences=3)
            page = wikipedia.page(user_input)
            st.write(summary)
            if page.images:
                st.image(page.images[0], width=300)
            st.markdown(f"[Read more on Wikipedia]({page.url})")
        except Exception as e:
            st.error("Topic not found or an error occurred. Try another.")

    elif mode == "🧮 Mathematics":
        try:
            result = eval(user_input, {"__builtins__": None}, math.__dict__)
            st.success(f"Result: {result}")
        except:
            st.error("Invalid math expression. Try again.")

    elif mode == "🩺 Health":
        health_db = {
            "fever": "You may have an infection or flu. Rest, drink fluids, and consult a doctor if symptoms persist.",
            "cold": "It might be a common cold. Drink warm liquids and rest well.",
            "headache": "Possible causes: stress, dehydration, or eye strain. Drink water and rest.",
            "stomach pain": "Might be indigestion. Avoid spicy food and drink warm water."
        }
        reply = None
        for key in health_db:
            if key in user_input.lower():
                reply = health_db[key]
                break
        st.info(reply if reply else "I don't have info on that symptom. Please consult a doctor.")

    elif mode == "⚛️ Quantum Physics":
        quantum_facts = {
            "superposition": "A particle can exist in multiple states at once until measured.",
            "entanglement": "Particles can be connected so that one's state instantly affects the other.",
            "quantum tunneling": "Particles can pass through barriers they normally couldn’t.",
            "wave-particle duality": "Quantum entities can act like particles and waves."
        }
        reply = quantum_facts.get(user_input.lower(), "That's a deep topic! Let me know a specific quantum term.")
        st.write(reply)
