# Inter-team digitization error, Ecuador honey bee forewings

Wings matched one-to-one with near-certain identity: **642**  
Centroid-size correlation between teams: **r = 1.0000**

## Procrustes distance between teams on the same wing

| statistic | value |
|---|---|
| median | 0.00964 |
| 25th-75th percentile | 0.00819 - 0.01123 |
| 90th percentile | 0.01335 |
| maximum | 0.13413 |

## Error variance estimators

34 of 642 pairs lie above three times the median distance, with a maximum of 0.13413. That is beyond plausible landmarking disagreement and indicates a failed match, so the median-based estimator is used as the headline.

| estimator | error variance |
|---|---|
| median-based (**used**) | **0.000047** |
| 5% trimmed mean of d^2 | 0.000053 |
| mean of d^2 (outlier-inflated) | 0.000110 |

## Variance components

| component | variance |
|---|---|
| total shape | 0.000624 |
| within colony | 0.000417 |
| among colony | 0.000208 |
| digitization error | 0.000047 |

## Error as a share of each denominator

| denominator | error share |
|---|---|
| total shape variance | 7.5% |
| within-colony variance | 11.2% |
| among-colony variance | 22.3% |
| among-colony variance, after averaging 9.8 wings per colony | 2.3% |

Within-colony variance that is real signal rather than digitizing noise: **88.8%**

## Reading these numbers

Colony-mean analyses are protected by averaging, so reference-based 
assignment is largely unaffected. Analyses that use the spread of 
wings within a colony are not protected, and must subtract the error 
variance of 0.000047 before interpretation.

These shares are an upper bound. The denominator here is variance 
within a single population, so for comparisons spanning evolutionary 
lineages the same absolute error is a much smaller fraction.

This is one pair of teams on one set of images. It is the only such 
pair in the public record, which makes it informative, but it does 
not license a general claim about cross-dataset comparison.
