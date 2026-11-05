#!/usr/bin/env python3
"""Figures for the Journal of Apicultural Research submission.

Journal requirements applied here: sans-serif fonts in figures, no titles or
captions inside the illustration, 300 dpi for colour and 600 dpi for
greyscale, supplied as JPEG. Three main figures, one supplementary.
"""
import csv
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.optimize import linear_sum_assignment

REPO = "/home/claude/honeybee-wing-reliability-"
sys.path.insert(0, os.path.join(REPO, "scripts"))
from wingio import (NLM, centroid_size, gpa, load_identifly_csv,
                    load_tps_xlsx, pairwise_procrustes, preshape, rotate_onto)

DATA, RES = os.path.join(REPO, "data"), os.path.join(REPO, "results")
OUT = os.path.join(REPO, "figures_jar")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 9, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.05,
})
GREY, DARK, HL = "#9a9a9a", "#2b2b2b", "#b03030"


def save(fig, name, dpi):
    path = os.path.join(OUT, name + ".jpg")
    fig.savefig(path, format="jpeg", dpi=dpi, pil_kwargs={"quality": 95})
    plt.close(fig)
    print(f"  {name}.jpg  {dpi} dpi  {os.path.getsize(path)/1e6:.2f} MB")


# ------------------------------------------------------------------ data
perm = np.load(os.path.join(RES, "landmark_map.npy"))
A, Anames = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B, Bnames = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B = B[:, perm, :]
A = A.copy(); A[:, :, 0] = -A[:, :, 0]
acs, bcs = centroid_size(A), centroid_size(B)
Ap, _ = preshape(A); Bp, _ = preshape(B)
r_, c_ = linear_sum_assignment(
    pairwise_procrustes(Ap, Bp)
    + 5.0 * np.abs(acs[:, None] - bcs[None, :]) / np.median(acs))
m = np.abs(acs[r_] - bcs[c_]) < 2.0
ia, ib = r_[m], c_[m]
n = len(ia)
P, _ = gpa(np.concatenate([A[ia], B[ib]], axis=0))
PA, PB = P[:n], P[n:]
PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(n)])
d = np.sqrt(((PA - PB) ** 2).sum(axis=(1, 2)))
med = float(np.median(d)); keep = d <= 3 * med
disp = float(np.sqrt(((PA - PB).mean(axis=0) ** 2).sum()))
LAB = [int(x) + 1 for x in perm]
L7, L14 = LAB.index(7), LAB.index(14)

print("writing figures:")

# =========================================== Figure 1  per-landmark profile
diff = PA[keep] - PB[keep]
rms = np.sqrt((diff ** 2).sum(axis=2).mean(axis=0))
order = np.argsort(LAB)
fig, ax = plt.subplots(figsize=(5.2, 2.3))
ax.bar(range(1, 20), rms[order],
       color=[HL if LAB[i] in (7, 14) else GREY for i in order],
       edgecolor="white", lw=0.4)
oth = float(np.median([rms[i] for i in range(19) if LAB[i] not in (7, 14)]))
ax.axhline(oth, color=DARK, lw=0.8, ls=(0, (4, 2)))
ax.set_ylim(0, rms.max() * 1.18)
ax.set_xticks(range(1, 20))
ax.set_xlabel("Landmark")
ax.set_ylabel("RMS disagreement\n(units of centroid size)")
ax.spines[["top", "right"]].set_visible(False)
save(fig, "Figure1", 300)

# ===================================== Figure 2  displacement vs separation
Pfull, _ = gpa(B)
col = np.array([(mm.group(1) if (mm := re.match(r"EC-\d+-([A-Za-z0-9]+)-", s))
                 else "NA") for s in Bnames])
means = np.stack([Pfull[col == c].mean(axis=0) for c in sorted(set(col))
                  if c != "NA" and (col == c).sum() >= 3])
mp, _ = preshape(means)
pd_ = pairwise_procrustes(mp, mp)[np.triu_indices(len(means), 1)]
fig, ax = plt.subplots(figsize=(5.2, 2.3))
ax.hist(pd_, bins=40, color=GREY, edgecolor="white", lw=0.3)
ax.axvspan(0.00844, 0.00916, color=HL, alpha=0.22, lw=0)
ax.axvline(disp, color=HL, lw=1.3)
ax.axvline(float(np.median(pd_)), color=DARK, lw=1.0, ls=(0, (4, 2)))
ax.axvline(float(np.percentile(pd_, 10)), color=DARK, lw=0.8, ls=(0, (1, 2)))
ax.set_xlim(0.004, pd_.max() * 1.02)
ax.set_xlabel("Procrustes distance between colony means")
ax.set_ylabel("Colony pairs")
ax.spines[["top", "right"]].set_visible(False)
save(fig, "Figure2", 300)

# ========================================== Figure 3  assignment, 2 panels
kr = [x for x in csv.DictReader(
    open(os.path.join(RES, "known_crosses_assignments.csv")))]
CLS = ["carnica", "caucasia", "mellifera"]
SHOW = ["carnica", "caucasica", "mellifera"]
GRP = [("Pure lines", tuple(g for g in {x["genotype"] for x in kr}
                            if g.startswith("P"))),
       ("F1 hybrids", tuple(g for g in {x["genotype"] for x in kr}
                            if g.startswith("F1"))),
       ("Backcrosses", tuple(g for g in {x["genotype"] for x in kr}
                             if g.startswith("BC")))]
fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.4), sharey=True)
for ax, key, ttl in zip(axes, ("assigned_raw", "assigned_corrected"),
                        ("(a) Uncorrected", "(b) After centring")):
    M, labs = [], []
    for name, gs_ in GRP:
        sub = [x for x in kr if x["genotype"] in gs_]
        cnt = np.array([sum(1 for x in sub if x[key] == c) for c in CLS],
                       dtype=float)
        M.append(cnt / max(cnt.sum(), 1))
        labs.append(f"{name}\n(n = {len(sub)})")
    M = np.array(M)
    ax.imshow(M, cmap="Greys", vmin=0, vmax=1, aspect="auto")
    for i in range(M.shape[0]):
        sub = [x for x in kr if x["genotype"] in GRP[i][1]]
        for j in range(M.shape[1]):
            k = sum(1 for x in sub if x[key] == CLS[j])
            ax.text(j, i, str(k), ha="center", va="center", fontsize=8,
                    color="white" if M[i, j] > 0.55 else DARK)
    ax.set_xticks(range(3)); ax.set_xticklabels(SHOW, style="italic",
                                                fontsize=8)
    ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs, fontsize=8)
    ax.set_xlabel(ttl, fontsize=9)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
save(fig, "Figure3", 600)

# ============================== Supplementary figure S1  full distribution
fig = plt.figure(figsize=(5.2, 2.3))
gs = GridSpec(1, 2, width_ratios=[2.2, 1], wspace=0.34, figure=fig)
ax = fig.add_subplot(gs[0])
ax.hist(d, bins=np.linspace(0, 0.04, 61), color=GREY, edgecolor="white",
        lw=0.3)
ax.axvline(med, color=DARK, lw=1.0)
ax.axvline(3 * med, color=HL, lw=1.0, ls=(0, (4, 2)))
ax.set_xlim(0, 0.04)
ax.set_xlabel("Procrustes distance between the two measurements")
ax.set_ylabel("Candidate pairs")
ax.text(0.97, 0.95, "(a)", transform=ax.transAxes, ha="right", va="top",
        fontsize=9)
ax2 = fig.add_subplot(gs[1])
ax2.hist(d, bins=np.logspace(np.log10(max(d.min(), 1e-4)),
                             np.log10(d.max()), 34),
         color=GREY, edgecolor="white", lw=0.3)
ax2.set_xscale("log")
ax2.axvline(3 * med, color=HL, lw=1.0, ls=(0, (4, 2)))
ax2.set_xlabel("Same, logarithmic scale")
ax2.set_ylabel("Candidate pairs")
ax2.text(0.97, 0.95, "(b)", transform=ax2.transAxes, ha="right", va="top",
         fontsize=9)
for a_ in (ax, ax2):
    a_.spines[["top", "right"]].set_visible(False)
save(fig, "FigureS1", 300)

print(f"\nkey values: LM7 {rms[L7]:.5f}  LM14 {rms[L14]:.5f}  "
      f"others {oth:.5f}  displacement {disp:.5f}  "
      f"colonies {len(means)}  pairs {len(pd_)}")
