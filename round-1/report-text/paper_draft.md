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

This artifact is a 41-row table of boiling temperature from 0 to 4,000 m in 100 m steps. Each row is calculated from a published equation. The boiling values come from a barometric levelling table on a public web page, not from field measurements. Its evidence type is recorded in every row as `equation_derived`. The table was built so that a later step could add measured sites under the same schema, with a predefined holdout rule (measured sites in the Americas above 1,000 m), but none were added.

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

The saturation curve is the Wagner and Pruß formulation, inverted by bisection. Its checks passed: the boiling temperature at 101,325 Pa is 373.1243 K (99.9743 °C), and the inversion error, the relative difference between the saturation pressure at the inverted temperature and the input pressure, is 4.2 × 10⁻¹⁵. A separate calculation with the `iapws` package reproduces the sea-level boiling temperature and the altitude values at 0, 2,000 and 4,000 m to within 0.00024 K. The lapse-rate pressures reproduce the tabulated standard-atmosphere nodes to within 0.0073 %.

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

Table 2 gives the structural term at 500 m steps. Figure 1 plots it. The term rises roughly as the square of altitude over this range, which is what a small difference in the exponent of the pressure profile would produce.

The experiment's summary gives the error statistics against the reference. The isothermal form has a maximum absolute error of 0.588 K at 4,000 m and an RMS error of 0.269 K across the grid. The 0.6 K limit is set in the hypothesis's own altitude-only claim, and the isothermal error sits 0.012 K below it. The experiment labels the verdict borderline and makes no pass or fail claim.

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

The refitted Antoine equation is the closest of the three to the reference across the grid, and its largest error is at sea level. The constant-latent-heat form has errors that grow with altitude, and it is the method most often taught. Using the grid-mean latent heat rather than the anchored value makes the error about 0.41 K at 4,000 m, which shows how sensitive the constant-latent-heat route is to the choice of that single constant. The Antoine fit has residual RMS 6.0 Pa and maximum 15.2 Pa in pressure over the fit range.

Ranking the three methods by RMS: Antoine (0.0022 K), temperature-dependent latent heat (0.1082 K), constant latent heat (0.1521 K).

The experiment's own consistency check of the Clapeyron relation at a 1 % tolerance failed, with a maximum deviation of 1.59 % and a median of 0.52 %. The experiment attributes the deviation to the ideal-vapour factor (the compressibility of the vapour, 1/Z_v, which is about 1.6 % at 373 K). The check was reported as failed and was not corrected or relaxed.

## Dead ends and limits of this iteration

- **Measured site records: not obtained.** Three candidate publications with site-level boiling records could not be read (HTTP 403 for the journal full text and the DOI page). No site was verified, and the hypothesis's central comparison has not been run. The dataset's measured-site count is zero, and the holdout set is empty.
- **Weather-driven pressure deviation: not tested.** No station pressure series was used. The hypothesis's claim that most of the residual comes from weather cannot be assessed from this iteration.
- **Clapeyron consistency at 1 %: failed.** Reported as failed. The deviation follows the ideal-vapour correction, so the constant-latent-heat route is not invalidated by it, but the check did not pass at the tolerance set.
- **Primary source for the standard atmosphere: not read.** The lapse rate (6.5 K/km), the sea-level values and the troposphere extent were taken from a secondary summary, because the primary PDF exceeded the fetch size limit. The NASA record confirms the document exists. This is a limit on the provenance of the pressure model, not on its numbers, since the standard values agree with the tabulated nodes in Artifact B.
- **Log path discrepancy.** The run log of Artifact B records its output paths on a different storage volume (`aii-s20005`) from the one the artifact sits on. The result files are the ones read for every number in this section.

## Result of this iteration

On the reference equations alone, a constant-lapse-rate barometric formula and an isothermal one differ by a structural term of 0.33 K at 3,000 m and 0.59 K at 4,000 m. The isothermal form's maximum error against the reference is 0.588 K at 4,000 m, which sits 0.012 K inside the 0.6 K altitude-only limit. The anchored constant-latent-heat Clausius-Clapeyron route reaches 0.278 K at 4,000 m, and the refitted Antoine equation stays within 0.004 K of the saturation curve over the grid.

These numbers say how large the model-structure term is. They do not say how well the chain agrees with measured boiling points, which was the hypothesis's question. The hypothesis's predictions about measured residuals, weather scatter and the dominance of the weather-driven pressure deviation remain untested.

## What we have learned so far

- The structural term of the isothermal barometric form is 0.33 K at 3,000 m and 0.59 K at 4,000 m, against the hypothesis's predicted 0.3 K and about 0.5 K. The 4,000 m value exceeds the stated target. [ARTIFACT:art_YU39iUPrFWbZ]
- The refitted Antoine equation reproduces the water saturation curve to 0.004 K over 0 to 4,000 m, and the anchored constant-latent-heat Clausius-Clapeyron route reaches 0.28 K at 4,000 m. [ARTIFACT:art_jKGn4P2Rlpy1]
- The published reference table and its formula check agree with each other to 0.21 K at most, but that agreement is between two calculations, and no measured record has been compared with either. [ARTIFACT:art__Ga8TbdhmlP8]
- The measured comparison, the weather-driven pressure deviation and the test of the ±0.3 °C and ±0.6 °C predictions have not been run. Those are the open items for the next iteration.

## Figure index

- Figure 1 (fig1): structural term against altitude, from Artifact B.

## References

[1] W. Wagner and A. Pruß, "The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use," *Journal of Physical and Chemical Reference Data*, vol. 31, no. 2, pp. 387-535, 2002. doi:10.1063/1.1461829.
