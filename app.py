import streamlit as st
import joblib
import os
from gtts import gTTS
import plotly.graph_objects as go

st.set_page_config(page_title="🌊 AquaAssist", layout="wide")
st.title("🎤 Voice or Manual Input")

# ------------------------------
# Load ML Model
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
# Columns: Left for sliders, Right for graph + output
# ------------------------------
col1, col2 = st.columns([1, 2])  # Left 1/3, Right 2/3

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

    # Show initial graph
    fig = go.Figure(
        data=[go.Bar(x=parameters, y=values, text=values, textposition='auto', marker_color='royalblue')]
    )
    fig.update_layout(title_text="Current Pond Parameters", yaxis_title="Value", xaxis_title="Parameter")
    st.plotly_chart(fig, use_container_width=True)

    # Prediction button
    if st.button("🌊 AquaAssist - AI Pond Water Quality Checker"):
        try:
            input_data = [[ph, salinity, do, ammonia]]
            prediction = model.predict(input_data)[0]

            st.markdown(f"✅ **Water Quality: {prediction}**")
            st.markdown("నీటి నాణ్యత బాగుంది. ప్రస్తుత విధానాన్ని కొనసాగించండి.")

            # History counter
            if "history" not in st.session_state:
                st.session_state.history = 0
            st.session_state.history += 1

            st.markdown(f"{st.session_state.history}")
            st.markdown("📁 Saved to history.")

            # Text-to-speech
            tts_text = f"The predicted water quality is {prediction}"
            tts = gTTS(text=tts_text, lang='en')
            tts.save("tts_output.mp3")
            st.audio("tts_output.mp3")

            # Update graph colors after prediction
            fig = go.Figure(
                data=[go.Bar(
                    x=parameters,
                    y=values,
                    text=values,
                    textposition='auto',
                    marker_color='green' if prediction.lower()=='safe' else 'red'
                )]
            )
            fig.update_layout(title_text="Current Pond Parameters", yaxis_title="Value", xaxis_title="Parameter")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")
