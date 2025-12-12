from sklearn.tree import DecisionTreeClassifier


class RuleBasedEngine:
    def adjust(self, tracker, current_difficulty: int) -> int:
        acc = tracker.last_n_accuracy(3)
        avg_t = tracker.avg_time()
        if acc >= 0.8 and avg_t < 5:
            return min(2, current_difficulty + 1)
        if acc <= 0.4 or avg_t > 10:
            return max(0, current_difficulty - 1)
        return current_difficulty

class MLAdaptiveEngine:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.X = [] 
        self.y = []
    def update(self, correct: int, time_taken: float, cur_diff: int, next_diff: int):
        self.X.append([correct, float(time_taken), cur_diff])
        self.y.append(next_diff)
        if len(self.X) >= 8: 
            self.model.fit(self.X, self.y)
    def predict(self, correct: int, time_taken: float, cur_diff: int) -> int:
        if len(self.X) < 8:
            return cur_diff
        return int(self.model.predict([[correct, float(time_taken), cur_diff]])[0])
