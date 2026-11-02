# Corrected estimates

These figures replace those in steps 2, 4, 5 and 7 of this repository and in the first manuscript draft. The errors corrected are listed in the header of `08_corrected_estimates.py`.

One convention throughout: the variance of a single measurement about the truth is E[d^2]/2, with d the Procrustes distance between two measurements of the same specimen. Intervals are bootstrap percentile intervals over 2000 resamples of colonies where colony structure is recoverable, otherwise of specimens.

## 1. Two groups digitizing the same images (Ecuador)

642 wings matched one-to-one on translation-invariant centroid size and shape, out of 663 and 726 records. All figures below use these pairs only.

| quantity | all matched pairs | excluding 34 largest discrepancies |
|---|---|---|
| pairs | 642 | 608 |
| median Procrustes distance | 0.00964 | 0.00952 |
| total per-measurement variance | 0.000110 | 0.000052 |
| 95% interval | 0.000075 to 0.000154 | 0.000049 to 0.000056 |
| systematic displacement between groups | 0.00875 | 0.00866 |
| random component of variance | 0.000072 | 0.000015 |
| systematic share of total variance | 34.8% | 72.0% |

Excluding the 34 largest discrepancies lowers the variance by a factor of 2.1. Those pairs were not confirmed against the images, so both columns are reported and the reader may choose. The lower figure is not preferred here.

**The systematic component does not average away.** The two groups differ by a constant displacement of 0.00875 Procrustes units, which is 35% of the total variance between them. Averaging more wings per colony shrinks the random part and leaves this untouched, so the claim in the first draft that colony averaging reduces digitization error to 2.3% of among-colony variance was wrong in kind, not only in size.

### What this means for colony means

| quantity | variance | share of among-colony variance |
|---|---|---|
| total shape variance of the deposit | 0.000624 | |
| within-colony variance | 0.000417 | |
| among-colony variance | 0.000208 | |
| per-measurement error, all pairs | 0.000110 | 53% |
| random part after averaging 9.8 wings | 0.000007 | 3.5% |
| systematic part, unchanged by averaging | 0.000038 | 18.4% |
| **error in a colony mean** | **0.000046** | **22%** |

Error as a share of total shape variance is 17.7% with all matched pairs and 8.3% excluding the 34 unconfirmed discrepancies. The first draft reported 7.5%, which came from the median-based estimator adopted to match the mis-scaled bilateral figure.

The practical consequence is the opposite of the first draft's. Averaging 9.8 wings per colony reduces the random component to 3.5% of among-colony variance, but the systematic displacement contributes 18% whatever the sample size. Colony averaging therefore leaves about 22% of among-colony variance as between-group measurement displacement, not the 2.3% claimed before. This is a mechanism for the misassignment of known pure lines reported in step 3.

Offset between the two groups' grand means on these pairs: **0.00875**. The first draft reported 0.00891, computed from the means of the unequal full record sets.

## 2. Left and right forewings of the same bee

Under the same convention as section 1. This estimates a different quantity: it contains fluctuating asymmetry as well as within-session digitizing error, so it bounds each from above and is not a replicate of section 1.

| deposit | bees | median L-R distance | variance | 95% interval | systematic (directional asymmetry) |
|---|---|---|---|---|---|
| Algeria 2018 | 460 | 0.01303 | 0.000091 | 0.000087 to 0.000095 | 0.00153 |
| Serbia | 1065 | 0.01286 | 0.000089 | 0.000087 to 0.000092 | 0.00120 |
| Algeria 2024 | 164 | 0.01276 | 0.000089 | 0.000081 to 0.000095 | 0.00214 |

The bilateral estimates run 0.000089 to 0.000091, against 0.000110 (0.000075 to 0.000154) for two groups on the same images. These are consistent in order of magnitude and are **not** presented as agreeing: they measure different components, and the first draft's claim of agreement to 5% rested on the scaling error named in the header.

Directional asymmetry is near zero in all three deposits, confirming on 1,689 bees that forewing shape does not differ between body sides.

## 3. Within-reference split-half baseline

200 random splits of the 41 reference colonies of the three subspecies into halves, offsets between half means:

- median **0.00559**, 2.5th to 97.5th percentile 0.00316 to 0.01064

The first draft quoted 0.00550 from an uncommitted script. The value is reproduced here with its procedure and spread.

## 4. Assignment of known crosses, all counts

The first draft reported a single modal class per genotype, which hid ties. F1mc was reported as *carnica* when the counts are an exact three-way tie, and the accompanying text wrongly said it was assigned to neither parent when eight of twelve colonies went to a parent.

| genotype | queen | drone | colonies | carnica | caucasia | mellifera | to queen | to drone |
|---|---|---|---|---|---|---|---|---|
| BCckc | caucasia | caucasia | 10 | 5 | 3 | 2 | 3 | 3 |
| BCckk | caucasia | carnica | 6 | 6 | 0 | 0 | 0 | 6 |
| BCcmc | caucasia | caucasia | 8 | 4 | 4 | 0 | 4 | 4 |
| BCcmm | caucasia | mellifera | 5 | 0 | 1 | 4 | 1 | 4 |
| BCkcc | carnica | caucasia | 5 | 1 | 4 | 0 | 1 | 4 |
| BCkck | carnica | carnica | 6 | 6 | 0 | 0 | 6 | 6 |
| BCkmk | carnica | carnica | 17 | 13 | 0 | 4 | 13 | 13 |
| BCkmm | carnica | mellifera | 19 | 0 | 0 | 19 | 0 | 19 |
| BCmcc | mellifera | caucasia | 4 | 1 | 3 | 0 | 0 | 3 |
| BCmcm | mellifera | mellifera | 10 | 1 | 4 | 5 | 5 | 5 |
| BCmkk | mellifera | carnica | 4 | 4 | 0 | 0 | 0 | 4 |
| BCmkm | mellifera | mellifera | 5 | 1 | 0 | 4 | 4 | 4 |
| F1ck | caucasia | carnica | 14 | 10 | 3 | 1 | 3 | 10 |
| F1cm | caucasia | mellifera | 10 | 2 | 7 | 1 | 7 | 1 |
| F1kc | carnica | caucasia | 17 | 8 | 9 | 0 | 8 | 9 |
| F1km | carnica | mellifera | 18 | 0 | 0 | 18 | 0 | 18 |
| F1mc | mellifera | caucasia | 12 | 4 | 4 | 4 | 4 | 4 |
| F1mk | mellifera | carnica | 12 | 4 | 0 | 8 | 8 | 4 |
| P0cc | caucasia | caucasia | 2 | 0 | 2 | 0 | 2 | 2 |
| P0kk | carnica | carnica | 1 | 1 | 0 | 0 | 1 | 1 |
| P0mm | mellifera | mellifera | 1 | 0 | 0 | 1 | 1 | 1 |
| P1cc | caucasia | caucasia | 3 | 0 | 2 | 1 | 2 | 2 |
| P1kk | carnica | carnica | 5 | 5 | 0 | 0 | 5 | 5 |
| P1mm | mellifera | mellifera | 8 | 0 | 1 | 7 | 7 | 7 |

Across 83 F1 colonies, 30 (36.1%) were assigned to the queen's subspecies and 46 (55.4%) to the drone's. Reciprocal pairs of identical expected composition were assigned differently, but reciprocal crosses do not have identical nuclear genotypes: different parental individuals, maternal effects and cytoplasmic inheritance all remain in play. The result is reported as a limitation of forcing hybrids into pure classes, not as evidence about parental direction.

## 5. Measured ancestry against shape-derived equivalents

| quantity | value |
|---|---|
| mean African ancestry, California (96 bees) | 20.33% |
| mean African ancestry, Argentina (172 bees) | 40.74% |
| **measured** difference | **20.4 percentage points** |
| shape-derived equivalent for the same pair | 31% |
| shape variance explained by measured ancestry | 5.7% |

The first draft called the 31% figure the real difference between the two hybrid zones. It is not: the measured difference is 20.4 percentage points, and 31% is what the shape projection returns for that pair. The projection therefore overstates a known difference by about 52%, which is a calibration check the scale partly fails. All ancestry equivalents are exploratory and are retained only as a rough scale for the offsets.

## 6. Bookkeeping corrections

- Of the eight largest offsets, **6** involve the single deposit measured by another group, not all eight as the first draft stated.

- The cross dataset yields 200 distinct colony identifiers across 202 genotype-colony groups; 2 identifiers appear under more than one genotype label, which accounts for the discrepancy against the 200 queens reported in the source data paper. Affected identifiers: 0203_13, 0489_12.

- The nine analytical datasets derive from seven sources, and from fewer independent biological samples: the Ecuador wings appear twice, as the same specimens measured by two groups, and the two Calfee sets are regional subsets of one collection. Counts of deposits should not be read as counts of independent samples.

- Landmarks 7 and 14 carried the largest between-group disagreement. This is **not** reported as unreliability. Nawrocka et al. describe altering the positions of two landmarks relative to an earlier convention, so a computational renumbering does not establish anatomical equivalence, and a convention difference would produce exactly this pattern. Resolving it requires the definitions used by each source, with annotated images.
