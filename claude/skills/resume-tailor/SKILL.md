---
name: resume-tailor
description: >-
  Tailor a resume to a specific job description, sharpen/rewrite the bullet points
  of any experience, or draft new bullet points/content to add — all in the
  candidate's verified facts and house voice (one-line, strong, honest, formal yet
  eye-catching), targeted at Data Analyst, Founder's Office, Product, or Consulting
  roles. Use this skill whenever the user wants to tailor/customize a resume for a
  JD, "make these bullets stronger / one-liner / not bluffing", "improve my
  experience points", "what points should I add for X role", "optimize my resume
  for ATS", or pastes a job description and asks to align the resume. Outputs
  ready-to-paste LaTeX (\resumeItem{...}) and can compile to PDF. Reads the shared
  resume-knowledge-base for facts, strategy, voice, and template.
---

# Resume Tailor

Tailor and sharpen the candidate's resume. Three common modes — figure out which
the user wants (ask if unclear), then execute.

## Always start here (load the knowledge base)
Base: `/Users/aditya.pandey/.claude/skills/resume-knowledge-base/`

1. Read `references/candidate-profile.md` — the **only** source of facts. Never
   invent metrics, tools, employers, or dates. If something's missing, ask.
2. Read `references/bullet-writing.md` — the house voice (one line; strong but no
   bluffing/over-confidence; XYZ shape; quantify honestly; bold 2–4 phrases).
3. Read `references/role-playbooks.md` for the target role (and section order).
4. Read `references/ats-parsing.md` only if formatting/ATS-pure questions come up.

If the user hasn't said the target role, ask which of: Data Analyst / Founder's
Office / Product / Consulting.

## Mode A — Tailor the whole resume to a JD
The user pastes/links a job description (or names a company+role).

1. Extract the JD's **must-have keywords, tools, and priorities** (its exact
   words — "Power BI" not "BI tool"). List them back briefly.
2. Map each against the profile: which she truly has (weave in), which she lacks
   (do NOT claim — note the gap to the user; suggest if a true adjacent skill
   covers it).
3. Reorder/select sections per the role playbook; lead with the most JD-relevant
   experience; cut or compress off-target roles.
4. Rewrite bullets in the house voice, front-loading JD keywords she genuinely
   matches. Keep one page.
5. Produce the filled `assets/resume-template.tex` (copy it, edit the marked
   regions). Save as `<Name>_<Role>_Resume.tex` where the user wants (ask;
   default beside their existing resume).
6. Offer to compile: `python3 <base>/scripts/compile_resume.py "<file.tex>"`.
7. Report: keywords matched, anything you cut and why, and **every gap** where the
   JD wants something she hasn't shown (so she can confirm or supply it).

## Mode B — Improve / sharpen bullets for an experience
The user gives an experience (or pastes existing bullets) and says e.g. "make
these one-liner, strong, not bluffing, formal but eye-catching."

1. Rewrite each bullet to the house voice — same count and order, each fits one
   line, strong action verb, real tool, honest scope, a true number where the
   profile has one.
2. Return them ready to paste as `\resumeItem{...}` (bold the 2–4 highest-signal
   phrases). Then, in one line, flag anything you changed because a claim wasn't
   supported, or any `[needs metric: ...]` you couldn't fill.
3. Do not add scale or outcomes she didn't state. If a bullet is weak only
   because a number is missing, ask for the number rather than inventing one.

## Mode C — Draft new points / content to add
The user asks "what should I add for a <role> resume" for an experience/project.

1. Propose 2–4 candidate bullets grounded ONLY in facts from the profile (or what
   the user states), aligned to the target role's keyword bank.
2. Mark any bullet that needs a number the user must supply as
   `[needs metric: ...]`. Never fabricate one.
3. Present them in house voice, paste-ready, and say which existing bullet (if
   any) each could replace.

## Output discipline
- Default deliverable for a full tailor: the edited `.tex` (and PDF if compiled).
- Default deliverable for bullet work: paste-ready `\resumeItem{...}` lines.
- Always keep the resume to **one page** for this candidate.
- Never multi-column the body; keep dates "Mon YYYY"; spell acronyms once.
- For strict enterprise portals (Workday/Taleo/iCIMS), offer the ATS-pure variant
  (see `references/ats-parsing.md`).
