#!/usr/bin/env python3
"""Rebuild etamc.dat robustly: average only the finite per-sample 'de'
values, so a single NaN sample no longer poisons a whole bin.
Usage: python recover_eta.py <run.log>  (reads inmdi.dat for npoi/nev/header)"""
import sys, numpy as np

log = sys.argv[1] if len(sys.argv) > 1 else "run_full_reseed.log"

# header info from inmdi.dat
cfg = [l.split("!")[0].strip() for l in open("inmdi.dat")]
cfg = [l for l in cfg if l]
bmom = float(cfg[0].split()[0]); ivec = int(cfg[3].split()[0])
vcut = float(cfg[5].split()[0]); nev = int(cfg[6].split()[0])
seed = int(cfg[7].split()[0]); npoi = int(cfg[8].split()[0])

# per-sample 'de' (5th token after 'main') in file order
de = []
for l in open(log):
    if l.lstrip().startswith("main"):
        t = l.split()
        try: de.append(float(t[4]))   # t=['main',born,dev,der,de,mean,err]
        except (IndexError, ValueError): de.append(np.nan)
de = np.array(de).reshape(npoi, nev)

eta = np.full(npoi, np.nan); err = np.zeros(npoi); ndrop = 0
for i in range(npoi):
    g = de[i][np.isfinite(de[i])]
    ndrop += nev - len(g)
    if len(g):
        eta[i] = g.mean()
        err[i] = g.std(ddof=1) / np.sqrt(len(g)) if len(g) > 1 else 0.0

with open("etamc.dat", "w") as f:
    f.write(f" bmom = {bmom:7.3f}\n tmom =   0.000\n lepton  1\n")
    f.write(f" ivec = {ivec:2d}\n cutv = {vcut:7.3f}\n  nev = {nev:4d}\n")
    f.write(f" iy : {seed:9d}\n npoi = {npoi:2d}\n")
    for i in range(npoi):
        f.write(f"{i+1:5d}{eta[i]:7.3f}{err[i]:7.3f}\n")

nbad = int(np.sum(~np.isfinite(eta)))
print(f"recovered {npoi-nbad}/{npoi} points; dropped {ndrop} NaN samples; "
      f"{nbad} bins still all-NaN")
