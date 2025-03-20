import streamlit as st
from src.huggingface_client import HuggingFaceClient
from src.ollama_client import OllamaClient
import src.utils.template as template
import os


# Environment variables
HF_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Get HuggingFace API key from multiple sources
def get_hf_api_key():
    # Try environment variable first
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    # Try to get from Streamlit secrets if available
    try:
        if not api_key and hasattr(st, "secrets") and "huggingface" in st.secrets:
            api_key = st.secrets["huggingface"]["api_key"]
    except Exception:
        pass
        
    return api_key

# Initialize client based on selection
def initialize_client(client_type):
    if client_type == "HuggingFace":
        api_key = get_hf_api_key()
        if not api_key and "hf_api_key" in st.session_state:
            api_key = st.session_state.hf_api_key
            
        if not api_key:
            return None
            
        return HuggingFaceClient(api_key=api_key, model=HF_MODEL)
    else:  # Ollama
        try:
            return OllamaClient(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        except Exception:
            return None

# Function to check if client is available
def is_client_available(client):
    if not client:
        return False
        
    try:
        # Simple test prompt to check connection
        client.llm.invoke("Test connection")
        return True
    except Exception:
        return False

def main():
    # Set up the page
    template.setup_page("Unified Email Assistant")
    
    # App title
    st.title("📧 Email Writing Assistant")
    
    # Client selection
    if "client_type" not in st.session_state:
        st.session_state.client_type = "HuggingFace"
        
    client_type = st.sidebar.radio(
        "Select AI Provider:",
        ["HuggingFace", "Ollama"]
    )
    
    if client_type != st.session_state.client_type:
        st.session_state.client_type = client_type
        st.session_state.client = None
    
    # Display configuration options based on selected client
    with st.sidebar.expander("Configuration"):
        if client_type == "HuggingFace":
            st.write(f"Current Model: {HF_MODEL}")
            input_api_key = st.text_input(
                "HuggingFace API Key:",
                type="password",
                value="" if not get_hf_api_key() else "********"
            )
            
            if input_api_key and input_api_key != "********":
                st.session_state.hf_api_key = input_api_key
                st.success("API key set for this session!")
                st.session_state.client = None  # Reset client to force reinitialization
        else:  # Ollama
            st.write(f"Model: {OLLAMA_MODEL}")
            st.write(f"URL: {OLLAMA_BASE_URL}")
            st.write("Make sure Ollama is running locally")
    
    # Initialize client if needed
    if "client" not in st.session_state or st.session_state.client is None:
        st.session_state.client = initialize_client(client_type)
    
    # Check client connection
    client_available = is_client_available(st.session_state.client)
    
    if not client_available:
        if client_type == "HuggingFace":
            st.error("HuggingFace API key is missing or invalid. Please check your configuration.")
        else:
            st.error(f"Could not connect to Ollama. Is it running?\nTry running 'ollama pull {OLLAMA_MODEL}'")
    else:
        # Show model info
        client_info = st.session_state.client.get_model_info()
        st.markdown(client_info)
        
        # Main application UI
        tab1, tab2 = st.tabs(["Draft New Email", "Generate Reply"])
        
        tone_options = ["Professional", "Friendly", "Formal", "Persuasive", "Concise"]
        
        with tab1:
            st.header("Create a New Email")
            
            email_content = st.text_area("Enter the main content or purpose of your email:", height=150)
            selected_tone = st.selectbox("Select tone:", tone_options, index=0, key="new_tone")
            
            if st.button("Generate Email", key="generate_new"):
                if email_content:
                    with st.spinner("Drafting your email..."):
                        result = st.session_state.client.generate_email(email_content, selected_tone)
                        
                        st.subheader("Generated Email")
                        st.text_area("Copy your email:", result, height=300)
                        st.success("Email drafted successfully!")
                else:
                    st.error("Please enter email content.")
        
        with tab2:
            st.header("Reply to an Email")
            
            original_email = st.text_area("Paste the email you're responding to:", height=150)
            response_content = st.text_area("What would you like to communicate in response:", height=100)
            reply_tone = st.selectbox("Select tone for your reply:", tone_options, index=0, key="reply_tone")
            
            if st.button("Generate Reply", key="generate_reply"):
                if original_email:
                    with st.spinner("Drafting your reply..."):
                        result = st.session_state.client.generate_reply(original_email, response_content, reply_tone)
                        
                        st.subheader("Generated Reply")
                        st.text_area("Copy your reply:", result, height=300)
                        st.success("Reply drafted successfully!")
                else:
                    st.error("Please paste the original email.")
    
    # Footer
    st.markdown("---")
    st.markdown("Email Assistant - Built with Streamlit and AI")

if __name__ == "__main__":
    main()