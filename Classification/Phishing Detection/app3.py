import streamlit as st
import joblib
import numpy as np
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

model = joblib.load('phishing.pkl')


st.set_page_config(page_title="PhishShield", layout="centered")

def image_to_base64(img):
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="WEBP")
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode()


image = Image.open("Phishing.png")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/webp;base64,{image_to_base64(image)}');
        background-size: cover;
        background-position: center;
    }}
    .css-1d391kg {{
        background-color: #f0f0f0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; font-size: 50px; color: white;'>Welcome to PhishShield</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 25px; color: white;'>Your AI-powered defense against phishing attacks.</p>", unsafe_allow_html=True)

st.sidebar.header("Enter URL Features")
nb_www = st.sidebar.number_input("Number of 'www' in URL", min_value=0, max_value=10, value=1, step=1)
ratio_digits_url = st.sidebar.number_input("Ratio of Digits in URL", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
domain_in_title = st.sidebar.selectbox("Domain in Title?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
google_index = st.sidebar.selectbox("Indexed by Google?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
page_rank = st.sidebar.number_input("Page Rank", min_value=0.0, max_value=10.0, value=5.0, step=0.1)


if st.sidebar.button("Analyze URL"):
    input_data = np.array([[nb_www, ratio_digits_url, domain_in_title, google_index, page_rank]])
    
   
    prediction = model.predict(input_data)
    result = "Legitimate" if prediction[0] == 0 else "Phishing"

   
    color = "#4CAF50" if prediction[0] == 0 else "#FF5733"
    st.markdown(f"<h2 style='text-align: center; color: {color};'>This URL is classified as: {result}</h2>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h2 style='color: white; font-size: 35px;'>About the Model</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: white; font-weight: bold;'>PhishShield is powered by a Naïve Bayes classifier trained on key URL characteristics to detect phishing attempts.</p>", unsafe_allow_html=True)

st.markdown("<h3 style='color: white; font-size: 30px;'>Feature Description</h3>", unsafe_allow_html=True)
st.markdown("""
<p style='color: white; font-weight: bold;'>
- <b>Number of 'www' in URL:</b> Counts the occurrences of 'www' in the URL.<br>
- <b>Ratio of Digits in URL:</b> Measures the ratio of digits to the total length of the URL.<br>
- <b>Domain in Title?</b> Checks if the domain name is present in the title of the webpage.<br>
- <b>Indexed by Google?</b> Indicates if the URL is indexed by Google.<br>
- <b>Page Rank:</b> Represents the page rank of the URL.<br>
</p>
""", unsafe_allow_html=True)