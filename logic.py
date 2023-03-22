class Task:
    def __init__(self, text, answer, solution):
        self.text: str = text
        self.answer: str = answer
        self.solution: bool = solution


class Editor:
    def __init__(self, title):
        self.tokens = {
            "title": title,
            "tasks": []
        }

    def create_new_assembly(self, title):
        pass

    def add_new_task(self, text, answer, solution):
        new_task = Task(text, answer, solution)
        self.tokens["tasks"].append({"text": new_task.text, "answer": new_task.answer, "solution": new_task.solution})

    def remove_task(self, index):
        self.tokens["tasks"].pop(index)
