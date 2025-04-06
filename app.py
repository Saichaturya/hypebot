import streamlit as st
from transformers import pipeline
from PIL import Image

# Load a text generation pipeline (using a lightweight model)
generator = pipeline("text-generation", model="distilgpt2")

st.set_page_config(page_title="🚀 HypeBot: Startup Hype Generator", layout="centered")
st.title("🚀 HypeBot: AI-Powered Startup Hype Generator")

st.markdown("Generate killer startup pitches, taglines, social media posts, and more!")

# Image uploader
uploaded_image = st.file_uploader("Upload a logo or image (optional)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    st.image(Image.open(uploaded_image), use_column_width=True)

# User inputs
startup_name = st.text_input("Startup Name")
description = st.text_area("Brief Description of Your Startup")
audience = st.text_input("Target Audience", value="General Public")

content_type = st.selectbox("Content Type", ["Elevator Pitch", "Tagline", "Social Media Post"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Funny", "Bold"])
num_variations = st.slider("Number of Variations", 1, 5, 1)

# Generate button
if st.button("Generate"):
    if not startup_name or not description:
        st.warning("Please fill in all required fields.")
    else:
        with st.spinner("Generating hype content..."):
            for i in range(num_variations):
                prompt = f"Create a {tone.lower()} {content_type.lower()} for a startup called {startup_name}. It is {description}. Target audience: {audience}.\n"

                output = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]

                st.subheader(f"Variation {i + 1}")
                st.write(output.strip())
