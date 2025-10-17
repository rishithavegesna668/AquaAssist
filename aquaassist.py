import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
from datetime import datetime
from gtts import gTTS
import tempfile

# Optional: Speech Recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except:
    SR_AVAILABLE = False

st.set_page_config(page_title="AquaAssist", layout="wide", page_icon="🐟")
st.title("🌊 AquaAssist - AI Pond Water Quality Checker")

MODEL_FILE = "aqua_model.pkl"
HISTORY_FILE = "pond_history.csv"

# Ensure model exists
if not os.path.exists(MODEL_FILE):
    st.error("Model not found. Please run train_model.py first.")
else:
    model = joblib.load(MODEL_FILE)

# Create history file if missing
if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["timestamp","pH","salinity","DO","ammonia","prediction"]).to_csv(HISTORY_FILE, index=False)

st.sidebar.header("🎤 Voice or Manual Input")

ph = st.sidebar.slider("pH Level", 4.0, 9.0, 7.0, 0.1)
salinity = st.sidebar.slider("Salinity (ppt)", 5, 40, 15, 1)
do = st.sidebar.slider("Dissolved Oxygen (mg/L)", 2.0, 10.0, 6.0, 0.1)
ammonia = st.sidebar.slider("Ammonia (ppm)", 0.0, 2.0, 0.3, 0.01)

if SR_AVAILABLE:
    if st.sidebar.button("🎙️ Voice Input (English)"):
        recognizer = sr.Recognizer()
        st.sidebar.info("Say: 'pH seven, salinity twenty, oxygen five, ammonia point five'")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            st.sidebar.success(f"Recognized: {text}")
        except:
            st.sidebar.warning("Voice not recognized. Try again.")
else:
    st.sidebar.warning("SpeechRecognition not installed.")

if st.button("🔮 Predict Water Quality"):
    df = pd.DataFrame([[ph, salinity, do, ammonia]], columns=['pH','salinity','DO','ammonia'])
    prediction = model.predict(df)[0]

    if prediction == "Safe":
        st.success("✅ Water Quality: Safe")
        suggestion = "నీటి నాణ్యత బాగుంది. ప్రస్తుత విధానాన్ని కొనసాగించండి."
    elif prediction == "Moderate":
        st.warning("⚠️ Water Quality: Moderate")
        suggestion = "నీటి ఆక్సిజన్ స్థాయి తగ్గింది. గాలి ప్రవాహం పెంచండి."
    else:
        st.error("🚫 Water Quality: Unsafe")
        suggestion = "నీరు కలుషితమైంది. వెంటనే నీటి మార్పు చేయండి."

    st.info(suggestion)

    # Telugu Voice Output
    try:
        tts = gTTS(text=suggestion, lang='te')
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        audio = open(tmp.name, 'rb').read()
        st.audio(audio, format='audio/mp3')
    except Exception as e:
        st.warning(f"Audio failed: {e}")

    # Plot graph
    fig, ax = plt.subplots()
    ax.bar(['pH', 'Salinity', 'DO', 'Ammonia'], [ph, salinity, do, ammonia],
           color=['#4CAF50', '#2196F3', '#FFC107', '#F44336'])
    ax.set_title("Pond Parameters")
    st.pyplot(fig)

    # Save history
    new_row = pd.DataFrame([[datetime.now(), ph, salinity, do, ammonia, prediction]],
                           columns=["timestamp","pH","salinity","DO","ammonia","prediction"])
    history = pd.read_csv(HISTORY_FILE)
    updated = pd.concat([history, new_row], ignore_index=True)
    updated.to_csv(HISTORY_FILE, index=False)
    st.success("📁 Saved to history.")
