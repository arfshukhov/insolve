from cryptography.fernet import Fernet


class Cryptographer:
    def __init__(self, key):
        self.key = key
        self.fernet = Fernet(key)

    def encrypt(self, word):
        return self.fernet.encrypt(word.encode())

    def decrypt(self, word):
        return self.fernet.decrypt(word).decode()