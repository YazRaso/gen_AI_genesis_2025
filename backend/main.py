import os
from google import genai
from google.genai import types

# Configure the API key
# in bash: `export GEMINI_API_KEY=[key]`
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Set your API key in environment variables
client = genai.Client(api_key='AIzaSyAUWuyUe5Hicxeqz_xHNFMG-kgYOd32EvY')

# Create the Generative Model instance
model = 'gemini-2.0-flash'

def get_content(learn_file):
    text = "Summarize the following content into easy to follow core concepts."
    try:
        response = client.models.generate_content(model=model, contents=[text, learn_file])
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

<<<<<<< Updated upstream
def reinforce_tutor(question, concepts):
    """
    Pass concepts file, tutor instruct, and student prompt
    """
    prompt =  "You are an encouraging and kind high school level tutor. These are the concepts the student is learning.\n\n"
    prompt += concepts
    prompt += f"\n\n{question}\n\n"       
    prompt +=  "Based on the student's question, can you highlight the concept that the student is struggling with and provide them with guidance. Give me the answer in Spasnish"

    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"
    
=======

>>>>>>> Stashed changes

# Example usage
if __name__ == "__main__":
    file = client.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
    concepts = get_content(file)

    question1 = "What is the difference between magnification and resolution in a microscope, and why is resolution more important for seeing fine details?"
    
    question2 = "How does the electron microscope differ from the light microscope in terms of function and limitations?"

    question3 = "Why is staining necessary when using a light microscope, and how does it affect the visibility of cell structures?"

    question4 = "How do diffusion, osmosis, and active transport differ in terms of energy use and direction of movement?"

    question5 = "Why do plant cells have both a cell membrane and a cell wall, and how do their functions differ?"

    question6 = "What is the significance of mitochondria in cells, and why do some cells have more mitochondria than others?"

    question7 = "How does the structure of specialized cells, such as nerve cells or muscle cells, relate to their function in the human body?"

    question8 = "Why are cells considered the basic unit of life according to cell theory, and how was this theory developed?"

    question9 = "What adaptations help increase the efficiency of diffusion in living organisms, and why is this important?"
    
    answer = reinforce_tutor(question1, concepts)
    print(answer)
