class Quiz:
    concepts: []
    questions: list[str]
    wrong_ques: dict[int: str]

    def __init__(self, cons) -> None:
        self.failed_cons = []
        self.wrong_ques = {}
        self.questions = []
        self.concepts = cons
        for concept in self.concepts:
            concept.generate_questions()
        for concept in self.concepts:
            self.questions.extend(concept.questions)

    def quiz_user(self) -> None:
        for i in range(len(self.concepts)):
            concept = self.concepts[i]
            if not concept.learned:
                outcome = concept.check_concept()
                if len(outcome) != 0:
                    self.failed_cons.append(concept)
                    for j in range(len(outcome)):
                        self.wrong_ques[i * 3 + outcome[j][0]] = outcome[j][1]
                        # For testing
                        # print(outcome[j][1])

# For testing
if __name__ == "__main__":
    q = Quiz()
    q.quiz_user()
    print(q.wrong_ques)
    print(q.failed_cons)



