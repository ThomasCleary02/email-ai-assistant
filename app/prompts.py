

class Prompts():
    
    @staticmethod
    def get_new_email_prompt(content: str, tone: str):
        prompt = f"""
        Write a single professional email with the following details:

        Content/Purpose: {content}
        Tone: {tone}

        Provide exactly one email with both a subject line and the email body.

        """
        return prompt

    @staticmethod
    def get_new_reply_prompt(original_email: str, message: str, tone: str):
        prompt = f"""

        Write a reply to the following email:

        Original Email: {original_email}

        Your reply should communicate this message:
        {message}

        It should also be in this tone: {tone}
        """
        return prompt