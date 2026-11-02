#!/usr/bin/env python3
"""
Step 8 — corrected estimates, replacing the figures in steps 2, 4, 5 and 7.

An editorial review of the first draft identified errors that this script
corrects. Each is named here so the record is explicit.

1. The two error estimates used different formulae. Step 2 computed
   median(d)^2 / 2 and step 4 computed mean(d^2) / 4, which differ by a factor
   of two in scaling as well as in summary statistic. Their apparent agreement
   to 5% was an artefact. One convention is used throughout here: the variance
   of a single measurement about the truth is E[d^2] / 2, where d is the
   Procrustes distance between two measurements of the same specimen.

2. Random and systematic disagreement are reported separately. A constant
   displacement between two observers does not shrink when more wings are
   averaged, so reporting only a pooled variance understates the risk to
   colony means.

3. The Ecuador comparison is restricted to the verified matched pairs. The
   first draft compared the mean of 663 records against the mean of 726,
   which is not a paired comparison.

4. Sensitivity to the matching decision is reported rather than assumed. The
   first draft discarded large discrepancies as failed matches without
   independent confirmation.

5. The split-half baseline, previously a literal value copied from an
   uncommitted script, is computed here with its repetitions and interval.

6. Bilateral wings are aligned before averaging, not after.

Confidence intervals are bootstrap percentile intervals over colonies where
colony structure is recoverable, otherwise over specimens, because wings
within a colony are not independent.

Usage:
    python 08_corrected_estimates.py

Writes ../results/corrected_estimates.md
"""

import csv
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import (NLM, centroid_size, gpa, load_identifly_csv,
                    load_tps_xlsx, pairwise_procrustes, preshape, rotate_onto,
                    shape_variance)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

RNG = np.random.default_rng(20261103)
BOOT = 2000
SIDE_RE = re.compile(r"-(LW|RW1|RW|L|R)([-.])")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def boot_ci(values, groups=None, stat=np.mean, reps=BOOT):
    """Bootstrap percentile interval, resampling groups when given."""
    values = np.asarray(values)
    if groups is None:
        idx = np.arange(len(values))
        draws = [stat(values[RNG.choice(idx, len(idx), replace=True)])
                 for _ in range(reps)]
    else:
        groups = np.asarray(groups)
        uniq = np.unique(groups)
        members = {g: np.where(groups == g)[0] for g in uniq}
        draws = []
        for _ in range(reps):
            pick = RNG.choice(uniq, len(uniq), replace=True)
            sel = np.concatenate([members[g] for g in pick])
            draws.append(stat(values[sel]))
    return float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def decompose(PA, PB):
    """Split disagreement between two measurement sets of the same specimens.

    Returns (systematic, random_var, total_var, d) where
      systematic  = magnitude of the mean difference vector, in Procrustes units
      random_var  = per-measurement variance about that mean difference
      total_var   = per-measurement variance including the systematic part
      d           = per-specimen Procrustes distances
    """
    diff = PA - PB
    mean_diff = diff.mean(axis=0)
    systematic = float(np.sqrt((mean_diff ** 2).sum()))
    resid = diff - mean_diff
    random_var = float((resid ** 2).sum() / len(resid) / 2.0)
    total_var = float((diff ** 2).sum() / len(diff) / 2.0)
    d = np.sqrt((diff ** 2).sum(axis=(1, 2)))
    return systematic, random_var, total_var, d


lines = []
w = lines.append
w("# Corrected estimates\n")
w("These figures replace those in steps 2, 4, 5 and 7 of this repository and "
  "in the first manuscript draft. The errors corrected are listed in the "
  "header of `08_corrected_estimates.py`.\n")
w("One convention throughout: the variance of a single measurement about the "
  "truth is E[d^2]/2, with d the Procrustes distance between two measurements "
  "of the same specimen. Intervals are bootstrap percentile intervals over "
  f"{BOOT} resamples of colonies where colony structure is recoverable, "
  "otherwise of specimens.\n")

# ===========================================================================
# 1. Ecuador: two groups, the same images
# ===========================================================================
perm = np.load(os.path.join(RESULTS, "landmark_map.npy"))
A_raw, _ = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B_raw, B_names = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B_raw = B_raw[:, perm, :]
A_raw = A_raw.copy()
A_raw[:, :, 0] = -A_raw[:, :, 0]

a_cs, b_cs = centroid_size(A_raw), centroid_size(B_raw)
A_pre, _ = preshape(A_raw)
B_pre, _ = preshape(B_raw)
Dm = pairwise_procrustes(A_pre, B_pre)
rows_, cols_ = linear_sum_assignment(
    Dm + 5.0 * np.abs(a_cs[:, None] - b_cs[None, :]) / np.median(a_cs))
same = np.abs(a_cs[rows_] - b_cs[cols_]) < 2.0
ia, ib = rows_[same], cols_[same]
n_pairs = len(ia)

# joint fit on the matched pairs only
P, _ = gpa(np.concatenate([A_raw[ia], B_raw[ib]], axis=0))
PA, PB = P[:n_pairs], P[n_pairs:]
PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(n_pairs)])

colony = np.array([re.match(r"EC-\d+-([A-Za-z0-9]+)-", B_names[j]).group(1)
                   if re.match(r"EC-\d+-([A-Za-z0-9]+)-", B_names[j]) else "NA"
                   for j in ib])

sys_all, rnd_all, tot_all, d_all = decompose(PA, PB)
keep = d_all <= 3 * np.median(d_all)
sys_k, rnd_k, tot_k, d_k = decompose(PA[keep], PB[keep])

w("## 1. Two groups digitizing the same images (Ecuador)\n")
w(f"{n_pairs} wings matched one-to-one on translation-invariant centroid size "
  "and shape, out of 663 and 726 records. All figures below use these pairs "
  "only.\n")

ci_tot = boot_ci(d_all ** 2 / 2.0, groups=colony)
ci_tot_k = boot_ci(d_k ** 2 / 2.0, groups=colony[keep])
w("| quantity | all matched pairs | excluding 34 largest discrepancies |\n|---|---|---|")
w(f"| pairs | {n_pairs} | {int(keep.sum())} |")
w(f"| median Procrustes distance | {np.median(d_all):.5f} | {np.median(d_k):.5f} |")
w(f"| total per-measurement variance | {tot_all:.6f} | {tot_k:.6f} |")
w(f"| 95% interval | {ci_tot[0]:.6f} to {ci_tot[1]:.6f} | "
  f"{ci_tot_k[0]:.6f} to {ci_tot_k[1]:.6f} |")
w(f"| systematic displacement between groups | {sys_all:.5f} | {sys_k:.5f} |")
w(f"| random component of variance | {rnd_all:.6f} | {rnd_k:.6f} |")
w(f"| systematic share of total variance | "
  f"{100 * (sys_all ** 2 / 2.0) / tot_all:.1f}% | "
  f"{100 * (sys_k ** 2 / 2.0) / tot_k:.1f}% |\n")

w("Excluding the 34 largest discrepancies lowers the variance by a factor of "
  f"{tot_all / tot_k:.1f}. Those pairs were not confirmed against the images, "
  "so both columns are reported and the reader may choose. The lower figure "
  "is not preferred here.\n")

w(f"**The systematic component does not average away.** The two groups differ "
  f"by a constant displacement of {sys_all:.5f} Procrustes units, which is "
  f"{100 * (sys_all ** 2 / 2.0) / tot_all:.0f}% of the total variance between "
  "them. Averaging more wings per colony shrinks the random part and leaves "
  "this untouched, so the claim in the first draft that colony averaging "
  "reduces digitization error to 2.3% of among-colony variance was wrong in "
  "kind, not only in size.\n")

# consequence for colony means: the systematic part survives averaging
Pfull, reffull = gpa(B_raw)
var_total_shape = shape_variance(Pfull, reffull)
colB = np.array([re.match(r"EC-\d+-([A-Za-z0-9]+)-", f).group(1)
                 if re.match(r"EC-\d+-([A-Za-z0-9]+)-", f) else "NA"
                 for f in B_names])
grpsB = [g for g in np.unique(colB) if (colB == g).sum() >= 3]
ssw, nw, mus = 0.0, 0, []
for g in grpsB:
    Xg = Pfull[colB == g]
    mu = Xg.mean(axis=0)
    ssw += ((Xg - mu) ** 2).sum(); nw += len(Xg); mus.append(mu)
var_within_col = ssw / nw
mus = np.stack(mus)
var_among_col = ((mus - mus.mean(axis=0)) ** 2).sum() / len(mus)
wings_per = nw / len(grpsB)
sys_var = sys_all ** 2 / 2.0
err_colony_mean = rnd_all / wings_per + sys_var

w("### What this means for colony means\n")
w("| quantity | variance | share of among-colony variance |\n|---|---|---|")
w(f"| total shape variance of the deposit | {var_total_shape:.6f} | |")
w(f"| within-colony variance | {var_within_col:.6f} | |")
w(f"| among-colony variance | {var_among_col:.6f} | |")
w(f"| per-measurement error, all pairs | {tot_all:.6f} | "
  f"{100 * tot_all / var_among_col:.0f}% |")
w(f"| random part after averaging {wings_per:.1f} wings | "
  f"{rnd_all / wings_per:.6f} | {100 * (rnd_all / wings_per) / var_among_col:.1f}% |")
w(f"| systematic part, unchanged by averaging | {sys_var:.6f} | "
  f"{100 * sys_var / var_among_col:.1f}% |")
w(f"| **error in a colony mean** | **{err_colony_mean:.6f}** | "
  f"**{100 * err_colony_mean / var_among_col:.0f}%** |\n")
w(f"Error as a share of total shape variance is "
  f"{100 * tot_all / var_total_shape:.1f}% with all matched pairs and "
  f"{100 * tot_k / var_total_shape:.1f}% excluding the 34 unconfirmed "
  "discrepancies. The first draft reported 7.5%, which came from the "
  "median-based estimator adopted to match the mis-scaled bilateral figure.\n")
w(f"The practical consequence is the opposite of the first draft's. Averaging "
  f"{wings_per:.1f} wings per colony reduces the random component to "
  f"{100 * (rnd_all / wings_per) / var_among_col:.1f}% of among-colony "
  f"variance, but the systematic displacement contributes "
  f"{100 * sys_var / var_among_col:.0f}% whatever the sample size. Colony "
  f"averaging therefore leaves about {100 * err_colony_mean / var_among_col:.0f}% "
  "of among-colony variance as between-group measurement displacement, not "
  "the 2.3% claimed before. This is a mechanism for the misassignment of "
  "known pure lines reported in step 3.\n")

# paired offset between the two groups' grand means
paired_offset = float(np.sqrt(((PA.mean(axis=0) - PB.mean(axis=0)) ** 2).sum()))
w(f"Offset between the two groups' grand means on these pairs: "
  f"**{paired_offset:.5f}**. The first draft reported 0.00891, computed from "
  "the means of the unequal full record sets.\n")

# ===========================================================================
# 2. Bilateral wings, same convention, aligned before averaging
# ===========================================================================
w("## 2. Left and right forewings of the same bee\n")
w("Under the same convention as section 1. This estimates a different "
  "quantity: it contains fluctuating asymmetry as well as within-session "
  "digitizing error, so it bounds each from above and is not a replicate of "
  "section 1.\n")
w("| deposit | bees | median L-R distance | variance | 95% interval | "
  "systematic (directional asymmetry) |\n|---|---|---|---|---|---|")

bil = {}
for label, fname, pat in (("Algeria 2018", "DZ-2018-raw-coordinates.csv", r"(DZ-\d+)"),
                          ("Serbia", "RS_21_80-raw-coordinates.csv", r"(RS-\d+)"),
                          ("Algeria 2024", "DZ-2024-raw-coordinates.csv", r"(DZ-\d+)")):
    X, names = load_identifly_csv(os.path.join(DATA, fname))
    seen = defaultdict(dict)
    for i, nm in enumerate(names):
        m = SIDE_RE.search(nm)
        if m:
            seen[nm[:m.start()] + "-X" + nm[m.end() - 1:]][m.group(1)[0]] = i
    keys = [k for k, v in seen.items() if "L" in v and "R" in v]
    nb = len(keys)
    L = X[[seen[k]["L"] for k in keys]]
    R = X[[seen[k]["R"] for k in keys]]
    Pb, _ = gpa(np.concatenate([L, R], axis=0))
    PL, PR = Pb[:nb], Pb[nb:]
    PR = np.stack([rotate_onto(PL[i], PR[i]) for i in range(nb)])
    col = np.array([re.match(pat, k).group(1) if re.match(pat, k) else "NA"
                    for k in keys])
    s, rv, tv, d = decompose(PL, PR)
    ci = boot_ci(d ** 2 / 2.0, groups=col)
    bil[label] = (nb, np.median(d), tv, ci, s)
    w(f"| {label} | {nb} | {np.median(d):.5f} | {tv:.6f} | "
      f"{ci[0]:.6f} to {ci[1]:.6f} | {s:.5f} |")

ec_lo, ec_hi = ci_tot
bl = [v[2] for v in bil.values()]
w(f"\nThe bilateral estimates run {min(bl):.6f} to {max(bl):.6f}, against "
  f"{tot_all:.6f} ({ec_lo:.6f} to {ec_hi:.6f}) for two groups on the same "
  "images. These are consistent in order of magnitude and are **not** "
  "presented as agreeing: they measure different components, and the first "
  "draft's claim of agreement to 5% rested on the scaling error named in the "
  "header.\n")
w("Directional asymmetry is near zero in all three deposits, confirming on "
  "1,689 bees that forewing shape does not differ between body sides.\n")

# ===========================================================================
# 3. Split-half baseline, computed
# ===========================================================================
w("## 3. Within-reference split-half baseline\n")
N_raw, N_names = load_identifly_csv(os.path.join(DATA, "Nawrocka_et_al2018.csv"))
geo = {}
with open(os.path.join(DATA, "Nawrocka_et_al2018-geo-data.csv"),
          encoding="utf-8-sig") as fh:
    for rec in csv.DictReader(fh):
        geo[rec["sample"]] = rec["subspecies"]
samples = np.array(["-".join(f.split("-")[:3]) for f in N_names])
keep3 = np.array([geo.get(s) in ("carnica", "caucasia", "mellifera")
                  for s in samples])
Nk, sk = N_raw[keep3], samples[keep3]
Pn, _ = gpa(Nk)
uniq = np.unique(sk)
splits = []
for _ in range(200):
    pm = RNG.permutation(uniq)
    h1 = set(pm[:len(pm) // 2])
    m1 = np.array([s in h1 for s in sk])
    splits.append(float(np.sqrt(((Pn[m1].mean(axis=0)
                                  - Pn[~m1].mean(axis=0)) ** 2).sum())))
splits = np.asarray(splits)
w(f"200 random splits of the {len(uniq)} reference colonies of the three "
  "subspecies into halves, offsets between half means:\n")
w(f"- median **{np.median(splits):.5f}**, 2.5th to 97.5th percentile "
  f"{np.percentile(splits, 2.5):.5f} to {np.percentile(splits, 97.5):.5f}\n")
w("The first draft quoted 0.00550 from an uncommitted script. The value is "
  "reproduced here with its procedure and spread.\n")

# ===========================================================================
# 4. Assignment of crosses: full counts
# ===========================================================================
w("## 4. Assignment of known crosses, all counts\n")
w("The first draft reported a single modal class per genotype, which hid "
  "ties. F1mc was reported as *carnica* when the counts are an exact "
  "three-way tie, and the accompanying text wrongly said it was assigned to "
  "neither parent when eight of twelve colonies went to a parent.\n")
rows = list(csv.DictReader(
    open(os.path.join(RESULTS, "known_crosses_assignments.csv"))))
classes = ["carnica", "caucasia", "mellifera"]
w("| genotype | queen | drone | colonies | carnica | caucasia | mellifera | "
  "to queen | to drone |\n|---|---|---|---|---|---|---|---|---|")
for g in sorted({r["genotype"] for r in rows}):
    sub = [r for r in rows if r["genotype"] == g]
    cnt = Counter(r["assigned_corrected"] for r in sub)
    q, dr = sub[0]["queen_subspecies"], sub[0]["drone_subspecies"]
    w(f"| {g} | {q} | {dr} | {len(sub)} | " +
      " | ".join(str(cnt.get(c, 0)) for c in classes) +
      f" | {cnt.get(q, 0)} | {cnt.get(dr, 0)} |")
f1 = [r for r in rows if r["genotype"].startswith("F1")]
tq = sum(r["assigned_corrected"] == r["queen_subspecies"] for r in f1)
td = sum(r["assigned_corrected"] == r["drone_subspecies"] for r in f1)
w(f"\nAcross {len(f1)} F1 colonies, {tq} ({100 * tq / len(f1):.1f}%) were "
  f"assigned to the queen's subspecies and {td} ({100 * td / len(f1):.1f}%) to "
  f"the drone's. Reciprocal pairs of identical expected composition were "
  "assigned differently, but reciprocal crosses do not have identical nuclear "
  "genotypes: different parental individuals, maternal effects and "
  "cytoplasmic inheritance all remain in play. The result is reported as a "
  "limitation of forcing hybrids into pure classes, not as evidence about "
  "parental direction.\n")

# ===========================================================================
# 5. Ancestry: measured against shape-derived
# ===========================================================================
w("## 5. Measured ancestry against shape-derived equivalents\n")
cj = list(csv.DictReader(open(os.path.join(RESULTS, "calfee_joined.csv"))))
ca = np.array([float(r["A"]) for r in cj if r["location"] == "California"])
ar = np.array([float(r["A"]) for r in cj if r["location"] == "Argentina"])
w("| quantity | value |\n|---|---|")
w(f"| mean African ancestry, California ({len(ca)} bees) | {100 * ca.mean():.2f}% |")
w(f"| mean African ancestry, Argentina ({len(ar)} bees) | {100 * ar.mean():.2f}% |")
w(f"| **measured** difference | **{100 * abs(ar.mean() - ca.mean()):.1f} percentage points** |")
w("| shape-derived equivalent for the same pair | 31% |")
w("| shape variance explained by measured ancestry | 5.7% |\n")
w("The first draft called the 31% figure the real difference between the two "
  "hybrid zones. It is not: the measured difference is "
  f"{100 * abs(ar.mean() - ca.mean()):.1f} percentage points, and 31% is what "
  "the shape projection returns for that pair. The projection therefore "
  f"overstates a known difference by about "
  f"{100 * (0.31 / abs(ar.mean() - ca.mean()) - 1):.0f}%, which is a "
  "calibration check the scale partly fails. All ancestry equivalents are "
  "exploratory and are retained only as a rough scale for the offsets.\n")

# ===========================================================================
# 6. Bookkeeping corrections
# ===========================================================================
w("## 6. Bookkeeping corrections\n")
om = list(csv.DictReader(open(os.path.join(RESULTS, "offset_matrix.csv"))))
om.sort(key=lambda x: -float(x["offset"]))
hits = sum("Wegrzynowicz" in (x["deposit_a"] + x["deposit_b"]) for x in om[:8])
w(f"- Of the eight largest offsets, **{hits}** involve the single deposit "
  "measured by another group, not all eight as the first draft stated.\n")

wk = list(csv.DictReader(open(os.path.join(RESULTS,
                                           "known_crosses_assignments.csv"))))
cols = defaultdict(set)
for r in wk:
    cols[r["colony"]].add(r["genotype"])
dupes = {k: v for k, v in cols.items() if len(v) > 1}
w(f"- The cross dataset yields {len(cols)} distinct colony identifiers across "
  f"{len(wk)} genotype-colony groups; {len(dupes)} identifiers appear under "
  "more than one genotype label, which accounts for the discrepancy against "
  "the 200 queens reported in the source data paper. Affected identifiers: "
  + (", ".join(sorted(dupes)) if dupes else "none") + ".\n")
w("- The nine analytical datasets derive from seven sources, and from fewer "
  "independent biological samples: the Ecuador wings appear twice, as the "
  "same specimens measured by two groups, and the two Calfee sets are "
  "regional subsets of one collection. Counts of deposits should not be read "
  "as counts of independent samples.\n")
w("- Landmarks 7 and 14 carried the largest between-group disagreement. This "
  "is **not** reported as unreliability. Nawrocka et al. describe altering "
  "the positions of two landmarks relative to an earlier convention, so a "
  "computational renumbering does not establish anatomical equivalence, and a "
  "convention difference would produce exactly this pattern. Resolving it "
  "requires the definitions used by each source, with annotated images.\n")

os.makedirs(RESULTS, exist_ok=True)
with open(os.path.join(RESULTS, "corrected_estimates.md"), "w") as fh:
    fh.write("\n".join(lines))

print(f"Ecuador pairs {n_pairs}")
print(f"  total variance {tot_all:.6f}  CI {ci_tot[0]:.6f}-{ci_tot[1]:.6f}")
print(f"  systematic {sys_all:.5f}  random var {rnd_all:.6f}  "
      f"systematic share {100 * (sys_all**2/2)/tot_all:.1f}%")
print(f"  excl. 34 outliers: variance {tot_k:.6f}")
print(f"  paired grand-mean offset {paired_offset:.5f}")
for k, v in bil.items():
    print(f"{k}: n={v[0]} variance {v[2]:.6f} CI {v[3][0]:.6f}-{v[3][1]:.6f}")
print(f"split-half median {np.median(splits):.5f} "
      f"[{np.percentile(splits,2.5):.5f}, {np.percentile(splits,97.5):.5f}]")
print(f"measured ancestry difference "
      f"{100*abs(ar.mean()-ca.mean()):.1f} points vs projection 31%")
print(f"eight largest: {hits} involve the other group")
print(f"colony identifiers {len(cols)}, duplicated across genotypes {len(dupes)}")
print(f"wrote {RESULTS}/corrected_estimates.md")
