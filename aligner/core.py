"""Needleman-Wunsch (global) and Smith-Waterman (local) alignment."""
from dataclasses import dataclass

STOP, DIAG, UP, LEFT = 0, 1, 2, 3

@dataclass
class Scoring:
    match: int = 1
    mismatch: int = -1
    gap: int = -2

def align(a, b, mode="global", s=Scoring()):
    n, m = len(a), len(b)
    local = mode == "local"
    H = [[0] * (m + 1) for _ in range(n + 1)]
    T = [[STOP] * (m + 1) for _ in range(n + 1)]
    if not local:
        for i in range(1, n + 1): H[i][0], T[i][0] = i * s.gap, UP
        for j in range(1, m + 1): H[0][j], T[0][j] = j * s.gap, LEFT

    best, best_pos = 0, (0, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = s.match if a[i - 1] == b[j - 1] else s.mismatch
            diag, up, left = H[i-1][j-1] + sub, H[i-1][j] + s.gap, H[i][j-1] + s.gap
            score = max(diag, up, left)
            ptr = DIAG if score == diag else UP if score == up else LEFT
            if local and score <= 0:
                score, ptr = 0, STOP
            H[i][j], T[i][j] = score, ptr
            if local and score > best:
                best, best_pos = score, (i, j)

    i, j = best_pos if local else (n, m)
    total = best if local else H[n][m]
    top, bot, path = [], [], [(i, j)]
    while T[i][j] != STOP:
        p = T[i][j]
        if p == DIAG:   top.append(a[i-1]); bot.append(b[j-1]); i -= 1; j -= 1
        elif p == UP:   top.append(a[i-1]); bot.append("-");    i -= 1
        else:           top.append("-");    bot.append(b[j-1]); j -= 1
        path.append((i, j))
    top, bot = "".join(reversed(top)), "".join(reversed(bot))
    mid = "".join("|" if x == y else " " for x, y in zip(top, bot))
    return {"score": total, "top": top, "middle": mid, "bottom": bot,
            "matrix": H, "path": path[::-1]}
