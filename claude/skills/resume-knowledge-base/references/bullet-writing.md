# Bullet Writing — The House Voice

Every resume bullet must sound like the candidate's own confident-but-honest
voice. This is the single most important style file.

## The house tone (non-negotiable)
- **One line each.** A bullet must fit on a single line in the template (≈ 1 to
  1.5 lines max). If it spills to a second line, cut words, not meaning.
- **Strong and eye-catching**, but **formal**. It should make a recruiter pause —
  through a real result or sharp verb, never through hype.
- **No bluffing, no over-confidence.** Don't claim "spearheaded a company-wide
  transformation" for an intern task. Don't add a number she didn't give. Don't
  use "expert", "guru", "world-class", "revolutionary", "passionate". Confidence
  comes from concrete scope + outcome, not adjectives.
- **Honest scope.** An intern *contributed to / supported / built / analyzed* —
  she didn't single-handedly run the company. Match the verb to the real role.
- **No fluff connectors.** Drop "responsible for", "worked on", "helped to",
  "various", "successfully", "in order to".

## The XYZ shape (use for most bullets)
> **Accomplished [X] measured by [Y] by doing [Z].**
Start with a strong past-tense action verb → what you did (with the real tool) →
the measurable result. Lead with impact when the number is the headline.

**Action verbs (pick precise ones):** Built, Designed, Developed, Analyzed,
Automated, Integrated, Led, Launched, Drove, Optimized, Translated, Conducted,
Modeled, Delivered, Streamlined, Identified, Improved, Reduced, Scaled.

## Quantify honestly
- Use a number whenever the profile has one (10K+ records, 40% retention, 25%
  MoM, 30% adoption, 25K+ rows, 95% accuracy, 12 influencers, 500+ users/
  participants, 6 GDSCs).
- If a bullet needs a number she never gave, **either ask the user for it or
  write the bullet around concrete scope/action instead** — never fabricate.
- Numbers carry more weight than adjectives. Replace "significantly improved" →
  "improved X by 30%".

## Keywords
- Weave the role's exact keywords (see role-playbooks.md) and the JD's exact tool
  names into bullets naturally — recruiters search the parsed JSON for them.
- Name specific tools: "Tableau", not "BI software"; "PostgreSQL", not "a
  database". Spell each acronym once: "Extract, Transform, Load (ETL)".

## Bolding (template uses \textbf for skim-scannability)
Bold the **2–4 highest-signal phrases** per bullet — the tool, the metric, the
outcome. Don't bold half the sentence; over-bolding reads as shouting.

## Length budget
- Current/most-relevant role: 3 bullets. Older/tangential: 1–2.
- Projects: 2 bullets. Leadership: 1 line each.

## Before / after (the voice in action)

**Vague →**
- ✗ "Responsible for working on data and helping the team with various analysis
  tasks to improve things."
- ✓ "Built **ETL pipelines** over **10K+ product records** for cleaning and EDA,
  surfacing seasonal trends that informed **pricing strategy**."

**Over-confident / bluffing →**
- ✗ "Single-handedly revolutionized the company's entire product strategy and
  drove massive growth."
- ✓ "Worked directly with the **Founder** on product strategy and monetization,
  contributing to decisions across product, ops, and revenue."

**Two lines → one line →**
- ✗ "Conducted a comprehensive market and competitor analysis exercise in order
  to identify a range of different product growth opportunities for the team,
  which helped onboard influencers and users."
- ✓ "Ran **market & competitor analysis** to find growth levers, onboarding **12
  influencers** and **500+ users** in 6 weeks."

## When asked only to "improve / sharpen bullets"
Return the rewritten bullets in the same count and order, each one-line, in the
house voice above, ready to paste into `\resumeItem{...}`. If you changed scope
or dropped a claim because it wasn't supported, say so in one line after.

## When asked to "give content / points to add"
Propose 2–4 candidate bullets grounded ONLY in facts from candidate-profile.md or
what the user states. Mark any bullet that needs a number from the user as
`[needs metric: ...]` rather than inventing one.
