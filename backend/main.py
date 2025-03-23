import os
from google import genai
#from text_extract import extract_text
from gemini.utils import prompt_gemini, prompt_pdf_gemini


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
CLIENT = genai.Client(api_key='AIzaSyAUWuyUe5Hicxeqz_xHNFMG-kgYOd32EvY')
MODEL = 'gemini-2.0-flash'
SUMMARY_FILE = 'summary.txt'
MARKDOWN_FILE = 'lesson_md.md'

def make_summary(prompt, lesson_file, summary_file):
    # PDF into persistent summary file
    prompt = "Summarize the following content into easy to follow core concepts in Spanish."
    summary = prompt_pdf_gemini(prompt, lesson_file)
    with open(summary_file, 'w') as f:
        f.write(summary)

def make_lesson_md(lesson_file, lesson_md_file):
    # PDF into persistent summary file
    prompt = "Translate this to Spanish."
    lesson_md = prompt_pdf_gemini(prompt, lesson_file)
    with open(lesson_md_file, 'w') as f:
        f.write(lesson_md)

     
def reinforce_tutor(question, concepts):
    # Student question and returns answer
    prompt =  "You are an encouraging and kind high school level tutor. These are the concepts the student is learning.\n\n"
    prompt += concepts
    prompt += f"\n\n{question}\n\n"
    prompt +=  "Based on the student's question, can you highlight the concept that the student is struggling with and provide them with guidance. Give me the answer in Spasnish"
    return prompt_gemini(prompt)

def main():
    """if not os.path.exists(MARKDOWN_FILE) or os.path.getsize(SUMMARY_FILE) == 0:
        file = CLIENT.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
        make_lesson_md(file, MARKDOWN_FILE)

    markdown = open(MARKDOWN_FILE, "r").read()
    print(markdown)
    return"""

    # TODO: Find way to convert PDF to lesson in student language
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


