from random import randrange


class Quiz:
    concepts: list
    used_cons: list

    def __init__(self, cons) -> None:
        self.concepts = cons
        for concept in self.concepts:
            concept.generate_questions()

    def choose_ques(self, num: int) -> list:
        self.used_cons = []
        i = 0
        while i < num:
            curr_con = self.concepts[randrange(len(self.concepts))]
            if curr_con not in self.used_cons:
                self.used_cons.append(curr_con)
                i += 1

        ques = []
        for concept in self.used_cons:
            ques.extend(concept.questions)
        return ques

    def check_answers(self, answers: list) -> list:
        feedback = []
        for ans in range(len(answers) // 3):
            cons_answers = [answers[ans * 3], answers[ans * 3 + 1], answers[ans * 3 + 2]]
            for i in range(3):
                feedback.append(self.used_cons[ans].check_answer(i, cons_answers[i]))
        return feedback



