import os
from utils import prompt_gemini, make_persistent
from helper import Helper

class Tutor():
    def __init__(self, summary_path, concepts_path, pdf_path, spanish=True, helper_mode=True):
        self.spanish = spanish
        summary_prompt = "Summarize the following content into easy to follow core concepts"
        concepts_prompt = "Extract the core concepts and list them as precise bullet points"
        if spanish:
            summary_prompt += "in Spanish"
            concepts_prompt += "in Spanish"
        self.summary_path = make_persistent(summary_prompt, pdf_path, summary_path)
        self.concepts_path = make_persistent(concepts_prompt, pdf_path, concepts_path)
        self.helper_mode = helper_mode

    def user_question(self, question_prompt):
        # Asks tutor agent a clarification question in helper mode
        self.helper = Helper(self.summary_path, spanish=self.spanish)
        self.helper.get_advice(question_prompt)
    
    # TODO: Add quiz methods

    def helper_mode(self):
        # Converts tutor agent to helper mode
        self.helper_mode = True

    def quiz_mode(self):
        # Converts tutor agent to quiz mode
        self.helper_mode = False

    def print_summary(self):
        # Prints summary file to verify its existance
        if os.path.exists((self.summary_path)):
            with open(self.summary_path, 'r') as f:
                print(f.read())
        else:
            print("Unable to find summary file!")

    def print_concepts(self):
        # Prints summary file to verify its existance
        if os.path.exists((self.concepts_path)):
            with open(self.concepts_path, 'r') as f:
                print(f.read())
        else:
            print("Unable to find concepts file!")