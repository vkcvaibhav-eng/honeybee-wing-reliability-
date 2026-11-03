#!/usr/bin/env python3
"""Step 11 - figures for v4, as vector PDF plus 600 dpi TIFF."""
import os, re, sys, csv
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
FIGS = os.path.join(REPO, "figures"); os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "font.size": 8, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6,
                     "savefig.bbox": "tight", "savefig.pad_inches": 0.04})
GREY, DARK, HL = "#9a9a9a", "#2b2b2b", "#b03030"

def save(fig, name):
    fig.savefig(os.path.join(FIGS, name + ".pdf"))
    fig.savefig(os.path.join(FIGS, name + ".tif"), format="tiff", dpi=600)
    plt.close(fig)
    print("wrote", name + ".pdf /.tif")

# ---------------------------------------------------------------- data
perm = np.load(os.path.join(RES, "landmark_map.npy"))
A_raw, _ = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B_raw, B_names = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B_raw = B_raw[:, perm, :]
A_raw = A_raw.copy(); A_raw[:, :, 0] = -A_raw[:, :, 0]
a_cs, b_cs = centroid_size(A_raw), centroid_size(B_raw)
A_pre, _ = preshape(A_raw); B_pre, _ = preshape(B_raw)
r_, c_ = linear_sum_assignment(
    Dm := pairwise_procrustes(A_pre, B_pre)
    + 5.0 * np.abs(a_cs[:, None] - b_cs[None, :]) / np.median(a_cs))
ia, ib = r_[np.abs(a_cs[r_] - b_cs[c_]) < 2.0], c_[np.abs(a_cs[r_] - b_cs[c_]) < 2.0]
n = len(ia)
P, _ = gpa(np.concatenate([A_raw[ia], B_raw[ib]], axis=0))
PA, PB = P[:n], P[n:]
PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(n)])
d = np.sqrt(((PA - PB) ** 2).sum(axis=(1, 2)))
med = float(np.median(d)); keep = d <= 3 * med
disp = float(np.sqrt(((PA - PB).mean(axis=0) ** 2).sum()))
LAB = [int(x) + 1 for x in perm]
L7, L14 = LAB.index(7), LAB.index(14)

# ================================================== Fig 1  full distribution
fig = plt.figure(figsize=(5.1, 2.5))
gs = GridSpec(1, 2, width_ratios=[2.25, 1], wspace=0.32, figure=fig)
ax = fig.add_subplot(gs[0])
ax.hist(d, bins=np.linspace(0, 0.04, 61), color=GREY, edgecolor="white", lw=0.3)
ax.axvline(med, color=DARK, lw=1.0)
ax.axvline(3 * med, color=HL, lw=1.0, ls=(0, (4, 2)))
ax.annotate(f"median\n{med:.5f}", (med, ax.get_ylim()[1] * 0.93),
            xytext=(6, 0), textcoords="offset points", fontsize=7,
            va="top", color=DARK)
ax.annotate(f"3 x median\n{3*med:.4f}", (3 * med, ax.get_ylim()[1] * 0.60),
            xytext=(6, 0), textcoords="offset points", fontsize=7,
            va="top", color=HL)
ax.set_xlabel("Procrustes distance between the two measurements")
ax.set_ylabel("candidate pairs")
ax.set_xlim(0, 0.04)
ax.text(0.98, 0.98, "a", transform=ax.transAxes, fontsize=9,
        fontweight="bold", ha="right", va="top")
ax2 = fig.add_subplot(gs[1])
ax2.hist(d, bins=np.logspace(np.log10(max(d.min(), 1e-4)),
                             np.log10(d.max()), 34),
         color=GREY, edgecolor="white", lw=0.3)
ax2.set_xscale("log")
ax2.axvline(3 * med, color=HL, lw=1.0, ls=(0, (4, 2)))
ax2.set_xlabel("same, logarithmic scale")
ax2.set_ylabel("candidate pairs")
ax2.text(0.98, 0.98, "b", transform=ax2.transAxes, fontsize=9,
         fontweight="bold", ha="right", va="top")
ax2.annotate(f"max {d.max():.3f}", (d.max(), 1), xytext=(-4, 16),
             textcoords="offset points", fontsize=6.5, ha="right", color=DARK,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=DARK))
for a_ in (ax, ax2):
    a_.spines[["top", "right"]].set_visible(False)
save(fig, "Fig1")
print(f"  n={len(d)}  above 3x median={int((~keep).sum())}  max={d.max():.5f}")

# ================================================== Fig 2  scale comparison
Pfull, _ = gpa(B_raw)
col_all = np.array([(m.group(1) if (m := re.match(r"EC-\d+-([A-Za-z0-9]+)-", s))
                     else "NA") for s in B_names])
means = np.stack([Pfull[col_all == c].mean(axis=0) for c in sorted(set(col_all))
                  if c != "NA" and (col_all == c).sum() >= 3])
mp, _ = preshape(means)
Dc = pairwise_procrustes(mp, mp)
pairdist = Dc[np.triu_indices(len(means), 1)]
frac = float((pairdist < disp).mean())

fig, ax = plt.subplots(figsize=(5.1, 2.4))
ax.hist(pairdist, bins=40, color=GREY, edgecolor="white", lw=0.3)
ax.axvspan(0.00844, 0.00916, color=HL, alpha=0.22, lw=0)
ax.axvline(disp, color=HL, lw=1.2)
ax.axvline(np.median(pairdist), color=DARK, lw=1.0, ls=(0, (4, 2)))
ax.axvline(np.percentile(pairdist, 10), color=DARK, lw=0.8, ls=(0, (1, 2)))
y = ax.get_ylim()[1]
ax.annotate(f"displacement {disp:.5f}", (disp, y * 0.97), xytext=(7, 0),
            textcoords="offset points", fontsize=7, ha="left", va="top",
            color=HL)
ax.annotate(f"10th percentile {np.percentile(pairdist,10):.5f}",
            (np.percentile(pairdist, 10), y * 0.82), xytext=(-6, 0),
            textcoords="offset points", fontsize=6.5, ha="right", va="top",
            color=DARK)
ax.annotate(f"median {np.median(pairdist):.5f}", (np.median(pairdist), y * 0.97),
            xytext=(6, 0), textcoords="offset points", fontsize=7, va="top",
            color=DARK)
ax.set_xlim(0.004, pairdist.max() * 1.02)
ax.set_xlabel("Procrustes distance between colony means "
              "(re-measured Ecuadorian set)")
ax.set_ylabel("colony pairs")
ax.spines[["top", "right"]].set_visible(False)
ax.text(0.99, 0.62,
        f"{len(means)} colonies, {len(pairdist)} pairs\n"
        f"{100*frac:.1f}% of pairs below the displacement",
        transform=ax.transAxes, fontsize=6.5, ha="right", va="top")
save(fig, "Fig2")
print(f"  colonies={len(means)} pairs={len(pairdist)} "
      f"p10={np.percentile(pairdist,10):.5f} frac_below={frac:.4f}")

# ================================================== Fig 3  assignments, 2 panels
kr = list(csv.DictReader(open(os.path.join(RES, "known_crosses_assignments.csv"))))
BADID = {"0489_12", "0203_13"}
kr = [r for r in kr if r["colony"] not in BADID]
CLS = ["carnica", "caucasia", "mellifera"]
SHOW = ["carnica", "caucasica", "mellifera"]
GRP = [("pure lines", ("P0cc", "P1cc", "P0kk", "P1kk", "P0mm", "P1mm")),
       ("F1 hybrids", ("F1ck", "F1kc", "F1cm", "F1mc", "F1km", "F1mk")),
       ("backcrosses", tuple(sorted({r["genotype"] for r in kr}
                                    if False else
                                    [g for g in {r["genotype"] for r in kr}
                                     if g.startswith("BC")])))]
fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.5), sharey=True)
for ax, key, ttl in zip(axes, ("assigned_raw", "assigned_corrected"),
                        ("a  uncorrected", "b  after grand-mean centring")):
    rowsl, labs = [], []
    for name, gs_ in GRP:
        sub = [r for r in kr if r["genotype"] in gs_]
        cnt = np.array([sum(1 for r in sub if r[key] == c) for c in CLS],
                       dtype=float)
        rowsl.append(cnt / max(cnt.sum(), 1))
        labs.append(f"{name}\n(n={len(sub)})")
    M = np.array(rowsl)
    ax.imshow(M, cmap="Greys", vmin=0, vmax=1, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            sub = [r for r in kr if r["genotype"] in GRP[i][1]]
            k = sum(1 for r in sub if r[key] == CLS[j])
            ax.text(j, i, str(k), ha="center", va="center", fontsize=7.5,
                    color="white" if M[i, j] > 0.55 else DARK)
    ax.set_xticks(range(3)); ax.set_xticklabels(SHOW, style="italic",
                                                fontsize=7)
    ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs, fontsize=7)
    ax.set_xlabel("assigned subspecies", fontsize=8)
    ax.set_title(ttl, fontsize=8, loc="left")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
fig.text(0.5, -0.07, "colonies, 12 principal components; shading gives the "
         "proportion within each row", ha="center", fontsize=6.5)
save(fig, "Fig3")

# ================================================== Fig 4  per-landmark profile
diff = PA[keep] - PB[keep]
rms = np.sqrt((diff ** 2).sum(axis=2).mean(axis=0))
ordr = np.argsort(LAB)
fig, ax = plt.subplots(figsize=(5.1, 2.2))
cols = [HL if LAB[i] in (7, 14) else GREY for i in ordr]
ax.bar(range(1, 20), rms[ordr], color=cols, edgecolor="white", lw=0.4)
oth = np.median([rms[i] for i in range(19) if LAB[i] not in (7, 14)])
ax.axhline(oth, color=DARK, lw=0.8, ls=(0, (4, 2)))
ax.annotate(f"median of the other seventeen, {oth:.5f}", (19.4, oth),
            xytext=(0, 4), textcoords="offset points", fontsize=6.5,
            ha="right", color=DARK)
ax.set_ylim(0, rms.max() * 1.30)
ax.set_xticks(range(1, 20)); ax.set_xticklabels(range(1, 20), fontsize=7)
ax.set_xlabel("landmark (Nawrocka et al. 2018 numbering)")
ax.set_ylabel("RMS disagreement\n(unit centroid size)")
ax.spines[["top", "right"]].set_visible(False)
sq = ((PA[keep] - PB[keep]).mean(axis=0) ** 2).sum(axis=1)
ax.text(0.015, 0.97, f"landmarks 7 and 14 carry "
        f"{100*(sq[L7]+sq[L14])/sq.sum():.1f}%\nof the squared displacement",
        transform=ax.transAxes, fontsize=7, ha="left", va="top", color=HL)
save(fig, "Fig4")
print(f"  LM7={rms[L7]:.5f} LM14={rms[L14]:.5f} other_median={oth:.5f} "
      f"share={100*(sq[L7]+sq[L14])/sq.sum():.1f}%")
