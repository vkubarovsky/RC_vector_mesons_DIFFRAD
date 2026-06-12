#!/usr/bin/env python3
"""
plot_mdiffrad.py  --  Plot RC factor eta vs Q^2 from mdiffrad MC output

Usage:
    python plot_mdiffrad.py mc_result_nocut.txt mc_result_vmax20.txt mc_result_vmax12.txt

Each result file is the stdout of mdiffrad.exe, containing lines like:
 main  828.3      0.889  0.045  0.934  0.934  0.000
 main  828.2      0.889  0.045  0.934  0.934  0.000
 main  828.2      0.889  0.046  0.935  0.934  0.000   <-- take this (nev=3)

Column meanings:
    col 1: 'main'
    col 2: Born cross section (arb. units)
    col 3: delta_VS  (virtual+soft)
    col 4: delta_R   (real radiation)
    col 5: delta_total
    col 6: eta = running mean over nev iterations  <-- YOUR RESULT
    col 7: statistical error

The script takes every NEV-th 'main' line as the final result per point.

Output: eta_vs_q2_mc.png
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

Q2_VALS = [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
NEV     = 3   # nev in hermes_*.dat input files

STYLES = [
    {"label": r"no cut on $v_{\rm max}$",     "marker": "o", "fill": "none"},
    {"label": r"$v_{\rm max} = 2.0$ GeV$^2$", "marker": "^", "fill": "black"},
    {"label": r"$v_{\rm max} = 1.2$ GeV$^2$", "marker": "o", "fill": "black"},
]


def read_result(path, nev):
    """Read mdiffrad output, return (eta, err) taking every nev-th 'main' line."""
    eta_list, err_list = [], []
    count = 0
    with open(path) as f:
        for line in f:
            if not line.strip().startswith("main"):
                continue
            parts = line.split()
            if len(parts) < 7:
                continue
            count += 1
            if count % nev == 0:
                eta_list.append(float(parts[5]))  # running mean
                err_list.append(float(parts[6]))  # stat error
    return np.array(eta_list), np.array(err_list)


if len(sys.argv) < 4:
    print(__doc__)
    sys.exit(1)

files = sys.argv[1:4]

fig, ax = plt.subplots(figsize=(7, 5.5))

for i, fpath in enumerate(files):
    if not os.path.exists(fpath):
        print(f"WARNING: {fpath} not found, skipping.")
        continue

    eta, err = read_result(fpath, NEV)

    if len(eta) == 0:
        print(f"WARNING: no data found in {fpath}")
        continue

    npts = min(len(Q2_VALS), len(eta))
    q2   = Q2_VALS[:npts]
    eta  = eta[:npts]
    err  = err[:npts]

    style = STYLES[i]

    ax.errorbar(q2, eta, yerr=err,
                marker=style["marker"],
                color="black",
                markerfacecolor=style["fill"],
                markeredgecolor="black",
                markersize=7,
                linewidth=1.0,
                capsize=3,
                linestyle="-",
                label=style["label"])

    print(f"\n{'='*50}")
    print(f"File: {fpath}  ({style['label']})")
    print(f"{'Q2':>6}  {'eta':>8}  {'err':>8}")
    for j in range(npts):
        print(f"{q2[j]:6.2f}  {eta[j]:8.4f}  {err[j]:8.4f}")

ax.set_xlabel(r"$Q^2$, GeV$^2$", fontsize=13)
ax.set_ylabel(r"$\eta$",          fontsize=14)
ax.set_xlim(0, 5)
ax.set_ylim(0.75, 1.15)
ax.set_title(
    r"RC factor $\rho(770)$ electroproduction [MC], HERMES kinematics" + "\n" +
    r"$\sqrt{S}=7.9$ GeV,  $t=-0.11$ GeV$^2$,  $\langle y\rangle=0.55$",
    fontsize=10)
ax.legend(fontsize=10, frameon=True, loc="upper right")
ax.grid(True, linestyle="--", alpha=0.4)
ax.tick_params(direction="in", which="both")

fig.tight_layout()
outfile = "eta_vs_q2_mc.png"
fig.savefig(outfile, dpi=150)
print(f"\nPlot saved to: {outfile}")
plt.show()
