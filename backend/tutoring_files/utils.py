import os
from google import genai

CLIENT = genai.Client('GOOGLE_API_KEY')
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

def make_persistent(prompt, input_path, output_path):
    # Uses prompt and input_file to build persistent output_file to save prompt
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        in_file = CLIENT.files.upload(file=input_path)
        output = prompt_pdf_gemini(prompt, in_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
    return output_path
