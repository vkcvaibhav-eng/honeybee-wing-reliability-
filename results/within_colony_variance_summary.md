# Is within-colony shape variance comparable across deposits?

Every Wegrzynowicz colony was inseminated with semen from one drone, so its workers share a father. Serbian and Algerian queens mated naturally with many. Single-drone colonies should therefore show **less** within-colony variance.

| deposit | mating | colonies | bees per colony | raw variance | error floor | corrected |
|---|---|---|---|---|---|---|
| Serbia | natural | 60 | 20.3 | 0.000273 | 0.000023 | 0.000250 |
| Algeria 2018 | natural | 46 | 10.0 | 0.000425 | 0.000023 | 0.000402 |
| Wegrzynowicz | single-drone | 201 | 47.7 | 0.000483 | 0.000047 | 0.000436 |

The raw column is the descriptive within-colony variance; the corrected column subtracts an error floor whose provenance differs between deposits and is reported for comparison only. The raw values are the ones quoted in the manuscript.

## The prediction fails, in the opposite direction

| group | colonies | median | 25th-75th percentile |
|---|---|---|---|
| naturally mated | 106 | 0.000291 | 0.000239 - 0.000385 |
| single-drone | 201 | 0.000436 | 0.000375 - 0.000511 |

Mann-Whitney, naturally mated greater than single-drone: **p = 1**. Single-drone colonies are the *most* variable of the three deposits, which is biologically backwards.

The clearest sign that deposit, not biology, drives this: Serbia and Algeria 2018 share a mating structure and a digitizing group, yet their median within-colony variances differ by 1.6x. No plausible difference in polyandry spans that.

## What this means

**Within a single deposit the quantity is sound.** In Serbia the error floor is only 8% of within-colony variance, so the spread there is mostly real signal and can be compared between colonies measured together.

**Across deposits it is not comparable.** Within-colony variance cannot serve as a cross-deposit index of admixture or paternal diversity, because deposit-specific effects exceed the biological signal it would have to detect.

This completes the picture from step 3. Cross-deposit comparison fails for **location** — the offset between deposit means matches the difference between subspecies — and it fails for **scale** — within-colony variances differ by more than mating structure can explain. Within one deposit, both quantities behave.

A caveat on what is not shown: the Wegrzynowicz deposit has no replicate or bilateral wings, so its own measurement error is unknown and may be larger than the floor subtracted here. That would explain its high variance without any biology, and these data cannot distinguish the two.
