---
name: resume-knowledge-base
description: >-
  Shared knowledge base for resume and cover-letter work — the candidate's
  verified profile (single source of truth), how ATS parsers work
  (Workday/Greenhouse/Lever/iCIMS/Taleo), role playbooks (Data Analyst, Founder's
  Office, Product, Consulting), the house bullet-writing voice, cover-letter style
  rules, and the canonical LaTeX template. This is a REFERENCE skill consumed by
  the `resume-tailor` and `cover-letter-writer` skills; consult it whenever
  working on a resume, CV, bullet points, or cover letter so facts, formatting,
  and voice stay consistent. Don't invent facts — everything must trace back to
  candidate-profile.md or what the user states.
---

# Resume Knowledge Base

This skill is a **library**, not a workflow. It is the single, consistent source
of facts, strategy, formatting, and voice that the two action skills draw from:

- **resume-tailor** — tailors the resume to a JD, sharpens bullets, drafts new
  points.
- **cover-letter-writer** — writes role-aligned cover letters in simple Indian
  student English.

When you (or another skill) do resume/cover-letter work, read the relevant file
below. Paths are given absolute so the action skills can reference them directly.

## The one rule above all
**Never fabricate.** Employers, titles, dates, metrics, tools, and credentials
must come from `references/candidate-profile.md` or from what the user says in the
conversation. If a JD or bullet needs something not on record, **ask the user** —
do not guess or inflate. A made-up resume is worse than a modest true one.

## Contents

Base path: `/Users/aditya.pandey/.claude/skills/resume-knowledge-base/`

| File | Read it when you need… |
|------|------------------------|
| `references/candidate-profile.md` | Any fact about the candidate (contact, experience, projects, skills, education, leadership). The source of truth. |
| `references/ats-parsing.md` | To justify/choose formatting; the parser-safe ruleset; styled vs ATS-pure template tiers. |
| `references/role-playbooks.md` | Per-role angle, keyword bank, what to lead with vs cut, section order — Data Analyst / Founder's Office / Product / Consulting. |
| `references/bullet-writing.md` | The house bullet voice: one line, strong, honest (no bluffing), XYZ shape, quantify-honestly, bolding. |
| `references/cover-letter-style.md` | Simple Indian student English, anti-AI rules, cover-letter structure. |
| `assets/resume-template.tex` | The canonical LaTeX template (Sakshi's house format) to edit. |
| `scripts/extract_linkedin.py` | Extract text from a LinkedIn/resume PDF. |
| `scripts/compile_resume.py` | Compile a `.tex` to PDF (tectonic/xelatex/pdflatex, else Overleaf guidance). |

## Keeping it current
When the user shares a new fact (a metric, a new role, an award, a new target
JD's must-have skill she actually has), update `references/candidate-profile.md`
so future runs stay consistent.
