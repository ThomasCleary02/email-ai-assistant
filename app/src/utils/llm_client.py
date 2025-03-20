from langchain.prompts import PromptTemplate
from abc import ABC

class LLMClient(ABC):

    def __init__(self, model):
        self.model = model
    
    def generate_email(self, content, tone):
        prompt = self.get_new_email_prompt()
        chain = prompt | self.llm
        result = chain.invoke({"content": content, "tone": tone})
        return result
    
    def generate_reply(self, original_email, message, tone):
        prompt = self.get_new_reply_prompt()
        chain = prompt | self.llm
        result = chain.invoke({"original_email": original_email, "message": message, "tone": tone})
        return result
    
    def get_model_info(self):
        """Get information about the model being used."""
        return f"**Model:** `{self.model}`"
    
    def get_new_email_prompt(self) -> PromptTemplate:
        template = """
        Write a single professional email with the following details:

        Content/Purpose: {content}
        Tone: {tone}

        Provide exactly one email with both a subject line and the email body.
        """
        return PromptTemplate(template=template, input_variables=["content", "tone"])
    
    def get_new_reply_prompt(self) -> PromptTemplate:
        template = """
        Write a reply to the following email:

        Original Email: {original_email}

        Your reply should communicate this message:
        {message}

        It should also be in this tone: {tone}
        """
        return PromptTemplate(template=template, input_variables=["original_email", "message", "tone"])