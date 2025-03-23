from utils import prompt_gemini

class Helper:
    def __init__(self, summary, language):
        self.summary = summary
        self.language = language

    def get_advice(self, question):
        # Intakes student question and returns helpful answer
        prompt =  f"You are an encouraging and kind high school level tutor. These are the concepts the student is learning.\n\n{self.summary}\n\n{question}\n\nBased on the student's question, can you highlight the concept that the student is struggling with and provide them with guidance. Give me the answer in {self.language}."
        return prompt_gemini(prompt)
