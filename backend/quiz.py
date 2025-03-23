import os
from google import genai

from main import CLIENT, MODEL

# For testing cause no clue how to get answers
TEST_ANSWERS = ["Midocondira?", "Cell formations?", "I don't understand"]

# Replace with actual summary file
with open("summary.txt", 'r') as f:
    SUMMARY = f.read()

class Concept:
    name: str
    questions: list
    learned: bool

    def __init__(self, name: str) -> None:
        self.name = name
        self.learned = False
        self.questions = []

    def check_answer(self, question_index: int, answer: str) -> (bool, str):
        text = ("You are a high school tutor. The following answer to the question "
                "was given by a student. Check to see if this answer is correct "
                "based on the summary of the content. Return your response so that "
                "it is only 'Correct' for correct answers and 'Incorrect' "
                "for incorrect answers followed by an explanation why:\n")
        text += "Question: " + self.questions[question_index] + "\n"
        text += "Student's Answer: " + answer + "\n"
        text += "Summary: " + SUMMARY + "\n"
        # TODO Util here
        response = CLIENT.models.generate_content(model=MODEL, contents=text)
        if response.text == 'Correct':
            return True, "Correct"
        else:
            return False, response.text

    def generate_questions(self) -> None:
        # Generate 3 new questions based on concept
        self.questions = []
        for i in range(3):
            text = ("You are a high school tutor. Create a quiz question for this "
                    "core concept that is different from the other questions in "
                    "the attached list. Return your response so it is only the question.:\n")
            text += "Concept: " + self.name + "\n"
            text += "Summary: " + SUMMARY + "\n"
            text += "Previous Questions: " + str(self.questions)
            # TODO Util here
            response = CLIENT.models.generate_content(model=MODEL, contents=text)
            self.questions.append(response.text)

    def check_concept(self) -> list[list[int, str]]:
        outcomes = []
        for i in range(3):
            outputs = self.check_answer(i, TEST_ANSWERS[i])
            if not outputs[0]:
                outcomes.append([i, outputs[1]])
        if len(outcomes) == 0:
            self.learned = True
        return outcomes

# Concepts for testing
TEST_CONCEPTS = [Concept("Cell Formation"),Concept("Cell Transportation")]

class Quiz:
    failed_cons: list[Concept]
    questions: list[str]
    wrong_ques: dict[int: str]

    def __init__(self) -> None:
        self.failed_cons = []
        self.wrong_ques = {}
        self.questions = []
        for concept in TEST_CONCEPTS:
            concept.generate_questions()
        for concept in TEST_CONCEPTS:
            self.questions.extend(concept.questions)

    def quiz_user(self) -> None:
        for i in range(len(TEST_CONCEPTS)):
            concept = TEST_CONCEPTS[i]
            if not concept.learned:
                outcome = concept.check_concept()
                if len(outcome) != 0:
                    self.failed_cons.append(concept)
                    for j in range(len(outcome)):
                        self.wrong_ques[i * 3 + outcome[j][0]] = outcome[j][1]
                        # For testing
                        print(outcome[j][1])

if __name__ == "__main__":
    q = Quiz()
    q.quiz_user()
    print(q.wrong_ques)
    print(q.failed_cons)



