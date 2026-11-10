from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from aligner.core import align, Scoring

app = FastAPI(title="DNA Sequence Aligner")
MAX_LEN = 1500

class AlignRequest(BaseModel):
    seq1: str
    seq2: str
    mode: str = "global"
    match: int = 1
    mismatch: int = -1
    gap: int = -2

def clean(seq: str) -> str:
    """Accepts plain text or FASTA (header lines are dropped)."""
    lines = [l for l in seq.splitlines() if not l.startswith(">")]
    return "".join("".join(lines).split()).upper()

@app.post("/align")
def run(r: AlignRequest):
    a, b = clean(r.seq1), clean(r.seq2)
    if not a or not b:
        raise HTTPException(400, "Enter both sequences.")
    if len(a) > MAX_LEN or len(b) > MAX_LEN:
        raise HTTPException(400, f"Each sequence can have at most {MAX_LEN} letters.")
    if r.mode not in ("global", "local"):
        raise HTTPException(400, "Mode must be global or local.")
    res = align(a, b, r.mode, Scoring(r.match, r.mismatch, r.gap))
    return {**res, "seq1": a, "seq2": b}

app.mount("/", StaticFiles(directory="static", html=True), name="static")  # keep last
