#!/usr/bin/env python3
"""Plot eta(t) and eta(Q2) for phi from MDIFFRAD output.
Reads inmdi.dat (kinematics grid) and etamc.dat (eta per point)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- read kinematics from inmdi.dat ---
with open("inmdi.dat") as f:
    lines = [l.split("!")[0].strip() for l in f]
lines = [l for l in lines if l]
npoi = int(lines[8].split()[0])
rows = [list(map(float, lines[9 + i].split())) for i in range(6)]
W2min, W2max, Q2min, Q2max, tmn, tmx = (np.abs(np.array(r)) for r in rows)
Q2c = 0.5 * (Q2min + Q2max)
tc = 0.5 * (tmn + tmx)

# --- read eta from etamc.dat ---
eta, err = [], []
for l in open("etamc.dat"):
    p = l.split()
    if len(p) == 3 and p[0].isdigit():
        eta.append(float(p[1])); err.append(float(p[2]))
eta = np.array(eta); err = np.array(err)
vcut = float([l for l in open("etamc.dat") if "cutv" in l][0].split("=")[1])
VC = f"$v_{{cut}}=${vcut:.3f} GeV$^2$"

# drop NaN points (numerical edge in a sample)
good = np.isfinite(eta)
if not good.all():
    print(f"dropping {np.sum(~good)} NaN point(s): {list(np.where(~good)[0] + 1)}")
Q2c, tc, eta, err = Q2c[good], tc[good], eta[good], err[good]

# group by Q2 bin
ubins = sorted(set(np.round(Q2c, 3)))
colors = plt.cm.viridis(np.linspace(0, 0.9, len(ubins)))

# --- eta(t), one curve per Q2 bin ---
fig, ax = plt.subplots(figsize=(7, 5))
for q, c in zip(ubins, colors):
    m = np.round(Q2c, 3) == q
    o = np.argsort(tc[m])
    ax.errorbar(tc[m][o], eta[m][o], yerr=err[m][o], marker="o", ms=4,
                color=c, label=f"$Q^2\\approx${q:.2f} GeV$^2$")
ax.axhline(1.0, ls=":", c="grey")
ax.set_xlabel("$|t|$ (GeV$^2$)"); ax.set_ylabel(r"$\eta=\sigma_{obs}/\sigma_{Born}$")
ax.set_title(r"$\phi$ radiative correction $\eta(|t|)$, "+VC+"")
ax.legend(fontsize=8); ax.grid(alpha=.3); fig.tight_layout()
fig.savefig("eta_t_phi.png", dpi=130)

# --- eta(Q2): interpolate eta(t) at common |t| targets within each Q2 bin ---
t_targets = [0.5, 1.0, 2.0]
fig, ax = plt.subplots(figsize=(7, 5))
for tt in t_targets:
    xq, ye = [], []
    for q in ubins:
        m = np.round(Q2c, 3) == q
        o = np.argsort(tc[m])
        tt_b, eta_b = tc[m][o], eta[m][o]
        if tt_b.min() <= tt <= tt_b.max():
            xq.append(q); ye.append(np.interp(tt, tt_b, eta_b))
    ax.plot(xq, ye, marker="s", ms=5, label=f"$|t|=${tt:.1f} GeV$^2$")
ax.axhline(1.0, ls=":", c="grey")
ax.set_xlabel("$Q^2$ (GeV$^2$)"); ax.set_ylabel(r"$\eta=\sigma_{obs}/\sigma_{Born}$")
ax.set_title(r"$\phi$ radiative correction $\eta(Q^2)$, "+VC+"")
ax.legend(fontsize=8); ax.grid(alpha=.3); fig.tight_layout()
fig.savefig("eta_q2_phi.png", dpi=130)
print("wrote eta_t_phi.png and eta_q2_phi.png")
print(f"eta range: {eta.min():.3f} - {eta.max():.3f}")
