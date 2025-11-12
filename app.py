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

from ai_generator import AIGenerator
import os
user_prompt = st.text_input("Blog Topic/Prompt (e.g., 'Describe this scene')")  # User input

if st.button("Generate Blog") and 'processed_image' in st.session_state:
    with st.spinner("Generating..."):  # UX (Goal 2)
        generator = AIGenerator(api_key=os.getenv('euri-c243bba3cbdc9b7bb96b5c1f8ebbd74fe717da1138b22baf62ad0c9e2dd604d6'))
        raw_blog = generator.generate_blog(
            st.session_state.processed_image, user_prompt, style, tone, Length
        )
        st.session_state.raw_blog = raw_blog
        st.markdown(raw_blog)  # Preview (User Story 3)


from blog_formatter import BlogFormatter

if "raw_blog" in st.session_state and 'processed_image' in st.session_state:
    md, html = BlogFormatter.format(
        st.session_state.raw_blog, st.session_state.processed_image
    )
    st.subheader("Formatted Blog Preview")
    st.code(md, language = 'markdown')




