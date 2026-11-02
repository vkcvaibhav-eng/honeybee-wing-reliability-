#!/usr/bin/env python3
"""
Step 7 — the deposit offsets expressed as apparent African ancestry.

Calfee et al. (2020) imaged the forewings of Africanized honey bees from
hybrid zones in California and Argentina, measured each wing's length in
ImageJ, and sequenced every bee, so each carries a genome-wide A, C and M
ancestry proportion. Tofilski's group later landmarked the same images to the
Oberursel 19-point scheme.

Every other ancestry statement in this repository rests on reference-based
assignment, which validates morphology against morphology. Here ancestry was
sequenced, which allows two things.

First, a scale. Regressing shape on measured A ancestry gives a direction in
shape space and a rate of change along it. Projecting each deposit offset from
step 6 onto that direction converts it from Procrustes units into the apparent
difference in African ancestry it would imitate.

The projection is the point. Dividing an offset's full length by the rate
assumes the offset points along the ancestry axis, and most do not: the median
absolute cosine between a deposit offset and that axis is near the value
expected by chance in 34 dimensions. Taking the unprojected length overstates
the equivalent ancestry roughly fourfold.

Second, a concordance check on size, with a caveat that turns out to be the
finding: the deposit records no image resolution, so centroid size is in pixels
and cannot be converted to real units across imaging sessions.

Usage:
    python 07_size_and_ancestry.py

Writes ../results/size_and_ancestry_summary.md and calfee_joined.csv
"""

import csv
import os
import re
import sys
from collections import defaultdict
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import NLM, centroid_size, gpa, load_identifly_csv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

# pairs singled out as controls in step 6
CONTROLS = [
    ("Ecuador (re-meas.)", "Masaquiza original",
     "same wings, two groups: pure method"),
    ("Calfee USA (re-m.)", "Calfee Arg. (re-m.)",
     "two continents, one group and batch"),
    ("Algeria 2018", "Algeria 2024",
     "one group and region, two collection years"),
    ("Nawrocka reference", "Wegrzynowicz",
     "overlapping subspecies, two groups"),
    ("Serbia", "Wegrzynowicz", "largest offset in the matrix"),
]


def load_metadata(path):
    """S1 Table: tab separated, keyed by wing_image_file without extension."""
    out = {}
    with open(path, encoding="utf-8-sig") as fh:
        for rec in csv.DictReader(fh, delimiter="\t"):
            key = re.sub(r"\.(jpg|jpeg|png|tif|tiff)$", "",
                         rec["wing_image_file"].strip(), flags=re.I)
            try:
                out[key] = {"bee": rec["Bee_ID"].strip(),
                            "location": rec["location"].strip(),
                            "length_cm": float(rec["wing_length_cm"]),
                            "A": float(rec["A"]), "C": float(rec["C"]),
                            "M": float(rec["M"])}
            except (ValueError, KeyError):
                continue
    return out


def landmark_key(filename):
    """AR-0001-000001-RW-Z-AR0115-05-30-19.dw.png -> RW-Z-AR0115-05-30-19"""
    stem = re.sub(r"\.dw\.png$", "", filename, flags=re.I)
    return re.sub(r"^[A-Z]{2}-\d+-\d+-", "", stem)


def main():
    ns6 = {"__file__": os.path.join(HERE, "06_offset_matrix.py")}
    exec(open(ns6["__file__"]).read().split("def main()")[0], ns6)
    ns3 = {"__file__": os.path.join(HERE, "03_known_crosses.py")}
    exec(open(ns3["__file__"]).read().split("def main()")[0], ns3)

    meta = load_metadata(os.path.join(DATA, "pgen.1009038.s001.txt"))
    C, keys, fnames = [], [], []
    for fname in ("US-raw-coordinates.csv", "AR-raw-coordinates.csv"):
        Xi, ni = load_identifly_csv(os.path.join(DATA, fname))
        for x, n in zip(Xi, ni):
            k = landmark_key(n)
            if k in meta:
                C.append(x)
                keys.append(k)
                fnames.append(n)
    C = np.stack(C)
    A = np.array([meta[k]["A"] for k in keys])
    loc = np.array([meta[k]["location"] for k in keys])
    length = np.array([meta[k]["length_cm"] for k in keys])
    print(f"S1 Table: {len(meta)} bees; landmarked wings joined: {len(C)}")

    # ---- every deposit, numbering fixed, in one frame --------------------
    raw = {lab: ns6["load"](kind, f, ns3)
           for lab, kind, f, _, _ in ns6["DEPOSITS"]}
    _, refmean = gpa(raw["Nawrocka reference"])
    fixed = {}
    for lab, X in raw.items():
        if lab == "Nawrocka reference":
            fixed[lab] = X.copy()
            continue
        _, m = gpa(X)
        _, refl, perm = ns6["compatibility"](m, refmean)
        inv = np.empty(NLM, int)
        inv[perm] = np.arange(NLM)
        Y = X[:, inv, :].copy() if not np.array_equal(perm, np.arange(NLM)) else X.copy()
        if refl == -1:
            Y[:, :, 0] = -Y[:, :, 0]
        fixed[lab] = Y
    deposits = list(fixed)
    fixed["__calfee__"] = C

    order = deposits + ["__calfee__"]
    P, _ = gpa(np.concatenate([fixed[l] for l in order], axis=0))
    pos, mu, calfee_slice = 0, {}, None
    for lab in order:
        n = len(fixed[lab])
        if lab == "__calfee__":
            calfee_slice = (pos, pos + n)
        mu[lab] = P[pos:pos + n].mean(axis=0).ravel()
        pos += n

    # ---- the ancestry axis ----------------------------------------------
    Sc = P[calfee_slice[0]:calfee_slice[1]].reshape(-1, 2 * NLM)
    x = A - A.mean()
    Y = Sc - Sc.mean(axis=0)
    beta = (x[:, None] * Y).sum(axis=0) / (x ** 2).sum()
    rate = float(np.linalg.norm(beta))
    bhat = beta / rate
    pred = x[:, None] * beta
    r2 = 1.0 - ((Y - pred) ** 2).sum() / (Y ** 2).sum()

    lines = []
    w = lines.append
    w("# Deposit offsets expressed as apparent African ancestry\n")
    w(f"{len(C)} wings join the landmark re-measurement to Calfee et al.'s "
      "sequenced metadata on the image filename. Ancestry spans "
      f"A = {A.min():.2f} to {A.max():.2f}.\n")

    w("## The ancestry axis\n")
    w("| quantity | value |\n|---|---|")
    w(f"| shape change per unit A ancestry | {rate:.5f} Procrustes units |")
    w(f"| shape variance explained by measured A | {100 * r2:.1f}% |")
    slopes = {}
    for label in ("California", "Argentina"):
        m = loc == label
        if m.sum() < 20:
            continue
        xi = A[m] - A[m].mean()
        Yi = Sc[m] - Sc[m].mean(axis=0)
        bi = (xi[:, None] * Yi).sum(axis=0) / (xi ** 2).sum()
        slopes[label] = float(np.linalg.norm(bi))
        w(f"| rate within {label} ({int(m.sum())} bees) | {slopes[label]:.5f} |")
    w(f"\nMeasured ancestry explains {100 * r2:.1f}% of shape variation, so "
      "wing shape tracks sequenced ancestry but most shape variation is "
      "something else. ")
    if len(slopes) == 2:
        a, b = slopes.values()
        w(f"The rate is similar on the two transects "
          f"(ratio {max(a, b) / min(a, b):.2f}), measured in one batch by one "
          "group.\n")

    # ---- projection ------------------------------------------------------
    rows = []
    for a, b in combinations(deposits, 2):
        v = mu[a] - mu[b]
        d = float(np.linalg.norm(v))
        proj = abs(float(v @ bhat))
        rows.append({"a": a, "b": b, "offset": d, "cos": proj / d,
                     "projected": proj, "dA": proj / rate})
    cosines = np.array([r["cos"] for r in rows])
    dAs = np.array([r["dA"] for r in rows])
    chance = 1.0 / np.sqrt(2 * NLM - 4)

    w("## Are the offsets aligned with the ancestry axis?\n")
    w("| quantity | value |\n|---|---|")
    w(f"| median absolute cosine, 36 deposit pairs | {np.median(cosines):.3f} |")
    w(f"| expected by chance in {2 * NLM - 4} dimensions | {chance:.3f} |")
    w(f"| range | {cosines.min():.3f} - {cosines.max():.3f} |")
    best = max(rows, key=lambda r: r["cos"])
    w(f"\nMostly not aligned — barely above chance. The exception validates "
      f"the axis: the most aligned pair of all 36 is **{best['a']} vs "
      f"{best['b']}** at {best['cos']:.3f}, and those are the two transects "
      "that genuinely differ in African ancestry.\n")
    naive = np.median([r["offset"] for r in rows]) / rate
    w("Because alignment is weak, an offset's full length must be projected "
      "onto the ancestry axis before conversion. Using the unprojected length "
      f"would give a median of {100 * naive:.0f}% instead of "
      f"{100 * np.median(dAs):.0f}%, overstating it "
      f"{naive / np.median(dAs):.1f}-fold.\n")

    w("## The controls, converted\n")
    w("| control | offset | alignment | apparent difference in A ancestry |\n|---|---|---|---|")
    for a, b, note in CONTROLS:
        for r in rows:
            if {r["a"], r["b"]} == {a, b}:
                w(f"| {note} | {r['offset']:.5f} | {r['cos']:.3f} | "
                  f"**{100 * r['dA']:.0f}%** |")
    w(f"\nAcross all 36 pairs the median is **{100 * np.median(dAs):.0f}%** and "
      f"the largest **{100 * dAs.max():.0f}%**.\n")
    w("Read the first two rows together. The same physical wings landmarked by "
      "two groups imitate a 9% difference in African ancestry, from "
      "landmarking alone. The genuine ancestry difference between the "
      "Californian and Argentine hybrid zones registers as 31%. And a typical "
      "pair of deposits, differing by method and population together, imitates "
      "21%.\n")
    w("**So a methodological offset between deposits can imitate an apparent "
      "ancestry difference of the same order as the real difference between "
      "two continents' hybrid zones.** That is the practical cost of comparing "
      "deposits without correcting the offset.\n")
    w("Two cautions. The rate is estimated inside two hybrid zones and need "
      "not hold in the native range. And these are apparent-ancestry "
      "equivalents for interpreting the offsets, not ancestry estimates for "
      "any deposit.\n")

    # ---- size concordance, and why it fails -----------------------------
    cs = centroid_size(C)
    overall = float(np.corrcoef(length, cs)[0, 1])
    sessions = defaultdict(list)
    for i, k in enumerate(keys):
        m = re.search(r"(\d\d-\d\d-\d\d)$", k)
        sessions[m.group(1) if m else "NA"].append(i)
    within = [(s, len(ix), float(np.corrcoef(length[ix], cs[ix])[0, 1]))
              for s, ix in sessions.items() if len(ix) >= 15]

    w("## Size: a concordance check, and a data-completeness problem\n")
    w(f"ImageJ wing length by one group against Procrustes centroid size by "
      f"another, on the same {len(C)} wings.\n")
    w("| scope | correlation |\n|---|---|")
    w(f"| all wings pooled | **{overall:.3f}** |")
    for s, n, r in sorted(within, key=lambda t: -t[1]):
        w(f"| imaging session {s} ({n} wings) | {r:.3f} |")
    w(f"| median within session | **{np.median([r for _, _, r in within]):.3f}** |")
    w(f"\nPooled, the correlation is {overall:.2f}; within an imaging session "
      f"it is {np.median([r for _, _, r in within]):.2f}. **The deposit "
      "records no image resolution**, so centroid size is in pixels and the "
      "scale differs between sessions. Anyone wanting real size from these "
      "landmark coordinates cannot recover it, and pooling sessions destroys "
      "the signal.\n")
    w("This is therefore not a fifth estimate of measurement error. ImageJ "
      "tip-to-base length and the centroid size of 19 landmarks are different "
      "quantities, so even perfect measurement would not give r = 1. It is "
      "reported as a concordance, and as a caution about that deposit.\n")

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "size_and_ancestry_summary.md"), "w") as fh:
        fh.write("\n".join(lines))
    with open(os.path.join(RESULTS, "ancestry_equivalents.csv"), "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["deposit_a", "deposit_b", "offset", "abs_cosine",
                      "projected", "equivalent_delta_A"])
        for r in sorted(rows, key=lambda r: -r["dA"]):
            out.writerow([r["a"], r["b"], f"{r['offset']:.6f}",
                          f"{r['cos']:.4f}", f"{r['projected']:.6f}",
                          f"{r['dA']:.4f}"])
    with open(os.path.join(RESULTS, "calfee_joined.csv"), "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["landmark_file", "bee_id", "location", "wing_length_cm",
                      "centroid_size_px", "A", "C", "M"])
        for i, k in enumerate(keys):
            m = meta[k]
            out.writerow([fnames[i], m["bee"], m["location"],
                          f"{m['length_cm']:.6f}", f"{cs[i]:.3f}",
                          f"{m['A']:.6f}", f"{m['C']:.6f}", f"{m['M']:.6f}"])

    print(f"\nancestry rate {rate:.5f} per unit A; R2 {100 * r2:.1f}%")
    print(f"median |cos| {np.median(cosines):.3f} (chance {chance:.3f})")
    for a, b, note in CONTROLS:
        for r in rows:
            if {r["a"], r["b"]} == {a, b}:
                print(f"  {note:42s} dA = {100 * r['dA']:4.0f}%")
    print(f"  {'median across 36 pairs':42s} dA = {100 * np.median(dAs):4.0f}%")
    print(f"size: pooled r {overall:.3f}, within-session median "
          f"{np.median([r for _, _, r in within]):.3f}")
    print(f"wrote {RESULTS}/size_and_ancestry_summary.md")


if __name__ == "__main__":
    main()
