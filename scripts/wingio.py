"""
Loaders and Procrustes utilities for honey bee forewing landmark data.

No side effects on import. Two input formats are supported, because the two
Ecuador deposits use different ones:

  * TPS blocks stored inside a single spreadsheet column (Masaquiza & Arenal)
  * one row per wing, 19 x/y pairs after an identifier column (IdentiFly CSV)

Landmark configuration throughout is the 19-point scheme of
Nawrocka, Kandemir, Fuchs and Tofilski (2018).
"""

import csv
import re

import numpy as np

NLM = 19


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def load_tps_xlsx(path, sheet=None):
    """Read TPS blocks held in one spreadsheet column.

    Each specimen is  LM=19  /  19 lines of "x y"  /  IMAGE=<file>.
    Lines naming an apiary are carried down as a group label.

    Returns (coords, labels) with coords shape (n, 19, 2) and labels a list of
    (apiary, image, running_index) tuples.
    """
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    rows = [str(r[0]).strip() if r[0] is not None else ""
            for r in ws.iter_rows(values_only=True)]

    specs, labels = [], []
    group, cur = None, []
    for line in rows:
        if re.match(r"(?i)^apiary", line):
            group = line
        elif re.match(r"(?i)^lm\s*=", line):
            cur = []
        elif re.match(r"(?i)^image\s*=", line):
            image = line.split("=", 1)[1].strip()
            if len(cur) == NLM:
                specs.append(np.asarray(cur, float))
                labels.append((group, image, len(specs)))
            cur = []
        else:
            m = re.match(r"^(-?[\d.]+)[ \t]+(-?[\d.]+)$", line)
            if m:
                cur.append([float(m.group(1)), float(m.group(2))])

    if not specs:
        raise ValueError(f"{path}: no complete TPS blocks found")
    return np.stack(specs), labels


def load_identifly_csv(path):
    """Read one-wing-per-row CSV: identifier column then x1,y1 ... x19,y19.

    Returns (coords, labels) with coords shape (n, 19, 2) and labels the
    identifier strings.
    """
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        next(reader)  # header
        specs, labels = [], []
        for row in reader:
            if len(row) < 1 + 2 * NLM:
                continue
            try:
                vals = [float(x) for x in row[1:1 + 2 * NLM]]
            except ValueError:
                continue
            specs.append(np.asarray(vals, float).reshape(NLM, 2))
            labels.append(row[0])

    if not specs:
        raise ValueError(f"{path}: no parseable rows")
    return np.stack(specs), labels


# --------------------------------------------------------------------------
# Procrustes
# --------------------------------------------------------------------------

def centroid_size(A):
    """Centroid size of each configuration. A: (n, 19, 2) -> (n,).

    Invariant to translation, so it survives the cropping that separates the
    two Ecuador deposits and therefore identifies the same physical wing.
    """
    C = A - A.mean(axis=1, keepdims=True)
    return np.sqrt((C ** 2).sum(axis=(1, 2)))


def preshape(A):
    """Centre each configuration and scale to unit centroid size.

    Returns (preshaped, centroid_sizes).
    """
    C = A - A.mean(axis=1, keepdims=True)
    cs = np.sqrt((C ** 2).sum(axis=(1, 2), keepdims=True))
    if np.any(cs == 0):
        raise ValueError("degenerate configuration with zero centroid size")
    return C / cs, cs.ravel()


def rotate_onto(reference, X):
    """Rotate preshaped X onto preshaped reference. Reflection not allowed."""
    U, _, Vt = np.linalg.svd(X.T @ reference)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        D = np.eye(2)
        D[-1, -1] = -1.0
        R = U @ D @ Vt
    return X @ R


def pairwise_procrustes(P, Q, block=64):
    """Full Procrustes distance between every P[i] and Q[j].

    P and Q must already be preshaped. Reflection is not allowed, so a
    mirrored configuration stays far away rather than matching spuriously.
    Uses the closed form for 2x2 singular values, so the full matrix is cheap.

    Returns (len(P), len(Q)).
    """
    out = np.empty((len(P), len(Q)))
    for start in range(0, len(P), block):
        stop = min(start + block, len(P))
        M = np.einsum("ikm,jkn->ijmn", P[start:stop], Q)
        a, b = M[..., 0, 0], M[..., 0, 1]
        c, d = M[..., 1, 0], M[..., 1, 1]
        E, F = (a + d) / 2.0, (a - d) / 2.0
        G, H = (c + b) / 2.0, (c - b) / 2.0
        q = np.sqrt(E * E + H * H)
        r = np.sqrt(F * F + G * G)
        s1, s2 = q + r, np.abs(q - r)
        det = a * d - b * c
        trace = np.where(det >= 0, s1 + s2, s1 - s2)
        out[start:stop] = np.sqrt(np.clip(2.0 - 2.0 * trace, 0.0, None))
    return out


def gpa(A, iterations=15):
    """Generalized Procrustes alignment. Reflection not allowed.

    Returns (aligned, mean_shape); mean_shape has unit centroid size.
    """
    P, _ = preshape(A)
    ref = P[0].copy()
    for _ in range(iterations):
        P = np.stack([rotate_onto(ref, x) for x in P])
        ref = P.mean(axis=0)
        ref = ref - ref.mean(axis=0)
        ref = ref / np.sqrt((ref ** 2).sum())
    return P, ref


def shape_variance(aligned, mean_shape):
    """Mean squared Procrustes distance from the mean shape."""
    return ((aligned - mean_shape) ** 2).sum() / len(aligned)
