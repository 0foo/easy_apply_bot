from nick_py_utils import file_system as file_util
import json

class Questions:
    questions_file="./data/questions.json"
    questions={}

    def __init__(self):
        if not file_util.path_exists(self.questions_file):
            file_util.create_empty_file(self.questions_file)

            with open(self.questions_file, "w") as q_file:
                q_file.write("{}")
        
        self.load_questions()
    
    def load_questions(self):
        with open(self.questions_file, "r") as questions_file:
            self.questions = json.load(questions_file)

    def add_question(self, question_text, question_data):
        if question_text in self.questions:
            print(f"Question Exists: {question_text}. Updating.")
        self.questions[question_text] = question_data

    def save_questions(self):
        with open(self.questions_file, "w") as questions_file:
            json.dump(self.questions, questions_file, indent=4)

    def get_question(self, question_text):
        if question_text in self.questions:
            return self.questions[question_text]
        else:
            return False
    def in_questions(self, question_key):
        if question_key not in self.questions:
            return False
        return True