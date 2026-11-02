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
| error as share of total shape variance | 7.5% |
| error as share of within-colony variance | 11.2% |
| error as share of among-colony variance | 22.3% |
| same, after averaging 9.8 wings per colony | 2.3% |

Two consequences:

**Colony-mean analyses are protected by averaging.** Reference-based lineage
and subspecies assignment compares colony means, and averaging around ten
wings reduces error in the mean to roughly 5% of among-colony variance. That
practice holds up.

**Analyses using within-colony spread are not protected.** 11.2% of
within-colony variance is digitizing noise; 89% is real signal. Any use of
within-colony variance must subtract the error variance first.

### Two independent routes to the same number

The error variance is estimated twice, by methods that share no step:

| route | deposits | error variance |
|---|---|---|
| two teams digitizing the same images (step 2) | Ecuador pair | 0.000047 |
| left-right pairs within one bee (step 4) | Algeria 2018, Serbia, Algeria 2024 — 1,689 bees | 0.000044 - 0.000046 |

Agreement to about 5%. Step 2 depends on matching specimens across deposits;
step 4 depends on bilateral pairs inside one deposit. Neither relies on the
other.

This convergence is why step 2 reports a median-based estimator rather than a
mean-based one. Thirty-four of its 642 pairs sit above three times the median
distance, with a maximum of 0.134 — beyond plausible landmarking disagreement,
and a sign of a failed match rather than measurement error. They inflate a
mean-based estimate roughly twofold, to 0.000110.

Directional asymmetry in shape is essentially zero across all 1,689 paired
bees, independently confirming the published result that forewing shape does
not differ between body sides while size does. Fluctuating asymmetry cannot be
separated from within-session digitizing error with public data: the
left-right variance contains both, so it bounds each from above.

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
scripts/04_paired_wings.py         independent error estimate from bilateral pairs
scripts/05_within_colony_variance.py  is within-colony spread comparable across deposits?
scripts/06_offset_matrix.py        pairwise offsets across all nine deposits
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

python 04_paired_wings.py ../data/DZ-2018-raw-coordinates.csv \
    ../data/RS_21_80-raw-coordinates.csv ../data/DZ-2024-raw-coordinates.csv
```

python 05_within_colony_variance.py
python 06_offset_matrix.py
```

Step 1 must run first; step 2 reads the landmark map it writes. Steps 3, 4 and
5 are independent of both.

## Within-colony spread does not transfer either

Colony averaging discards the spread of wings within a colony, and that spread
should carry paternal diversity. Step 5 tests the premise where mating
structure is known: every Węgrzynowicz colony was inseminated with semen from
one drone, while Serbian and Algerian queens mated naturally with many, so
single-drone colonies should be the least variable.

| deposit | mating | colonies | within-colony variance, error-corrected |
|---|---|---|---|
| Serbia | natural | 60 | 0.000250 |
| Algeria 2018 | natural | 46 | 0.000402 |
| Węgrzynowicz | single-drone | 201 | 0.000436 |

The prediction fails in the opposite direction: single-drone colonies are the
most variable of the three. Serbia and Algeria 2018 share a mating structure
and a digitizing group yet differ by 1.6x, which no difference in polyandry
spans.

Within one deposit the quantity is sound — in Serbia the error floor is 8% of
within-colony variance. Across deposits it is not comparable, so within-colony
variance cannot serve as a cross-deposit index of admixture.

Together with step 3 this gives one conclusion. Cross-deposit comparison fails
for **location**, because the offset between deposit means matches the
difference between subspecies, and for **scale**, because within-colony
variances differ by more than mating structure can explain. Within a single
deposit, both behave.

## The digitizing group matters more than geography

Step 6 puts all nine deposits in one frame and reports every pairwise offset,
after verifying landmark numbering and handedness for each. Offsets grow as
deposits share less:

| comparison | pairs | median offset |
|---|---|---|
| same group, same region | 1 | 0.01256 |
| same group, other region | 20 | 0.01711 |
| different group | 15 | 0.02398 |
| *reference between-subspecies, for scale* | | *0.01941 - 0.03216* |
| *reference split-half baseline* | | *0.00550* |

Four controls separate method from biology:

| control | offset | what varies |
|---|---|---|
| same wings, two groups (Ecuador vs Masaquiza) | **0.00891** | digitizing only |
| two continents, one group and batch (Calfee California vs Argentina) | **0.00781** | geography only |
| one group and region, two collection years (Algeria 2018 vs 2024) | **0.01256** | collection and preparation |
| overlapping subspecies, two groups (reference vs Węgrzynowicz) | **0.02654** | group, subspecies shared |

The smallest offset of all 36 spans two continents. One of the largest is
between deposits sharing all three subspecies but measured by different
groups. Every one of the eight largest involves the single deposit measured by
another group.

The compatibility audit found one deposit of nine using a different landmark
numbering and two needing reflection — silent failures that produce Procrustes
distances near the theoretical maximum with no error raised.

```text

```text

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
