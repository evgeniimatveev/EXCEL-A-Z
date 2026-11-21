"""Static checks for the course files (nothing is computed).

* no spaces or non-ASCII characters in tracked file names
* .gitattributes: every rule line starts with a pattern (a line without '#' is silently ignored by git)
* every CSV / XLSX is either a well-formed Git LFS pointer or a real file that parses / opens
* every PDF opens and has at least one page
* relative links in every README point to files that exist
"""
import csv
import glob
import os
import re
import subprocess
import sys
import zipfile

from pypdf import PdfReader

csv.field_size_limit(10**8)
problems = []
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True, encoding="utf-8").stdout.splitlines()
tracked = [t.strip('"') for t in tracked]
for f in tracked:
    if " " in os.path.basename(f) or any(ord(c) > 127 for c in f):
        problems.append(f"{f}: file name has a space or a non-ASCII character")

for n, line in enumerate(open(".gitattributes", encoding="utf-8").read().splitlines(), 1):
    t = line.strip()
    if t and not t.startswith("#") and (t.startswith("---") or not re.match(r"^[\w*./\[\]-]+\s", t + " ")):
        problems.append(f".gitattributes:{n}: not a valid rule (comment lines need a leading '#'): {t[:50]}")

PTR = re.compile(r"^version https://git-lfs\.github\.com/spec/v1\noid sha256:[0-9a-f]{64}\nsize \d+\n?$")
n_ptr = n_real = n_pdf = 0
for f in tracked:
    ext = os.path.splitext(f)[1].lower()
    if ext in (".csv", ".xlsx"):
        raw = open(f, "rb").read()
        if raw.startswith(b"version https://git-lfs"):
            n_ptr += 1
            if not PTR.match(raw.decode("utf-8", "replace")):
                problems.append(f"{f}: malformed Git LFS pointer")
            continue
        n_real += 1
        if not raw.strip():
            problems.append(f"{f}: empty file")
        elif ext == ".xlsx":
            if not zipfile.is_zipfile(f) or "xl/workbook.xml" not in zipfile.ZipFile(f).namelist():
                problems.append(f"{f}: not a valid .xlsx workbook")
        else:
            try:
                rows = list(csv.reader(raw.decode("utf-8-sig", errors="replace").splitlines()))
                if len(rows) < 2:
                    problems.append(f"{f}: fewer than 2 rows")
            except csv.Error as exc:
                problems.append(f"{f}: not valid CSV: {exc}")
    elif ext == ".pdf":
        n_pdf += 1
        try:
            if len(PdfReader(f).pages) < 1:
                problems.append(f"{f}: PDF has no pages")
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{f}: unreadable PDF: {str(exc)[:80]}")

readmes = sorted(glob.glob("**/README.md", recursive=True))
for r in readmes:
    base = os.path.dirname(r)
    for target in re.findall(r"\]\(([^)\s]+)\)", open(r, encoding="utf-8").read()):
        if re.match(r"^(https?:|#|mailto:)", target):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, target.split("#")[0]))):
            problems.append(f"{r}: broken relative link '{target}'")

print(f"Checked {len(tracked)} files: {n_pdf} PDFs, {n_ptr} LFS pointers, {n_real} real data files, {len(readmes)} READMEs, {len(problems)} problem(s)")
for p in problems:
    print("FAIL ", p)
sys.exit(1 if problems else 0)
