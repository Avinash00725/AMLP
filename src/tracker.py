import csv
import os
from typing import List, Dict


class PerformanceTracker:
    def __init__(self, csv_path: str = "session_log.csv"):
        self.records: List[Dict] = []
        self.csv_path = csv_path
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "username", "question_idx", "difficulty", "expression", "correct", "user_answer", "time_taken"])
    def log(self, timestamp: str, username: str, question_idx: int, difficulty: int, expression: str, correct: int, user_answer: str, time_taken: float):
        rec = {
            "timestamp": timestamp,
            "username": username,
            "question_idx": question_idx,
            "difficulty": difficulty,
            "expression": expression,
            "correct": correct,
            "user_answer": user_answer,
            "time_taken": time_taken
            }
        self.records.append(rec)
        self._append_csv(rec)
    def _append_csv(self, rec: Dict):
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                rec["timestamp"], rec["username"], rec["question_idx"], rec["difficulty"],
                rec["expression"], rec["correct"], rec["user_answer"], f"{rec['time_taken']:.3f}"
                ])
    def accuracy(self) -> float:
        if not self.records:
            return 0.0
        return sum(r["correct"] for r in self.records) / len(self.records)


    def avg_time(self) -> float:
        if not self.records:
            return 0.0
        return sum(r["time_taken"] for r in self.records) / len(self.records)


    def last_n_accuracy(self, n: int = 3) -> float:
        last = self.records[-n:]
        if not last:
            return 0.0
        return sum(r["correct"] for r in last) / len(last)


    def difficulty_trend(self) -> List[int]:
        return [r["difficulty"] for r in self.records]