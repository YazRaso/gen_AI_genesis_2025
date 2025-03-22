import os
from google import genai

from backend.main import client, model, get_content


class Lesson:
    folder = str
    questions = dict[str: list]
    _core_concepts = list
    summary = str

    def __init__(self, folder: str, con: list) -> None:
        self._folder = folder
        # f = open(os.path.join(folder, "concepts.txt"), "r")
        # self._core_concepts = f.readlines()
        self._core_concepts = con
        self.questions = {}
        for concept in self._core_concepts:
            self.questions[concept] = []

    def generate_questions(self, concept: str) -> None:
        # Generate 3 questions based on concept
        if concept in self.questions:
            for i in range(3):
                text = "You are a high school tutor. Create a quiz question for this core concept that is different from the other questions in the attached list:\n"
                text += "Concept: " + concept + "\n"
                text += "Summary: " + self.summary + "\n"
                text += "Previous Questions: " + str(self.questions[concept])
                response = client.models.generate_content(model=model, contents=text)
                self.questions[concept].append(response.text)

if __name__ == "__main__":
    file = client.files.upload(file='biology-student-textbook-grade-9_cell_biology.pdf')
    result = get_content(file)
    cons = ["Cell Formation", "Cell Transportation"]
    l = Lesson("heh", cons)
    l.summary = result
    l.generate_questions("Cell Formation")
    l.generate_questions("Cell Transportation")
    print(l.questions)



