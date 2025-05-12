import streamlit as st
from openai import OpenAI
import os

# Page configuration
st.set_page_config(page_title="OpenAI Assistant", layout="centered")

st.title("🤖 OpenAI Assistant")
st.markdown("Enter your question, and the OpenAI API will provide an answer.")

# Sidebar configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

model = st.sidebar.selectbox(
    "Select OpenAI model",
    options=["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
    index=0
)

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Main input
user_input = st.text_area("Enter your question:", placeholder="How do I make pizza margherita?")

response_format = st.radio("Response format:", options=["Full text", "Bullet points", "Numbered list"])

# Submit
if st.button("Generate Response") and user_input and api_key:
    st.markdown("#### Response:")

    # Format the prompt
    system_prompt = "You are a helpful assistant."
    user_prompt = user_input
    if response_format == "Bullet points":
        user_prompt += "\n\nPlease respond in bullet points."
    elif response_format == "Numbered list":
        user_prompt += "\n\nPlease respond in numbered list."

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)

        # Send request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )

        # Display
        st.success(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption("This app uses the OpenAI API to generate responses to your questions.")
