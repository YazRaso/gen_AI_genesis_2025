import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
CLIENT = genai.Client(api_key='AIzaSyAUWuyUe5Hicxeqz_xHNFMG-kgYOd32EvY')
MODEL = 'gemini-2.0-flash'

def prompt_gemini(prompt):
    # Sends prompt to Gemini
    try:
        response = CLIENT.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {str(e)}")

def prompt_pdf_gemini(prompt, pdf_client_file):
    # Sends prompt and pdf to Gemini
    try:
        response = CLIENT.models.generate_content(model=MODEL, contents=[prompt, pdf_client_file])
        return response.text
    except Exception as e:
        print(f"Error generating content: {str(e)}")