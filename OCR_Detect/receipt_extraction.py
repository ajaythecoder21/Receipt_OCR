import cv2 as cv
import numpy as np
import easyocr
import streamlit as st
import pytesseract

from PIL import Image

st.write(""" 
# My first app
""")
file = st.file_uploader('Upload the image', type=['jpeg', 'pneg', 'png'])    

if file is not None:  
    #st.image(image) 
    pil_image = Image.open(file)
    st.image(pil_image, caption="Uploaded Image", use_column_width=True)

    try:
        text = pytesseract.image_to_string(pil_image)
        st.write(text)
    except pytesseract.TesseractError as e:
        st.error(f"Error during OCR: {e}")









