#!/usr/bin/env python3
"""
Step 1 — recover the landmark-numbering map between the two Ecuador deposits.

The deposits hold the same 19 anatomical points but number them differently,
in close to reverse order. Pooling them without correcting this produces
Procrustes distances near the theoretical maximum of sqrt(2) with no error or
warning of any kind, so the map must be established before anything else.

Within each deposit the numbering is self-consistent, so each deposit's GPA
mean shape is well defined. The two means are matched point-to-point by
sweeping rotation and reflection and solving the assignment problem at each
angle; the lowest cost gives the map.

Usage:
    python 01_find_landmark_map.py \
        ../data/raw_coordinates.xlsx ../data/EC-raw-coordinates.csv

Writes ../results/landmark_map.csv and ../results/landmark_map.npy
"""

import os
import sys

import numpy as np
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import NLM, gpa, load_identifly_csv, load_tps_xlsx

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def find_map(mean_a, mean_b, step_deg=0.5):
    """Best (cost, reflection, rotation, permutation) mapping mean_a -> mean_b."""
    best = None
    for reflection in (1, -1):
        M = mean_a.copy()
        M[:, 0] *= reflection
        for deg in np.arange(0.0, 360.0, step_deg):
            t = np.deg2rad(deg)
            R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
            rotated = M @ R
            cost_matrix = ((rotated[:, None, :] - mean_b[None, :, :]) ** 2).sum(-1)
            rows, cols = linear_sum_assignment(cost_matrix)
            cost = cost_matrix[rows, cols].sum()
            if best is None or cost < best[0]:
                best = (cost, reflection, deg, cols.copy())
    return best


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    path_a, path_b = sys.argv[1], sys.argv[2]

    A, _ = load_tps_xlsx(path_a)
    B, _ = load_identifly_csv(path_b)
    print(f"deposit A  {os.path.basename(path_a)}  n = {len(A)}")
    print(f"deposit B  {os.path.basename(path_b)}  n = {len(B)}")

    _, mean_a = gpa(A)
    _, mean_b = gpa(B)

    cost, reflection, deg, perm = find_map(mean_a, mean_b)
    print(f"\nbest map: cost {cost:.6f}   reflection {reflection}   rotation {deg:.1f} deg")

    M = mean_a.copy()
    M[:, 0] *= reflection
    t = np.deg2rad(deg)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    residual = np.sqrt((((M @ R) - mean_b[perm]) ** 2).sum(-1))

    print("\n A landmark -> B landmark   residual")
    for i, j in enumerate(perm):
        print(f"   A{i + 1:2d} -> B{j + 1:2d}            {residual[i]:.5f}")
    print(f"\nmedian residual {np.median(residual):.5f}   max {residual.max():.5f}")
    print(f"identity map? {np.array_equal(perm, np.arange(NLM))}")
    print(f"landmarks that move: {(perm != np.arange(NLM)).sum()} of {NLM}")

    os.makedirs(RESULTS, exist_ok=True)
    np.save(os.path.join(RESULTS, "landmark_map.npy"), perm)
    with open(os.path.join(RESULTS, "landmark_map.csv"), "w") as fh:
        fh.write("deposit_a_landmark,deposit_b_landmark,mean_shape_residual\n")
        for i, j in enumerate(perm):
            fh.write(f"{i + 1},{j + 1},{residual[i]:.6f}\n")
    print(f"\nwrote {RESULTS}/landmark_map.csv")


if __name__ == "__main__":
    main()
