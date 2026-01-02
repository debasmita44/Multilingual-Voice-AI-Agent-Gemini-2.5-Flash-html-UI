import os
import google.generativeai as genai


class LLMHandler:
    """
    Handles interaction with Google Gemini LLM
    """

    def __init__(self):
        # Fetch API key from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please set it in Hugging Face Space Settings → Repository secrets."
            )

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Initialize model once
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_response(self, user_input: str, language: str) -> str:
        """
        Generate AI response using Google Gemini

        Args:
            user_input (str): User's transcribed text
            language (str): Detected language code

        Returns:
            str: AI-generated response
        """
        try:
            language_instruction = f"Please respond in {language} language."

            prompt = f"""
{language_instruction}

User message:
{user_input}

Provide a helpful, natural, and conversational response.
"""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"Error generating response: {e}")
            return (
                "I'm sorry, I encountered an error while processing your request."
            )
