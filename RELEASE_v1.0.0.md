Analysis code and generated results for the Apidologie submission
"Disagreement between independently produced honey bee wing datasets is
localized at two landmarks and limits reference transfer"
(V. K. Chaudhari and J. J. Pastagia).

## What this is

A reanalysis of published open deposits of honey bee (*Apis mellifera*)
forewing landmark coordinates. It asks whether a morphometric reference built
by one group transfers to wings landmarked by another, using the one case in
the public record where two groups independently landmarked the same images.

## Main results reproduced here

- Mean displacement between the two measurement sets: 0.00875 Procrustes
  units (95% CI 0.00844 to 0.00916), 0.44 times the median distance between
  colony means. Unchanged under 200 random re-pairings of the same wings, so
  it does not depend on how the wings were matched.
- About 94% of the squared mean displacement falls on landmarks 7 and 14 —
  the two whose position Nawrocka et al. (2018) record as moved from the
  earlier convention of Gerula et al. (2009).
- A reference classifier separating its own subspecies in 41 of 41 colonies
  assigned zero or one of five known pure *A. m. caucasica* colonies
  correctly in a dataset produced elsewhere, across 6 to 20 principal
  components.
- One of nine datasets numbers the same 19 landmarks in a different, close to
  reversed order, with no warning from the software.

## Contents

- `scripts/` — eleven numbered analysis scripts and a shared module. Run in
  order from `scripts/`; step 11 writes the figures and must run last. See
  `RUNORDER.md`.
- `results/` — every generated table. `corrected_estimates.md`,
  `review_round2.md` and `review_round3.md` are the authoritative figures.
- `figures/` — Figures 1–4 as vector PDF and 600 dpi LZW-compressed TIFF.
- `manuscript/` — the submitted manuscript, cover letter, supplementary
  tables, and the scripts that build them.

Raw deposits are not redistributed. Every source is listed with its DOI in
`data/README.md` and in Table X of the manuscript.

## Dependencies

NumPy, SciPy, pandas, openpyxl, Pillow, Matplotlib.

## Licence

Code: MIT. Derived data in `results/` is a derived database built from sources
under the Open Database License v1.0, and is released under the same licence
with attribution.
