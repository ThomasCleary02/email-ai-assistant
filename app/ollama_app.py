import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
import os
import template

# Ollama settings from environment variables
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Initialize the Ollama LLM
@st.cache_resource
def get_ollama_llm():
    return OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

# Create email generation prompt templates
def create_new_email_prompt():
    template_text = """
    Write a single professional email with the following details:

    Content/Purpose: {content}
    Tone: {tone}

    Provide exactly one email with both a subject line and the email body.
    """
    return PromptTemplate(template=template_text, input_variables=["content", "tone"])

def create_email_reply_prompt():
    template_text = """
    Write a reply to the following email:

    Original Email: {original_email}

    Your reply should communicate this message:
    {message}

    It should also be in this tone: {tone}
    """
    return PromptTemplate(template=template_text, input_variables=["original_email", "message", "tone"])

# Check if Ollama is running
def is_ollama_available():
    try:
        llm = get_ollama_llm()
        llm.invoke("Test connection")
        st.session_state.llm = llm
        st.session_state.connected = True
        return True
    except Exception as e:
        st.session_state.connected = False
        st.warning("Could not connect to Ollama. Is it running?")
        return False

# Function to generate a new email
def generate_email(content, tone):
    prompt = create_new_email_prompt()
    chain = prompt | st.session_state.llm
    result = chain.invoke({"content": content, "tone": tone})
    return result

# Function to generate a reply
def generate_reply(original_email, message, tone):
    prompt = create_email_reply_prompt()
    chain = prompt | st.session_state.llm
    result = chain.invoke({"original_email": original_email, "message": message, "tone": tone})
    return result

def main():
    # Set up the page
    template.setup_page("Email Assistant Powered by Ollama")
    
    # Render the header with model info
    model_info = f"**Model:** `{OLLAMA_MODEL}`  \n**URL:** `{OLLAMA_BASE_URL}`"
    template.render_header("Email Writing Assistant (Ollama)", model_info)
    
    # Check connection to Ollama
    is_ollama_available()
    
    # Render the main email interface
    template.render_email_interface(
        generate_email_fn=generate_email,
        generate_reply_fn=generate_reply,
        connection_check_fn=lambda: st.session_state.get("connected", False)
    )
    
    # Render the footer
    template.render_footer()

if __name__ == "__main__":
    main()