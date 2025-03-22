import os
import google.generativeai as genai

# Configure the API key
# in bash: `export GEMINI_API_KEY=[key]`
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
genai.configure(api_key=GEMINI_API_KEY)

# Create the Generative Model instance
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "Write a short poem about technology and nature"
    result = generate_content(prompt)
    print(result)