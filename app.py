import streamlit as st
import pandas as pd
import numpy as np
import joblib
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import os

# Load your trained ML model
model = joblib.load("model/your_model.pkl")  # Replace with your model path

st.title("🌊 AquaAssist - AI Pond Water Quality Checker")

# --------------------------
# 1️⃣ Manual Input
# --------------------------
st.subheader("Manual Input")

ph = st.slider("pH Level", min_value=4.0, max_value=9.0, step=0.1)
salinity = st.slider("Salinity (ppt)", min_value=5, max_value=40, step=1)
dissolved_oxygen = st.slider("Dissolved Oxygen (mg/L)", min_value=2.0, max_value=10.0, step=0.1)
ammonia = st.slider("Ammonia (ppm)", min_value=0.0, max_value=2.0, step=0.01)

if st.button("Predict Water Quality (Manual)"):
    input_data = [[ph, salinity, dissolved_oxygen, ammonia]]
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Water Quality: {prediction}")
    
    # Text-to-speech
    tts = gTTS(text=f"The predicted water quality is {prediction}", lang='en')
    tts.save("output.mp3")
    st.audio("output.mp3")

st.markdown("---")

# --------------------------
# 2️⃣ Voice Input via File Upload
# --------------------------
st.subheader("Voice Input (Upload Audio)")

st.markdown("Record your voice saying something like: 'pH seven, salinity twenty, oxygen five, ammonia point five' and upload the file.")

uploaded_file = st.file_uploader("Upload your voice recording (.wav or .mp3)", type=["wav","mp3"])

if uploaded_file is not None:
    # Convert mp3 to wav if needed
    if uploaded_file.name.endswith(".mp3"):
        sound = AudioSegment.from_mp3(uploaded_file)
        sound.export("temp.wav", format="wav")
        audio_file = "temp.wav"
    else:
        audio_file = uploaded_file

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("You said:", text)
            
            # Optional: extract numbers from speech for prediction (if you have a parser)
            # Example: parse "pH seven, salinity twenty..." into float values
            # ph, salinity, dissolved_oxygen, ammonia = parse_numbers_from_text(text)
            # prediction = model.predict([[ph, salinity, dissolved_oxygen, ammonia]])[0]
            # st.success(f"Predicted Water Quality: {prediction}")
            
        except sr.UnknownValueError:
            st.write("Could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
