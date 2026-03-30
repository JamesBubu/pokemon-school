#!/usr/bin/env python3
"""
Pokemon School — 題庫產生器 / 擴充工具
========================================
用途：
  1. 自動產生各年級數學題目（加減乘除、時間、幾何）
  2. 提供國語 / 英文題目的擴充模板
  3. 將結果寫入 questions/<grade>/<subject>.json

執行方式（需在專案根目錄）：
  python3 scrapers/generate_questions.py

需要 Python 3.8+，無需額外套件。
"""

import json
import random
import os
from pathlib import Path
from typing import Optional

# ── 設定 ─────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent.parent / "questions"
GRADES = ["kinder", "grade1", "grade2", "grade3"]
SUBJECTS = ["math", "chinese", "english"]

# ── 工具函式 ──────────────────────────────────────────────────────

def make_id(grade: str, sub: str, n: int) -> str:
    prefix = {
        "kinder": "k", "grade1": "g1", "grade2": "g2", "grade3": "g3"
    }[grade]
    sletter = {"math": "m", "chinese": "c", "english": "e"}[sub]
    return f"{prefix}{sletter}{n:04d}"

def mcq(q: str, opts: list, a: int, tags: list = None) -> dict:
    return {"type": "mcq", "q": q, "opts": opts, "a": a, "tags": tags or []}

def tf(q: str, correct: bool, tags: list = None) -> dict:
    return {
        "type": "tf",
        "q": q,
        "opts": ["正確", "錯誤"],
        "a": 0 if correct else 1,
        "tags": tags or [],
    }

def shuffle_opts(answer: str, distractors: list) -> tuple[list, int]:
    """Shuffle answer + distractors; return (opts, answer_index)."""
    pool = distractors[:3]
    opts = pool + [answer]
    random.shuffle(opts)
    return opts, opts.index(answer)

def write_bank(grade: str, sub: str, questions: list):
    out_dir = OUTPUT_DIR / grade
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{sub}.json"

    # Load existing file if present, merge (avoid duplicates by id)
    existing = []
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            existing = data.get("questions", [])
        except Exception:
            pass

    existing_ids = {q["id"] for q in existing}

    # Assign IDs to new questions
    counter = len(existing) + 1
    for q in questions:
        if "id" not in q:
            while make_id(grade, sub, counter) in existing_ids:
                counter += 1
            q["id"] = make_id(grade, sub, counter)
            existing_ids.add(q["id"])
            counter += 1

    merged = existing + questions
    grade_names = {
        "kinder": "幼稚園大班", "grade1": "小學一年級",
        "grade2": "小學二年級", "grade3": "小學三年級",
    }
    sub_names = {"math": "數學", "chinese": "國語", "english": "英文"}
    payload = {
        "meta": {
            "grade": grade,
            "subject": sub,
            "description": f"{grade_names[grade]} {sub_names[sub]}",
            "version": "1.0",
            "count": len(merged),
        },
        "questions": merged,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ {grade}/{sub}.json  ({len(merged)} 題，新增 {len(questions)} 題)")


# ════════════════════════════════════════════════════════════════
# 數學題目產生器
# ════════════════════════════════════════════════════════════════

def gen_kinder_math() -> list:
    qs = []
    # 1-digit addition
    for a in range(1, 6):
        for b in range(1, 6):
            ans = a + b
            d = [ans - 1, ans + 1, ans + 2]
            opts, ai = shuffle_opts(str(ans), [str(x) for x in d])
            qs.append(mcq(f"{a} + {b} = ?", opts, ai, ["addition", "single-digit"]))
    # 1-digit subtraction
    for a in range(3, 9):
        for b in range(1, a):
            ans = a - b
            d = [ans + 1, ans - 1 if ans > 0 else ans + 2, ans + 2]
            opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x != ans][:3])
            qs.append(mcq(f"{a} - {b} = ?", opts, ai, ["subtraction", "single-digit"]))
    # True/False
    combos = [(2, 3, 5), (3, 4, 7), (1, 5, 6), (4, 2, 6), (3, 3, 6)]
    for a, b, c in combos:
        correct = (a + b == c)
        qs.append(tf(f"{a} + {b} = {c}，這是正確的嗎？", correct, ["addition", "tf"]))
    combos2 = [(5, 2, 3), (7, 3, 4), (6, 4, 2), (4, 1, 3)]
    for a, b, c in combos2:
        correct = (a - b == c)
        qs.append(tf(f"{a} - {b} = {c}，這是正確的嗎？", correct, ["subtraction", "tf"]))
    # Counting shapes
    for n, emoji in [(3, "🍎"), (4, "⭐"), (5, "🌸"), (2, "🐶")]:
        q_text = f"{''.join([emoji]*n)} 有幾個？"
        d = [str(n - 1), str(n + 1), str(n + 2)]
        opts, ai = shuffle_opts(str(n), d)
        qs.append(mcq(q_text, opts, ai, ["counting", "emoji"]))
    return qs


def gen_grade1_math() -> list:
    qs = []
    # Addition within 20
    pairs = [(8,7),(9,6),(6,7),(7,8),(9,5),(8,6),(5,9),(7,6),(8,5),(9,4)]
    for a, b in pairs:
        ans = a + b
        d = [ans - 2, ans - 1, ans + 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d])
        qs.append(mcq(f"{a} + {b} = ?", opts, ai, ["addition", "within-20"]))
    # Subtraction within 20
    pairs2 = [(15,6),(17,8),(14,5),(16,7),(13,4),(18,9),(12,5),(11,4)]
    for a, b in pairs2:
        ans = a - b
        d = [ans + 2, ans + 1, ans - 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x > 0])
        qs.append(mcq(f"{a} - {b} = ?", opts, ai, ["subtraction", "within-20"]))
    # Multiplication intro (×2, ×3, ×4, ×5)
    for m in [2, 3, 4, 5]:
        for n in range(2, 6):
            ans = m * n
            d = [ans - m, ans + m, ans + 1]
            opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x != ans][:3])
            qs.append(mcq(f"{m} × {n} = ?", opts, ai, ["multiplication", f"times-{m}"]))
    # Counting by 2s/5s/10s
    for start, step, label in [(2, 2, "2"), (5, 5, "5"), (10, 10, "10")]:
        seq = [start * i for i in range(1, 5)]
        next_val = seq[-1] + step
        seq_str = ", ".join(str(x) for x in seq)
        d = [next_val - step, next_val + step, next_val + step * 2]
        opts, ai = shuffle_opts(str(next_val), [str(x) for x in d if x != next_val][:3])
        qs.append(mcq(f"{seq_str}, ___ 下一個是？", opts, ai, ["patterns", f"count-by-{label}"]))
    # TF
    for a, b in [(10, 10), (7, 8), (15, 6), (3, 3)]:
        ans = a + b
        wrong = ans + random.choice([-1, 1, 2])
        qs.append(tf(f"{a} + {b} = {ans}，這是正確的嗎？", True, ["addition", "tf"]))
        qs.append(tf(f"{a} + {b} = {wrong}，這是正確的嗎？", False, ["addition", "tf"]))
    return qs


def gen_grade2_math() -> list:
    qs = []
    # 3-digit addition/subtraction
    pairs_add = [(45,38),(72,19),(53,47),(86,35),(124,237),(315,168),(204,385)]
    for a, b in pairs_add:
        ans = a + b
        d = [ans - 10, ans + 10, ans - 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d])
        qs.append(mcq(f"{a} + {b} = ?", opts, ai, ["addition", "3-digit"]))
    pairs_sub = [(72,35),(100,37),(150,68),(200,85),(500,237),(350,168)]
    for a, b in pairs_sub:
        ans = a - b
        d = [ans + 10, ans - 10, ans + 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x >= 0])
        qs.append(mcq(f"{a} - {b} = ?", opts, ai, ["subtraction", "3-digit"]))
    # Multiplication tables 1–9
    for m in range(2, 10):
        for n in range(2, 10):
            ans = m * n
            d = [ans - m, ans + m, ans - n]
            opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x != ans and x > 0][:3])
            qs.append(mcq(f"{m} × {n} = ?", opts, ai, ["multiplication", f"times-{m}"]))
    # TF for multiplication
    for m, n in [(3,6),(4,7),(8,8),(5,9),(6,7)]:
        ans = m * n
        qs.append(tf(f"{m} × {n} = {ans}，這是正確的嗎？", True, ["multiplication", "tf"]))
        qs.append(tf(f"{m} × {n} = {ans + m}，這是正確的嗎？", False, ["multiplication", "tf"]))
    # Time reading
    times = [(3,2,"5點"),(8,3,"11點"),(10,2,"12點"),(1,4,"5點")]
    for h, add, ans in times:
        opts, ai = shuffle_opts(ans, [f"{h+add-1}點", f"{h+add+1}點", f"{h}點"])
        qs.append(mcq(f"現在 {h} 點整，{add} 小時後是幾點？", opts, ai, ["time"]))
    return qs


def gen_grade3_math() -> list:
    qs = []
    # Multiplication all combinations
    for m in range(2, 10):
        for n in range(m, 10):
            ans = m * n
            d = [ans - m, ans + m, ans - n]
            opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x != ans and x > 0][:3])
            qs.append(mcq(f"{m} × {n} = ?", opts, ai, ["multiplication", f"times-{m}"]))
    # Division
    for divisor in range(2, 10):
        for quotient in range(2, 10):
            dividend = divisor * quotient
            d = [quotient - 1, quotient + 1, quotient + 2]
            opts, ai = shuffle_opts(str(quotient), [str(x) for x in d if x != quotient and x > 0][:3])
            qs.append(mcq(f"{dividend} ÷ {divisor} = ?", opts, ai, ["division"]))
    # TF for division
    for d, v, q in [(48,6,8),(35,7,5),(72,9,8),(56,8,7)]:
        qs.append(tf(f"{d} ÷ {v} = {q}，這是正確的嗎？", True, ["division", "tf"]))
        qs.append(tf(f"{d} ÷ {v} = {q+1}，這是正確的嗎？", False, ["division", "tf"]))
    # Geometry
    shapes = [
        ("三角形", "幾個邊", "3個", ["2個", "4個", "5個"]),
        ("正方形", "幾個角", "4個", ["3個", "5個", "6個"]),
        ("長方形", "幾個邊", "4個", ["3個", "5個", "6個"]),
        ("五邊形", "幾個角", "5個", ["3個", "4個", "6個"]),
    ]
    for shape, q_part, ans, d in shapes:
        opts, ai = shuffle_opts(ans, d)
        qs.append(mcq(f"{shape}有{q_part}？", opts, ai, ["geometry"]))
    # Large number computation
    pairs = [(125,368),(503,278),(1000,375),(256,449),(718,283)]
    for a, b in pairs:
        ans = a + b
        d = [ans - 10, ans + 10, ans - 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d])
        qs.append(mcq(f"{a} + {b} = ?", opts, ai, ["addition", "large-numbers"]))
    for a, b in pairs:
        ans = a - b if a > b else b - a
        big, small = max(a, b), min(a, b)
        d = [ans + 10, ans - 10, ans + 1]
        opts, ai = shuffle_opts(str(ans), [str(x) for x in d if x >= 0])
        qs.append(mcq(f"{big} - {small} = ?", opts, ai, ["subtraction", "large-numbers"]))
    return qs


# ════════════════════════════════════════════════════════════════
# 英文題目擴充工具（範例模板，可自行擴充）
# ════════════════════════════════════════════════════════════════

def extra_grade3_english() -> list:
    """Additional grade 3 English questions with sentence patterns."""
    qs = []
    # Simple present tense
    sentences = [
        ("I ___ to school every day.（我每天去上學）", ["go", "goes", "going", "went"], 0),
        ("She ___ cats.（她喜歡貓）", ["like", "likes", "liked", "liking"], 1),
        ("They ___ soccer.（他們踢足球）", ["play", "plays", "played", "playing"], 0),
        ("He ___ breakfast every morning.（他每天早上吃早餐）", ["eat", "eats", "ate", "eating"], 1),
        ("We ___ English at school.（我們在學校學英文）", ["learn", "learns", "learned", "learning"], 0),
    ]
    for q_text, opts, ai in sentences:
        qs.append(mcq(q_text, opts, ai, ["grammar", "present-tense"]))
    # Question words
    qwords = [
        ("___ is your name?（你叫什麼名字？）", ["What", "Who", "Where", "When"], 0),
        ("___ are you?（你在哪裡？）", ["What", "Who", "Where", "When"], 2),
        ("___ is your birthday?（你的生日是什麼時候？）", ["What", "Who", "Where", "When"], 3),
        ("___ is your best friend?（誰是你最好的朋友？）", ["What", "Who", "Where", "When"], 1),
        ("___ old are you?（你幾歲？）", ["What", "How", "Where", "When"], 1),
    ]
    for q_text, opts, ai in qwords:
        qs.append(mcq(q_text, opts, ai, ["grammar", "question-words"]))
    # TF vocabulary
    tf_vocab = [
        ("Monday 是星期一", True),
        ("Friday 是星期三", False),
        ("January 是一月份", True),
        ("Summer 是冬天", False),
        ("Pencil 是鉛筆", True),
        ("Table 是椅子", False),
    ]
    for q_text, correct in tf_vocab:
        qs.append(tf(f"{q_text}，這是正確的嗎？", correct, ["vocabulary", "tf"]))
    return qs


# ════════════════════════════════════════════════════════════════
# 主程式
# ════════════════════════════════════════════════════════════════

def main():
    print("🔧 Pokemon School 題庫產生器")
    print(f"   輸出目錄：{OUTPUT_DIR}\n")

    generators = {
        ("kinder",  "math"): gen_kinder_math,
        ("grade1",  "math"): gen_grade1_math,
        ("grade2",  "math"): gen_grade2_math,
        ("grade3",  "math"): gen_grade3_math,
        ("grade3",  "english"): extra_grade3_english,
    }

    for (grade, sub), fn in generators.items():
        print(f"▶ {grade}/{sub}")
        questions = fn()
        write_bank(grade, sub, questions)

    print("\n✅ 完成！請重新整理遊戲頁面以載入新題目。")
    print("\n提示：若要手動新增題目，直接編輯對應的 questions/<grade>/<sub>.json 即可。")
    print("題目格式：")
    print('  { "id": "g3m9999", "type": "mcq", "q": "題目文字",')
    print('    "opts": ["選A","選B","選C","選D"], "a": 0, "tags": ["multiplication"] }')
    print('  { "id": "g3m9998", "type": "tf",  "q": "判斷題文字（是非）",')
    print('    "opts": ["正確","錯誤"], "a": 0, "tags": ["division"] }')


if __name__ == "__main__":
    main()
