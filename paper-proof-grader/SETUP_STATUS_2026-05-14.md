# Paper Proof Grader setup status

Checked: 2026-05-14 00:00 local
Reviewer: codex-forge

## Ready state

- Runtime root: `\\dlowenas\brain\paper-proof-grader`
- Mirror/root path also reachable: `X:\paper-proof-grader`
- Drop folder: `\\dlowenas\paper-proof-grader\DROP_PAPERS_HERE`
- Output folder: `\\dlowenas\paper-proof-grader\OUTPUT`
- Archive folder: `\\dlowenas\paper-proof-grader\ARCHIVE`
- Runner: `\\dlowenas\paper-proof-grader\RUN.bat`
- Direct command: `C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe \\dlowenas\paper-proof-grader\pipeline.py`

## Verification

- Python 3.13.13 is available.
- `openpyxl` imports successfully, so Excel output support is available.
- `DROP_PAPERS_HERE` was empty at setup time.
- Smoke run completed cleanly with 0 candidate files and no errors.

## Next run

Drop one `.txt`, `.md`, `.html`, or `.htm` paper into `DROP_PAPERS_HERE`, then run `RUN.bat`.
