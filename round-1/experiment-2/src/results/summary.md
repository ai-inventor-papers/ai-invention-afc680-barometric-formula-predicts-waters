# Summary: screening vapour-pressure shortcuts for water boiling temperature

Reference: IAPWS-IF97 saturation pressure (region 4, iapws package). Grid: 81 altitudes, 0-4000 m, U.S. Standard Atmosphere 1976.
Survival rule: max |error| <= 0.6 K. Ranking by RMS error among survivors.

| Method | max abs error (K) | RMS (K) | altitude of max (m) | bias (K) | error at 4000 m (K) | survives |
|---|---|---|---|---|---|---|
| (a) constant latent heat Clausius-Clapeyron (primary) | 0.2780 | 0.1521 | 4000 | -0.1286 | -0.2780 | yes |
| (b) temperature-dependent latent heat Clausius-Clapeyron | 0.1773 | 0.1082 | 4000 | -0.0951 | -0.1773 | yes |
| (c) Antoine equation (NIST constants, refitted) | 0.0042 | 0.0022 | 0 | +0.0006 | +0.0031 | yes |
| sensitivity: (a) with grid-mean Lv (not ranked) | 0.4069 | 0.2473 | 4000 | +0.2167 | +0.4069 | yes |

## Ranking (survivors, by RMS)

1. (c) Antoine equation (NIST constants, refitted): RMS 0.0022 K
2. (b) temperature-dependent latent heat Clausius-Clapeyron: RMS 0.1082 K
3. (a) constant latent heat Clausius-Clapeyron (primary): RMS 0.1521 K

## Antoine fit

A = 7.125207, B = 1689.0362, C = 229.9526 over 273.15-373.15 K; residual RMS 6.006 Pa, max 15.155 Pa; residual after inversion RMS 0.05529 K.

## Reference checks

- 1_reference: pass=True
- 2_atmosphere: pass=True
- 3_clapeyron_consistency: pass=False
- 4_method_single_point_h0: pass=True
- 5_antoine_fit: pass=True
- 6_sensitivity_a_anchor_identity: pass=None
