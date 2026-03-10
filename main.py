import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import pandas as pd
import io
from processor import DocumentProcessor
from database import init_db, save_document_data, get_all_documents

# 1. INITIALIZE SYSTEM
init_db()

@st.cache_resource
def load_tools():
    # EasyOCR for text detection + Gemini 2.0 Pro for intelligence
    return easyocr.Reader(['en']), DocumentProcessor()

reader, ai_brain = load_tools()

# 2. PAGE CONFIGURATION
st.set_page_config(page_title="SmartDMS | AI Life Manager", layout="wide", page_icon="🛡️")

# 3. SIDEBAR NAVIGATION
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/8132/8132530.png", width=80)
st.sidebar.title("SmartDMS Control")
menu = st.sidebar.radio("Navigate Modules", 
    ["📤 Upload & Process", "📈 Life Timeline View", "📑 One-Tap Tax Folder"])

# --- MODULE 1: UPLOAD & PROCESS ---
if menu == "📤 Upload & Process":
    st.title("🛡️ AI Document Ingestion")
    st.markdown("Scan any document to trigger **Medical**, **Legal**, or **Financial** intelligence.")

    uploaded_file = st.file_uploader("Drop image here...", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Scan Preview", width=350)

        if st.button("🚀 Analyze & Categorize"):
            with st.spinner("Gemini Pro is decoding document structure..."):
                # A. OCR Engine
                img_np = np.array(img)