import time
from datetime import datetime

from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import RuleBasedEngine, MLAdaptiveEngine

DIFF_LABELS = {0: "Easy", 1: "Medium", 2: "Hard"}

def safe_float(s: str):
    try:
        return float(s)
    except Exception:
        return None




def run_console_session():
    print("Welcome to Adaptive Math Practice!")
    username = input("Enter your name: ").strip() or "anon"
    start_choice = input("Choose starting difficulty (easy/medium/hard) [easy]: ").strip().lower()
    start_map = {"easy": 0, "medium": 1, "hard": 2}
    cur_diff = start_map.get(start_choice, 0)
    generator = PuzzleGenerator()
    tracker = PerformanceTracker()
    rule_engine = RuleBasedEngine()
    ml_engine = MLAdaptiveEngine()
    use_ml = False
    use_ml_answer = input("Use ML adaptive engine (requires warm-up)? (y/N): ").strip().lower()
    if use_ml_answer == "y":
        use_ml = True
    session_len = 10
    print(f"Starting session of {session_len} questions. Current difficulty: {DIFF_LABELS[cur_diff]}")
    for idx in range(1, session_len + 1):
        expr, answer = generator.generate(cur_diff)
        print(f"\nQ{idx} [{DIFF_LABELS[cur_diff]}]: {expr}")
        t0 = time.time()
        user_raw = input("Your answer: ")
        t1 = time.time()
        elapsed = t1 - t0
        user_val = safe_float(user_raw)
        correct = 0
        if user_val is not None:
            if isinstance(answer, float):
                correct = 1 if abs(user_val - answer) < 0.05 else 0
            else:
                correct = 1 if user_val == answer else 0
        timestamp = datetime.utcnow().isoformat()
        tracker.log(timestamp, username, idx, cur_diff, expr, correct, user_raw, elapsed)
        if use_ml:
            next_diff_pred = ml_engine.predict(correct, elapsed, cur_diff)
            next_diff = next_diff_pred
            teacher_next = rule_engine.adjust(tracker, cur_diff)
            ml_engine.update(correct, elapsed, cur_diff, teacher_next)
        else:
            next_diff = rule_engine.adjust(tracker, cur_diff)
        if correct:
            print("Correct!")
        else:
            print(f"Incorrect. Answer was: {answer}")
        print(f"Time taken: {elapsed:.2f}s")
        if next_diff > cur_diff:
            print("Difficulty increased ->", DIFF_LABELS[next_diff])
        elif next_diff < cur_diff:
            print("Difficulty decreased ->", DIFF_LABELS[next_diff])
        else:
            print("Difficulty maintained ->", DIFF_LABELS[next_diff])
        cur_diff = next_diff

    print(f"Accuracy: {tracker.accuracy() * 100:.2f}%")
    print(f"Average time: {tracker.avg_time():.2f}s")
    print(f"Difficulty trend: {tracker.difficulty_trend()}")

if __name__ == '__main__':
    run_console_session()