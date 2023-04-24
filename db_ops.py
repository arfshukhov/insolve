#from peewee import *
import datetime
import io
import json
from cryptographer import Cryptographer


class SolutionsBase:
    """
    Класс базы всех решений ученика, хранящихся в .json файле.
    cryptographer шифрует данные
    """
    def __init__(self):
        self.cryptographer = Cryptographer(b'pbBf8hbN2YybfvP_ieCQmZf7ZDdg9934mY7bA_b4rUM=')
        self.tokens: list = self.get_tokens()

    def get_tokens(self):
        """
        метод достает из .json файла все решения и расшифровывет их
        """
        with open("data/solutions.json", "rb") as file:
            try:
                tokens: list = json.loads(
                    self.cryptographer.decrypt(file.read())
                )
            except Exception:
                tokens = []
            return tokens

    def add_solution(self, name: str, elo: int, date=datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")):
        self.tokens.append({"name": name, "elo": elo,  "date": date})
        jsn = json.dumps(self.tokens)
        dump = self.cryptographer.encrypt(jsn)
        with open("data/solutions.json", "wb") as file:
            file.write(dump)
        self.tokens = self.get_tokens()
        print(self.tokens)

    def __repr__(self):
        return self.tokens
