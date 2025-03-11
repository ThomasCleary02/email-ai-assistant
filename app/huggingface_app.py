import streamlit as st
from huggingface_hub import InferenceClient
import os
import template

# Get API key from environment first
api_key = os.getenv("HUGGINGFACE_API_KEY")

# Get model name from environment or use default
HF_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

# Try to get API key from Streamlit secrets if available and not in environment
try:
    if not api_key and hasattr(st, "secrets") and "huggingface" in st.secrets:
        api_key = st.secrets["huggingface"]["api_key"]
except Exception:
    pass

# Initialize HuggingFace client
@st.cache_resource
def get_hf_client():
    return InferenceClient(model=HF_MODEL, api_key=api_key)

# Function to generate a new email
def generate_email(content, tone):
    client = get_hf_client()
    
    prompt_text = f"""
    Write a professional email with the following details:

    Content/Purpose: {content}
    Tone: {tone}

    Provide both a subject line and the email body.
    """
    
    response = client.text_generation(prompt_text, max_new_tokens=500, temperature=0.7, do_sample=True, top_p=0.95)
    return response

# Function to generate a reply
def generate_reply(original_email, message, tone):
    client = get_hf_client()
    
    prompt_text = f"""
    Write a reply to the following email:

    Original Email: {original_email}

    Your reply should communicate this message:
    {message}

    It should also be in this tone: {tone}
    """
    
    response = client.text_generation(prompt_text, max_new_tokens=500, temperature=0.7, do_sample=True, top_p=0.95)
    return response

# Check API key
def is_api_key_set():
    return api_key is not None and api_key != ""

def main():
    # Set up the page
    template.setup_page("Email Assistant (HuggingFace)")
    
    # Render the header with model info
    model_info = f"**Connected to HuggingFace** \n**Current Model:** `{HF_MODEL}`"
    template.render_header("Email Writing Assistant (HuggingFace)", model_info)
    
    # API Key Input
    with st.expander("API Key Settings"):
        input_api_key = st.text_input("HuggingFace API Key (leave blank to use environment variable or secrets):", 
                                      type="password", 
                                      value="" if not api_key else "********")
        if input_api_key and input_api_key != "********":
            global api_key
            api_key = input_api_key
            st.success("API key set for this session!")
    
    # Render the main email interface
    template.render_email_interface(
        generate_email_fn=generate_email,
        generate_reply_fn=generate_reply,
        connection_check_fn=is_api_key_set
    )
    
    # Render the footer
    template.render_footer()

if __name__ == "__main__":
    main()