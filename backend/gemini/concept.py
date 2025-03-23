from utils import prompt_gemini

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