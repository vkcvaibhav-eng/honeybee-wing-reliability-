#!/usr/bin/env python3
"""
Step 10 - second review round.

Addresses, without access to the deposit images:
  (a) whether the 642 candidate pairs behave like the same wings measured
      twice, by testing the per-landmark signature of their disagreement
      against the signature of deliberately mismatched pairs;
  (b) the concentration of disagreement at landmarks 7 and 14, which
      Nawrocka et al. (2018) state were moved relative to Gerula et al.
      (2009) to match Ruttner (1988);
  (c) the stale percentile and colony-displacement figures;
  (d) the proportion of colony-mean distances below the displacement;
  (e) a bootstrap interval for the excluding-34 estimate;
  (f) the pure-line table with the two conflicting colony identifiers
      excluded.
"""
import os, re, sys, csv
import numpy as np
from scipy.optimize import linear_sum_assignment

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from wingio import (NLM, centroid_size, gpa, load_identifly_csv,
                    load_tps_xlsx, pairwise_procrustes, preshape, rotate_onto)

DATA = os.path.join(REPO, "data")
RESULTS = os.path.join(REPO, "results")
rng = np.random.default_rng(20261103)

perm = np.load(os.path.join(RESULTS, "landmark_map.npy"))
A_raw, _ = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B_raw, B_names = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B_raw = B_raw[:, perm, :]
A_raw = A_raw.copy(); A_raw[:, :, 0] = -A_raw[:, :, 0]

a_cs, b_cs = centroid_size(A_raw), centroid_size(B_raw)
A_pre, _ = preshape(A_raw); B_pre, _ = preshape(B_raw)
Dm = pairwise_procrustes(A_pre, B_pre)
r_, c_ = linear_sum_assignment(
    Dm + 5.0 * np.abs(a_cs[:, None] - b_cs[None, :]) / np.median(a_cs))
same = np.abs(a_cs[r_] - c_ * 0 + 0 - b_cs[c_]) < 2.0
ia, ib = r_[same], c_[same]
n = len(ia)

def align(iA, iB):
    P, _ = gpa(np.concatenate([A_raw[iA], B_raw[iB]], axis=0))
    m = len(iA)
    PA, PB = P[:m], P[m:]
    PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(m)])
    return PA, PB

def profile(PA, PB):
    """per-landmark RMS disagreement and the squared share at each landmark"""
    diff = PA - PB
    md = diff.mean(axis=0)                      # mean displacement vector
    rms = np.sqrt((diff ** 2).sum(axis=2).mean(axis=0))
    sq = (md ** 2).sum(axis=1)                  # squared displacement / landmark
    return rms, sq / sq.sum()

PA, PB = align(ia, ib)
d = np.sqrt(((PA - PB) ** 2).sum(axis=(1, 2)))
keep = d <= 3 * np.median(d)
L7, L14 = 11, 4   # array indices of Nawrocka landmarks 7 and 14

out = []
w = out.append

rows = []
for lab, (p_, q_) in {
        "all 642 candidate pairs": (ia, ib),
        "608 retained (d <= 3x median)": (ia[keep], ib[keep]),
        "34 disputed (d > 3x median)": (ia[~keep], ib[~keep])}.items():
    pa, pb = align(p_, q_)
    rms, share = profile(pa, pb)
    rows.append((lab, len(p_), share[L7] + share[L14],
                 rms[L7], rms[L14], float(np.median(np.delete(rms, [L7, L14])))))

diff = PA - PB
disp = float(np.sqrt((diff.mean(axis=0) ** 2).sum()))

w("# Step 10 - matching signature and remaining corrections\n")

w("## 1. Where the disagreement sits, and what it does not depend on\n")
w("Nawrocka et al. (2018) state that their landmark positions followed "
  "Gerula et al. (2009) but were changed for landmarks 7 and 14 to agree "
  "with standard morphometry (Ruttner 1988). Two published versions of the "
  "convention therefore differ at those two landmarks, and a group working "
  "to one version would disagree with a group working to the other there "
  "and almost nowhere else.\n")

w("| pair set | n | share of squared displacement at LM7+LM14 | "
  "RMS LM7 | RMS LM14 | median RMS, other 17 |")
w("|---|---|---|---|---|---|")
for lab, k, sg, r7, r14, rm in rows:
    w(f"| {lab} | {k} | {100*sg:.1f}% | {r7:.5f} | {r14:.5f} | {rm:.5f} |")
w("")
w(f"Even division across 19 landmarks would be {200/19:.1f}%. On the "
  f"retained pairs the two landmarks carry {100*rows[1][2]:.1f}% of the "
  f"squared displacement, and their RMS disagreement is "
  f"{np.mean([rows[1][3], rows[1][4]])/rows[1][5]:.1f} times the median of "
  f"the other seventeen. The landmark-map step reached the same two "
  f"landmarks independently: residuals between the two mean shapes were "
  f"0.00654 at landmark 7 and 0.00567 at landmark 14, against 0.00241 or "
  f"less at all seventeen others.\n")

inv = []
for _ in range(200):
    sh = rng.permutation(ib)
    pa, pb = align(ia, sh)
    inv.append(float(np.sqrt(((pa - pb).mean(axis=0) ** 2).sum())))
inv = np.array(inv)

w("### What the estimate does not depend on\n")
w(f"- mean displacement on the matching as fitted: **{disp:.5f}**")
w(f"- the same quantity under 200 random re-pairings of the same wings: "
  f"median **{np.median(inv):.5f}**, range {inv.min():.5f} to "
  f"{inv.max():.5f}\n")
w("The displacement is the difference between the two grand means, so which "
  "wing is paired with which leaves it unchanged. The central estimate "
  "therefore does not rest on the matching being correct, and no claim here "
  "is made that the per-landmark profile identifies correct matches: it "
  "does not, because the profile of a mean difference is also invariant to "
  "the pairing. What does rest on the matching is the residual scatter, "
  "reported as a range in section 3.\n")

# ---- 2. percentile and colony displacement, recomputed ----
w("## 2. Displacement against colony-mean distances\n")
Pfull, _ = gpa(B_raw)
col_all = np.array([(m.group(1) if (m := re.match(
    r"EC-\d+-([A-Za-z0-9]+)-", nm)) else "NA") for nm in B_names])
means, labs = [], []
for c in sorted(set(col_all)):
    if c == "NA":
        continue
    s = Pfull[col_all == c]
    if len(s) >= 3:
        means.append(s.mean(axis=0)); labs.append(c)
means = np.stack(means)
mp, _ = preshape(means)
Dc = pairwise_procrustes(mp, mp)
iu = np.triu_indices(len(means), 1)
pairdist = Dc[iu]

w(f"- colonies with 3 or more wings: **{len(means)}**")
w(f"- pairwise distances between their means: **{len(pairdist)}** "
  f"(not independent; each colony enters {len(means)-1} of them)")
w(f"- median distance between colony means: **{np.median(pairdist):.5f}**")
w(f"- 10th percentile: **{np.percentile(pairdist, 10):.5f}**")
w(f"- mean displacement between measurement sets: **{disp:.5f}**")
w(f"- ratio: **{disp/np.median(pairdist):.2f}**")
frac = float((pairdist < disp).mean())
w(f"- proportion of colony-mean distances below the displacement: "
  f"**{100*frac:.1f}%** ({int((pairdist < disp).sum())} of {len(pairdist)})\n")

colony = col_all[ib]
both = [c for c in set(colony) if c != "NA" and (colony == c).sum() >= 3]
cd = []
for c in both:
    m = colony == c
    cd.append(float(np.sqrt(((PA[m].mean(axis=0) - PB[m].mean(axis=0)) ** 2).sum())))
cd = np.array(cd)
# the average of the colony-specific difference VECTORS, then its magnitude,
# computed from the vectors rather than reusing the pooled-wing value
cvec = np.stack([(PA[colony == c].mean(axis=0) - PB[colony == c].mean(axis=0))
                 for c in both])
colony_mean_disp = float(np.sqrt((cvec.mean(axis=0) ** 2).sum()))
w(f"- colonies measured by both sets with 3+ wings: **{len(cd)}**")
w(f"- median magnitude of their colony-specific displacement: "
  f"**{np.median(cd):.5f}**")
w(f"- magnitude of the mean of the colony-specific difference vectors: "
  f"**{colony_mean_disp:.5f}** (computed from the colony vectors, not "
  f"carried over from the pooled-wing figure of {disp:.5f})\n")

# ---- residual after removing the mean displacement ----
w("## 2a. Total and residual disagreement\n")
w("| quantity | all 642 | retained 608 |")
w("|---|---|---|")
PAk_, PBk_ = align(ia[keep], ib[keep])
dk_ = np.sqrt(((PAk_ - PBk_) ** 2).sum(axis=(1, 2)))
dispk_ = float(np.sqrt(((PAk_ - PBk_).mean(axis=0) ** 2).sum()))
tot_a = float((d ** 2).sum() / len(d) / 2.0)
tot_k = float((dk_ ** 2).sum() / len(dk_) / 2.0)
res_a, res_k = tot_a - disp ** 2 / 2, tot_k - dispk_ ** 2 / 2
w(f"| half mean squared total disagreement | {tot_a:.6f} | {tot_k:.6f} |")
w(f"| half the squared mean displacement | {disp**2/2:.7f} | "
  f"{dispk_**2/2:.7f} |")
w(f"| residual after removing it | {res_a:.7f} | {res_k:.7f} |")
w(f"| displacement share of the total | {100*(disp**2/2)/tot_a:.1f}% | "
  f"{100*(dispk_**2/2)/tot_k:.1f}% |")
w("")
w(f"Excluding the 34 reduces total disagreement by "
  f"{100*(1-tot_k/tot_a):.0f}% and residual disagreement by "
  f"{100*(1-res_k/res_a):.0f}%. These are two sensitivity scenarios, not "
  f"bounds: neither establishes a mathematical limit on disagreement under "
  f"an unknown true matching.\n")

# ---- 3. bootstrap for the excluding-34 estimate ----
w("## 3. Excluding the 34 disputed matches\n")
PAk, PBk = align(ia[keep], ib[keep])
dk = np.sqrt(((PAk - PBk) ** 2).sum(axis=(1, 2)))
ck = colony[keep]
def boot(dv, cv, reps=2000):
    uq = np.array(sorted(set(cv)))
    o = []
    for _ in range(reps):
        pick = rng.choice(uq, len(uq), replace=True)
        idx = np.concatenate([np.where(cv == u)[0] for u in pick])
        o.append((dv[idx] ** 2).sum() / len(idx) / 2.0)
    return np.percentile(o, 2.5), np.percentile(o, 97.5)
lo, hi = boot(dk, ck)
v_keep = float((dk ** 2).sum() / len(dk) / 2.0)
dispk = float(np.sqrt(((PAk - PBk).mean(axis=0) ** 2).sum()))
w(f"- half mean squared disagreement: **{v_keep:.6f}** "
  f"(95% CI {lo:.6f} to {hi:.6f})")
w(f"- mean displacement: **{dispk:.5f}**, against {disp:.5f} on all 642")
w(f"- the displacement moves by {100*abs(dispk-disp)/disp:.1f}% when the "
  f"34 are removed, while the variance changes by "
  f"{100*abs(v_keep-float((d**2).sum()/len(d)/2.0))/float((d**2).sum()/len(d)/2.0):.0f}%.\n")

# ---- 4. pure lines excluding the conflicting identifiers ----
w("## 4. The two conflicting colony identifiers\n")
kr = list(csv.DictReader(open(os.path.join(RESULTS,
                                           "known_crosses_assignments.csv"))))
bad = {"0489_12", "0203_13"}
EXP = {"cc": "caucasia", "kk": "carnica", "mm": "mellifera"}
w("Both appear under two genotype labels. The wing counts identify which "
  "entry is spurious:\n")
w("| colony | genotype | wings | raw | centred |")
w("|---|---|---|---|---|")
for r in kr:
    if r["colony"] in bad:
        w(f"| {r['colony']} | {r['genotype']} | {r['wings']} | "
          f"{r['assigned_raw']} | {r['assigned_corrected']} |")
w("")
w("| genotype | all entries | excluding the two |")
w("|---|---|---|")
for g in ("P0cc", "P1cc", "P0kk", "P1kk", "P0mm", "P1mm"):
    e = EXP[g[2:]]
    s1 = [r for r in kr if r["genotype"] == g]
    s2 = [r for r in s1 if r["colony"] not in bad]
    f = lambda s: (f"{sum(1 for r in s if r['assigned_raw']==e)}/{len(s)} raw, "
                   f"{sum(1 for r in s if r['assigned_corrected']==e)}/{len(s)} centred")
    w(f"| {g} | {f(s1)} | {f(s2)} |")
w("")
w("The single colony that centring fails to recover, P1mm 0489_12, is "
  "represented by one wing and also appears as P1kk with 41 wings. Excluded, "
  "the centred pure-line result is 4 of 5 caucasica colonies and 12 of 12 "
  "for the other lines. The earlier statement that neither identifier is a "
  "pure parental line was wrong.\n")

# per-landmark profile for both samples, for the supplementary table
rms_all, _ = profile(PA, PB)
rms_keep, _ = profile(*align(ia[keep], ib[keep]))
LABEL = [int(x) + 1 for x in perm]
with open(os.path.join(RESULTS, "per_landmark_both_samples.csv"), "w",
          newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["landmark_nawrocka_scheme", "rms_all_642", "rms_retained_608"])
    for k in range(1, NLM + 1):
        j = LABEL.index(k)
        wr.writerow([k, f"{rms_all[j]:.5f}", f"{rms_keep[j]:.5f}"])

open(os.path.join(RESULTS, "review_round3.md"), "w").write("\n".join(out))
print("\n".join(out))
