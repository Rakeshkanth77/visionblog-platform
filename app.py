import streamlit as st
from PIL import Image

st.title("Welcome to Multi Model VisionBlog Generation Platform")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption= 'Uploaded Image.',  use_container_width=True)

st.sidebar.header('Customization Options')
style = st.sidebar.selectbox('Blog Style', ['Casual', 'Formal', 'Informative'])
tone = st.sidebar.selectbox('Tone', ['Neutral', 'Enthusiastic', 'Formal'])
Length = st.sidebar.slider('Blog Length', 100, 1000, 300)

st.write(f" Selected Style: {style} , Tone: {tone} , Length: {Length} words ")

from image_processor import ImageProcessor

if uploaded_file:
    if ImageProcessor.validate(uploaded_file):
        preprocessed_image = ImageProcessor.preprocess(uploaded_file)
        st.session_state.preprocessed_image = preprocessed_image
        st.success("Image processed successfully!")

    else: 
        st.error("Invalid image file. Please upload a valid JPG or PNG image, less than 5MB.")

