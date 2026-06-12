#!/usr/bin/env python3
"""
plot_idiffrad.py  --  Plot RC factor eta vs Q^2 from idiffrad output

Usage:
    python plot_idiffrad.py result_nocut.txt result_vmax20.txt result_vmax12.txt

Each result file is the stdout of idiffrad.exe, containing lines like:
    0.012 0.550   0.400  34.806  -0.110    0.886    0.870    0.016
    xs    ys      q2     w2      t         eta      wei      |diff|

Column meanings:
    col 1: x  (Bjorken x)
    col 2: y
    col 3: Q^2
    col 4: W^2
    col 5: t
    col 6: eta = sig_rad / sig_Born  <-- YOUR RESULT
    col 7: wei = analytic approximation
    col 8: |eta - wei|  (difference)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Q2 values matching your input files
Q2_VALS = [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]

# Curve styles matching Fig. 7
STYLES = [
    {"label": r"no cut on $v_{\rm max}$",     "marker": "o", "fill": "none"},
    {"label": r"$v_{\rm max} = 2.0$ GeV$^2$", "marker": "^", "fill": "black"},
    {"label": r"$v_{\rm max} = 1.2$ GeV$^2$", "marker": "o", "fill": "black"},
]


def read_result(path):
    """
    Read idiffrad stdout file.
    Returns arrays: q2, eta, wei
    Looks for lines with 8 numeric columns (the main result line).
    """
    q2_list, eta_list, wei_list = [], [], []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 8:
                continue
            try:
                vals = [float(p) for p in parts]
            except ValueError:
                continue
            # col 3 = Q2, col 6 = eta, col 7 = wei
            q2_list.append(vals[2])
            eta_list.append(vals[5])
            wei_list.append(vals[6])
    return np.array(q2_list), np.array(eta_list), np.array(wei_list)


# ── Parse arguments ───────────────────────────────────────────────────────────
if len(sys.argv) < 4:
    print(__doc__)
    sys.exit(1)

files = sys.argv[1:4]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5.5))

for i, fpath in enumerate(files):
    if not os.path.exists(fpath):
        print(f"WARNING: {fpath} not found, skipping.")
        continue

    q2, eta, wei = read_result(fpath)

    if len(q2) == 0:
        print(f"WARNING: no data found in {fpath}")
        continue

    style = STYLES[i]
    fc = style["fill"]

    ax.plot(q2, eta,
            marker=style["marker"],
            color="black",
            markerfacecolor=fc,
            markeredgecolor="black",
            markersize=7,
            linewidth=1.0,
            linestyle="-",
            label=style["label"])

    # Print table to terminal
    print(f"\n{'='*50}")
    print(f"File: {fpath}  ({style['label']})")
    print(f"{'Q2':>6}  {'eta':>8}  {'wei':>8}  {'diff':>8}")
    for j in range(len(q2)):
        print(f"{q2[j]:6.2f}  {eta[j]:8.4f}  {wei[j]:8.4f}  {abs(eta[j]-wei[j]):8.4f}")

ax.set_xlabel(r"$Q^2$, GeV$^2$", fontsize=13)
ax.set_ylabel(r"$\eta$",          fontsize=14)
ax.set_xlim(0, 5)
ax.set_ylim(0.75, 1.15)
ax.set_title(
    r"RC factor $\rho(770)$ electroproduction, HERMES kinematics" + "\n" +
    r"$\sqrt{S}=7.9$ GeV,  $t=-0.11$ GeV$^2$,  $\langle y\rangle=0.55$",
    fontsize=10)
ax.legend(fontsize=10, frameon=True, loc="upper right")
ax.grid(True, linestyle="--", alpha=0.4)
ax.tick_params(direction="in", which="both")

fig.tight_layout()
outfile = "eta_vs_q2.png"
fig.savefig(outfile, dpi=150)
print(f"\nPlot saved to: {outfile}")
plt.show()
