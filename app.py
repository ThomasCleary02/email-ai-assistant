import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from huggingface_hub import InferenceClient
import os

# Set page config
st.set_page_config(page_title="Email Assistant", page_icon="📧")

envkey = os.getenv("HUGGINGFACE_API_KEY")
api_key = envkey if envkey else st.secrets["huggingface"]["api_key"]

# Hugging Face model setup
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"  # Define Hugging Face model name here

# Initialize the LLM (Fallback to Hugging Face if Ollama is unavailable)
@st.cache_resource
def get_llm():
    if os.getenv("STREAMLIT_CLOUD"):  # Detects if running on Streamlit Cloud
        hf_client = InferenceClient(model=HF_MODEL, api_key=api_key)
        return hf_client
    try:
        llm = OllamaLLM(model="llama2", base_url="http://127.0.0.1:11434")
        llm.invoke("Test connection")  # Test Ollama
        return llm
    except Exception:
        hf_client = InferenceClient(api_key=api_key)
        return hf_client

# Create email generation prompt templates
def create_new_email_prompt():
    template = """
    Write a professional email with the following details:

    Content/Purpose: {content}
    Tone: {tone}

    Provide both a subject line and the email body.
    """
    return PromptTemplate(template=template, input_variables=["content", "tone"])

def create_email_reply_prompt():
    template = """
    Write a reply to the following email:

    Original Email: {original_email}

    Your reply should communicate this message:
    {message}

    It should also be in this tone: {tone}
    """
    return PromptTemplate(template=template, input_variables=["original_email", "message", "tone"])

# Function to generate text using the selected LLM
def generate_text(llm, prompt_data):
    if isinstance(llm, OllamaLLM):
        prompt = create_new_email_prompt() if "content" in prompt_data else create_email_reply_prompt()
        chain = prompt | llm
        return chain.invoke(prompt_data)
    else:
        # If using Hugging Face, format the prompt manually
        if "content" in prompt_data:
            prompt_text = f"""
            Write a professional email with the following details:

            Content/Purpose: {prompt_data['content']}
            Tone: {prompt_data['tone']}

            Provide both a subject line and the email body.
            """
        else:
            prompt_text = f"""
            Write a reply to the following email:

            Original Email: {prompt_data['original_email']}

            Your reply should communicate this message:
            {prompt_data['message']}

            It should also be in this tone: {prompt_data['tone']}
            """
            
        response = llm.text_generation(prompt_text, max_new_tokens=500, temperature=0.7)
        return response


# Main UI

# Display model and provider in UI
st.title("📧 Email Writing Assistant")

llm = get_llm()  # Load the LLM

# Extract model and provider dynamically
if isinstance(llm, OllamaLLM):
    model_name = llm.model
    provider = "Ollama"
else:
    model_name = HF_MODEL  # Hugging Face model name
    provider = "HuggingFace (SambaNova)"

st.markdown(f"**Current Model:** `{model_name}`  \n**Provider:** `{provider}`")

tab1, tab2 = st.tabs(["Draft New Email", "Generate Reply"])

with tab1:
    st.header("Create a New Email")

    email_content = st.text_area("Enter the main content or purpose of your email:", height=150)
    tone_options = ["Professional", "Friendly", "Formal", "Persuasive", "Concise"]
    selected_tone = st.selectbox("Select tone:", tone_options, index=0)

    if st.button("Generate Email", key="generate_new"):
        if email_content:
            with st.spinner("Drafting your email..."):
                prompt_data = {"content": email_content, "tone": selected_tone}
                result = generate_text(llm, prompt_data)

                st.subheader("Generated Email")
                st.text_area("Copy your email:", result, height=300)
                st.success("Email drafted successfully!")
        else:
            st.error("Please enter email content.")

with tab2:
    st.header("Reply to an Email")

    original_email = st.text_area("Paste the email you're responding to:", height=150)
    response_content = st.text_area("What would you like to communicate in response:", height=100)
    reply_tone = st.selectbox("Select tone for your reply:", tone_options, index=0)

    if st.button("Generate Reply", key="generate_reply"):
        if original_email:
            with st.spinner("Drafting your reply..."):
                prompt_data = {"original_email": original_email, "message": response_content, "tone": reply_tone}
                result = generate_text(llm, prompt_data)

                st.subheader("Generated Reply")
                st.text_area("Copy your reply:", result, height=300)
                st.success("Reply drafted successfully!")
        else:
            st.error("Please paste the original email.")

# Footer
st.markdown("---")
st.markdown("Email Assistant - Built with Streamlit, LangChain, and Ollama/Hugging Face")
