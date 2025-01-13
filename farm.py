import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key1 = os.getenv('api_key1')

# Streamlit page configuration
st.set_page_config(page_title="Vital Image Analytics", page_icon=":robot:")

# Configure Gemini API
if api_key1:
    genai.configure(api_key=api_key1)
else:
    st.error("API key is missing. Please check your .env file.")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """
You are an agriculture/horticulture specialist. Analyze the uploaded image and provide a report including:
1. Detailed analysis of the image.
2. Requirements for the crop's growth.
3. Recommendations and next steps for better yield.
4. Suggestions for fertilizers/nutrients with specific ratios.
5. Other compatible plants to grow alongside the crop.

If the image is not related to agriculture, respond with: "Please upload a valid image."
"""

# Streamlit UI
st.image("OIG2.jpeg", width=150)
st.title("AI 🤖 Agriculture Assistant 🌾🧑‍🌾👩‍🌾")
st.subheader("Analyze agricultural images for insights.")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=250, caption="Uploaded Image")

submit_button = st.button("Generate Analysis")

if submit_button:
    if not uploaded_file:
        st.error("No image uploaded. Please upload an image for analysis.")
    else:
        try:
            image_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
            prompt_parts = [image_parts[0], system_prompt]

            # Generating response
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro-latest",
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            response = model.generate_content(prompt_parts)

            st.title("Analysis Results")
            st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
