"""Independent re-derivation of the reference-grid headline numbers.

Different code path from method.py: saturation pressure from the iapws package
(IAPWS97 psat) inverted with scipy brentq; atmosphere constants recomputed inline
from the physical constants, not imported from method.py.
"""
import math
from iapws import IAPWS97
from scipy.optimize import brentq

R, M, g, T0, P0, L = 8.314462618, 0.0289644, 9.80665, 288.15, 101325.0, 0.0065
H = R * T0 / (M * g)
E = g * M / (R * L)

def tb(p_pa):
    f = lambda T: IAPWS97(T=T, x=0).P * 1e6 - p_pa
    return brentq(f, 273.2, 378.0, xtol=1e-10)

def s(z):
    p_iso = P0 * math.exp(-z / H)
    p_lap = P0 * (1 - L * z / T0) ** E
    return tb(p_iso) - tb(p_lap)

print(f"s(3000 m) = {s(3000):.4f} K")
print(f"s(4000 m) = {s(4000):.4f} K")
print(f"dTb/dp at 1 atm = {(tb(P0 + 100) - tb(P0 - 100)) / 0.2:.4f} K/kPa")
