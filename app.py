import streamlit as st
from PIL import Image

st.title("Welcome to Multi Model VisionBlog Generation Platform")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', width='stretch')

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

user_prompt = st.text_input("Blog Topic/Prompt (e.g., 'Describe this scene')")

if st.button("Generate Blog") and 'preprocessed_image' in st.session_state:
    with st.spinner("Generating..."):
        api_key = "euri-5cd3ca21b0a6363bd776ef0340d2457d9d11d4af3c46dda391134d95ae793624"
        generator = AIGenerator(api_key=api_key)
        raw_blog = generator.generate_blog(
            st.session_state.preprocessed_image, 
            user_prompt, 
            style, 
            tone, 
            Length
        )
        st.session_state.raw_blog = raw_blog
        st.markdown(raw_blog)

from blog_formatter import BlogFormatter

if 'raw_blog' in st.session_state:
    md, html = BlogFormatter.format(st.session_state.raw_blog, st.session_state.preprocessed_image)
    st.subheader("Markdown Preview")
    st.code(md, language='markdown')

    # Download
    st.download_button("Download Markdown", md, "blog.md", "text/markdown")  # Core Feature
    st.download_button("Download HTML", html, "blog.html", "text/html")


if 'raw_blog' in st.session_state:
    edited_blog = st.text_area("Edit Content", st.session_state.raw_blog, height=300)  # User Story 3
    if st.button("Update"):
        st.session_state.raw_blog = edited_blog
        st.rerun()  # Refresh preview
