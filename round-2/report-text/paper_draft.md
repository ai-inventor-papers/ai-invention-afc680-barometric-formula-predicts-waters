# Barometric pressure, saturation vapour pressure and the boiling point of water with altitude: internal research report

## Framing

This run asks how well a simple barometric formula predicts the boiling point of water at altitude, compared with published measurements. The hypothesis couples a barometric pressure-altitude formula to the saturation vapour pressure curve of water (the Wagner and Pruß formulation, [1]) and predicts that the calculated boiling temperature matches measured values to about ±0.3 °C from sea level to 4,000 m when station pressure is used, and to about 0.6 °C when only altitude is known and standard-atmosphere pressure is assumed. The hypothesis also predicts that most of the residual comes from weather-driven pressure deviations, and that the structural difference between the isothermal and the lapse-rate barometric forms is about 0.3 °C at 3,000 m and 0.5 °C at 4,000 m.

Testing the claim needs three things: measured boiling records with paired station pressure and elevation, a saturation curve, and the barometric chain that connects them. The run tried to collect the first and did not succeed. Its evidence so far is therefore a model-to-reference screen of the physics chain, plus a dataset calculated from published equations and not measured. The measured comparison that the hypothesis asks for has not been run. The sections below record each step in the order it ran.

# Iteration 1

## Strategy

The first iteration had three aims, in this order:

1. Collect published site records (elevation, station pressure, observed boiling temperature) so that the predicted and observed boiling points could be compared directly.
2. Screen the barometric formulas against a reference pressure model and the water saturation curve, so that the size of the structural term is known before weather is added.
3. Screen cheaper closed-form alternatives (constant and temperature-dependent latent heat Clausius-Clapeyron, and an Antoine fit) against the same reference curve, because these are the shortcuts a practitioner would use.

The reviewer feedback that prompted this iteration's new artifacts is not reproduced in the inputs to this section. The iteration's three artifacts are the ones listed below, and their own summaries state what they did and did not test.

The first aim failed. Candidate site papers were retrieved and then dropped, for the reasons in the drop log of the reference-table artifact: the Bhutto (2024) desk study on pressure and boiling point in Pakistan, the Harrison and Marlow (2020) note in *Weather*, and the Miller (2016) methods paper in *BAMS* could not be read (HTTP 403 on the publisher page and the journal full text), so no site record was extracted from any of them. No measured record was verified. The measured-site count is zero, and the holdout set the hypothesis asks for is empty.

Because of that, the iteration's experiments were run against the reference equations only. Each experiment states this in its own summary, and this section keeps the same limit.

## Artifacts run this iteration

### Artifact A: reference table of boiling temperature versus elevation (dataset)

[ARTIFACT:art__Ga8TbdhmlP8]

This artifact is a 41-row table of boiling temperature from 0 to 4,000 m in 100 m steps. *Correction (iteration 2, reviewer item on provenance): the earlier wording "each row is calculated from a published equation" is withdrawn. The boiling values are taken from a boiling-temperature-by-elevation table on a public web page (deleze.name, per the artifact's summary), not from a verified equation or from field measurements. The artifact labels the rows as calculated rather than measured in its metadata, but that label describes the kind of table, not a derivation the run checked.* Its evidence type is recorded in every row as `equation_derived`. The table was built so that a later step could add measured sites under the same schema, with a predefined holdout rule (measured sites in the Americas above 1,000 m), but none were added.

The artifact also carries a formula check. It compares each row's table value with an altitude-to-boiling-point calculation built from the U.S. Standard Atmosphere 1976 troposphere pressure and an empirical pressure-to-boiling-point fit. I recomputed the residuals from the 41 rows. The mean residual is −0.004 °C and the largest absolute residual is 0.21 °C. Table 1 gives the rows at 500 m steps; the full set of 41 rows is in the artifact's output file.

**Table 1.** Reference table rows at 500 m steps, with the formula check from the same artifact. Values are from `full_data_out.json`. Residual is table value minus formula value, in °C.

| Elevation (m) | Table boiling temperature (°C) | Formula boiling temperature (°C) | Residual (°C) |
|---|---|---|---|
| 0 | 100.0 | 100.01 | 0.01 |
| 500 | 98.3 | 98.38 | 0.08 |
| 1,000 | 96.7 | 96.73 | 0.03 |
| 1,500 | 95.0 | 95.06 | 0.06 |
| 2,000 | 93.3 | 93.38 | 0.08 |
| 2,500 | 91.7 | 91.67 | −0.03 |
| 3,000 | 90.0 | 89.95 | −0.05 |
| 3,500 | 88.3 | 88.20 | −0.10 |
| 4,000 | 86.6 | 86.43 | −0.17 |

The agreement in this table is between two equation-based calculations. It does not test the barometric chain against measurements. The artifact says the same, and this report does not treat the agreement as validation.

### Artifact B: reference-grid screen of the isothermal and lapse-rate barometric forms (experiment)

[ARTIFACT:art_YU39iUPrFWbZ]

This experiment asks how far the isothermal barometric formula (one scale height, about 8,435 m, from RT/Mg at 288.15 K) departs from the standard lapse-rate form (L = 6.5 K/km) once each is converted to a boiling temperature with the water saturation curve. The standard lapse-rate form is also the reference pressure model (the U.S. Standard Atmosphere 1976 troposphere), so its own error is zero by construction. The only informative error is the isothermal form against that reference. The structural term is the difference between the two boiling temperatures.

The saturation curve is the Wagner and Pruß formulation, inverted by bisection. Its checks passed: the boiling temperature at 101,325 Pa is 373.1243 K (99.9743 °C), and the inversion error, the relative difference between the saturation pressure at the inverted temperature and the input pressure, is 4.2 × 10⁻¹⁵. A separate calculation with the `iapws` package reproduces the sea-level boiling temperature and the altitude values at 0, 2,000 and 4,000 m to within 0.00024 K. The lapse-rate pressures reproduce the tabulated standard-atmosphere nodes to within 0.0073 %. *Correction (iteration 2): the node values in `method.py` are typed in from a standard-atmosphere table recalled while the run was built, not read from the primary source. The 0.0073 % figure therefore checks the formula against remembered values. It is not a verification of the reference against the document.*

**Table 2.** Boiling temperature and structural term at 500 m steps. Values are from the experiment's `grid_values.csv`. Columns: reference pressure model with the lapse-rate form (which is the reference), isothermal form, structural term (isothermal minus lapse-rate, in K). Temperatures in °C.

| Altitude (m) | Reference pressure (Pa) | Isothermal pressure (Pa) | Reference boiling (°C) | Isothermal boiling (°C) | Structural term (K) |
|---|---|---|---|---|---|
| 0 | 101,325.0 | 101,325.0 | 99.97430 | 99.97430 | 0.000000 |
| 500 | 95,460.8 | 95,493.0 | 98.31248 | 98.32182 | 0.009342 |
| 1,000 | 89,874.6 | 89,996.7 | 96.64875 | 96.68602 | 0.037271 |
| 1,500 | 84,556.0 | 84,816.7 | 94.98298 | 95.06663 | 0.083651 |
| 2,000 | 79,495.2 | 79,934.9 | 93.31504 | 93.46340 | 0.148352 |
| 2,500 | 74,682.5 | 75,334.0 | 91.64482 | 91.87607 | 0.231254 |
| 3,000 | 70,108.5 | 70,998.0 | 89.97217 | 90.30442 | 0.332247 |
| 3,500 | 65,764.1 | 66,911.5 | 88.29696 | 88.74819 | 0.451227 |
| 4,000 | 61,640.2 | 63,060.3 | 86.61905 | 87.20715 | 0.588101 |

The isothermal form predicts too high a pressure at every altitude above zero, and the gap grows with height. At 4,000 m the isothermal pressure is about 2.3 % above the reference, and the boiling temperature is about 0.59 K high.

[FIGURE:fig1]

Table 2 gives the structural term at 500 m steps. Figure 1 plots it. *Correction (iteration 2): the earlier sentence that the term "rises roughly as the square of altitude" was a visual reading of Table 2. No fit was run, and no exponent was tested, so no mechanism is attributed to it here.*

The experiment's summary gives the error statistics against the reference. The isothermal form has a maximum absolute error of 0.588 K at 4,000 m and an RMS error of 0.269 K across the grid. The 0.6 K limit is set in the hypothesis's own altitude-only claim, and the isothermal error sits 0.012 K below it. The experiment labels the verdict borderline and makes no pass or fail claim. *Correction (iteration 2, reviewer item on the 0.6 K bound): the 0.6 K limit applies to total predicted-minus-measured error, which includes measurement and weather error. The structural term is a structural-error budget and cannot be tested against that limit. The "borderline" framing is withdrawn. The structural term is tested against the 0.5 K structural target, which it misses at 4,000 m, and the 0.6 K total bound remains untested until measured residuals exist.*

Against the hypothesis's structural target, the numbers are mixed. At 3,000 m the term is 0.33 K, close to the predicted 0.3 K. At 4,000 m it is 0.59 K, above the predicted "about 0.5 °C", and the success criterion asks for the structural term to stay at or below about 0.5 K at 4,000 m. On that criterion the structural part does not meet the stated target. The margin against the broader 0.6 K bound is thin.

### Artifact C: screen of closed-form boiling-point methods against the IAPWS saturation curve (experiment)

[ARTIFACT:art_jKGn4P2Rlpy1]

This experiment screens three closed-form methods for the boiling temperature against the IAPWS Industrial Formulation 1997 saturation curve (region 4, through the `iapws` package 1.5.5). The three methods are:

- (a) Clausius-Clapeyron with constant latent heat, anchored at the normal boiling point (373.124 K). This is the textbook route and is the primary method.
- (b) Clausius-Clapeyron with a temperature-dependent latent heat, integrated from the same anchor with enthalpies from the IAPWS Industrial Formulation 1997.
- (c) The Antoine equation, with the constants refitted to the reference over 273.15 to 373.15 K. The starting constants came from the NIST WebBook water entry.

Each method is inverted for temperature on an 81-point grid from 0 to 4,000 m in 50 m steps. Pressure comes from the U.S. Standard Atmosphere 1976 troposphere formula. The survival rule is a maximum absolute error of 0.6 K or less, and survivors are ranked by RMS error. A sensitivity case with the grid-mean latent heat is reported but not ranked.

**Table 3.** Error of each closed-form method against the IAPWS Industrial Formulation 1997 reference, 81 altitudes from 0 to 4,000 m. Values are from `summary.md`, and the per-method statistics in `rederivation.json` match them to the stored precision. Errors in K; the sign is method minus reference.

| Method | Max absolute error (K) | Altitude of max (m) | RMS (K) | Bias (K) | Error at 4,000 m (K) | Survives 0.6 K |
|---|---|---|---|---|---|---|
| (a) Constant latent heat, Clausius-Clapeyron (primary) | 0.2780 | 4,000 | 0.1521 | −0.1286 | −0.2780 | yes |
| (b) Temperature-dependent latent heat, Clausius-Clapeyron | 0.1773 | 4,000 | 0.1082 | −0.0951 | −0.1773 | yes |
| (c) Antoine equation, refitted | 0.0042 | 0 | 0.0022 | +0.0006 | +0.0031 | yes |
| Sensitivity: (a) with grid-mean latent heat (not ranked) | 0.4069 | 4,000 | 0.2473 | +0.2167 | +0.4069 | yes |

*Correction (iteration 2): the Antoine row and the ranking below are in-sample. The constants were refitted to the same IAPWS-IF97 reference over 273.15 to 373.15 K, and that reference then scored the method over 0 to 4 km. The 0.0042 K figure is a fit-quality statement, not a predictive error. Iteration 2 re-ran the Antoine refit on 273.15 to 363.15 K and scored it on held-out points, with the result given in the iteration 2 section below. Iteration 1's own fit residual over the full fit range is RMS 0.0553 K and maximum 0.192 K after inversion (`results/antoine_fit.json` in the iteration 1 artifact), which the table above does not show.* The refitted Antoine equation is the closest of the three to the reference across the grid, and its largest error is at sea level. The constant-latent-heat form has errors that grow with altitude, and it is the method most often taught. Using the grid-mean latent heat rather than the anchored value makes the error about 0.41 K at 4,000 m, which shows how sensitive the constant-latent-heat route is to the choice of that single constant. The Antoine fit has residual RMS 6.0 Pa and maximum 15.2 Pa in pressure over the fit range.

Ranking the three methods by RMS: Antoine (0.0022 K), temperature-dependent latent heat (0.1082 K), constant latent heat (0.1521 K).

The experiment's own consistency check of the Clapeyron relation at a 1 % tolerance failed, with a maximum deviation of 1.59 % and a median of 0.52 %. The experiment attributes the deviation to the ideal-vapour factor (the compressibility of the vapour, 1/Z_v, which is about 1.6 % at 373 K). *Correction (iteration 2): in iteration 1 this attribution was the artifact's expectation written into its interpretation field, not a tested result. Iteration 2 tests it directly (below).* The check was reported as failed and was not corrected or relaxed.

## Dead ends and limits of this iteration

- **Measured site records: not obtained.** Three candidate publications with site-level boiling records could not be read (HTTP 403 for the journal full text and the DOI page). No site was verified, and the hypothesis's central comparison has not been run. The dataset's measured-site count is zero, and the holdout set is empty.
- **Weather-driven pressure deviation: not tested.** No station pressure series was used. The hypothesis's claim that most of the residual comes from weather cannot be assessed from this iteration.
- **Clapeyron consistency at 1 %: failed.** Reported as failed. The deviation follows the ideal-vapour correction, so the constant-latent-heat route is not invalidated by it, but the check did not pass at the tolerance set.
- **Primary source for the standard atmosphere: not read.** The lapse rate (6.5 K/km), the sea-level values and the troposphere extent were taken from a secondary summary, because the primary PDF exceeded the fetch size limit. The NASA record confirms the document exists. This is a limit on the provenance of the pressure model, not on its numbers, since the standard values agree with the tabulated nodes in Artifact B.
- **Log path discrepancy.** The run log of Artifact B records its output paths on a different storage volume (`aii-s20005`) from the one the artifact sits on. The result files are the ones read for every number in this section.

## Result of this iteration

On the reference equations alone, a constant-lapse-rate barometric formula and an isothermal one differ by a structural term of 0.33 K at 3,000 m and 0.59 K at 4,000 m. The isothermal form's maximum error against the reference is 0.588 K at 4,000 m, which sits 0.012 K inside the 0.6 K altitude-only limit. The anchored constant-latent-heat Clausius-Clapeyron route reaches 0.278 K at 4,000 m, and the refitted Antoine equation stays within 0.004 K of the saturation curve over the grid. *Correction (iteration 2): the 0.004 K figure is the in-sample grid maximum and is not reproduced by the iteration 2 refit, which gives 0.086 K on the full grid (see the iteration 2 section). The full-fit-range residual is 0.192 K maximum. The statement "stays within 0.004 K" is withdrawn.*

These numbers say how large the model-structure term is. They do not say how well the chain agrees with measured boiling points, which was the hypothesis's question. The hypothesis's predictions about measured residuals, weather scatter and the dominance of the weather-driven pressure deviation remain untested.

# Iteration 2

## Strategy and why this iteration ran what it ran

Iteration 1 left two open items. The measured comparison had not been run, and the reviewer's critiques of iteration 1 named several defects in its record. The reviewer's principal objection was that the run had answered a neighbouring question (the size of the structural term against the reference) and not the question asked, which is how well the formula predicts measured boiling points. The reviewer also objected that the Antoine ranking was in-sample, that the 0.004 K figure omitted a larger full-range residual, that the 0.6 K bound was misapplied to a structural term, and that the reference table's provenance was not stated.

This iteration ran three artifacts against that feedback:

1. A search for measured boiling records with paired station pressure and elevation (`art_oMR0bkvIAeZz`). It answers the reviewer's first major item by trying to find the records the hypothesis needs.
2. A test of the isothermal and lapse-rate chain against those records, built to run the hypothesis's residual, structural-term and weather-term decomposition as soon as sites are accepted (`art_oV3FDo8XI1EV`). It was written to report `UNDERPOWERED` rather than a verdict when the accepted set is smaller than its minimum.
3. A re-screen of the three closed-form routes with a held-out split of the Antoine fit, a Z_v-corrected Clapeyron check, and an independent IAPWS-95 check (`art_C9Wp9EX0Cl2Z`). It answers the reviewer's in-sample item and the Clapeyron attribution item.

The planned measured-record step is the first thing the strategy asked for. Its result is recorded first below, because it decides what the rest of the iteration can say. Of the sources the reviewer named, NOAA GHCN-Daily and the NIST steam-table PDF were on the planned list, and the search did not reach them, as recorded in the dead ends below.

## Artifacts run this iteration

### Artifact D: search for measured boiling-point records (dataset)

[ARTIFACT:art_oMR0bkvIAeZz]

The search covered eight broad web queries, page fetches of the most promising leads, and a Hugging Face search. The target was at least 25 measured sites (with elevation, station pressure, observed boiling temperature and thermometer uncertainty) and a fixed holdout of at least 8 sites. No record meeting all four measured-record criteria (station pressure, elevation, observed boiling temperature and thermometer uncertainty) was verified.

The best lead was Forbes (1857), which reports 17 boiling-point and barometer pairs at Alpine stations. Its table is damaged by optical character recognition in the archive text, and the site elevations are not in the copies the run could read, so no row passed the drop rules. The Denver Public Library index card was dropped because it has no date and no thermometer uncertainty. The Snyder calibration tables and the NBS steam tables are calculated rather than measured and were kept only as reference values.

The candidate log of the test artifact (`art_oV3FDo8XI1EV`, `data/candidates.csv`) records the six sources it screened and the reason each was dropped:

| Candidate | Type | Elevation | Station pressure | Boiling temperature | Uncertainty | Reason dropped |
|---|---|---|---|---|---|---|
| engineeringtoolbox.com altitude table | handbook calculator table | yes | no | yes | no | calculated, not measured (steam-table calculation; no measured origin stated) |
| whiz.tools altitude calculator | calculator table | yes | yes (computed) | yes (computed) | no | calculated, not measured |
| compoundchem.com infographic | infographic PDF | yes | no | yes | no | calculated, not measured; no station pressure |
| LibreTexts vapour-pressure page (Denver 633 mmHg) | textbook table | yes | yes | yes | no | provenance not stated as measurement; no barometer uncertainty |
| UC Davis extension sheet (Snyder) | extension-service formula | no | no | no | no | empirical formula fit; no measured records |
| Lankford and Fox (2017) history essay | history essay | unknown | unknown | unknown | unknown | secondary essay not checked for measured records with all four fields |

The reference-only rows in the dataset are four values from the Snyder table: 100.0, 99.0, 98.0 and 97.0 °C at 0, 1,000, 2,000 and 3,000 ft (the source gives 212.0, 210.2, 208.4 and 206.6 °F). Their artifact's full output file holds `metadata.measured_rows = 0`, and every row is flagged `metadata_measured: false`. The Forbes table is the one lead that could still yield measured rows. Its transcription from the page image is the first step of the next iteration.

*Result of Artifact D: zero measured rows. The measured-site count and the holdout are both empty, the same state as iteration 1.*

### Artifact E: test of the barometric chain against measured records (experiment)

[ARTIFACT:art_oV3FDo8XI1EV]

This experiment was built to run the full chain once records exist. It inverts the Wagner and Pruß (IAPWS-95) saturation equation by bisection [1], with checks at the normal boiling point, the triple point and an inversion check. Those checks pass, with an error of 3.7 × 10⁻¹⁰ K when the inverted temperature is re-evaluated and a cross-check against the `iapws` package (IAPWS-IF97 region 4) at a maximum difference of 0.0020 K. The experiment computes the residuals of the isothermal and lapse-rate forms, the structural term (method minus method), the weather term (lapse-rate method minus measured pressure), bootstrap intervals over sites with a fixed seed, and a verdict for each claim. It requires at least 15 accepted sites and uses a holdout fixed in advance (every third site after sorting by elevation).

The accepted set is empty (`accepted_sites = 0`), and every claim is marked `UNDERPOWERED: untested`. The residual statistics for both the full set and the holdout are recorded as `n = 0` with no values. The bootstrap is recorded as "no sites". The only numbers it produced are the model-only reference-grid structural term.

**Table 4.** Claim verdicts and site counts from the test artifact, from `full_method_out.json` and `results/summary.json`.

| Quantity | Value |
|---|---|
| Accepted sites | 0 |
| Minimum sites for test | 15 |
| Holdout rule | sort by elevation then id; every third site |
| Residual RMS, all sites | not computed (n = 0) |
| Residual RMS, holdout | not computed (n = 0) |
| Claim A | UNDERPOWERED: untested |
| Claim B | UNDERPOWERED: untested |
| Claim C | UNDERPOWERED: untested |

The artifact's output names the three claims by letter and gives their verdicts, but its output file does not spell out the wording of each claim, so this report does not map them onto the hypothesis's criteria. Whatever the mapping, all three verdicts are untested, because no site was accepted. The model-only structural term is 0.332 K at 3,000 m and 0.588 K at 4,000 m, and the artifact records it as "model-only reference-grid structural term; not validation". Those values reproduce the Artifact B figures, and Table 5 gives them without any verdict attached.

**Table 5.** Model-only structural term from the test artifact's reference grid (isothermal minus lapse-rate boiling temperature, K), at the 500 m steps. Values are from `results/reference_grid.json`.

| Altitude (m) | Structural term (K) |
|---|---|
| 500 | 0.009342 |
| 1,000 | 0.037271 |
| 1,500 | 0.083649 |
| 2,000 | 0.148349 |
| 2,500 | 0.231251 |
| 3,000 | 0.332241 |
| 3,500 | 0.451220 |
| 4,000 | 0.588092 |

Table 5 is read from `results/reference_grid.json`, and Table 2 from the iteration 1 grid. The two sets agree to less than 0.00001 K at every altitude they share. The artifact's own check against the earlier screen matched within 0.05 K. This agreement shows the two runs reproduce each other, and it says nothing about measured residuals.

*Result of Artifact E: no measured residual, weather term or holdout statistic was computed. The structural term is reproduced, and the 4,000 m value of 0.588 K is 0.088 K above the 0.5 K structural target, as in iteration 1.*

### Artifact F: re-screen of the closed-form routes with a held-out Antoine split (experiment)

[ARTIFACT:art_C9Wp9EX0Cl2Z]

This experiment re-ran the three closed-form routes of Artifact C against the IAPWS-IF97 saturation curve, changing two things. The Antoine constants were refitted on 273.15 to 363.15 K (91 points, with 81 points in the 0 to 4,000 m grid), and the grid points whose boiling temperature falls in 363.15 to 373.15 K were kept as a held-out set (60 points, 0 to 2,950 m). The grid points whose boiling temperature lies inside the fit range (21 points, 2,950 to 4,000 m) are labelled "in-sample" in the artifact, and they are the points the fit is allowed to see. The experiment also added a sensitivity fit on 273.15 to 353.15 K (not ranked), an independent check of the Clapeyron relation with the Antoine and IAPWS-95 derivatives, and a cross-check of the 100 m reference table of Artifact A. A separate brentq reference (`audit/rederive.py`) reproduced the headline values to 8 × 10⁻¹⁰ K.

**Table 6.** Route errors against the IAPWS-IF97 reference, from `results/summary.json` (`route_errors`). Errors in K; the sign is method minus reference. Full grid is 81 points from 0 to 4,000 m. Held-out is 60 points from 0 to 2,950 m. In-sample is 21 points from 2,950 to 4,000 m.

| Route | Split | n | RMS (K) | Max absolute (K) | Altitude of max (m) | Bias (K) | Error at 4,000 m (K) |
|---|---|---|---|---|---|---|---|
| Constant-L Clausius-Clapeyron | full grid | 81 | 0.153235 | 0.279825 | 4,000 | −0.129558 | −0.279825 |
| Constant-L Clausius-Clapeyron | held-out | 60 | 0.107780 | 0.194075 | 2,950 | −0.091514 | −0.279825 |
| Constant-L Clausius-Clapeyron | in-sample | 21 | 0.239541 | 0.279825 | 4,000 | −0.238255 | −0.279825 |
| Temperature-dependent-L Clausius-Clapeyron | full grid | 81 | 0.107726 | 0.176489 | 4,000 | −0.094632 | −0.176489 |
| Temperature-dependent-L Clausius-Clapeyron | held-out | 60 | 0.082794 | 0.137413 | 2,950 | −0.072358 | −0.176489 |
| Temperature-dependent-L Clausius-Clapeyron | in-sample | 21 | 0.158670 | 0.176489 | 4,000 | −0.158272 | −0.176489 |
| Antoine (refit 273.15 to 363.15 K) | full grid | 81 | 0.054835 | 0.085625 | 0 | −0.051705 | −0.023228 |
| Antoine (refit 273.15 to 363.15 K) | held-out | 60 | 0.061262 | 0.085625 | 0 | −0.059534 | −0.023228 |
| Antoine (refit 273.15 to 363.15 K) | in-sample | 21 | 0.029580 | 0.035756 | 3,000 | −0.029336 | −0.023228 |

[FIGURE:fig2]

The Antoine rows change the picture from iteration 1. On the held-out points, which the fit did not see, the refitted Antoine has an RMS of 0.061 K, which is larger than the 0.030 K it reaches on the fit-range points. Its largest error is at sea level, where it sits 0.086 K below the reference. On the full grid it is still the lowest RMS of the three routes, at 0.055 K, and the ranking by held-out RMS is Antoine (0.061 K), then temperature-dependent-L Clausius-Clapeyron (0.083 K), then constant-L Clausius-Clapeyron (0.108 K). The held-out ranking is the one the reviewer asked for, and it still puts Antoine first. The margin is smaller than the iteration 1 table suggested, and the held-out Antoine error is roughly 15 times the 0.0042 K iteration 1 value.

The sensitivity fit on 273.15 to 353.15 K (not ranked) gives a held-out RMS of 0.092 K and a maximum of 0.133 K at sea level. That fit moves the Antoine constants by enough to change its held-out ranking relative to the temperature-dependent route, so the Antoine ranking is sensitive to the fit range. This run does not resolve that. It is recorded as a limit, not as a result.

**Table 7.** Antoine sensitivity to the fit range, from `results/summary.json` (`sensitivity_antoine_273_353_fit`). Not ranked.

| Fit range | Held-out range | Held-out RMS (K) | Held-out max (K) | Altitude of max (m) | Bias (K) |
|---|---|---|---|---|---|
| 273.15 to 363.15 K (main) | 363.15 to 373.15 K | 0.061262 | 0.085625 | 0 | −0.059534 |
| 273.15 to 353.15 K (sensitivity) | 353.15 to 373.15 K | 0.092436 | 0.132504 | 0 | −0.089411 |

The regression check against iteration 1 did not pass for Antoine. The artifact expected the in-sample grid maximum of 0.0042 K and obtained 0.0358 K. The four constant-latent-heat and temperature-dependent routes reproduced their iteration 1 values to within 0.005 K. The artifact therefore marks its Antoine interpretation as provisional. The 0.0042 K value is not confirmed by this run. Its origin in iteration 1 is not resolved here either, and the iteration 1 Antoine figures should be read as in-sample statistics for a fit over a different range.

The Clapeyron check gives the attribution test the reviewer asked for. Table 8 shows the residual of the Clapeyron relation under three treatments of the vapour.

**Table 8.** Clapeyron relation residual on the 81-point grid (356 to 373 K), from `results/clapeyron.json`. Relative residual, maximum over the grid. Tolerance 1 %.

| Treatment of the vapour | Max absolute relative residual |
|---|---|
| Ideal vapour (1/Z_v not applied) | 0.016261 (1.63 %) |
| Z_v-corrected (vapour volume from IAPWS-IF97 density) | 0.000610 (0.061 %) |
| Z_v-corrected with liquid volume also included | 0.000361 (0.036 %) |
| Independent curve: Antoine derivative | 0.009204 (0.92 %) |
| Independent curve: IAPWS-95 derivative, Z_v-corrected | 0.000625 (0.062 %) |

Applying the vapour compressibility removes the failure, and the residual falls below the 1 % tolerance by more than an order of magnitude. This tests the attribution, which iteration 1 had only stated. The artifact adds a caveat that matters for the reading of the table. The Z_v-corrected IAPWS-IF97 residual is close to zero by construction, because the pressure derivative, the latent heat and the vapour compressibility all come from the same IAPWS-IF97 equations. The test that carries weight is the independent-curve pair. The Antoine derivative residual of 0.92 % passes the tolerance narrowly, and the IAPWS-95 derivative residual of 0.062 % passes with room to spare. The artifact's overall verdict is "holds, but largely an identity", and this report uses the same wording.

Table 9 gives the iteration 2 regression check against the iteration 1 values, so a reader can see which numbers reproduced and which did not.

**Table 9.** Regression of iteration 2 against the iteration 1 headline values, from `results/summary.json` (`regression_against_prior_screen`). Tolerance 0.005 K.

| Quantity | Iteration 1 value (K) | Iteration 2 value (K) | Passes |
|---|---|---|---|
| Constant-L maximum | 0.278 | 0.279825 | yes |
| Constant-L RMS | 0.152 | 0.153235 | yes |
| Temperature-dependent-L maximum | 0.177 | 0.176489 | yes |
| Temperature-dependent-L RMS | 0.108 | 0.107726 | yes |
| Antoine in-sample maximum | 0.0042 | 0.035756 | no |
| Antoine in-sample RMS | 0.0022 | 0.029580 | no |

Two further checks on the reference support the run. The Antoine refit on 273.15 to 363.15 K has an RMS residual of 0.00026 in log10 pressure and converged in 22 function evaluations. The table of Artifact A, cross-checked against the IAPWS-IF97 route at 100 m steps, differs from the reference by a maximum of 0.063 K and a mean of −0.018 K (`dataset_cross_check` in `results/summary.json`). Both numbers are consistency checks between two calculations, not measurements.

## Dead ends and limits of this iteration

- **Measured site records: still not obtained.** The search in Artifact D found no record meeting the measured-record criteria. The Forbes (1857) table is the only lead that could yield measured rows, and it is not yet transcribed. The hypothesis's central comparison, predicted against observed boiling temperature, has not been run. The accepted set in Artifact E is empty, and every claim verdict is "UNDERPOWERED: untested".
- **The sources the reviewer named were not reached.** NOAA GHCN-Daily station pressure and the NIST steam-table PDF are on the drop list as not yet fetched. Neither was fetched in this iteration. The record therefore does not show that they lack measured boiling records. It shows only that they were not tried.
- **Antoine as the best route: weakened, not confirmed.** On held-out points Antoine still has the lowest RMS, but the margin over temperature-dependent-L Clausius-Clapeyron is 0.022 K. The sensitivity fit on 273.15 to 353.15 K changes the held-out error by 0.03 K. The regression against iteration 1 did not reproduce the 0.0042 K value. The ranking is provisional.
- **Clapeyron attribution: tested, and it holds.** The ideal-vapour residual falls from 1.63 % to 0.06 % once the vapour compressibility is applied. Its status as a test rather than an expectation is the change in this iteration.
- **Structural term at 4,000 m: above target.** The model-only value of 0.588 K exceeds the 0.5 K structural target. Nothing in this iteration changes that value.
- **Nearest published results, not searched.** The reviewer asked that each positive claim be set against its nearest published neighbour, and that a scholarly search be recorded. No such search was run in this iteration, so no neighbour is named beyond the standard references already in the record ([1] for the saturation curve, the textbook Clausius-Clapeyron treatment, and the standard pressure-altitude tables). The claims in this iteration are therefore not credited as novel.
- **Log and volume discrepancy, iteration 1: not resolved.** The reviewer asked for the result files to be checksummed against the run log of Artifact B. That check was not done in this iteration, and the iteration 1 path discrepancy stands as recorded.

## Result of this iteration

The measured comparison, which is the question the run was set, has still not been run. Iteration 2 added the test that will run it (Artifact E), and it added the first sources checked against the record's own standards (Artifact D), none of which yielded a measured record.

On the reference equations, the iteration 2 results change two of the iteration 1 statements. The held-out Antoine error is 0.061 K RMS, not the 0.004 K value that iteration 1 reported. The Clapeyron attribution to the vapour compressibility is now tested, and it holds to 0.06 % after correction. The structural term and the two Clausius-Clapeyron routes reproduce their iteration 1 values.

## What we have learned so far

The run's evidence now runs in three layers, and only the first is about the question asked.

- **Measured comparison: not run.** No measured boiling record with station pressure and elevation has been verified. The accepted set is empty, and the predictions of 0.3 K (station pressure) and 0.6 K (altitude only) are untested. [ARTIFACT:art_oMR0bkvIAeZz] [ARTIFACT:art_oV3FDo8XI1EV]
- **Structural term of the isothermal form: 0.33 K at 3,000 m and 0.59 K at 4,000 m.** The 4,000 m value exceeds the 0.5 K structural target, and it reproduces across three artifacts. [ARTIFACT:art_YU39iUPrFWbZ] [ARTIFACT:art_oV3FDo8XI1EV]
- **Vapour-pressure routes against the reference: Antoine lowest on held-out RMS (0.061 K), temperature-dependent-L Clausius-Clapeyron next (0.083 K), constant-L Clausius-Clapeyron last (0.108 K), and the constant-L route reaches 0.28 K at 4,000 m.** The Antoine ranking is provisional, because it depends on the fit range and its 0.0042 K iteration 1 value did not reproduce. [ARTIFACT:art_C9Wp9EX0Cl2Z]
- **Clapeyron relation: holds after vapour compressibility is applied (0.06 % residual, against 1.63 % without it).** The verdict is largely an identity, and the independent-curve pair carries the test. [ARTIFACT:art_C9Wp9EX0Cl2Z]
- **Reference table: consistent with the two reference calculations to 0.06 K at 100 m steps, but not measured.** [ARTIFACT:art__Ga8TbdhmlP8]
- **Open items for the next iteration:** transcribe the Forbes (1857) table and obtain site elevations; fetch the NOAA and NIST sources the reviewer named; and, if records are found, compute the predicted-minus-observed residuals for the holdout set.

## Figure index

- Figure 1 (fig1): structural term against altitude, from Artifact B.
- Figure 2 (fig2): RMS error by vapour-pressure route, held-out and fit-range splits, from Artifact F (Table 6).

### Earlier closing summary (iteration 1, kept as the record of what was believed then)

- The structural term of the isothermal barometric form is 0.33 K at 3,000 m and 0.59 K at 4,000 m, against the hypothesis's predicted 0.3 K and about 0.5 K. The 4,000 m value exceeds the stated target. [ARTIFACT:art_YU39iUPrFWbZ]
- The refitted Antoine equation reproduces the water saturation curve to 0.004 K over 0 to 4,000 m, and the anchored constant-latent-heat Clausius-Clapeyron route reaches 0.28 K at 4,000 m. [ARTIFACT:art_jKGn4P2Rlpy1]
- The published reference table and its formula check agree with each other to 0.21 K at most, but that agreement is between two calculations, and no measured record has been compared with either. [ARTIFACT:art__Ga8TbdhmlP8]
- The measured comparison, the weather-driven pressure deviation and the test of the ±0.3 °C and ±0.6 °C predictions have not been run. Those are the open items for the next iteration.

## References

[1] W. Wagner and A. Pruß, "The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use," *Journal of Physical and Chemical Reference Data*, vol. 31, no. 2, pp. 387-535, 2002. doi:10.1063/1.1461829.
