import math, sys
import numpy as np
from iapws import IAPWS97
from scipy.optimize import least_squares, curve_fit
def ps(T): return IAPWS97(T=T, x=0).P*1e6
T = np.linspace(273.15, 363.15, 91)
lp = np.log10([ps(t) for t in T])
def model(T, A, B, C): return A - B/(T+C)
# (a) log-space least squares (current method)
p, _ = curve_fit(model, T, lp, p0=[10.19625,1730.63,-39.724], maxfev=20000)
print("a log-fit", p, "max|dlog|", np.max(np.abs(model(T,*p)-lp)))
# (b) linear-P curve_fit
P = 10**lp
pb, _ = curve_fit(lambda T,A,B,C: 10**model(T,A,B,C), T, P, p0=[10.19625,1730.63,-39.724], maxfev=20000, sigma=P)
print("b P-fit (rel weights)", pb, "max|dlog|", np.max(np.abs(model(T,*pb)-lp)))
# T-error of fit in log space at each point
for name, pp in [("a", p), ("b", pb)]:
    Tb_fit_err = []
    for t, l in zip(T, lp):
        slope = pp[1]*math.log(10)*0  # placeholder
    # invert on grid of pressures 61.6k..101.3k
    for pr in [61640.0, 70000.0, 90000.0, 101325.0]:
        Tref = None
    # compute Tb error by inversion
    from scipy.optimize import brentq
    errs=[]
    for pr in np.linspace(61600, 101325, 60):
        tr = brentq(lambda t: ps(t)-pr, 273.2, 373.9, xtol=1e-10)
        ta = pp[1]/(pp[0]-math.log10(pr)) - pp[2]
        errs.append(ta-tr)
    errs=np.array(errs)
    print(name, "Tb err max over 61.6-101 kPa:", np.max(np.abs(errs)), "rms", np.sqrt(np.mean(errs**2)))
