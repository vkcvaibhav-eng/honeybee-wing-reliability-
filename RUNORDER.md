# Reproduction order

Run from `scripts/`, in numerical order. Paths are derived from the script
location, so the repository can sit anywhere.

```
01_find_landmark_map.py
02_match_and_error.py
03_known_crosses.py        ../data/oo_404830.txt ../data/Nawrocka_et_al2018.csv ../data/Nawrocka_et_al2018-geo-data.csv
04_paired_wings.py
05_within_colony_variance.py
06_offset_matrix.py
07_size_and_ancestry.py
08_corrected_estimates.py
09_review_round2.py
10_matching_signature.py
11_figures.py              <- must run last; it writes figures/Fig1-4 as PDF and 600 dpi TIFF
```

Step 11 is the only step that writes figures. Earlier steps write result
tables to `results/` only.

Authoritative results: `results/corrected_estimates.md`,
`results/review_round2.md`, `results/review_round3.md`.
