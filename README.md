
# DNA-SEQUENCE-ALLIGNER-

# DNA Sequence Aligner

Global (Needleman-Wunsch) and local (Smith-Waterman) alignment with a visual
traceback, built from scratch with dynamic programming.

## Run
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload
Open http://127.0.0.1:8000

## Test and benchmark
    pytest
    python -m aligner.brute         # brute force vs memoized timing

## Layout
    aligner/core.py    the DP algorithms (start reading here)
    aligner/brute.py   brute force and memoized versions
    main.py            FastAPI server (POST /align, docs at /docs)
    static/index.html  the UI

