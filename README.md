# 🌊 AquaAssist - AI Pond Water Quality Checker

### Description
AquaAssist is a simple ML-powered tool for aquaculture farmers.  
Farmers can input pond parameters like pH, salinity, dissolved oxygen, and ammonia — the system predicts water safety and gives Telugu audio advice.

---

### 🎯 Features
- Machine Learning model (Random Forest)
- Streamlit web interface
- Telugu voice output (Text-to-Speech)
- Optional English voice input (SpeechRecognition)
- Auto data logging & visualization
- Simple CSV-based dataset (expandable)

---

### ⚙️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python (scikit-learn)
- **Audio:** gTTS, SpeechRecognition
- **Dataset:** CSV-based local data

---

### 🧠 Model Training
```bash
python train_model.py
