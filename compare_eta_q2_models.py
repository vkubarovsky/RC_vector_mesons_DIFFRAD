#!/usr/bin/env python3
"""Q2-dependence of the phi RC model-sensitivity: eta(Q2) at fixed |t|
for Akushevich GVD vs tuned/lAger. Tuned blow-up points (err>=0.05)
are excluded from the interpolation."""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = "/Users/vpk/RC_vector_mesons_DIFFRAD"

def read_eta_err(path):
    e, er = [], []
    for l in open(path):
        p = l.split()
        if len(p) == 3 and p[0].isdigit():
            e.append(float(p[1])); er.append(float(p[2]))
    return np.array(e), np.array(er)

def read_grid(path):
    L = [l.split("!")[0].strip() for l in open(path)]; L = [l for l in L if l]
    r = [list(map(float, L[9+i].split())) for i in range(6)]
    return 0.5*(np.abs(r[2])+np.abs(r[3])), 0.5*(np.abs(r[4])+np.abs(r[5]))

Q2c, tc = read_grid(f"{base}/akushevich_phi_run/inmdi.dat")
eA, erA = read_eta_err(f"{base}/akushevich_phi_run/etamc.dat")
eT, erT = read_eta_err(f"{base}/tuned_phi_run/etamc.dat")
okA = erA < 0.05; okT = erT < 0.05
ubins = sorted(set(np.round(Q2c, 3)))

def eta_at(tt, eta, ok):
    """interpolate eta at |t|=tt within each Q2 bin (stable pts only)."""
    xs, ys = [], []
    for q in ubins:
        m = (np.round(Q2c, 3) == q) & ok
        if m.sum() < 2: continue
        o = np.argsort(tc[m]); tb, eb = tc[m][o], eta[m][o]
        if tb.min() <= tt <= tb.max():
            xs.append(q); ys.append(np.interp(tt, tb, eb))
    return np.array(xs), np.array(ys)

t_targets = [0.3, 0.5, 1.0]
cols = ["#185FA5", "#BA7517", "#1D9E75"]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 8), height_ratios=[2, 1])
for tt, c in zip(t_targets, cols):
    xa, ya = eta_at(tt, eA, okA)
    xt, yt = eta_at(tt, eT, okT)
    ax1.plot(xa, ya, "-o", color=c, label=f"$|t|$={tt}  Akushevich")
    ax1.plot(xt, yt, "--s", color=c, mfc="none", label=f"$|t|$={tt}  tuned")
    # difference on the common Q2 grid
    common = np.intersect1d(np.round(xa,3), np.round(xt,3))
    if len(common):
        da = np.array([ya[np.round(xa,3)==q][0] for q in common])
        dt = np.array([yt[np.round(xt,3)==q][0] for q in common])
        ax2.plot(common, dt-da, "-d", color=c)
ax1.axhline(1, ls=":", c="grey")
ax1.set_ylabel(r"$\eta=\sigma_{obs}/\sigma_{Born}$")
ax1.set_title(r"Phi RC vs $Q^2$: Akushevich (solid) vs tuned (dashed)")
ax1.legend(fontsize=7, ncol=3); ax1.grid(alpha=.3)
ax2.axhline(0, ls=":", c="grey")
ax2.set_xlabel("$Q^2$ (GeV$^2$)"); ax2.set_ylabel(r"$\eta_{tun}-\eta_{Aku}$")
ax2.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{base}/eta_q2_model_compare.png", dpi=130)
print("wrote eta_q2_model_compare.png")
for tt in t_targets:
    xa, ya = eta_at(tt, eA, okA); xt, yt = eta_at(tt, eT, okT)
    common = np.intersect1d(np.round(xa,3), np.round(xt,3))
    da = np.array([ya[np.round(xa,3)==q][0] for q in common])
    dt = np.array([yt[np.round(xt,3)==q][0] for q in common])
    print(f"|t|={tt}: Q2 bins compared={len(common)}, "
          f"Delta(tuned-Aku) range {(dt-da).min():+.3f}..{(dt-da).max():+.3f}")
