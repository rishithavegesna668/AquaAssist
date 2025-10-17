import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import gdown
from gtts import gTTS

st.set_page_config(page_title="🌊 AquaAssist", layout="centered")
st.title("🎤 Voice or Manual Input")

# ------------------------------
# 1️⃣ Load ML Model Safely
# ------------------------------
model_path = "model/aqua_model.pkl"
if not os.path.exists(model_path):
    url = "https://drive.google.com/uc?id=YOUR_FILE_ID"  # Replace with your Google Drive file ID
    gdown.download(url, model_path, quiet=False)

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.markdown("---")

# ------------------------------
# 2️⃣ Input Sliders
# ------------------------------
st.subheader("pH Level")
ph = st.slider("", min_value=4.0, max_value=9.0, step=0.1)

st.subheader("Salinity (ppt)")
salinity = st.slider("", min_value=5, max_value=40, step=1)

st.subheader("Dissolved Oxygen (mg/L)")
do = st.slider("", min_value=2.0, max_value=10.0, step=0.1)

st.subheader("Ammonia (ppm)")
ammonia = st.slider("", min_value=0.0, max_value=2.0, step=0.01)

st.markdown("---")

# ------------------------------
# 3️⃣ Prediction
# ------------------------------
if st.button("Connecting 🌊"):
    try:
        input_data = [[ph, salinity, do, ammonia]]
        prediction = model.predict(input_data)[0]

        st.success(f"✅ Water Quality: {prediction}")
        st.info("నీటి నాణ్యత బాగుంది. ప్రస్తుత విధానాన్ని కొనసాగించండి.")

        # Save history counter
        if "history" not in st.session_state:
            st.session_state.history = 0
        st.session_state.history += 1

        st.write(st.session_state.history)
        st.write("📁 Saved to history.")

        # Text-to-speech
        tts_text = f"Predicted water quality is {prediction}"
        tts = gTTS(text=tts_text, lang='en')
        tts.save("tts_output.mp3")
        st.audio("tts_output.mp3")

    except Exception as e:
        st.error(f"Prediction error: {e}")

st.markdown("---")

# ------------------------------
# 4️⃣ Voice Upload (Optional)
# ------------------------------
st.subheader("Voice Input (Upload Audio)")
st.markdown("Record your voice saying e.g., 'pH seven, salinity twenty, oxygen five, ammonia point five' and upload the file.")
uploaded_file = st.file_uploader("Upload .wav or .mp3", type=["wav", "mp3"])
if uploaded_file is not None:
    st.info("Voice recognition available soon. Use sliders for now.")
