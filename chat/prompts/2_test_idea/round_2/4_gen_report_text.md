# gen_report_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_report_text`
> Run: `run_n3CnQnOIOGY3` — Barometric Boiling Formula: Structural Error at 4000 m
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_report_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-11-22 21:36:41 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: The run's resea... [truncated, 106961 chars total]
```

### [2] SYSTEM-USER prompt · 2026-11-22 21:40:09 UTC

```
<style_check>
The draft was measured against the <writing_register> in your prompt and trips it:

- 9.2 em dashes per 1,000 words; the limit is 3. Replace them with commas, colons or full stops.

Revise the PROSE of the draft in `./paper_draft.md` to fix each point, then emit the structured output again. Numbers, claims, citations, [FIGURE:...] markers and [ARTIFACT:...] markers stay exactly as they are; do not add content and do not change results. The figures array is unchanged.
</style_check>
```

### [3] SYSTEM-USER prompt · 2026-11-22 21:40:27 UTC

```
<terminology_check>
The draft was measured against <domain_vocabulary> and trips it in 2 place(s):

- Bare label codes in the body text: C01, C02, C03, C04, C05, C06, IF97. These are the run's own internal row labels, meaningless to a reader. Name each condition, metric or variant the way the field names it, and keep the codes in the tables only.
- Undefined coinages (8): none is in the field's term list or a cited title, and none is defined at its first use or in the abstract or introduction.
- barometric-levelling, first used in: "The boiling values are taken from a barometric-levelling table on a public web page (deleze.name, per the artifact's summary), not from a verified equation or…"
- equation-derived, first used in: "The artifact records the source as equation-derived in its metadata, but that label describes the kind of table, not a derivation the run checked.* Its evidenc…"
- model-structure, first used in: "The structural term is a model-structure budget and cannot be tested against that limit."
- follow-up, first used in: "Of the sources the reviewer named, NOAA GHCN-Daily and the NIST steam-table PDF were on the planned list, and the search did not reach them, as recorded in the…"
- OCR-garbled, first used in: "Its table is OCR-garbled in the archive text, and the site elevations are not in the copies the run could read, so no row passed the drop rules."
- food-safety, first used in: "The candidate log of the test artifact ( , ) records the six sources it screened and the reason each was dropped: | Candidate | Type | Elevation | Station pres…"
- round-trip, first used in: "Those checks pass, with a round-trip error of 3.7 × 10⁻¹⁰ K and a cross-check against the package (IAPWS-97 region 4) at a maximum difference of 0.0020 K."
- pre-declared, first used in: "It requires at least 15 accepted sites and uses a pre-declared holdout (every third site after sorting by elevation)."
Clear each one in one of two ways: replace it everywhere with the field's standard name for the same thing, or define it, spelled exactly as listed, in the sentence where it first appears (or anywhere in the abstract or introduction) with a phrase such as "we define <term> as ..." or "we call ... <term>"; later uses then need nothing more. A term defined only later: move that definition to the first use.

For each one, exactly one of these applies:
1. The field already names this — use <domain_vocabulary>'s spelling everywhere
2. It is genuinely new — define it once at first use ('we call X ...', 'we define X as ...') and keep the wording identical afterwards
3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only

Rename in the section you wrote this iteration. An earlier section keeps its words unless the rename is a factual correction, and then it is marked as one. Numbers, claims, citations and every [FIGURE:...] and [ARTIFACT:...] marker stay exactly as they are. Save the text to `./paper_draft.md`, then emit the structured output again.
</terminology_check>
```
