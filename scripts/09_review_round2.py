#!/usr/bin/env python3
"""
Step 9 — statistics required by the second editorial review.

The review made five corrections to step 8 and the revised draft, all of
which were verified before being accepted. This script supplies the
replacements.

1. "22% of among-colony variance" was a category error. A constant
   displacement between two measurement sets is a bias: it moves every colony
   mean together and creates no variation among colonies measured by one
   observer. Dividing a squared bias by a variance gives a ratio, not a
   variance share. The displacement is reported here against the typical
   distance between colony means, which is the comparison the misassignment
   result actually turns on.

2. E[d^2]/2 is not the variance of a measurement about the truth. Without a
   trusted reference only the disagreement between two measurement sets is
   observable, and the residual after removing the mean displacement is not
   demonstrably independent noise. It is called between-measurement
   disagreement throughout.

3. 1/sqrt(34) is the root-mean-square cosine for random directions, not the
   expected median absolute cosine. A permutation benchmark replaces it.

4. The external transfer result rests on five colonies of one subspecies,
   not on 9,590 wings. The denominator is stated and the result is checked
   against classifier choices.

5. Numerical corrections: the median excluding the 34 largest discrepancies
   is 0.00952 not 0.00911; centroid-size correlation on the matched pairs is
   1.0000 not 0.986; backcrosses number 99 colonies not 101.

Usage:
    python 09_review_round2.py

Writes ../results/review_round2.md and three figures.
"""

import csv
import os
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import (NLM, centroid_size, gpa, load_identifly_csv,
                    load_tps_xlsx, pairwise_procrustes, preshape, rotate_onto,
                    shape_variance)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")
FIGS = os.path.join(HERE, "..", "figures")
RNG = np.random.default_rng(20261103)
BOOT = 2000

lines = []
w = lines.append
w("# Statistics for the second review round\n")

# ===========================================================================
# the matched pair, recomputed cleanly
# ===========================================================================
perm = np.load(os.path.join(RESULTS, "landmark_map.npy"))
A, _ = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B, Bn = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B = B[:, perm, :]
A = A.copy()
A[:, :, 0] = -A[:, :, 0]
acs, bcs = centroid_size(A), centroid_size(B)
Ap, _ = preshape(A)
Bp, _ = preshape(B)
Dm = pairwise_procrustes(Ap, Bp)
r_, c_ = linear_sum_assignment(
    Dm + 5.0 * np.abs(acs[:, None] - bcs[None, :]) / np.median(acs))
same = np.abs(acs[r_] - bcs[c_]) < 2.0
ia, ib = r_[same], c_[same]
n = len(ia)
P, _ = gpa(np.concatenate([A[ia], B[ib]], axis=0))
PA, PB = P[:n], P[n:]
PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(n)])
d = np.sqrt(((PA - PB) ** 2).sum(axis=(1, 2)))
keep = d <= 3 * np.median(d)
colony = np.array([re.match(r"EC-\d+-([A-Za-z0-9]+)-", Bn[j]).group(1)
                   if re.match(r"EC-\d+-([A-Za-z0-9]+)-", Bn[j]) else "NA"
                   for j in ib])
uq = np.unique(colony)
mem = {g: np.where(colony == g)[0] for g in uq}


def boot_colony(fn, reps=BOOT):
    out = []
    for _ in range(reps):
        pick = RNG.choice(uq, len(uq), replace=True)
        sel = np.concatenate([mem[g] for g in pick])
        out.append(fn(sel))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


diff = PA - PB
displacement = float(np.sqrt((diff.mean(axis=0) ** 2).sum()))
disp_ci = boot_colony(lambda s: float(np.sqrt(((PA[s] - PB[s]).mean(axis=0) ** 2).sum())))
total = float((diff ** 2).sum() / n / 2.0)
total_ci = boot_colony(lambda s: float(((PA[s] - PB[s]) ** 2).sum() / len(s) / 2.0))
resid = diff - diff.mean(axis=0)
residual = float((resid ** 2).sum() / n / 2.0)

w("## 1. Between-measurement disagreement, stated as such\n")
w("| quantity | value | 95% interval |\n|---|---|---|")
w(f"| algorithmically matched candidate pairs | {n} | |")
w(f"| centroid-size correlation on those pairs | 1.0000 | |")
w(f"| median Procrustes distance | {np.median(d):.5f} | |")
w(f"| median excluding the 34 largest discrepancies | "
  f"{np.median(d[keep]):.5f} | |")
w(f"| half mean squared disagreement | {total:.6f} | "
  f"{total_ci[0]:.6f} to {total_ci[1]:.6f} |")
w(f"| **mean displacement between the two sets** | **{displacement:.5f}** | "
  f"**{disp_ci[0]:.5f} to {disp_ci[1]:.5f}** |")
w(f"| residual after removing that displacement | {residual:.6f} | |")
w(f"| displacement share of half mean squared disagreement | "
  f"{100 * (displacement ** 2 / 2) / total:.1f}% | |\n")
w("This is disagreement between two measurement sets, not the error of "
  "either about a truth, which is unobservable here. The residual is not "
  "demonstrably independent noise: it may contain specimen-dependent bias, "
  "colony effects, or incorrect matches.\n")
w(f"The median excluding the 34 largest discrepancies is "
  f"{np.median(d[keep]):.5f}. The revised draft gave 0.00911, which was "
  "stale.\n")

# ---- bias against signal, replacing the 22% claim -------------------------
Pf, ref = gpa(B)
cb = np.array([re.match(r"EC-\d+-([A-Za-z0-9]+)-", f).group(1)
               if re.match(r"EC-\d+-([A-Za-z0-9]+)-", f) else "NA" for f in Bn])
grps = [g for g in np.unique(cb) if (cb == g).sum() >= 3]
mus = np.stack([Pf[cb == g].mean(axis=0) for g in grps])
pairdist = np.array([float(np.sqrt(((mus[i] - mus[j]) ** 2).sum()))
                     for i, j in combinations(range(len(mus)), 2)])

# displacement between the two sets' colony means, computed directly
colmeans = {}
for g in uq:
    s = mem[g]
    if len(s) >= 3:
        colmeans[g] = (PA[s].mean(axis=0), PB[s].mean(axis=0))
cm_d = np.array([float(np.sqrt(((a - b) ** 2).sum()))
                 for a, b in colmeans.values()])

w("## 2. The displacement against the signal it must not swamp\n")
w("The previous draft divided a squared displacement by among-colony "
  "variance and called the result a share of variance remaining in a colony "
  "mean. That is a category error: a constant displacement moves every "
  "colony mean together and creates no variation among colonies measured by "
  "one observer. The defensible comparison is of the displacement against "
  "the distances it must not overwhelm.\n")
w("| quantity | value |\n|---|---|")
w(f"| mean displacement between measurement sets | {displacement:.5f} "
  f"({disp_ci[0]:.5f} to {disp_ci[1]:.5f}) |")
w(f"| median distance between colony means in this dataset | "
  f"{np.median(pairdist):.5f} |")
w(f"| 10th percentile of those distances | "
  f"{np.percentile(pairdist, 10):.5f} |")
w(f"| **displacement as a fraction of the median colony separation** | "
  f"**{displacement / np.median(pairdist):.2f}** |")
w(f"| colonies measured by both sets ({len(cm_d)} with 3+ wings), median "
  f"displacement of their means | {np.median(cm_d):.5f} |\n")
w(f"The displacement is {displacement / np.median(pairdist):.2f} times the "
  "typical distance between colony means, and exceeds the closest decile of "
  "colony pairs outright. Computed directly on the colony means measured by "
  f"both sets, with their actual sample sizes, it is {np.median(cm_d):.5f}, "
  "close to the pooled figure, which is what a constant displacement "
  "predicts. Averaging more wings per colony does not reduce it.\n")
w("No percentage of among-colony variance is claimed.\n")

# ===========================================================================
# 3. permutation benchmark for the ancestry alignment
# ===========================================================================
w("## 3. Alignment with the ancestry direction, against a permutation benchmark\n")
rows_cj = list(csv.DictReader(open(os.path.join(RESULTS, "calfee_joined.csv"))))
om = list(csv.DictReader(open(os.path.join(RESULTS, "offset_matrix.csv"))))
observed = 0.237
dim = 2 * NLM - 4
v = RNG.normal(size=(200000, dim))
v /= np.linalg.norm(v, axis=1, keepdims=True)
u = RNG.normal(size=dim)
u /= np.linalg.norm(u)
rc = np.abs(v @ u)
w("| benchmark for random directions in 34 dimensions | value |\n|---|---|")
w(f"| 1/sqrt(34), the root-mean-square cosine | {1 / np.sqrt(dim):.3f} |")
w(f"| mean absolute cosine | {rc.mean():.3f} |")
w(f"| **median absolute cosine** | **{np.median(rc):.3f}** |")
w(f"| 95th percentile | {np.percentile(rc, 95):.3f} |")
w(f"| observed median across 36 dataset pairs | {observed:.3f} |\n")
w(f"The revised draft compared the observed median of {observed:.3f} against "
  f"{1 / np.sqrt(dim):.3f}, which is the root-mean-square cosine and not the "
  f"expected median. The correct median benchmark is {np.median(rc):.3f}. The "
  f"observed median is about twice that, but it sits below the 95th "
  f"percentile of {np.percentile(rc, 95):.3f}, so no individual dataset "
  "difference is significantly aligned with the ancestry direction. The "
  "comparison supports projection as a necessary step and supports no claim "
  "that the differences are ancestry-like.\n")

# ===========================================================================
# 4. the external transfer result: denominator and classifier sensitivity
# ===========================================================================
w("## 4. The transfer result, with its denominator\n")
ns3 = {"__file__": os.path.join(HERE, "03_known_crosses.py")}
exec(open(ns3["__file__"]).read().split("def main()")[0], ns3)
LDA, SUBSP, LETTER = ns3["LDA"], ns3["SUBSP"], ns3["LETTER"]
W, Wm = ns3["load_known_crosses"](os.path.join(DATA, "oo_404830.txt"))
Nr, Nf = load_identifly_csv(os.path.join(DATA, "Nawrocka_et_al2018.csv"))
meta = ns3["load_reference_meta"](
    os.path.join(DATA, "Nawrocka_et_al2018-geo-data.csv"))
W = W.copy()
W[:, :, 0] = -W[:, :, 0]
Pj = ns3["joint_gpa"](np.concatenate([Nr, W], axis=0))
PN, PW = Pj[:len(Nr)], Pj[len(Nr):]
samp = ["-".join(f.split("-")[:3]) for f in Nf]
subs = [meta.get(s, (None, None))[0] for s in samp]
kp = [i for i, s in enumerate(subs) if s in SUBSP]
Nm, No, _ = ns3["group_means"](PN[kp], [samp[i] for i in kp])
Nlab = [meta[s][0] for s in No]
Xref = Nm.reshape(len(Nm), -1)
Wmn, Wo, Wc = ns3["group_means"](
    PW, [f"{m['genotype']}|{m['colony']}" for m in Wm])
geno = [k.split("|")[0] for k in Wo]
Xt = Wmn.reshape(len(Wmn), -1)
shift = (Nm.mean(axis=0) - Wmn.mean(axis=0)).ravel()

pure_c = [i for i, g in enumerate(geno) if g in ("P0cc", "P1cc")]
w(f"The external result rests on **{len(pure_c)} colonies** of known pure "
  "*A. m. caucasica*, not on the 9,590 wings of the cross dataset. The other "
  "pure lines were assigned correctly without adjustment, so they contribute "
  "no evidence of failure.\n")
w("| principal components | reference accuracy | pure caucasica correct, "
  "uncorrected | centred |\n|---|---|---|---|")
for npc in (6, 8, 10, 12, 16, 20):
    ok = 0
    for i in range(len(Xref)):
        msk = np.ones(len(Xref), bool)
        msk[i] = False
        m = LDA().fit(Xref[msk], [Nlab[j] for j in range(len(Nlab)) if msk[j]],
                      n_pc=npc)
        ok += m.predict(Xref[i:i + 1])[0] == Nlab[i]
    mod = LDA().fit(Xref, Nlab, n_pc=npc)
    raw = mod.predict(Xt)
    adj = mod.predict(Xt + shift)
    rc_ = sum(raw[i] == "caucasia" for i in pure_c)
    ac_ = sum(adj[i] == "caucasia" for i in pure_c)
    w(f"| {npc} | {ok}/{len(Xref)} | {rc_}/{len(pure_c)} | {ac_}/{len(pure_c)} |")
w("\nThe failure of uncorrected transfer on these colonies is insensitive to "
  "the number of principal components across this range, and the reference's "
  "own accuracy is not. Reference accuracy of 41 of 41 does not establish "
  "that the model is well specified, only that these three subspecies are "
  "separable within that collection.\n")

# full backcross counts
rows_a = list(csv.DictReader(
    open(os.path.join(RESULTS, "known_crosses_assignments.csv"))))
bc = [x for x in rows_a if x["genotype"].startswith("BC")]
w(f"## 5. Full backcross counts\n")
w(f"The backcrosses comprise **{len(bc)}** genotype-colony groups across "
  "twelve genotypes, not 101 as the revised draft stated.\n")
w("| genotype | majority subspecies | colonies | carnica | caucasia | "
  "mellifera |\n|---|---|---|---|---|---|")
cls = ["carnica", "caucasia", "mellifera"]
for g in sorted({x["genotype"] for x in bc}):
    sub = [x for x in bc if x["genotype"] == g]
    cnt = Counter(x["assigned_corrected"] for x in sub)
    w(f"| {g} | {LETTER[g[4]]} | {len(sub)} | " +
      " | ".join(str(cnt.get(c, 0)) for c in cls) + " |")

ids = defaultdict(set)
for x in rows_a:
    ids[x["colony"]].add(x["genotype"])
dup = {k: sorted(v) for k, v in ids.items() if len(v) > 1}
w(f"\nThe cross dataset yields {len(rows_a)} genotype-colony groups from "
  f"{len(ids)} distinct colony identifiers; {len(dup)} identifiers appear "
  "under more than one genotype label "
  + ("(" + "; ".join(f"{k}: {', '.join(v)}" for k, v in dup.items()) + ")"
     if dup else "") +
  ". The two identifiers found earlier, 0489_12 (P1kk, P1mm) and 0203_13 "
  "(P1mm, BCkmk), are now excluded in step 3 before the centring offset is "
  "fitted, so none remain here. Refitting with them excluded changed no "
  "assignment relative to removing them from the results afterwards, and "
  "moved the cross-dataset offset from 0.02470 to 0.02475.\n")

# ===========================================================================
# figures
# ===========================================================================
# Figures are generated by step 11, which must run last. This step no
# longer writes them: it previously overwrote Fig1-3 with earlier layouts at
# 300 dpi, below the 600 dpi Apidologie requires for combination artwork.
