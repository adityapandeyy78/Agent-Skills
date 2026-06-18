#!/usr/bin/env python3
"""Compile a .tex resume to PDF using whatever LaTeX engine is available.

Usage:
    python3 compile_resume.py "/path/to/resume.tex"

Tries tectonic, then xelatex, then pdflatex. The template uses fontawesome5,
tcolorbox, newtxsf, etc. — a full TeX distribution (TeX Live / MacTeX) or
tectonic is needed. If no engine is found, prints Overleaf guidance.
"""
import os
import shutil
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 compile_resume.py <path-to-.tex>", file=sys.stderr)
        return 2
    tex = os.path.abspath(sys.argv[1])
    if not os.path.exists(tex):
        print(f"File not found: {tex}", file=sys.stderr)
        return 4
    workdir = os.path.dirname(tex)
    base = os.path.basename(tex)

    if shutil.which("tectonic"):
        cmd = ["tectonic", base]
    elif shutil.which("xelatex"):
        cmd = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", base]
    elif shutil.which("pdflatex"):
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", base]
    else:
        print(
            "No LaTeX engine found (tried tectonic, xelatex, pdflatex).\n"
            "Options:\n"
            "  1) Install one:  brew install tectonic   (lightweight, recommended)\n"
            "                   or install MacTeX/TeX Live.\n"
            "  2) Compile online: upload the .tex to https://overleaf.com and\n"
            "     click Recompile (set compiler to XeLaTeX for the fonts/icons).",
            file=sys.stderr,
        )
        return 5

    # pdflatex/xelatex usually need two passes for layout to settle.
    passes = 1 if cmd[0] == "tectonic" else 2
    for n in range(passes):
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stdout[-3000:], file=sys.stderr)
            print(proc.stderr[-1500:], file=sys.stderr)
            print(f"\nLaTeX compile failed on pass {n + 1}.", file=sys.stderr)
            return 6

    pdf = os.path.splitext(tex)[0] + ".pdf"
    if os.path.exists(pdf):
        print(f"OK -> {pdf}")
        return 0
    print("Compiler ran but no PDF was produced.", file=sys.stderr)
    return 7


if __name__ == "__main__":
    raise SystemExit(main())
