"""Brute force vs memoized recursion: the 'before DP' story."""
from functools import lru_cache
import time

def brute_force_score(a, b, match=1, mismatch=-1, gap=-2):
    """Tries every alignment. O(3^n): unusable beyond ~12 letters."""
    def rec(i, j):
        if i == len(a): return (len(b) - j) * gap
        if j == len(b): return (len(a) - i) * gap
        sub = match if a[i] == b[j] else mismatch
        return max(sub + rec(i + 1, j + 1), gap + rec(i + 1, j), gap + rec(i, j + 1))
    return rec(0, 0)

def memo_score(a, b, match=1, mismatch=-1, gap=-2):
    """Same recursion plus a cache. O(n*m)."""
    @lru_cache(maxsize=None)
    def rec(i, j):
        if i == len(a): return (len(b) - j) * gap
        if j == len(b): return (len(a) - i) * gap
        sub = match if a[i] == b[j] else mismatch
        return max(sub + rec(i + 1, j + 1), gap + rec(i + 1, j), gap + rec(i, j + 1))
    return rec(0, 0)

if __name__ == "__main__":
    import random
    print("length  brute(s)  memo(s)")
    for n in (4, 6, 8, 10, 11):
        a = "".join(random.choices("ACGT", k=n)); b = "".join(random.choices("ACGT", k=n))
        t = time.perf_counter(); brute_force_score(a, b); t1 = time.perf_counter() - t
        t = time.perf_counter(); memo_score(a, b); t2 = time.perf_counter() - t
        print(f"{n:<7} {t1:<9.5f} {t2:.5f}")
