import streamlit as st
import openai
from fpdf import FPDF

# Set OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="HypeBot 🚀", layout="centered")
st.title("🚀 HypeBot: AI-Powered Startup Hype Generator")
st.write("Generate killer startup pitches, taglines, social media posts, and more!")

# Optional logo/image upload
uploaded_file = st.file_uploader("Upload a logo or image (optional)", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, width=200)

# Inputs
startup_name = st.text_input("Startup Name")
description = st.text_area("Brief Description of Your Startup")
audience = st.selectbox("Target Audience", ["General Public", "Investors", "Developers", "Students", "Businesses"])
content_type = st.selectbox("Content Type", ["Elevator Pitch", "Tagline", "Social Media Post", "Marketing Copy"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Bold", "Witty", "Inspirational"])
num_variations = st.slider("Number of Variations", 1, 5, 1)

# Generate
responses = []
if st.button("Generate ✨"):
    if not startup_name or not description:
        st.warning("Please fill out the required fields.")
    else:
        prompt = (
            f"Generate a {tone.lower()} {content_type.lower()} for a startup called '{startup_name}'. "
            f"Here's the description: {description}. "
            f"The target audience is: {audience}."
        )

        with st.spinner("Generating content..."):
            try:
                for _ in range(num_variations):
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=200
                    )
                    responses.append(response.choices[0].message["content"])

                st.subheader("💡 Your Generated Hype:")
                for i, res in enumerate(responses, 1):
                    st.markdown(f"**Variation {i}:**")
                    st.success(res)

            except Exception as e:
                st.error(f"Error: {e}")

# Export as PDF
if responses and st.button("Download as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, res in enumerate(responses, 1):
        pdf.multi_cell(0, 10, f"Variation {i}:\n{res}\n")
    pdf_file = "hypebot_output.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name=pdf_file, mime="application/pdf")

# Copy to clipboard workaround (textarea)
if responses:
    st.text_area("📋 Copy First Variation:", responses[0], height=150)
