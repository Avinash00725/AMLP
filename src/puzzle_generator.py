import random

class PuzzleGenerator:
    def generate(self, difficulty):
        if difficulty == 0:
            a, b = random.randint(1, 100), random.randint(1, 10)
            op = random.choice(["+", "-"])
        elif difficulty == 1:
            a, b = random.randint(100, 2000), random.randint(10, 50)
            op = random.choice(["+", "-", "*"])
        else:
            a, b = random.randint(600, 10000), random.randint(1, 20)
            op = random.choice(["+", "-", "*", "/"])

        expr = f"{a} {op} {b}"
        ans = eval(expr)
        return expr,ans
