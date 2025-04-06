import streamlit as st
from transformers import pipeline

# Load the GPT-2 model
generator = pipeline("text-generation", model="distilgpt2")

st.set_page_config(page_title="HypeBot 🚀", layout="centered")
st.title("🚀 HypeBot: AI-Powered Startup Hype Generator")
st.caption("Create startup taglines, pitches, social posts & more using AI!")

# Upload image/logo
logo = st.file_uploader("Upload a logo or image (optional)", type=["png", "jpg", "jpeg"])
if logo:
    st.image(logo, width=200)

# Input fields
name = st.text_input("Startup Name")
desc = st.text_area("Brief Description of Your Startup")
audience = st.text_input("Target Audience")
content_type = st.selectbox("Content Type", ["Elevator Pitch", "Tagline", "Social Post"])
tone = st.selectbox("Tone", ["Professional", "Casual", "Funny", "Inspirational"])
num_variations = st.slider("Number of Variations", 1, 5, 1)

# Generate button
if st.button("Generate 🚀"):
    if not name or not desc or not audience:
        st.warning("Please fill out all required fields.")
    else:
        prompt = f"Generate a {tone.lower()} {content_type.lower()} for a startup named {name}, which is about {desc}. The target audience is {audience}."

        results = generator(prompt, max_length=100, num_return_sequences=num_variations, do_sample=True, temperature=0.9)

        st.subheader("Generated Content:")
        for i, result in enumerate(results, 1):
            st.markdown(f"**Variation {i}:**")
            st.success(result['generated_text'].strip())
