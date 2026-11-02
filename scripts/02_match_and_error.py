#!/usr/bin/env python3
"""
Step 2 — match the two deposits wing-to-wing and estimate inter-team
digitization error.

The deposits hold the same physical wings, but the second team cropped each
wing out of the first team's slide scans, so raw coordinates differ by
translation. Centroid size is translation-invariant and therefore identifies
the same wing across deposits.

Each wing in A must correspond to exactly one wing in B, so matching is solved
as a global one-to-one assignment on a combined centroid-size and shape cost,
not greedily. Greedy nearest-neighbour matching fails here: most wings are
crowded together in shape space and the runner-up sits only about twice as far
away as the best match.

Error is then reported against total, within-colony and among-colony variance,
because the three denominators carry different consequences for downstream
analysis.

Usage:
    python 02_match_and_error.py \
        ../data/raw_coordinates.xlsx ../data/EC-raw-coordinates.csv

Writes ../results/matched_pairs.csv, per_landmark_disagreement.csv,
error_summary.md
"""

import csv
import os
import re
import sys

import numpy as np
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import (NLM, centroid_size, gpa, load_identifly_csv,
                    load_tps_xlsx, pairwise_procrustes, preshape, rotate_onto,
                    shape_variance)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")

# weight on the centroid-size term in the assignment cost. Size agrees to
# ~1 px in 670 for the same wing, so it is the more reliable key; shape breaks
# the remaining ties.
SIZE_WEIGHT = 5.0

# a pair whose centroid sizes agree within this many pixels is the same wing
SAME_WING_PX = 2.0


def colony_of(filename):
    """Colony key from an IdentiFly filename such as EC-0001-A1H1-7.dw.png."""
    m = re.match(r"EC-\d+-([A-Za-z0-9]+)-", filename)
    return m.group(1) if m else "unknown"


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    path_a, path_b = sys.argv[1], sys.argv[2]

    perm = np.load(os.path.join(RESULTS, "landmark_map.npy"))

    A_raw, A_lab = load_tps_xlsx(path_a)
    B_raw, B_lab = load_identifly_csv(path_b)

    # put B into A's landmark order, and undo the horizontal image flip
    B_raw = B_raw[:, perm, :]
    A_raw = A_raw.copy()
    A_raw[:, :, 0] = -A_raw[:, :, 0]

    a_cs, b_cs = centroid_size(A_raw), centroid_size(B_raw)
    A, _ = preshape(A_raw)
    B, _ = preshape(B_raw)
    print(f"deposit A  n = {len(A)}")
    print(f"deposit B  n = {len(B)}")

    # ---- global one-to-one assignment ------------------------------------
    d_shape = pairwise_procrustes(A, B)
    d_size = np.abs(a_cs[:, None] - b_cs[None, :]) / np.median(a_cs)
    rows, cols = linear_sum_assignment(d_shape + SIZE_WEIGHT * d_size)

    pair_shape = d_shape[rows, cols]
    pair_size_px = np.abs(a_cs[rows] - b_cs[cols])
    same = pair_size_px < SAME_WING_PX
    n = int(same.sum())

    print(f"\nassigned one-to-one: {len(rows)} pairs")
    print(f"  shape distance        median {np.median(pair_shape):.5f}")
    print(f"  |delta centroid size| median {np.median(pair_size_px):.3f} px")
    print(f"  centroid-size correlation r = {np.corrcoef(a_cs[rows], b_cs[cols])[0, 1]:.6f}")
    print(f"  same wing (|delta| < {SAME_WING_PX} px): {n} ({100 * same.mean():.1f}%)")

    ra, rb = rows[same], cols[same]
    d_conf = pair_shape[same]

    # ---- variance components --------------------------------------------
    aligned, mean_shape = gpa(B_raw)
    var_total = shape_variance(aligned, mean_shape)

    colony = np.array([colony_of(f) for f in B_lab])
    groups = [g for g in np.unique(colony) if (colony == g).sum() >= 3]
    ss_within, n_within, means = 0.0, 0, []
    for g in groups:
        X = aligned[colony == g]
        m = X.mean(axis=0)
        ss_within += ((X - m) ** 2).sum()
        n_within += len(X)
        means.append(m)
    var_within = ss_within / n_within
    means = np.stack(means)
    var_among = ((means - means.mean(axis=0)) ** 2).sum() / len(means)

    # each team deviates about half the pair distance from the pair mean
    var_error = (d_conf ** 2).mean() / 2.0
    wings_per_colony = n_within / len(groups)
    var_error_mean = var_error / wings_per_colony

    # ---- per-landmark ----------------------------------------------------
    dev = np.zeros(NLM)
    for i, j in zip(ra, rb):
        dev += ((A[i] - rotate_onto(A[i], B[j])) ** 2).sum(axis=1)
    rms = np.sqrt(dev / n)

    # ---- report ----------------------------------------------------------
    lines = []
    w = lines.append
    w("# Inter-team digitization error, Ecuador honey bee forewings\n")
    w(f"Wings matched one-to-one with near-certain identity: **{n}**  ")
    w(f"Centroid-size correlation between teams: **r = "
      f"{np.corrcoef(a_cs[ra], b_cs[rb])[0, 1]:.4f}**\n")
    w("## Procrustes distance between teams on the same wing\n")
    w(f"| statistic | value |\n|---|---|")
    w(f"| median | {np.median(d_conf):.5f} |")
    w(f"| 25th-75th percentile | {np.percentile(d_conf, 25):.5f} - "
      f"{np.percentile(d_conf, 75):.5f} |")
    w(f"| 90th percentile | {np.percentile(d_conf, 90):.5f} |")
    w(f"| maximum | {d_conf.max():.5f} |\n")
    w("## Variance components\n")
    w("| component | variance |\n|---|---|")
    w(f"| total shape | {var_total:.6f} |")
    w(f"| within colony | {var_within:.6f} |")
    w(f"| among colony | {var_among:.6f} |")
    w(f"| digitization error | {var_error:.6f} |\n")
    w("## Error as a share of each denominator\n")
    w("| denominator | error share |\n|---|---|")
    w(f"| total shape variance | {100 * var_error / var_total:.1f}% |")
    w(f"| within-colony variance | {100 * var_error / var_within:.1f}% |")
    w(f"| among-colony variance | {100 * var_error / var_among:.1f}% |")
    w(f"| among-colony variance, after averaging "
      f"{wings_per_colony:.1f} wings per colony | "
      f"{100 * var_error_mean / var_among:.1f}% |\n")
    w(f"Within-colony variance that is real signal rather than digitizing "
      f"noise: **{100 * max(0.0, var_within - var_error) / var_within:.1f}%**\n")
    w("## Reading these numbers\n")
    w("Colony-mean analyses are protected by averaging, so reference-based ")
    w("assignment is largely unaffected. Analyses that use the spread of ")
    w("wings within a colony are not protected, and must subtract the error ")
    w(f"variance of {var_error:.6f} before interpretation.\n")
    w("These shares are an upper bound. The denominator here is variance ")
    w("within a single population, so for comparisons spanning evolutionary ")
    w("lineages the same absolute error is a much smaller fraction.\n")
    w("This is one pair of teams on one set of images. It is the only such ")
    w("pair in the public record, which makes it informative, but it does ")
    w("not license a general claim about cross-dataset comparison.\n")

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "error_summary.md"), "w") as fh:
        fh.write("\n".join(lines))

    with open(os.path.join(RESULTS, "per_landmark_disagreement.csv"), "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["landmark_nawrocka_scheme", "rms_disagreement_unit_centroid_size"])
        for i in range(NLM):
            out.writerow([perm[i] + 1, f"{rms[i]:.6f}"])

    with open(os.path.join(RESULTS, "matched_pairs.csv"), "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["apiary", "deposit_a_image", "deposit_a_block",
                      "deposit_b_file", "procrustes_distance",
                      "delta_centroid_size_px", "same_wing"])
        for k in range(len(rows)):
            apiary, image, block = A_lab[rows[k]]
            out.writerow([apiary, image, block, B_lab[cols[k]],
                          f"{pair_shape[k]:.6f}", f"{pair_size_px[k]:.3f}",
                          int(same[k])])

    print(f"\nerror as % of total variance        {100 * var_error / var_total:.1f}%")
    print(f"error as % of within-colony variance {100 * var_error / var_within:.1f}%")
    print(f"error as % of among-colony variance  {100 * var_error / var_among:.1f}%")
    print(f"\nnoisiest landmarks: "
          f"{', '.join(str(perm[i] + 1) for i in np.argsort(-rms)[:3])}")
    print(f"wrote {RESULTS}/error_summary.md and two CSV files")


if __name__ == "__main__":
    main()
