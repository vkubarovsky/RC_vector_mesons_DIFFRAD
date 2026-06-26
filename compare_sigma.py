#!/usr/bin/env python3
"""Compare sigma_T and sigma_L of the two phi cross-section models used in
the RC calculation: Akushevich GVD (difflt original) vs tuned/lAger
(difflt in tuned_phi_run). Both returned as dsigma/dt in nb/GeV^2.
t is negative (t = -|t|)."""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

amp = 0.938272; amp2 = amp**2; ap = 2*amp
amv = 1.019412; amv2 = amv**2
alpha = 0.729735e-2; pi = 3.1415926; barn = 0.389379e6
bslope = 5.0; al_s = 0.25; p02 = 0.5; ggam3 = 1.37e-6

def aku(q2, w2, t):                      # Akushevich GVD, -> nb/GeV^2
    sx = w2 + q2 - amp2; anu = sx/ap
    eh = (sx + t)/(2*amp)
    ff2 = np.exp(bslope*t)
    tqt = t + q2 - amv2
    pt2 = -(4*(anu**2+q2)*amv2 + 4*anu*eh*tqt - 4*eh**2*q2 + tqt**2)/(4*(anu**2+q2))
    pt2 = max(pt2, 0.0)
    q2b = (q2 + amv2 + pt2)/4
    if pt2 <= p02:
        fm = np.log((4*q2b - pt2 + p02)/(pt2 + p02))
    else:
        fm = np.log((pt2 + p02)/(4*q2b - pt2 + p02)*4*q2b**2/pt2**2)
    xsb = (q2 + amv2 + pt2)/w2
    sk = 3*(1-xsb)**5 * fm/(2*q2b*(2*q2b - pt2)*np.log(8*q2b/p02))
    sigt = al_s**2*ggam3*amv**3/3/alpha*pi**3*sk**2*ff2
    return sigt*barn, (q2/amv2)*sigt*barn      # sigT, sigL

def tuned(q2, w2, t):                     # tuned/lAger, already nb/GeV^2
    alf1, alf2, alf3, pnuT, btt, cRt = 400., -1.245, 0.762, 2.344, 1.284, 1.0
    wth2 = (amp+amv)**2
    if w2 <= wth2: return 0., 0.
    cT = alf1*(1 - wth2/w2)**alf2 * np.sqrt(w2)**alf3
    sigt = cT/(1 + q2/amv2)**pnuT * btt*np.exp(btt*t)
    return sigt, cRt*(q2/amv2)*sigt

W2 = 6.25                                 # W = 2.5 GeV
def curve(fn, q2arr, tarr):
    return np.array([fn(q, W2, -tt) for q, tt in zip(q2arr, tarr)])

# --- vs |t| at fixed Q^2 = 2.0 ---
Q2fix = 2.0
tt = np.linspace(0.05, 2.5, 60)
A = curve(aku, np.full_like(tt, Q2fix), tt)
T = curve(tuned, np.full_like(tt, Q2fix), tt)
fig, ax = plt.subplots(figsize=(7,5))
ax.plot(tt, A[:,0], 'b-',  label="$\\sigma_T$ Akushevich")
ax.plot(tt, A[:,1], 'b--', label="$\\sigma_L$ Akushevich")
ax.plot(tt, T[:,0], 'r-',  label="$\\sigma_T$ tuned")
ax.plot(tt, T[:,1], 'r--', label="$\\sigma_L$ tuned")
ax.set_yscale("log"); ax.set_xlabel("$|t|$ (GeV$^2$)")
ax.set_ylabel("$d\\sigma/dt$ (nb/GeV$^2$)")
ax.set_title(f"$\\phi$ cross sections vs $|t|$  (W=2.5 GeV, $Q^2$={Q2fix})")
ax.legend(); ax.grid(alpha=.3, which="both"); fig.tight_layout()
fig.savefig("sigma_vs_t.png", dpi=130)

# --- vs Q^2 at fixed |t| = 0.3 ---
tfix = 0.3
q2 = np.linspace(0.4, 8.0, 60)
A = curve(aku, q2, np.full_like(q2, tfix))
T = curve(tuned, q2, np.full_like(q2, tfix))
fig, ax = plt.subplots(figsize=(7,5))
ax.plot(q2, A[:,0], 'b-',  label="$\\sigma_T$ Akushevich")
ax.plot(q2, A[:,1], 'b--', label="$\\sigma_L$ Akushevich")
ax.plot(q2, T[:,0], 'r-',  label="$\\sigma_T$ tuned")
ax.plot(q2, T[:,1], 'r--', label="$\\sigma_L$ tuned")
ax.set_yscale("log"); ax.set_xlabel("$Q^2$ (GeV$^2$)")
ax.set_ylabel("$d\\sigma/dt$ (nb/GeV$^2$)")
ax.set_title(f"$\\phi$ cross sections vs $Q^2$  (W=2.5 GeV, $|t|$={tfix})")
ax.legend(); ax.grid(alpha=.3, which="both"); fig.tight_layout()
fig.savefig("sigma_vs_q2.png", dpi=130)

print("R = sigL/sigT identical (both Q^2/M_phi^2):",
      f"at Q2=2 -> {2.0/amv2:.3f}")
print("wrote sigma_vs_t.png, sigma_vs_q2.png")
