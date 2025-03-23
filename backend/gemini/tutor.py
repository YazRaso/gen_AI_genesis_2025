import os
from utils import prompt_gemini, make_persistent
from helper import Helper
from quiz import Quiz

TEST_ANSWERS = ["Midocondira?", "Cell formations?", "I don't understand"]

class Concept:
    name: str
    questions: list
    learned: bool
    summary: str

    def __init__(self, name: str, sum_path: str) -> None:
        self.name = name
        self.learned = False
        self.questions = []
        with open(sum_path, "r") as f:
            self.summary = f.read()

    def check_answer(self, question_index: int, answer: str) -> (bool, str):
        text = ("You are a high school tutor. The following answer to the question "
                "was given by a student. Check to see if this answer is correct "
                "based on the summary of the content. Return your response so that "
                "it is only 'Correct' for correct answers and 'Incorrect' "
                "for incorrect answers followed by an explanation why:\n")
        text += "Question: " + self.questions[question_index] + "\n"
        text += "Student's Answer: " + answer + "\n"
        text += "Summary: " + self.summary + "\n"
        response = prompt_gemini(text)
        if response in 'Correct':
            return True, "Correct"
        else:
            return False, response

    def generate_questions(self) -> None:
        # Generate 3 new questions based on concept
        self.questions = []
        for i in range(3):
            text = ("You are a high school tutor. Create a quiz question for this "
                    "core concept that is different from the other questions in "
                    "the attached list. Return your response so it is only the question.:\n")
            text += "Concept: " + self.name + "\n"
            text += "Summary: " + self.summary + "\n"
            text += "Previous Questions: " + str(self.questions)
            response = prompt_gemini(text)
            self.questions.append(response)

    def check_concept(self) -> list[list[int, str]]:
        outcomes = []
        for i in range(3):
            outputs = self.check_answer(i, TEST_ANSWERS[i])
            if not outputs[0]:
                outcomes.append([i, outputs[1]])
        if len(outcomes) == 0:
            self.learned = True
        return outcomes

class Tutor:
    helper: Helper
    quizzer: Quiz
    summary_path: str
    concepts_path: str
    pdf_path: str
    concepts: list[Concept]

    def __init__(self, summary_path, concepts_path, pdf_path, spanish=True):
        self.spanish = spanish
        summary_prompt = "Summarize the following content into easy to follow core concepts"
        concepts_prompt = "Extract the core concepts and list the names of the concepts each on a new line"
        if spanish:
            summary_prompt += "in Spanish"
            concepts_prompt += "in Spanish"
        self.summary_path = make_persistent(summary_prompt, pdf_path, summary_path)
        self.concepts_path = make_persistent(concepts_prompt, pdf_path, concepts_path)
        self.concepts = []

        # Create a list of the concepts
        with open(concepts_path, "r") as f:
            con_names = f.readlines()
            for i in range(len(con_names)):
                con_names[i].strip()
                self.concepts.append(Concept(con_names[i], self.summary_path))


    def user_question(self, question_prompt):
        # Asks tutor agent a clarification question in helper mode
        self.helper = Helper(self.summary_path, spanish=self.spanish)
        return self.helper.get_advice(question_prompt)

    def do_quiz(self) -> None:
        q = Quiz(self.concepts)
        q.quiz_user()
        grade = round(len(q.wrong_ques) / len(q.questions), 3) * 100
        print("You dumbo got these questions wrong:\n\n")
        for index in q.wrong_ques:
            print(q.questions[index] + ":\n")
            print(q.wrong_ques[index] + "\n\n")
        print(str(len(q.questions) - len(q.wrong_ques)) + " out of " + str(len(q.questions)) + " questions correct.")
        print("Grade: " + str(grade))



    # def helper_mode(self):
    #     # Converts tutor agent to helper mode
    #     self.helper_mode = True
    #
    # def quiz_mode(self):
    #     # Converts tutor agent to quiz mode
    #     self.helper_mode = False

    def print_summary(self):
        # Prints summary file to verify its existance
        if os.path.exists(self.summary_path):
            with open(self.summary_path, 'r') as f:
                print(f.read())
        else:
            print("Unable to find summary file!")

    def print_concepts(self):
        # Prints summary file to verify its existance
        if os.path.exists(self.concepts_path):
            with open(self.concepts_path, 'r') as f:
                print(f.read())
        else:
            print("Unable to find concepts file!")


