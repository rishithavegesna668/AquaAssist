import streamlit as st
import joblib
import gdown
import os

# Path to save model locally
model_path = "aqua_model.pkl"

# Download from Google Drive if not exists
if not os.path.exists(model_path):
    url = "https://drive.google.com/uc?id=FILE_ID"  # replace FILE_ID
    gdown.download(url, model_path, quiet=False)

# Load the model
model = joblib.load(model_path)
