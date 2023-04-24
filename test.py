class GreatMagician:
    def __init__(self, name, *words, power=10):
        self.name = name
        self.words = list(words)
        self.power = power

    def add(self, word):
        self.words = [word] + self.words
        self.power += len(word) // 2

    def __call__(self, number):
        cnt = 0
        for i in self.words:
            if len(i) > number:
                cnt += 1
        return cnt

    def __add__(self, other):
        name = self.name[:3] + other.name[:3]
        words = set()
        for i in self.words:
            if i in other.words:
                words.add(i)
        words = sorted(list(words))
        return GreatMagician(name, *words, power=10)

    def __isub__(self, line: str):
        try:
            self.words.remove(line)
            print(f"Delete {line}")
        except Exception:
            print("Nothing to delete")
        return self

    def __gt__(self, other):
        return self.power > other.power

    def __le__(self, other):
        return len(self.words) <= len(other.words)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"""GreatMagician by name {self.name} ({", ".join(self.words)}, {self.power})"""



gm = GreatMagician('Knuth')
gm1 = GreatMagician('Sam', 'Abracadabra', 'Sezam', power=3)
gm.add('Good day')
gm.add('Sezam')
print(gm, gm1, sep='\n')
print(gm < gm1, gm >= gm1, gm != gm1)
gm2 = gm + gm1
print(gm2)
print(gm2 > gm1, gm2 <= gm, gm2 == gm)