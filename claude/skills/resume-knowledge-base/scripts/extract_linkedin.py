#!/usr/bin/env python3
"""Extract text from a LinkedIn export / resume PDF, page by page.

Usage:
    python3 extract_linkedin.py "/path/to/profile.pdf"

Prints all text grouped by page so the calling agent can read the source data.
If pdfplumber is not installed, prints install instructions and exits non-zero.
"""
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 extract_linkedin.py <path-to-pdf>", file=sys.stderr)
        return 2
    path = sys.argv[1]
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        print(
            "pdfplumber is not installed. Install it with:\n"
            "    pip3 install pdfplumber\n"
            "Then re-run this script.",
            file=sys.stderr,
        )
        return 3
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                print(f"===== PAGE {i} =====")
                print(page.extract_text() or "(no extractable text on this page)")
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
