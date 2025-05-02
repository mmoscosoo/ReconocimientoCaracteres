import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os

st.set_page_config(page_title="Texto a Voz - OCR", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #2F4F4F;
        color: #F0E68C;
    }

    h1 {
        color: #FFFF00 !important;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 2.5em;
    }

    .stButton > button, .stCameraInput, .stRadio > div {
        background-color: #4B0082 !important;
        color: #F0E68C !important;
        border-radius: 8px;
        border: 1px solid #F0E68C;
        font-weight: bold;
    }

    .stSidebar {
        background-color: #1E1E1E !important;
    }

    .stSidebar div, .stSidebar label, .stSidebar span {
        color: #F0E68C !important;
    }

    .css-1offfwp, .css-1aumxhk {
        color: #F0E68C !important;
    }

    .stMarkdown {
        font-family: 'Georgia', serif;
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Transforma tu Imagen en Texto y Voz")

st.markdown("Captura una imagen que contenga texto y observa cómo lo convertimos a texto en pantalla y a audio.")

img_file_buffer = st.camera_input("¡Toma una foto ahora!")

with st.sidebar:
    apply_filter = st.radio("¿Quieres aplicar un filtro a la imagen?", ('Sí', 'No'))

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if apply_filter == 'Sí':
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    st.image(img_rgb, caption="Imagen procesada", use_column_width=True)

    extracted_text = pytesseract.image_to_string(img_rgb)
    st.subheader("Texto detectado:")
    st.write(extracted_text)

    if extracted_text.strip() != "":
        tts = gTTS(extracted_text, lang='es')
        audio_path = "audio_output.mp3"
        tts.save(audio_path)

        st.subheader("Escuchar el texto detectado:")
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        audio_file.close()
        os.remove(audio_path)
    else:
        st.error("No se pudo detectar texto en la imagen. Intenta con una imagen más clara.")
