import random
from aligner.core import align, Scoring
from aligner.brute import brute_force_score, memo_score

def rnd(k): return "".join(random.choices("ACGT", k=random.randint(1, k)))

def test_dp_matches_brute_force():
    for _ in range(50):
        a, b = rnd(7), rnd(7)
        assert align(a, b, "global")["score"] == brute_force_score(a, b) == memo_score(a, b)

def test_local_textbook_example():
    r = align("TGTTACGG", "GGTTGACTA", "local", Scoring(3, -3, -2))
    assert r["score"] == 13 and (r["top"], r["bottom"]) == ("GTT-AC", "GTTGAC")

def test_identical():
    assert align("ACGT", "ACGT")["score"] == 4
