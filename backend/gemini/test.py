# hi mom
from tutor import Tutor

if __name__ == "__main__":
    t = Tutor("summary.txt", "concepts.txt", "../bio_small.md")
    t.print_summary()
    t.print_concepts()
    response = t.user_question("What adaptations help increase the efficiency of diffusion in living organisms, and why is this important?")
    print(response)
    t.do_quiz()
