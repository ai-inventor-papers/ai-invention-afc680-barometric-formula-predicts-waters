# Measured Boiling-Point Records by Altitude: source search (run result: 0 verified Tier A rows)

## What was done
Searched for measured water boiling temperatures paired with elevation and station pressure, as the artifact plan asks.
Eight broad searches (general and scholarly), follow-up fetches, one Hugging Face search, and a grep of the 1857 Forbes paper.

## Result
- Tier A (measured boiling temperature plus same-site station pressure, same time window): **0 verified rows**.
  The 25-site target is not met, and no held-out set is defined.
- The records file `temp/datasets/measured_boiling_point_records_full.json` is schema-valid with an empty `records` array.
  Mini and preview copies are identical to it because there are no rows to truncate.
- Forbes (1857) measured the boiling point with barometer pairs at Alpine sites. It is the strongest lead, with 17 pairs
  (count taken from the R package documentation). Its table is OCR-garbled, and elevations are not in the R copies, so no row was added.
  Transcribing the table from the page image with cited elevations is the next step.

## Layout
- `temp/datasets/measured_boiling_point_records_full.json`: dataset file (empty records, metadata with tier definitions)
- `temp/datasets/measured_boiling_point_records.schema.json`: JSON Schema for a record (Tier A/B/C, elevation uncertainty at most 30 m)
- `temp/datasets/candidates.json`: each candidate source, its URL, access date, tier and status
- `temp/datasets/drop_log.json`: drop reasons
- `search/`: raw search and fetch outputs, kept as citation notes
- `.aii/manifest.yaml`: heavy-path decisions (none needed)

## Restoring removed files
No heavy files were deleted. Nothing needs restoring.
