import json
import os


from cryptography.fernet import Fernet


class Cryptographer:
    KEY = b'pbBf8hbN2YybfvP_ieCQmZf7ZDdg9934mY7bA_b4rUM='
    fernet = Fernet(KEY)

    @staticmethod
    def encrypt(word, fernet=fernet):
        return fernet.encrypt(word.encode())

    @staticmethod
    def decrypt(word, fernet=fernet):
        return fernet.decrypt(word).decode()


class User:
    def __init__(self, role, fname, lname):
        self.role = role
        self.fname = fname
        self.lname = lname
        self.__dict__ = {"role": self.role, "fname": self.fname, "lname": self.lname}

    def __str__(self):
        if self.role == "teacher":
            role = "Учитель"
        else:
            role = "Ученик"
        return f"{role}: {self.fname} {self.lname}"


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

    def make_json(self):
        with open(f"files/{self.tokens['title']}.json", "wb") as f:
            jsn = Cryptographer.encrypt(json.dumps(self.tokens))
            f.write((jsn))

    def remove_json(self):
        os.remove(f"files/{self.tokens['title']}.json")


class Solution():
    def __init__(self):
        self.tokens = {
            "title": ...,
            "solutions": [],
            "right_percent": ...,
            "name": ...
        }
        self.data = None

    def set_title(self, title):
        self.tokens["title"] = title

    def add_new_solution(self, text, solution, answer):
        self.tokens["solutions"].append({"text": text, "solution": solution, "answer": answer})

    def set_result(self, percent):
        self.tokens["right_percent"] = percent

    def set_name(self, user):
        self.tokens["name"] = str(user)