import os
from google import genai

from main import CLIENT, MODEL

TEST_ANSWERS = ["Midocondira?", "Cell formations?", "I don't understand"]
TEST_CONCEPTS = ["Cell Formation", "Cell Transportation"]

class Concept:
    name: str
    questions: list
    learned: bool
    summary: str

    def __init__(self, name: str, con_sum: str) -> None:
        self.name = name
        self.learned = False
        self.questions = []
        self.summary = con_sum

    def check_answer(self, question_index: int, answer: str) -> (bool, str):
        text = ("You are a high school tutor. The following answer to the question "
                "was given by a student. Check to see if this answer is correct "
                "based on the summary of the content. Return your response so that "
                "it is only 'Correct' for correct answers and 'Incorrect' "
                "for incorrect answers followed by an explanation why:\n")
        text += "Question: " + self.questions[question_index] + "\n"
        text += "Student's Answer: " + answer + "\n"
        text += "Summary: " + self.summary + "\n"
        response = CLIENT.models.generate_content(model=MODEL, contents=text)
        if response.text == 'Correct':
            return True, "Correct"
        else:
            return False, response.text

    def generate_questions(self) -> None:
        # Generate 3 questions based on concept
        for i in range(3):
            text = "You are a high school tutor. Create a quiz question for this core concept that is different from the other questions in the attached list. Return your response so it is only the question.:\n"
            text += "Concept: " + self.name + "\n"
            text += "Summary: " + self.summary + "\n"
            text += "Previous Questions: " + str(self.questions)
            response = CLIENT.models.generate_content(model=MODEL, contents=text)
            self.questions.append(response.text)


def check_concept(concept: Concept) -> bool | str:
    for i in range(3):
        result = concept.check_answer(i, TEST_ANSWERS[i])
        if not result[0]:
            return "You got the following question incorrect: " + concept.questions[i] + result[1]
    concept.learned = True
    return True


class Lesson:
    folder: str
    _core_concepts: list[Concept]
    summary: str
    learned: bool

    def __init__(self, folder: str, c: Concept) -> None:
        self._folder = folder
        self._core_concepts = [c]
        # Code below is used for getting concepts from a file
        # f = open(os.path.join(folder, "concepts.txt"), "r")
        # self._core_concepts = f.readlines()
        """
        self.questions = {}
        for i in range(len(self._core_concepts)):
            concept = self._core_concepts[i].strip()
            self.questions[concept] = []
            """

    # Checks if they got the lesson correct (All concepts are right)
    # def check_lesson(self) -> None:
    #     for concept in self._core_concepts:
    #         if not concept.learned:
    #             if isinstance(check_concept(concept), str):



if __name__ == "__main__":
    with open("summary.txt", 'r') as f:
        result = f.read()
    c = Concept(TEST_CONCEPTS[0], result)
    l = Lesson("heh", c)
    l.summary = result
    c.generate_questions()
    print(check_concept(c))




