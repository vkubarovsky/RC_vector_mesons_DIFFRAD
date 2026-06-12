#!/usr/bin/env python3
"""
Plot radiative correction eta vs Q2 from 3 result files.

Usage:
    python plot_hermes.py hermes_nocut_res.txt hermes20_res.txt hermes12_res.txt

Each file is the redirected terminal output of run_fortran.sh, e.g.:
    ./run_fortran.sh mdiffrad hermes_nocut.dat  > hermes_nocut_res.txt
    ./run_fortran.sh mdiffrad hermes_vmax20.dat > hermes20_res.txt
    ./run_fortran.sh mdiffrad hermes_vmax12.dat > hermes12_res.txt
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

# ── Q2 points: must match your input files ────────────────────────────────────
Q2_VALS = [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
NEV     = 3   # nev in input file: MC iterations per kinematic point

# ── Curve style: matches Fig. 7 ───────────────────────────────────────────────
CURVES = [
    {"label": r"no cut on $v_{max}$",      "marker": "o", "fill": "none"},
    {"label": r"$v_{max} = 2.0$ GeV$^2$",  "marker": "^", "fill": "black"},
    {"label": r"$v_{max} = 1.2$ GeV$^2$",  "marker": "o", "fill": "black"},
]

# ── Read result file ──────────────────────────────────────────────────────────
def read_result(path, nev):
    """
    Extract eta (col 6) and err (col 7) from every nev-th 'main' line.
    col 1: 'main'
    col 2: Born xs
    col 3: delta_VS
    col 4: delta_R
    col 5: delta_total
    col 6: eta = running mean  <-- result
    col 7: stat error
    """
    eta_list, err_list = [], []
    count = 0
    with open(path) as f:
        for line in f:
            if " main" not in line:
                continue
            parts = line.split()
            if parts[0] != "main":
                continue
            count += 1
            if count % nev == 0:
                eta_list.append(float(parts[5]))
                err_list.append(float(parts[6]))
    return np.array(eta_list), np.array(err_list)

# ── Main ──────────────────────────────────────────────────────────────────────
if len(sys.argv) < 4:
    print(__doc__)
    sys.exit(1)

files = sys.argv[1:4]

fig, ax = plt.subplots(figsize=(7, 5.5))

for i, fpath in enumerate(files):
    eta, err = read_result(fpath, NEV)
    npts = min(len(Q2_VALS), len(eta))
    q2   = Q2_VALS[:npts]
    eta  = eta[:npts]
    err  = err[:npts]

    style = CURVES[i]
    ax.errorbar(q2, eta, yerr=err,
                label=style["label"],
                marker=style["marker"],
                color="black",
                markerfacecolor=style["fill"],
                markeredgecolor="black",
                markersize=7,
                linewidth=1.0,
                capsize=3,
                linestyle="-")

ax.set_xlabel(r"$Q^2$, GeV$^2$", fontsize=13)
ax.set_ylabel(r"$\eta$",          fontsize=14)
ax.set_xlim(0, 5)
ax.set_ylim(0.75, 1.15)
ax.set_title(
    r"RC factor $\rho(770)$ electroproduction, HERMES kinematics" + "\n" +
    r"$\sqrt{S}=7.9$ GeV,  $t=-0.11$ GeV$^2$,  $\langle y\rangle=0.55$",
    fontsize=10)
ax.legend(fontsize=10, frameon=True)
ax.grid(True, linestyle="--", alpha=0.4)
ax.tick_params(direction="in", which="both")

fig.tight_layout()
fig.savefig("eta_vs_q2.png", dpi=150)
print("Saved: eta_vs_q2.png")
plt.show()
