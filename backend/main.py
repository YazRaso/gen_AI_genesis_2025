import os
from google import genai
from text_extract import extract_text

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
CLIENT = genai.Client(api_key='AIzaSyAUWuyUe5Hicxeqz_xHNFMG-kgYOd32EvY')
MODEL = 'gemini-2.0-flash'
SUMMARY_FILE = 'summary.txt'
MARKDOWN_FILE = 'lesson_md.md'

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

def make_summary(lesson_file, summary_file):
    prompt = "Summarize the following content into easy to follow core concepts in Spanish."
    summary = prompt_pdf_gemini(prompt, lesson_file)
    with open(summary_file, 'w') as f:
        f.write(summary)

def make_lesson_md(lesson_file, lesson_md_file):
    # PDF into persistent summary file
    prompt = "Convert PDF to markdown."
    lesson_md = prompt_pdf_gemini(prompt, lesson_file)
    with open(lesson_md_file, 'w') as f:
        f.write(lesson_md)

     

def reinforce_tutor(question, concepts):
    """
    Pass concepts file, tutor instruct, and student prompt
    """
    prompt =  "You are an encouraging and kind high school level tutor. These are the concepts the student is learning.\n\n"
    prompt += concepts
    prompt += f"\n\n{question}\n\n"       
    prompt +=  "Based on the student's question, can you highlight the concept that the student is struggling with and provide them with guidance. Give me the answer in Spasnish only"
    return prompt_gemini(prompt)

def main():
    """if not os.path.exists(MARKDOWN_FILE) or os.path.getsize(SUMMARY_FILE) == 0:
        file = CLIENT.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
        make_lesson_md(file, MARKDOWN_FILE)

    markdown = open(MARKDOWN_FILE, "r").read()
    print(markdown)
    return"""

    if not os.path.exists(MARKDOWN_FILE) or os.path.getsize(MARKDOWN_FILE) == 0:
        file = CLIENT.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
        make_lesson_md(file, MARKDOWN_FILE)

    summary = open(MARKDOWN_FILE, "r").read()

    question1 = "What is the difference between magnification and resolution in a microscope, and why is resolution more important for seeing fine details?"
    
    question2 = "How does the electron microscope differ from the light microscope in terms of function and limitations?"

    question3 = "Why is staining necessary when using a light microscope, and how does it affect the visibility of cell structures?"

    question4 = "How do diffusion, osmosis, and active transport differ in terms of energy use and direction of movement?"

    question5 = "Why do plant cells have both a cell membrane and a cell wall, and how do their functions differ?"

    question6 = "What is the significance of mitochondria in cells, and why do some cells have more mitochondria than others?"

    question7 = "How does the structure of specialized cells, such as nerve cells or muscle cells, relate to their function in the human body?"

    question8 = "Why are cells considered the basic unit of life according to cell theory, and how was this theory developed?"

    question9 = "What adaptations help increase the efficiency of diffusion in living organisms, and why is this important?"

    answer = reinforce_tutor(question1, summary)
    print(answer)



# Example usage
if __name__ == "__main__":
    main()


