# Reference transfer and assignment of known crosses

Reference colonies: {'carnica': 15, 'mellifera': 14, 'caucasia': 12}  
Cross dataset: 9590 wings, 202 colonies, 24 genotypes

## Reference internal accuracy

Leave-one-colony-out: **41/41 (100.0%)**. The reference separates its own subspecies cleanly, so anything that follows is about transfer, not about the classifier.

## The cross-dataset offset

| quantity | value |
|---|---|
| offset between dataset grand means | **0.02470** |
| reference carnica to caucasia | 0.03216 |
| reference carnica to mellifera | 0.02831 |
| reference caucasia to mellifera | 0.01941 |
| inter-team digitization error (step 2, Ecuador) | 0.00964 |

The offset sits inside the range of between-subspecies distances (0.01941 to 0.03216), and is 2.6 times the inter-team digitization error measured on the same images in step 2. Landmarking alone therefore does not account for it.

## Do the two datasets agree on how subspecies differ?

| contrast | reference | crosses | cosine |
|---|---|---|---|
| carnica to caucasia | 0.03216 | 0.01560 | 0.707 |
| carnica to mellifera | 0.02831 | 0.02136 | 0.662 |
| caucasia to mellifera | 0.01941 | 0.01756 | 0.116 |

Mean cosine **0.495**. Agreement is partial, and the cross dataset is less differentiated than the wild reference. So this is not a pure measurement offset: a measurement difference and genuine divergence of selected breeding lines are confounded here, and these data cannot separate them.

## Known-pure parental lines

Correct assignment of these is not in doubt, so they test transfer.

| genotype | expected | colonies | raw | offset-corrected |
|---|---|---|---|---|
| P0cc | caucasia (O) | 2 | C:2 — 0% | O:2 — 100% |
| P1cc | caucasia (O) | 3 | M:2 C:1 — 0% | O:2 M:1 — 67% |
| P0kk | carnica (C) | 1 | C:1 — 100% | C:1 — 100% |
| P1kk | carnica (C) | 5 | C:5 — 100% | C:5 — 100% |
| P0mm | mellifera (M) | 1 | M:1 — 100% | M:1 — 100% |
| P1mm | mellifera (M) | 8 | M:8 — 100% | M:7 O:1 — 88% |

Raw transfer misassigns known-pure caucasica entirely. The correction recovers it. Note also that a raw 'correct' call can rest on a margin far below the offset, so it carries no evidential weight.

## Reciprocal F1 pairs (offset-corrected)

Identical nuclear composition, opposite parental direction.

| genotype | queen | drone | colonies | assignment |
|---|---|---|---|---|
| F1ck | caucasia | carnica | 14 | C:10 O:3 M:1 |
| F1kc | carnica | caucasia | 17 | O:9 C:8 |
| F1cm | caucasia | mellifera | 10 | O:7 C:2 M:1 |
| F1mc | mellifera | caucasia | 12 | C:4 M:4 O:4 |
| F1km | carnica | mellifera | 18 | M:18 |
| F1mk | mellifera | carnica | 12 | M:8 C:4 |

Across **83 F1 colonies**: 36.1% assigned to the queen's subspecies, 55.4% to the drone's, 8.4% to a third. Two of the three reciprocal pairs are assigned to different subspecies despite identical composition, so **assignment of a known F1 is not predictable from parentage**. The lean toward the drone's subspecies follows from which subspecies pairs exist, not from a paternal effect.

## Backcrosses, 3:1 composition (offset-corrected)

| genotype | majority subspecies | colonies | assignment | matches majority |
|---|---|---|---|---|
| BCckc | caucasia | 10 | C:5 O:3 M:2 | 30% |
| BCckk | carnica | 6 | C:6 | 100% |
| BCcmc | caucasia | 8 | C:4 O:4 | 50% |
| BCcmm | mellifera | 5 | M:4 O:1 | 80% |
| BCkcc | caucasia | 5 | O:4 C:1 | 80% |
| BCkck | carnica | 6 | C:6 | 100% |
| BCkmk | carnica | 17 | C:13 M:4 | 76% |
| BCkmm | mellifera | 19 | M:19 | 100% |
| BCmcc | caucasia | 4 | O:3 C:1 | 75% |
| BCmcm | mellifera | 10 | M:5 O:4 C:1 | 50% |
| BCmkk | carnica | 4 | C:4 | 100% |
| BCmkm | mellifera | 5 | M:4 C:1 | 80% |

Median across the twelve backcross genotypes: **80%**. Skewed composition is usually recovered, but not dependably.
