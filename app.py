from gtts import gTTS
import streamlit as st

# Text to speech
tts = gTTS(text="Predicted water quality is good", lang='en')
tts.save("output.mp3")

# Play in Streamlit
st.audio("output.mp3")
