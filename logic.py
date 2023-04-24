import json
import os

from db_ops import SolutionsBase


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


class Elo:
    def __init__(self, count_, percent):
        self.count_ = count_
        self.percent = percent

    def __repr__(self):
        return round((self.percent - 50) / 100 * self.count_ * 1.3)


class Statistic:
    """
    Класс статистики, вычисляет общее эло и выдает ранг в соответствии с эло
    """
    def __init__(self):
        self.rank_match = {
            range(-10 ** 9, 101): "20 Кю", range(101, 201): "19 Кю", range(201, 301): "18 Кю", range(301, ): "17 Кю",
            range(301, 401): "16 Кю", range(401, 501): "15 Кю", range(501, 601): "14 Кю", range(601, 701): "13 Кю",
            range(701, 801): "12 Кю", range(801, 901): "11 Кю", range(901, 1001): "10 Кю", range(1001, 1101): "9 Кю",
            range(1101, 1201): "8 Кю", range(1201, 1301): "7 Кю", range(1301, 1401): "6 Кю", range(1401, 1501): "5 Кю",
            range(1501, 1601): "4 Кю", range(1601, 1701): "3 Кю", range(1701, 1801): "2 Кю",
            range(1801, 1901): "1 Кю", range(1901, 2001): "1 Дан", range(2101, 2201): "2 Дан",
            range(2301, 2401): "3 Дан", range(2401, 2501): "4 Дан", range(2601, 2701): "5 Дан",
            range(2701, 2801): "6 Дан", range(2801, 2901): "7 Дан", range(2901, 3001): "8 Дан",
            range(2701, 2801): "6 Дан", range(2801, 2901): "1 профессиональный Дан",
            range(2901, 3001): "2 профессиональный Дан", range(3101, 3201): "3 профессиональный Дан",
            range(3201, 3301): "4 профессиональный Дан", range(3301, 3401): "5 профессиональный Дан",
            range(3401, 3501): "6 профессиональный Дан", range(3501, 3601): "7 профессиональный Дан",
            range(3601, 3701): "8 профессиональный Дан", range(3701, 10 ** 8): "9 профессиональный Дан"}
        self.elo = 0
        self.rank: str = ""
        try:
            self.calculate_elo()
        except Exception:
            self.elo = 0
        self.calculate_rank()

    def calculate_elo(self):
        base = SolutionsBase()
        for elem in base.tokens:
            self.elo += elem["elo"]

    def calculate_rank(self):
        for i in self.rank_match.keys():
            if self.elo in i:
                self.rank = self.rank_match[i]
                break
        else:
            self.rank = "undefined rank"
