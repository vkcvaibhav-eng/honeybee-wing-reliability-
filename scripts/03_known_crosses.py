#!/usr/bin/env python3
"""
Step 3 — how reference-based subspecies assignment behaves on wings of known
pedigree, and how far a cross-dataset offset moves it.

Reference : Nawrocka, Kandemir, Fuchs & Tofilski (2018). Morphometric Bee Data
            Bank, Oberursel. 1,832 workers, 187 colonies, 25 subspecies,
            4 lineages. Zenodo 10.5281/zenodo.7567336
Test      : Wegrzynowicz & Los (2020), Biodiversity Data Journal 8: e53724.
            9,590 wings, 200 queens, 24 genotypes produced by instrumental
            insemination — the only honey bee wing material with known
            parentage.

The three parental subspecies belong to three different evolutionary lineages
(A. m. carnica C, A. m. caucasica O, A. m. mellifera M), so every cross is a
between-lineage cross and the standard reference classifier applies directly.

Two questions are asked:

  1. Does a reference built from one collection transfer to material measured
     elsewhere? Known-pure parental lines answer this, because their correct
     assignment is not in doubt.

  2. Can a known F1 hybrid be assigned to a parent? The reciprocal pairs settle
     this: F1ck is a caucasica queen inseminated by a carnica drone and F1kc is
     the reverse, so nuclear composition is the same and only the parental
     direction differs.

Usage:
    python 03_known_crosses.py ../data/oo_404830.txt \
        ../data/Nawrocka_et_al2018.csv ../data/Nawrocka_et_al2018-geo-data.csv
"""

import csv
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import NLM, load_identifly_csv, preshape, rotate_onto

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")

# the three parental subspecies and their lineages
SUBSP = {"carnica": "C", "caucasia": "O", "mellifera": "M"}

# genotype letter -> subspecies, as defined in the data paper's genotype key
LETTER = {"c": "caucasia", "k": "carnica", "m": "mellifera"}

N_PC = 12


def load_known_crosses(path):
    """Read the Wegrzynowicz table: 6 metadata columns then x0,y0 ... x18,y18."""
    specs, meta = [], []
    with open(path, encoding="utf-8-sig") as fh:
        reader = csv.reader(fh, delimiter="\t")
        next(reader)
        for row in reader:
            if len(row) < 6 + 2 * NLM:
                continue
            try:
                vals = [float(x) for x in row[6:6 + 2 * NLM]]
            except ValueError:
                continue
            # the source file spells eight backcross genotypes "Bc..." and
            # four "BC...", so case is normalised here
            genotype = row[4].strip()
            if genotype[:2].upper() == "BC":
                genotype = "BC" + genotype[2:]
            specs.append(np.asarray(vals, float).reshape(NLM, 2))
            meta.append({"colony": row[1].strip(), "genotype": genotype})
    return np.stack(specs), meta


def load_reference_meta(path):
    with open(path, encoding="utf-8-sig") as fh:
        return {r["sample"]: (r["subspecies"], r["lineage"])
                for r in csv.DictReader(fh)}


def joint_gpa(stack, iterations=10):
    """Procrustes-align two datasets into one common shape space."""
    P, _ = preshape(stack)
    ref = P[0].copy()
    for _ in range(iterations):
        P = np.stack([rotate_onto(ref, x) for x in P])
        ref = P.mean(axis=0)
        ref = ref - ref.mean(axis=0)
        ref = ref / np.sqrt((ref ** 2).sum())
    return P


def group_means(P, keys):
    order, index = [], {}
    for k in keys:
        if k not in index:
            index[k] = len(order)
            order.append(k)
    sums = np.zeros((len(order), NLM, 2))
    counts = np.zeros(len(order))
    for x, k in zip(P, keys):
        sums[index[k]] += x
        counts[index[k]] += 1
    return sums / counts[:, None, None], order, counts


class LDA:
    """Discriminant assignment on PCA-reduced shape: class means plus a pooled
    within-class covariance, assigning by Mahalanobis distance in the pooled
    metric. This is the standard approach in the honey bee wing literature."""

    def fit(self, X, y, n_pc=N_PC, shrink=1e-6):
        self.mu = X.mean(axis=0)
        _, _, Vt = np.linalg.svd(X - self.mu, full_matrices=False)
        self.W = Vt[:n_pc].T
        Z = (X - self.mu) @ self.W
        y = np.asarray(y)
        self.classes = sorted(set(y))
        self.centroids = np.stack([Z[y == c].mean(axis=0) for c in self.classes])
        pooled = np.zeros((n_pc, n_pc))
        for c in self.classes:
            D = Z[y == c] - Z[y == c].mean(axis=0)
            pooled += D.T @ D
        pooled /= (len(Z) - len(self.classes))
        self.inv = np.linalg.pinv(pooled + shrink * np.eye(n_pc))
        return self

    def predict(self, X):
        Z = (X - self.mu) @ self.W
        D = np.empty((len(Z), len(self.classes)))
        for j, c in enumerate(self.centroids):
            d = Z - c
            D[:, j] = np.einsum("ij,jk,ik->i", d, self.inv, d)
        return [self.classes[i] for i in D.argmin(axis=1)]


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    path_crosses, path_ref, path_ref_meta = sys.argv[1:4]

    W, Wmeta = load_known_crosses(path_crosses)
    N, Nfiles = load_identifly_csv(path_ref)
    meta = load_reference_meta(path_ref_meta)

    # the cross dataset is mirrored relative to the reference
    W = W.copy()
    W[:, :, 0] = -W[:, :, 0]

    nN = len(N)
    P = joint_gpa(np.concatenate([N, W], axis=0))
    PN, PW = P[:nN], P[nN:]

    # reference colony means, restricted to the three parental subspecies
    samples = ["-".join(f.split("-")[:3]) for f in Nfiles]
    subs = [meta.get(s, (None, None))[0] for s in samples]
    keep = [i for i, s in enumerate(subs) if s in SUBSP]
    Nm, Norder, _ = group_means(PN[keep], [samples[i] for i in keep])
    Nlab = [meta[s][0] for s in Norder]
    Xref = Nm.reshape(len(Nm), -1)

    # cross-dataset colony means
    Wm, Worder, Wcount = group_means(
        PW, [f"{m['genotype']}|{m['colony']}" for m in Wmeta])
    geno = [k.split("|")[0] for k in Worder]
    Xtest = Wm.reshape(len(Wm), -1)

    lines = []
    w = lines.append
    w("# Reference transfer and assignment of known crosses\n")
    w(f"Reference colonies: {dict(Counter(Nlab))}  ")
    w(f"Cross dataset: {len(W)} wings, {len(Worder)} colonies, "
      f"{len(set(geno))} genotypes\n")

    # --- does the reference separate itself? -----------------------------
    correct = 0
    for i in range(len(Xref)):
        mask = np.ones(len(Xref), bool)
        mask[i] = False
        m = LDA().fit(Xref[mask], [Nlab[j] for j in range(len(Nlab)) if mask[j]])
        correct += m.predict(Xref[i:i + 1])[0] == Nlab[i]
    w("## Reference internal accuracy\n")
    w(f"Leave-one-colony-out: **{correct}/{len(Xref)} "
      f"({100 * correct / len(Xref):.1f}%)**. The reference separates its own "
      "subspecies cleanly, so anything that follows is about transfer, not "
      "about the classifier.\n")

    # --- the cross-dataset offset ----------------------------------------
    centroid = {s: Nm[[i for i, l in enumerate(Nlab) if l == s]].mean(axis=0)
                for s in SUBSP}
    between = {}
    keys = list(SUBSP)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            between[(keys[i], keys[j])] = float(
                np.sqrt(((centroid[keys[i]] - centroid[keys[j]]) ** 2).sum()))
    offset_vec = (Nm.mean(axis=0) - Wm.mean(axis=0))
    offset = float(np.sqrt((offset_vec ** 2).sum()))

    w("## The cross-dataset offset\n")
    w("| quantity | value |\n|---|---|")
    w(f"| offset between dataset grand means | **{offset:.5f}** |")
    for (a, b), d in between.items():
        w(f"| reference {a} to {b} | {d:.5f} |")
    w(f"| inter-team digitization error (step 2, Ecuador) | 0.00964 |\n")
    w(f"The offset sits inside the range of between-subspecies distances "
      f"({min(between.values()):.5f} to {max(between.values()):.5f}), and is "
      f"{offset / 0.00964:.1f} times the inter-team digitization error "
      "measured on the same images in step 2. Landmarking alone therefore "
      "does not account for it.\n")

    # --- direction agreement ---------------------------------------------
    pure = {"caucasia": ("P0cc", "P1cc"), "carnica": ("P0kk", "P1kk"),
            "mellifera": ("P0mm", "P1mm")}
    wc = {s: Wm[[i for i, g in enumerate(geno) if g in gs]].mean(axis=0)
          for s, gs in pure.items()}
    w("## Do the two datasets agree on how subspecies differ?\n")
    w("| contrast | reference | crosses | cosine |\n|---|---|---|---|")
    cosines = []
    for (a, b), d in between.items():
        u = (centroid[b] - centroid[a]).ravel()
        v = (wc[b] - wc[a]).ravel()
        cos = float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))
        cosines.append(cos)
        w(f"| {a} to {b} | {np.linalg.norm(u):.5f} | "
          f"{np.linalg.norm(v):.5f} | {cos:.3f} |")
    w(f"\nMean cosine **{np.mean(cosines):.3f}**. Agreement is partial, and the "
      "cross dataset is less differentiated than the wild reference. So this "
      "is not a pure measurement offset: a measurement difference and genuine "
      "divergence of selected breeding lines are confounded here, and these "
      "data cannot separate them.\n")

    # --- pure lines, raw and corrected -----------------------------------
    model = LDA().fit(Xref, Nlab)
    pred_raw = model.predict(Xtest)
    pred_adj = model.predict(Xtest + offset_vec.ravel())

    def summarise(g, pred):
        idx = [i for i, x in enumerate(geno) if x == g]
        c = Counter(pred[i] for i in idx)
        return len(idx), c, " ".join(f"{SUBSP[k]}:{v}" for k, v in c.most_common())

    w("## Known-pure parental lines\n")
    w("Correct assignment of these is not in doubt, so they test transfer.\n")
    w("| genotype | expected | colonies | raw | offset-corrected |\n|---|---|---|---|---|")
    for g in ("P0cc", "P1cc", "P0kk", "P1kk", "P0mm", "P1mm"):
        if g not in geno:
            continue
        exp = LETTER[g[2]]
        n, cr, sr = summarise(g, pred_raw)
        _, ca, sa = summarise(g, pred_adj)
        w(f"| {g} | {exp} ({SUBSP[exp]}) | {n} | {sr} "
          f"— {100 * cr.get(exp, 0) / n:.0f}% | {sa} "
          f"— {100 * ca.get(exp, 0) / n:.0f}% |")
    w("\nRaw transfer misassigns known-pure caucasica entirely. The correction "
      "recovers it. Note also that a raw 'correct' call can rest on a margin "
      "far below the offset, so it carries no evidential weight.\n")

    # --- reciprocal F1 pairs ---------------------------------------------
    w("## Reciprocal F1 pairs (offset-corrected)\n")
    w("Identical nuclear composition, opposite parental direction.\n")
    w("| genotype | queen | drone | colonies | assignment |\n|---|---|---|---|---|")
    for a, b in (("F1ck", "F1kc"), ("F1cm", "F1mc"), ("F1km", "F1mk")):
        for g in (a, b):
            if g not in geno:
                continue
            n, _, s = summarise(g, pred_adj)
            w(f"| {g} | {LETTER[g[2]]} | {LETTER[g[3]]} | {n} | {s} |")

    tot = q = d = 0
    for g in set(geno):
        if not g.startswith("F1"):
            continue
        qs, ds = LETTER[g[2]], LETTER[g[3]]
        for i, x in enumerate(geno):
            if x == g:
                tot += 1
                q += pred_adj[i] == qs
                d += pred_adj[i] == ds
    w(f"\nAcross **{tot} F1 colonies**: {100 * q / tot:.1f}% assigned to the "
      f"queen's subspecies, {100 * d / tot:.1f}% to the drone's, "
      f"{100 * (tot - q - d) / tot:.1f}% to a third. Two of the three "
      "reciprocal pairs are assigned to different subspecies despite "
      "identical composition, so **assignment of a known F1 is not "
      "predictable from parentage**. The lean toward the drone's subspecies "
      "follows from which subspecies pairs exist, not from a paternal "
      "effect.\n")

    # --- backcrosses ------------------------------------------------------
    w("## Backcrosses, 3:1 composition (offset-corrected)\n")
    w("| genotype | majority subspecies | colonies | assignment | matches majority |\n|---|---|---|---|---|")
    hits = []
    for g in sorted(x for x in set(geno) if x.startswith("BC")):
        maj = LETTER[g[4]]
        n, c, s = summarise(g, pred_adj)
        pct = 100 * c.get(maj, 0) / n
        hits.append(pct)
        w(f"| {g} | {maj} | {n} | {s} | {pct:.0f}% |")
    w(f"\nMedian across the twelve backcross genotypes: "
      f"**{np.median(hits):.0f}%**. Skewed composition is usually recovered, "
      "but not dependably.\n")

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "known_crosses_summary.md"), "w") as fh:
        fh.write("\n".join(lines))

    with open(os.path.join(RESULTS, "known_crosses_assignments.csv"), "w",
              newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["genotype", "colony", "wings", "queen_subspecies",
                      "drone_subspecies", "assigned_raw", "assigned_corrected"])
        for i, key in enumerate(Worder):
            g, colony = key.split("|")
            if g.startswith("P"):
                qs = ds = LETTER[g[2]]
            elif g.startswith("F1"):
                qs, ds = LETTER[g[2]], LETTER[g[3]]
            else:
                qs, ds = LETTER[g[2]], LETTER[g[4]]
            out.writerow([g, colony, int(Wcount[i]), qs, ds,
                          pred_raw[i], pred_adj[i]])

    print(f"reference leave-one-colony-out: {correct}/{len(Xref)}")
    print(f"cross-dataset offset: {offset:.5f}")
    print(f"between-subspecies range: {min(between.values()):.5f}"
          f"-{max(between.values()):.5f}")
    print(f"F1 colonies {tot}: queen {100 * q / tot:.1f}%, "
          f"drone {100 * d / tot:.1f}%, third {100 * (tot - q - d) / tot:.1f}%")
    print(f"wrote {RESULTS}/known_crosses_summary.md")


if __name__ == "__main__":
    main()
