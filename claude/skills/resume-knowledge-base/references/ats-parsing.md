# How Hiring Tools (ATS) Actually Parse Resumes

A resume passes two gates: (1) an **ATS parser** turns the file into a JSON record
that recruiters later search by keyword; (2) a **human** skims the parsed-clean
resume for ~6 seconds. If the parse scrambles, the candidate is invisible no
matter how strong they are. This file explains the machine so the resume clears
gate one. (Grounded in IEEE 2023 parsing-accuracy work + Workday/Greenhouse/
Lever/iCIMS/Taleo behavior reports.)

## The 5-stage parser pipeline (failures cascade)
1. **Text extraction** — PDF/DOCX bytes → character stream. Multi-column PDFs get
   read left-to-right across the page, interleaving the two columns into garbage.
2. **Tokenization** — split into words/numbers/punctuation. Unicode glyphs and
   custom icons create phantom tokens that confuse later stages.
3. **Section segmentation** — classify lines as Header / Summary / Experience /
   Education / Skills using regex + classifiers. Non-standard labels like "Career
   Journey" get misfiled.
4. **Named Entity Recognition (NER)** — tag PERSON, ORG, DATE, TITLE, SKILL,
   EMAIL, PHONE. Contact ~99% accurate; **skills only 70–90%** (open vocabulary,
   compositional).
5. **Structured output** — assemble into the JSON the ATS stores and recruiters
   query. Commercial parsers hit ~87% field accuracy vs ~96% human — ~1 wrong
   field in 8 even on a clean doc.

## Top failure modes (by frequency)
- **Multi-column scramble (~34%)** — #1 killer. "SQL Senior Product Manager
  Python" gets tagged as one job title.
- **Header/footer ghosts (~22%)** — contact info in a Word header/footer layer is
  skipped → "candidate has no email."
- **Non-standard section labels (~17%)** — use exact "Experience", "Education",
  "Skills", "Projects".
- **Date format breaks (~15%)** — mixing "Jan 2024" and "January '24" corrupts the
  whole employment timeline. Use **"Mon YYYY"** consistently.
- **Special characters (~12%)** — Unicode arrows/checkmarks/emoji tokenize as
  unknown entities; can even trigger false section boundaries.

## Platform notes
- **Greenhouse** — friendliest; preserves bullets; recruiter usually reads the
  actual PDF with parsed fields as metadata. Fails on weird section labels.
- **Lever** — forgiving on contact; aggressively drops sidebar/column content;
  truncates long skill lists.
- **Workday** — strict dates (MM/YYYY), merges bullets into one string, drops
  multi-word soft skills; handles DOCX cleanly.
- **iCIMS** — flags uncertain fields for manual review; drops content when unsure.
- **Taleo** — oldest/strictest; exact labels + MM/YYYY; silently deletes content;
  keeps only the first bullet sometimes; struggles with two-line company headers.

## Parser-safe ruleset
- Single-column **body** (the part that holds experience). No tables for
  experience/education content.
- Contact info in the document body text, never only in a header/footer layer.
- Exact section headers: Experience, Education, Skills, Projects.
- Dates as "Mon YYYY" everywhere; for strict portals use MM/YYYY.
- Standard round bullets; avoid decorative Unicode/icon glyphs as bullets.
- Skills as bare comma-separated tokens in a dedicated section.
- Spell acronyms once: "Extract, Transform, Load (ETL)", "Search Engine
  Optimization (SEO)".
- No text baked into images/graphics — it's invisible to extraction.
- When a portal accepts DOCX, DOCX parses more reliably than PDF.
- **No white-text / hidden keyword stuffing** — parsers and recruiters detect it;
  it gets resumes rejected. Win on real keyword match, not tricks.

## Two template tiers (see assets/resume-template.tex)
- **Styled tier (default)** — the candidate's house template: single-column body,
  but with tcolorbox section headers, fontawesome icons, and a two-column header.
  Parses well where humans read the PDF — **startups, founder's office, most
  product & consulting roles**. This is the default.
- **ATS-pure tier** — strip the tcolorbox boxes (use plain `\section` rule
  headers), remove icons, single-column header. Generate this when applying
  through **strict enterprise portals (Workday, Taleo, iCIMS)** or when the user
  says a company uses one. Same content, maximally safe formatting.

**Bottom line:** formatting only clears the technical threshold. Clean parse +
weak content still loses. Content (next files) is what wins the human.
