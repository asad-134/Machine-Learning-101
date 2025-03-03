import streamlit as st
import joblib
import numpy as np
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

# Load the saved model
model = joblib.load('gradient_boosting_model.pkl')

# Set the page configuration
st.set_page_config(page_title="Caronomics", layout="centered")

# Load the background image
def image_to_base64(img):
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="WEBP")
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode()

# Load your image for the background
image = Image.open("Car2.webp")

# Use CSS to set the background image and sidebar color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/webp;base64,{image_to_base64(image)}');
        background-size: cover;
        background-position: center;
    }}
    .css-1d391kg {{
        background-color: #f0f0f0;  /* Lighter grey color */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Add a stylish header with the desired text
st.markdown("<h1 style='text-align: center; font-size: 60px; color: white;'>Welcome to Caronomics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 30px; color: white;'>Where you unlock the true value of every ride.</p>", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Input Features")
engine_hp = st.sidebar.number_input("Engine HP", min_value=50.0, max_value=1000.0, value=200.0, step=10.0)
engine_cylinders = st.sidebar.number_input("Engine Cylinders", min_value=1, max_value=16, value=4, step=1)

# Predict button
if st.sidebar.button("Predict"):
    # Prepare input data
    input_data = np.array([[engine_hp, engine_cylinders]])
    
    # Make prediction
    prediction = model.predict(input_data)
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>Predicted MSRP: ${prediction[0]:,.2f}</h2>", unsafe_allow_html=True)

# Footer with model details and set the text color to white
st.markdown("---")

# Updated heading sizes for About the Model and Dataset Description
st.markdown("<h2 style='color: white; font-size: 40px;'>About the Model</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: white; font-weight: bold'>This model uses Gradient Boosting to predict the MSRP (Manufacturer's Suggested Retail Price) of a car based on its engine specifications.</p>", unsafe_allow_html=True)

st.markdown("<h3 style='color: white; font-size: 35px;'>Dataset Description</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: white; font-weight: bold;'>The dataset used for training includes features such as 'Engine HP', 'Engine Cylinders', and the target variable 'MSRP'.</p>", unsafe_allow_html=True)
