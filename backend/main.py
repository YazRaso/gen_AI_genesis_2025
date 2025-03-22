import os
from google import genai
from google.genai import types

# Configure the API key
# in bash: `export GEMINI_API_KEY=[key]`
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
client = genai.Client(api_key='AIzaSyAUWuyUe5Hicxeqz_xHNFMG-kgYOd32EvY')

# Create the Generative Model instance
model = 'gemini-2.0-flash'

def generate_content(prompt):
    try:
        response = client.models.generate_content(model, prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

def get_content(learn_file):
    text = "You are a high school level tutor. Summarize the following content into easy to follow core concepts."
    try:
        response = client.models.generate_content(model=model, contents=[text, learn_file])
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Example usage
if __name__ == "__main__":
    file = client.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
    result = get_content(file)
    print(result)
