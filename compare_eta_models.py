#!/usr/bin/env python3
"""How much does the phi RC (eta) depend on the sigma_L/T model?
Overlay eta(Akushevich GVD) vs eta(tuned/lAger) on the same 60-point grid
and quantify the difference."""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = "/Users/vpk/RC_vector_mesons_DIFFRAD"

def read_eta(path):
    e = []
    for l in open(path):
        p = l.split()
        if len(p) == 3 and p[0].isdigit():
            e.append(float(p[1]))
    return np.array(e)

def read_grid(path):
    lines = [l.split("!")[0].strip() for l in open(path)]
    lines = [l for l in lines if l]
    rows = [list(map(float, lines[9+i].split())) for i in range(6)]
    Q2 = 0.5*(np.abs(rows[2]) + np.abs(rows[3]))
    tc = 0.5*(np.abs(rows[4]) + np.abs(rows[5]))
    return Q2, tc

def read_eta_err(path):
    e, er = [], []
    for l in open(path):
        p = l.split()
        if len(p) == 3 and p[0].isdigit():
            e.append(float(p[1])); er.append(float(p[2]))
    return np.array(e), np.array(er)

Q2c, tc = read_grid(f"{base}/akushevich_phi_run/inmdi.dat")
eA = read_eta(f"{base}/akushevich_phi_run/etamc.dat")
eT, erT = read_eta_err(f"{base}/tuned_phi_run/etamc.dat")
stable = erT < 0.05            # tuned MC converged
d = eT - eA

ubins = sorted(set(np.round(Q2c, 3)))
colors = plt.cm.viridis(np.linspace(0, 0.9, len(ubins)))

# --- overlay eta(|t|): Akushevich solid, tuned dashed ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 8), height_ratios=[2, 1])
for q, c in zip(ubins, colors):
    m = np.round(Q2c, 3) == q; o = np.argsort(tc[m])
    ax1.plot(tc[m][o], eA[m][o], "-o", ms=3, color=c, label=f"$Q^2${q:.2f}")
    ms_ = m & stable; os_ = np.argsort(tc[ms_])
    ax1.plot(tc[ms_][os_], eT[ms_][os_], "--s", ms=3, color=c, mfc="none")
    su = m & stable
    ax2.plot(tc[su][np.argsort(tc[su])], (eT-eA)[su][np.argsort(tc[su])], "-", color=c)
# flag the MC blow-up points at the top
ax1.plot(tc[~stable], np.full((~stable).sum(), 1.45), "rx", ms=7,
         label="tuned MC blow-up (near thr.)")
ax1.axhline(1, ls=":", c="grey"); ax1.set_ylim(0.6, 1.5)
ax1.plot([], [], "k-o", ms=3, label="Akushevich (solid)")
ax1.plot([], [], "k--s", ms=3, mfc="none", label="tuned (dashed)")
ax1.set_ylabel(r"$\eta=\sigma_{obs}/\sigma_{Born}$")
ax1.set_title(r"Phi RC: does $\eta$ depend on the $\sigma_{L,T}$ model?")
ax1.legend(fontsize=7, ncol=2); ax1.grid(alpha=.3)
ax2.axhline(0, ls=":", c="grey")
ax2.set_xlabel("$|t|$ (GeV$^2$)"); ax2.set_ylabel(r"$\eta_{tun}-\eta_{Aku}$")
ax2.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{base}/eta_model_compare.png", dpi=130)

print(f"points: {len(eA)}")
print(f"eta_Aku   range {eA.min():.3f}-{eA.max():.3f}")
print(f"eta_tuned range {eT.min():.3f}-{eT.max():.3f}")
print(f"Delta = tuned - Aku:  mean {d.mean():+.4f}  RMS {np.sqrt((d**2).mean()):.4f}  max|.| {np.abs(d).max():.4f}")
# restrict to diffractive region |t|<1
sel = tc < 1.0
print(f"  in |t|<1 GeV^2:  RMS {np.sqrt((d[sel]**2).mean()):.4f}  max|.| {np.abs(d[sel]).max():.4f}")
