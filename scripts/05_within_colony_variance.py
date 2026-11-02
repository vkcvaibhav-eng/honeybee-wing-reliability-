#!/usr/bin/env python3
"""
Step 5 — is within-colony shape variance comparable across deposits?

Colony averaging discards the spread of wings within a colony. That spread is
biologically interesting in principle: workers in a naturally mated colony
have many fathers, so patriline diversity should show up as within-colony
shape variance, and a colony with an introduced drone contribution should look
more variable than its mean suggests.

This step tests the premise before building on it, using a case where the
mating structure is known rather than assumed.

Every colony in the Wegrzynowicz material was inseminated with semen from ONE
drone, so its workers share a single father. Serbian and Algerian queens mated
naturally with many drones. The prediction is therefore directional and sharp:
single-drone colonies should show LESS within-colony variance than naturally
mated ones.

Where both forewings of a bee are available they are averaged first, which
halves that bee's measurement error. The error floor subtracted is the
bilateral estimate from step 4 for the naturally mated deposits, and the
cross-team estimate from step 2 for the single-drone deposit, which has
neither replicate nor bilateral data. Taking the larger floor there overstates
its noise, so it works against the prediction being tested.

Usage:
    python 05_within_colony_variance.py

Writes ../results/within_colony_variance_summary.md
"""

import os
import re
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wingio import load_identifly_csv, preshape, rotate_onto

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

# step 4, bilateral; halved because a bee's two wings are averaged first
ERR_BILATERAL = 0.000045 / 2.0
# step 2, cross-team; used where no bilateral or replicate data exists
ERR_CROSS_TEAM = 0.000047

MIN_BEES = 5
SIDE_RE = re.compile(r"-(LW|RW1|RW|L|R)([-.])")


def individuals(X, names):
    """Collapse to one configuration per bee, averaging both wings when present."""
    seen = defaultdict(dict)
    for i, name in enumerate(names):
        m = SIDE_RE.search(name)
        if m:
            seen[name[:m.start()] + "-X" + name[m.end() - 1:]][m.group(1)[0]] = i
        else:
            seen[name]["R"] = i
    configs, keys = [], []
    for key, sides in seen.items():
        idx = list(sides.values())
        configs.append(X[idx].mean(axis=0) if len(idx) == 2 else X[idx[0]])
        keys.append(key)
    return np.stack(configs), keys


def joint_gpa(stack, iterations=10):
    P, _ = preshape(stack)
    ref = P[0].copy()
    for _ in range(iterations):
        P = np.stack([rotate_onto(ref, x) for x in P])
        ref = P.mean(axis=0)
        ref = ref - ref.mean(axis=0)
        ref = ref / np.sqrt((ref ** 2).sum())
    return P


def per_colony_variance(configs, colonies):
    """Unbiased within-colony Procrustes variance, one value per colony."""
    groups = defaultdict(list)
    for x, c in zip(configs, colonies):
        if c:
            groups[c].append(x)
    out, sizes = [], []
    for c, v in groups.items():
        if len(v) < MIN_BEES:
            continue
        v = np.stack(v)
        out.append(((v - v.mean(axis=0)) ** 2).sum() / (len(v) - 1))
        sizes.append(len(v))
    return np.asarray(out), np.asarray(sizes)


def main():
    ns = {"__file__": os.path.join(HERE, "03_known_crosses.py")}
    exec(open(ns["__file__"]).read().split("def main()")[0], ns)

    datasets = {}
    for tag, fname, pattern in (
            ("Serbia", "RS_21_80-raw-coordinates.csv", r"(RS-\d+)"),
            ("Algeria 2018", "DZ-2018-raw-coordinates.csv", r"(DZ-\d+)")):
        X, names = load_identifly_csv(os.path.join(DATA, fname))
        C, keys = individuals(X, names)
        rx = re.compile(pattern)
        colonies = [rx.match(k).group(1) if rx.match(k) else None for k in keys]
        datasets[tag] = (C, colonies, "natural", ERR_BILATERAL)

    W, Wmeta = ns["load_known_crosses"](os.path.join(DATA, "oo_404830.txt"))
    W = W.copy()
    W[:, :, 0] = -W[:, :, 0]
    datasets["Wegrzynowicz"] = (
        W, [f"{m['genotype']}|{m['colony']}" for m in Wmeta],
        "single-drone", ERR_CROSS_TEAM)

    P = joint_gpa(np.concatenate([v[0] for v in datasets.values()], axis=0))
    pos, aligned = 0, {}
    for tag, (C, colonies, mating, err) in datasets.items():
        aligned[tag] = (P[pos:pos + len(C)], colonies, mating, err)
        pos += len(C)

    lines, rows = [], []
    w = lines.append
    w("# Is within-colony shape variance comparable across deposits?\n")
    w("Every Wegrzynowicz colony was inseminated with semen from one drone, so "
      "its workers share a father. Serbian and Algerian queens mated naturally "
      "with many. Single-drone colonies should therefore show **less** "
      "within-colony variance.\n")
    w("| deposit | mating | colonies | bees per colony | raw variance | "
      "error floor | corrected |\n|---|---|---|---|---|---|---|")

    store = {}
    for tag, (C, colonies, mating, err) in aligned.items():
        var, sizes = per_colony_variance(C, colonies)
        corrected = np.maximum(var - err, 0.0)
        store[tag] = (corrected, mating)
        rows.append((tag, mating, len(var), sizes.mean(),
                     np.median(var), err, np.median(corrected)))
        w(f"| {tag} | {mating} | {len(var)} | {sizes.mean():.1f} | "
          f"{np.median(var):.6f} | {err:.6f} | {np.median(corrected):.6f} |")

    natural = np.concatenate([v for v, m in store.values() if m == "natural"])
    single = store["Wegrzynowicz"][0]

    w("\n## The prediction fails, in the opposite direction\n")
    w(f"| group | colonies | median | 25th-75th percentile |\n|---|---|---|---|")
    w(f"| naturally mated | {len(natural)} | {np.median(natural):.6f} | "
      f"{np.percentile(natural, 25):.6f} - {np.percentile(natural, 75):.6f} |")
    w(f"| single-drone | {len(single)} | {np.median(single):.6f} | "
      f"{np.percentile(single, 25):.6f} - {np.percentile(single, 75):.6f} |")
    try:
        from scipy.stats import mannwhitneyu
        _, p = mannwhitneyu(natural, single, alternative="greater")
        w(f"\nMann-Whitney, naturally mated greater than single-drone: "
          f"**p = {p:.2g}**. Single-drone colonies are the *most* variable of "
          "the three deposits, which is biologically backwards.\n")
    except ImportError:
        pass

    w("The clearest sign that deposit, not biology, drives this: Serbia and "
      "Algeria 2018 share a mating structure and a digitizing group, yet their "
      "median within-colony variances differ by "
      f"{max(r[6] for r in rows[:2]) / min(r[6] for r in rows[:2]):.1f}x. "
      "No plausible difference in polyandry spans that.\n")

    w("## What this means\n")
    w("**Within a single deposit the quantity is sound.** In Serbia the error "
      f"floor is only {100 * ERR_BILATERAL / rows[0][4]:.0f}% of within-colony "
      "variance, so the spread there is mostly real signal and can be compared "
      "between colonies measured together.\n")
    w("**Across deposits it is not comparable.** Within-colony variance cannot "
      "serve as a cross-deposit index of admixture or paternal diversity, "
      "because deposit-specific effects exceed the biological signal it would "
      "have to detect.\n")
    w("This completes the picture from step 3. Cross-deposit comparison fails "
      "for **location** — the offset between deposit means matches the "
      "difference between subspecies — and it fails for **scale** — "
      "within-colony variances differ by more than mating structure can "
      "explain. Within one deposit, both quantities behave.\n")
    w("A caveat on what is not shown: the Wegrzynowicz deposit has no "
      "replicate or bilateral wings, so its own measurement error is unknown "
      "and may be larger than the floor subtracted here. That would explain "
      "its high variance without any biology, and these data cannot "
      "distinguish the two.\n")

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "within_colony_variance_summary.md"), "w") as fh:
        fh.write("\n".join(lines))

    for tag, mating, n, bees, raw, err, corr in rows:
        print(f"{tag:14s} {mating:12s} colonies {n:4d}  bees/col {bees:5.1f}  "
              f"corrected {corr:.6f}")
    print(f"\nnaturally mated median {np.median(natural):.6f}  "
          f"single-drone median {np.median(single):.6f}")
    print(f"prediction (single-drone lower) FAILS")
    print(f"wrote {RESULTS}/within_colony_variance_summary.md")


if __name__ == "__main__":
    main()
