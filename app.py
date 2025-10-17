import streamlit as st
import pandas as pd
import numpy as np
import joblib
from gtts import gTTS
import os
import speech_recognition as sr
from pydub import AudioSegment

# Load ML model
model = joblib.load("model/your_model.pkl")  # replace with your model path

st.title("🌊 AquaAssist - AI Pond Water Quality Checker")

st.subheader("Input Water Parameters")
ph = st.number_input("Enter pH value:")
temperature = st.number_input("Enter temperature (°C):")
dissolved_oxygen = st.number_input("Enter Dissolved Oxygen:")

# ML Prediction
if st.button("Predict Water Quality"):
    input_data = [[ph, temperature, dissolved_oxygen]]
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Water Quality: {prediction}")
    
    # Text-to-speech
    tts = gTTS(text=f"The predicted water quality is {prediction}", lang='en')
    tts.save("output.mp3")
    st.audio("output.mp3")

st.markdown("---")
st.subheader("Speech Recognition (Upload Audio File)")

uploaded_file = st.file_uploader("Upload your voice recording (.wav or .mp3)", type=["wav","mp3"])

if uploaded_file is not None:
    # Convert mp3 to wav if needed
    if uploaded_file.name.endswith(".mp3"):
        sound = AudioSegment.from_mp3(uploaded_file)
        sound.export("temp.wav", format="wav")
        audio_file = "temp.wav"
    else:
        audio_file = uploaded_file

    # Recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("You said:", text)
        except sr.UnknownValueError:
            st.write("Could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
