import streamlit as st
import joblib
import os
from gtts import gTTS
import plotly.graph_objects as go
import io
import base64

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(page_title="🌊 AquaAssist", layout="wide")
st.title("🎤 Aquaassist")

# ------------------------------
# Load ML model
# ------------------------------
model_path = "model/aqua_model.pkl"
if not os.path.exists(model_path):
    st.error("ML model not found! Place your model in model/aqua_model.pkl")
    st.stop()

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.markdown("---")

# ------------------------------
# Columns: Left sliders, Right graph/output
# ------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**pH Level**\n\n4.00\n9.00")
    ph = st.slider("", 4.0, 9.0, step=0.1)

    st.markdown("**Salinity (ppt)**\n\n5\n40")
    salinity = st.slider("", 5, 40, step=1)

    st.markdown("**Dissolved Oxygen (mg/L)**\n\n2.00\n10.00")
    do = st.slider("", 2.0, 10.0, step=0.1)

    st.markdown("**Ammonia (ppm)**\n\n0.00\n2.00")
    ammonia = st.slider("", 0.0, 2.0, step=0.01)

with col2:
    parameters = ["pH", "Salinity", "DO", "Ammonia"]
    values = [ph, salinity, do, ammonia]

    # Initial graph
    fig = go.Figure(
        data=[go.Bar(
            x=parameters, y=values,
            text=values, textposition='auto',
            marker_color='royalblue'
        )]
    )
    fig.update_layout(title_text="Current Pond Parameters",
                      yaxis_title="Value",
                      xaxis_title="Parameter")
    st.plotly_chart(fig, use_container_width=True)

    # Prediction button
    if st.button("🌊 AquaAssist - AI Pond Water Quality Checker"):
        try:
            input_data = [[ph, salinity, do, ammonia]]
            prediction = model.predict(input_data)[0]

            # Display prediction + Telugu message
            telugu_msg = "నీటి నాణ్యత బాగుంది. ప్రస్తుత విధానాన్ని కొనసాగించండి."
            st.markdown(f"✅ **Water Quality: {prediction}**")
            st.markdown(telugu_msg)

            # History counter
            if "history" not in st.session_state:
                st.session_state.history = 0
            st.session_state.history += 1
            st.markdown(f"{st.session_state.history}")
            st.markdown("📁 Saved to history.")

            # ------------------------------
            # Text-to-Speech (auto-play) English + Telugu
            # ------------------------------
            def tts_autoplay(text, lang):
                tts = gTTS(text=text, lang=lang)
                tts_bytes = io.BytesIO()
                tts.write_to_fp(tts_bytes)
                tts_bytes.seek(0)
                b64_audio = base64.b64encode(tts_bytes.read()).decode()
                st.markdown(f"""
                <audio autoplay="true">
                  <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
                """, unsafe_allow_html=True)

            tts_autoplay(f"The predicted water quality is {prediction}", "en")
            tts_autoplay(telugu_msg, "te")

            # Update graph color after prediction
            fig = go.Figure(
                data=[go.Bar(
                    x=parameters,
                    y=values,
                    text=values,
                    textposition='auto',
                    marker_color='green' if prediction.lower()=='safe' else 'red'
                )]
            )
            fig.update_layout(title_text="Current Pond Parameters",
                              yaxis_title="Value",
                              xaxis_title="Parameter")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")
