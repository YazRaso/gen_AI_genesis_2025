from utils import prompt_gemini

class Helper():
    def __init__(self, summary, spanish=True):
        self.summary = summary
        self.spanish = spanish

    def get_advice(self, question):
        # Intakes student question and returns helpful answer
        prompt =  f"You are an encouraging and kind high school level tutor. These are the concepts the student is learning.\n\n{self.summary}\n\n{question}\n\nBased on the student's question, can you highlight the concept that the student is struggling with and provide them with guidance."
        if self.spanish: prompt += "Give me the answer in Spasnish."
        return prompt_gemini(prompt)