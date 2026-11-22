# Barometric boiling-point report (iteration 1)

Internal research report for the question: how well does a simple barometric formula, combined with the water saturation curve, predict the boiling point of water at altitude, compared with published measurements?

## What is here

- `paper_draft.md`: the report. Framing, then the iteration 1 section (strategy, three artifacts, tables, dead ends, result), then "What we have learned so far" and references.
- `figures/fig1_spec.json`, `figures/fig1_v1.png`, `figures/fig1_v1.pdf`: the chart of the structural term against altitude, rendered with the data-figure skill from the nine 500 m values in the experiment's grid output.
- `references.bib`, `references.json`: the one fetched entry (Wagner and Pruß 2002).
- `.aii/manifest.yaml`: storage manifest. This directory holds only text and one small chart, so the manifest has no entries.

## Artifacts summarised in the report

- Reference table of boiling temperature versus elevation (dataset, `art__Ga8TbdhmlP8`). Equation-derived. No measured records.
- Reference-grid screen of isothermal and lapse-rate barometric forms (experiment, `art_YU39iUPrFWbZ`).
- Screen of constant and temperature-dependent latent heat Clausius-Clapeyron and an Antoine fit against the IAPWS-IF97 saturation curve (experiment, `art_jKGn4P2Rlpy1`).

The artifact workspaces hold the code and full output files. They sit on the run's storage volume, not in this repository.

- `style_exemplars.md`: verbatim passages from three arXiv papers on water phase behaviour and boiling (abstracts, two results or conclusion passages), with section outlines for the two papers whose full text was read.
- `domain_terms.json`: 68 terms the field uses, each with a gloss and the title it came from. Several entries come from titles seen in search results, not from full texts.
- `field_extras.json`: three extras seen in the exemplar papers, each with what an experiment would need to save.

## Not done in this iteration

- Measured boiling-point records: none were obtained. Three candidate sources could not be read. The Miller (2016) BAMS PDF appeared in a search result but returned HTTP 403 on fetch.
- Weather (station pressure) comparison: not run.
- The exemplar set is drawn from physics papers on water and boiling, not from atmospheric or metrology papers, because the closest open-access atmospheric papers were not fetchable as text.

## Restoring removed files

Nothing was marked for deletion. No restore steps are needed.
