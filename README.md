# Measurement reliability in honey bee wing geometric morphometrics

Analysis code for a study of measurement reliability and within-colony shape
variance in *Apis mellifera* forewing geometric morphometrics, using published
open landmark data.

Wing geometric morphometrics on the 19-landmark configuration of Nawrocka
et al. (2018) is now the standard low-cost method for identifying honey bee
subspecies and evolutionary lineages, and tens of thousands of digitized
forewings have been deposited openly by several groups. That body of open data
is what makes this study possible.

What it has never had is a published error budget. This repository supplies
one, and then uses it to correct a second quantity that colony averaging
normally discards.

## Why an error budget is possible at all

Measuring digitization error requires the same physical wings to have been
digitized twice, independently. Across the whole public record that happens
once: Masaquiza and Arenal deposited images and coordinates of 663 worker
forewings from the central highlands of Ecuador, and Tofilski's group later
re-landmarked the same images to the Nawrocka configuration and deposited the
result separately.

Those two deposits are the only replicate pair available, and this analysis
exists because both groups deposited their data openly.

## Headline results

| quantity | value |
|---|---|
| wings matched one-to-one across deposits | 642 of 663 (96.8%) |
| centroid-size correlation between teams | r = 0.986 |
| median Procrustes distance between teams, same wing | 0.0096 |
| error as share of total shape variance | 17.7% |
| error as share of within-colony variance | 26.5% |
| error as share of among-colony variance | 52.9% |
| same, after averaging 9.8 wings per colony | 5.4% |

Two consequences:

**Colony-mean analyses are protected by averaging.** Reference-based lineage
and subspecies assignment compares colony means, and averaging around ten
wings reduces error in the mean to roughly 5% of among-colony variance. That
practice holds up.

**Analyses using within-colony spread are not protected.** 26.5% of
within-colony variance is digitizing noise; 73.5% is real signal. Any use of
within-colony variance must subtract the error variance first.

### A trap for anyone pooling these deposits

**The two deposits number the same 19 anatomical points in different, close to
reversed order.** Pooled without correction, Procrustes distances between the
same wings sit near 1.05 against a theoretical maximum of 1.41 — and nothing
raises an error. `results/landmark_map.csv` gives the correspondence.

### Landmark reliability

Disagreement is far from uniform across the configuration. Landmarks 7 and 14
carry the most, landmark 7 at about six times the most reliable point,
landmark 11. See `results/per_landmark_disagreement.csv`.

## Repository layout

```
scripts/wingio.py                  loaders and Procrustes utilities
scripts/01_find_landmark_map.py    recover the landmark-numbering map
scripts/02_match_and_error.py      match deposits, estimate error
scripts/03_known_crosses.py        reference transfer and known-pedigree crosses
data/README.md                     source DOIs and how to fetch them
results/                           generated tables and summary
```

Raw data is not committed. `data/README.md` lists every source with its DOI.

## Reproducing

```bash
pip install numpy scipy openpyxl
# fetch the two source files as described in data/README.md, into data/
cd scripts
python 01_find_landmark_map.py ../data/raw_coordinates.xlsx ../data/EC-raw-coordinates.csv
python 02_match_and_error.py  ../data/raw_coordinates.xlsx ../data/EC-raw-coordinates.csv
```

python 03_known_crosses.py ../data/oo_404830.txt \
    ../data/Nawrocka_et_al2018.csv ../data/Nawrocka_et_al2018-geo-data.csv
```

Step 1 must run first; step 2 reads the landmark map it writes. Step 3 is
independent of both.

## Reference transfer and known crosses

Step 3 applies a reference classifier built on the Oberursel material to
9,590 wings of known pedigree — 200 queens, 24 genotypes by instrumental
insemination.

| quantity | value |
|---|---|
| reference leave-one-colony-out accuracy | 41/41 (100%) |
| offset between the two datasets | 0.0247 |
| reference between-subspecies distances | 0.0194 - 0.0322 |
| inter-team digitization error (step 2) | 0.0096 |

The offset between datasets is as large as the difference between subspecies,
and 2.6 times the digitization error measured on the same images in step 2.
Applied raw, the classifier misassigns known-pure caucasica entirely;
correcting the offset recovers it.

Across 83 F1 colonies, 36.1% are assigned to the queen's subspecies, 55.4% to
the drone's and 8.4% to a third. Two of the three reciprocal pairs — identical
nuclear composition, opposite parental direction — are assigned to different
subspecies, so **assignment of a known F1 is not predictable from parentage**.

The two datasets agree only partly on how the subspecies differ (mean cosine
0.495). A measurement offset and genuine divergence of selected breeding lines
are confounded here and cannot be separated from these data.

```text

## Scope and limits

The variance shares above are an upper bound. The denominator is variance
within a single population, so for comparisons spanning evolutionary lineages
the same absolute error is a much smaller fraction of relevant variation.

This is one pair of teams on one set of images — the only such pair in the
public record. That makes it informative, and it does not license a general
claim about cross-dataset comparison.

## Licence

Code: MIT, see `LICENSE`.

Derived data in `results/` is a derived database built from sources under the
Open Database License v1.0 and is released under the same licence with
attribution. See `data/README.md`.
