---
name: cover-letter-writer
description: >-
  Write a role-aligned cover letter that sounds like a real final-year Indian
  student wrote it — simple, honest English, NOT AI-generated, not corporate or
  flowery. Use this skill whenever the user wants a cover letter, "write a cover
  letter for this JD", "draft a covering letter", "cover note for this
  application", or asks to pair a cover letter with a tailored resume — for Data
  Analyst, Founder's Office, Product, or Consulting roles. Aligns to the specific
  role/company, avoids AI tells (no "I am writing to express", no em-dashes, no
  "leverage/delve/passionate"), and uses only verified facts. Reads the shared
  resume-knowledge-base for the candidate's profile, role strategy, and the cover-
  letter voice rules.
---

# Cover Letter Writer

Write a cover letter that a recruiter believes a human student actually wrote, and
that clearly fits the role. Plain, warm, specific, honest.

## Always start here (load the knowledge base)
Base: `/Users/aditya.pandey/.claude/skills/resume-knowledge-base/`

1. Read `references/cover-letter-style.md` — the voice (simple Indian student
   English), the anti-AI banned-phrase list, structure, and length. This governs
   how it reads.
2. Read `references/candidate-profile.md` — the only source of facts. Use real
   stories (e.g. 10K+ records ETL, working with the founder, a project/case
   study). Never invent.
3. Read `references/role-playbooks.md` for the target role so the letter mirrors
   what that role values — in plain prose, not keyword lists.

## What to confirm before writing (ask if missing)
- **Target role** (Data Analyst / Founder's Office / Product / Consulting) and
  **company name**.
- **The JD** if available (paste/link) — best source for what to emphasize.
- **One genuine reason she likes this company/product.** If she hasn't given one,
  ask — do not invent a fake reason. A real, specific hook is what kills the
  "AI smell".
- Who to address it to (hiring manager name if known, else "Dear Hiring Team,").

## How to write it
1. Pick **1–2 real stories** from the profile that fit the role (don't restate the
   whole resume). Tell each simply: what she did, what came out of it.
2. Follow the structure in `cover-letter-style.md`: opening (role + true reason
   for this company, no "I am writing to..."), 1–2 body paragraphs (the stories),
   short honest closing. ~250–320 words, 3–4 short paragraphs.
3. Obey the anti-AI rules hard: no em-dashes; no "leverage/delve/synergy/
   passionate about/honed/spearheaded/robust/moreover/furthermore"; no empty
   superlatives; vary sentence rhythm; let it be plain and a little personal.
4. Match the story to the role — don't pitch content writing for a Data Analyst
   seat.

## Output
- Deliver the letter as plain text by default (easy to paste into an email or
  portal). Offer a matching `.tex`/PDF version only if the user wants a formatted
  letter to attach.
- After the draft, point out (one line) any place you had to leave generic
  because a real detail was missing, and ask for it so the letter gets sharper.

## Honesty check before sending
Re-read once: does every claim trace to the profile or something the user said?
Does it sound like a person, not a template? Did any banned phrase or em-dash
sneak in? Fix, then deliver.
