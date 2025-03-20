import streamlit as st

def setup_page(title, icon="📧"):
    """Set up the page configuration with title and icon"""
    st.set_page_config(page_title=title, page_icon=icon)

def render_header(title, model_info):
    """Render the app header with title and model information"""
    st.title(f"📧 {title}")
    st.markdown(model_info)
    
def render_footer():
    """Render the app footer"""
    st.markdown("---")
    st.markdown("Email Assistant - Built with Streamlit and AI")

def render_email_interface(generate_email_fn, generate_reply_fn, connection_check_fn=None):
    """
    Render the main email interface with tabs
    
    Parameters:
    - generate_email_fn: Function to generate a new email
    - generate_reply_fn: Function to generate a reply to an email
    - connection_check_fn: Optional function to check connection status
    """
    tab1, tab2 = st.tabs(["Draft New Email", "Generate Reply"])
    
    tone_options = ["Professional", "Friendly", "Formal", "Persuasive", "Concise"]
    
    # Check connection status if a function is provided
    is_connected = True
    if connection_check_fn:
        is_connected = connection_check_fn()
    
    with tab1:
        st.header("Create a New Email")
        
        email_content = st.text_area("Enter the main content or purpose of your email:", height=150)
        selected_tone = st.selectbox("Select tone:", tone_options, index=0, key="new_tone")
        
        if st.button("Generate Email", key="generate_new"):
            if not is_connected:
                st.error("Connection error: Please check your settings.")
            elif email_content:
                with st.spinner("Drafting your email..."):
                    result = generate_email_fn(email_content, selected_tone)
                    
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
            if not is_connected:
                st.error("Connection error: Please check your settings.")
            elif original_email:
                with st.spinner("Drafting your reply..."):
                    result = generate_reply_fn(original_email, response_content, reply_tone)
                    
                    st.subheader("Generated Reply")
                    st.text_area("Copy your reply:", result, height=300)
                    st.success("Reply drafted successfully!")
            else:
                st.error("Please paste the original email.")