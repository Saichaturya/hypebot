import streamlit as st
from openai import OpenAI
import os

# Load OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="🚀 HypeBot: AI-Powered Startup Hype Generator")
st.title("🚀 HypeBot: AI-Powered Startup Hype Generator")
st.caption("Generate killer startup pitches, taglines, social media posts, and more!")

# Upload Logo/Image (optional)
uploaded_file = st.file_uploader(
    "Upload a logo or image (optional)", type=["png", "jpg", "jpeg"]
)

# Form Inputs
startup_name = st.text_input("Startup Name")
description = st.text_area("Brief Description of Your Startup")
target_audience = st.text_input("Target Audience")
content_type = st.selectbox("Content Type", ["Elevator Pitch", "Tagline", "Tweet", "Ad Copy"])
tone = st.selectbox("Tone", ["Professional", "Casual", "Funny", "Inspirational"])
variations = st.slider("Number of Variations", min_value=1, max_value=5, value=1)

# Prompt builder
def generate_prompt(name, desc, audience, ctype, tone):
    return f"""
Generate a {ctype.lower()} for a startup.
Startup Name: {name}
Description: {desc}
Target Audience: {audience}
Tone: {tone}
Provide only the output text.
"""

# Submit Button
if st.button("Generate"):
    if not (startup_name and description and target_audience):
        st.error("Please fill in all the fields.")
    else:
        with st.spinner("Generating hype content..."):
            messages = [
                {"role": "system", "content": "You are a creative startup content generator."},
                {"role": "user", "content": generate_prompt(startup_name, description, target_audience, content_type, tone)}
            ]
            outputs = []
            for _ in range(variations):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                )
                outputs.append(response.choices[0].message.content.strip())

        st.success("Here you go!")
        for i, out in enumerate(outputs, 1):
            st.markdown(f"### 🔹 Variation {i}")
            st.write(out)
