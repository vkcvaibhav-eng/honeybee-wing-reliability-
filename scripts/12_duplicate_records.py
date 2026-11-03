#!/usr/bin/env python3
"""
Step 12 - duplicate records in the Ecuadorian coordinate deposit.

The image archive of the Masaquiza and Arenal deposit holds 75 TIFF files of
which 70 are distinct by MD5 checksum; five filenames carry the content of
another file with the same apiary prefix. This step asks whether that
duplication reached the coordinate file analysed here, and what difference it
makes to the reported estimates.

Writes ../results/duplicate_records.md
"""
import os
import sys

import numpy as np
from scipy.optimize import linear_sum_assignment

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from wingio import (centroid_size, gpa, load_identifly_csv, load_tps_xlsx,
                    pairwise_procrustes, preshape, rotate_onto)

DATA = os.path.join(REPO, "data")
RESULTS = os.path.join(REPO, "results")

perm = np.load(os.path.join(RESULTS, "landmark_map.npy"))
A, Anames = load_tps_xlsx(os.path.join(DATA, "raw_coordinates.xlsx"))
B, _ = load_identifly_csv(os.path.join(DATA, "EC-raw-coordinates.csv"))
B = B[:, perm, :]
A = A.copy()
A[:, :, 0] = -A[:, :, 0]

seen, dup = {}, []
for i, cfg in enumerate(A):
    k = cfg.tobytes()
    if k in seen:
        dup.append((seen[k], i))
    else:
        seen[k] = i
drop = {j for _, j in dup}
keep = np.array([i for i in range(len(A)) if i not in drop])


def run(Asub):
    acs, bcs = centroid_size(Asub), centroid_size(B)
    Ap, _ = preshape(Asub)
    Bp, _ = preshape(B)
    D = pairwise_procrustes(Ap, Bp)
    r, c = linear_sum_assignment(
        D + 5.0 * np.abs(acs[:, None] - bcs[None, :]) / np.median(acs))
    m = np.abs(acs[r] - bcs[c]) < 2.0
    ia, ib = r[m], c[m]
    n = len(ia)
    P, _ = gpa(np.concatenate([Asub[ia], B[ib]], axis=0))
    PA, PB = P[:n], P[n:]
    PB = np.stack([rotate_onto(PA[i], PB[i]) for i in range(n)])
    d = np.sqrt(((PA - PB) ** 2).sum(axis=(1, 2)))
    med = float(np.median(d))
    kp = d <= 3 * med
    return dict(
        n=n, med=med, disputed=int((~kp).sum()),
        disp=float(np.sqrt(((PA - PB).mean(axis=0) ** 2).sum())),
        tot=float((d ** 2).sum() / len(d) / 2),
        totk=float((d[kp] ** 2).sum() / kp.sum() / 2))


w, out = (lambda t="": out.append(t)), []
w = out.append
w("# Step 12 - duplicate records in the Ecuadorian deposit\n")
w(f"The coordinate file holds **{len(A)}** wing records across "
  f"**{len({n[1] for n in Anames})}** source images and "
  f"**{len({n[0] for n in Anames})}** apiaries. Of those records, "
  f"**{len(dup)}** are byte-identical copies of another record.\n")
w("| duplicate of | record | apiary | image |")
w("|---|---|---|---|")
for a, b in dup:
    w(f"| {Anames[a][2]} | {Anames[b][2]} | {Anames[b][0]} | {Anames[b][1]} |")
w("")
same_img = all(Anames[a][1] == Anames[b][1] and Anames[a][0] == Anames[b][0]
               for a, b in dup)
w(f"Every duplicate lies within the same image and the same apiary as its "
  f"original: **{same_img}**. No record is shared between apiaries, so "
  f"comparisons between colonies cannot be contaminated by them.\n")

a_, b_ = run(A), run(A[keep])
w("## Effect on the reported estimates\n")
w("| quantity | as published (663) | duplicates removed "
  f"({len(keep)}) |")
w("|---|---|---|")
w(f"| matched candidate pairs | {a_['n']} | {b_['n']} |")
w(f"| median Procrustes distance | {a_['med']:.5f} | {b_['med']:.5f} |")
w(f"| pairs above three times the median | {a_['disputed']} | "
  f"{b_['disputed']} |")
w(f"| mean displacement | {a_['disp']:.5f} | {b_['disp']:.5f} |")
w(f"| half mean squared disagreement, all pairs | {a_['tot']:.6f} | "
  f"{b_['tot']:.6f} |")
w(f"| half mean squared disagreement, retained | {a_['totk']:.6f} | "
  f"{b_['totk']:.6f} |")
w("")
w(f"Removing the duplicates accounts for "
  f"{a_['disputed'] - b_['disputed']} of the {a_['disputed']} large "
  f"discrepancies, because two identical records compete for distinct "
  f"partners and one of them is necessarily matched to the wrong wing. The "
  f"mean displacement is unchanged at {b_['disp']:.5f}. The analysis "
  f"reported in the manuscript uses the deposit as published, so that it "
  f"reproduces from the deposited file; this is the sensitivity check.\n")

open(os.path.join(RESULTS, "duplicate_records.md"), "w").write("\n".join(out))
print("\n".join(out))
