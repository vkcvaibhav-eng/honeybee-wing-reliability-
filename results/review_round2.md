# Statistics for the second review round

## 1. Between-measurement disagreement, stated as such

| quantity | value | 95% interval |
|---|---|---|
| algorithmically matched candidate pairs | 642 | |
| centroid-size correlation on those pairs | 1.0000 | |
| median Procrustes distance | 0.00964 | |
| median excluding the 34 largest discrepancies | 0.00952 | |
| half mean squared disagreement | 0.000110 | 0.000074 to 0.000155 |
| **mean displacement between the two sets** | **0.00875** | **0.00844 to 0.00916** |
| residual after removing that displacement | 0.000072 | |
| displacement share of half mean squared disagreement | 34.8% | |

This is disagreement between two measurement sets, not the error of either about a truth, which is unobservable here. The residual is not demonstrably independent noise: it may contain specimen-dependent bias, colony effects, or incorrect matches.

The median excluding the 34 largest discrepancies is 0.00952. The revised draft gave 0.00911, which was stale.

## 2. The displacement against the signal it must not swamp

The previous draft divided a squared displacement by among-colony variance and called the result a share of variance remaining in a colony mean. That is a category error: a constant displacement moves every colony mean together and creates no variation among colonies measured by one observer. The defensible comparison is of the displacement against the distances it must not overwhelm.

| quantity | value |
|---|---|
| mean displacement between measurement sets | 0.00875 (0.00844 to 0.00916) |
| median distance between colony means in this dataset | 0.01974 |
| 10th percentile of those distances | 0.01459 |
| **displacement as a fraction of the median colony separation** | **0.44** |
| colonies measured by both sets (73 with 3+ wings), median displacement of their means | 0.00909 |

The displacement is 0.44 times the typical distance between colony means, and exceeds the closest decile of colony pairs outright. Computed directly on the colony means measured by both sets, with their actual sample sizes, it is 0.00909, close to the pooled figure, which is what a constant displacement predicts. Averaging more wings per colony does not reduce it.

No percentage of among-colony variance is claimed.

## 3. Alignment with the ancestry direction, against a permutation benchmark

| benchmark for random directions in 34 dimensions | value |
|---|---|
| 1/sqrt(34), the root-mean-square cosine | 0.171 |
| mean absolute cosine | 0.138 |
| **median absolute cosine** | **0.118** |
| 95th percentile | 0.334 |
| observed median across 36 dataset pairs | 0.237 |

The revised draft compared the observed median of 0.237 against 0.171, which is the root-mean-square cosine and not the expected median. The correct median benchmark is 0.118. The observed median is about twice that, but it sits below the 95th percentile of 0.334, so no individual dataset difference is significantly aligned with the ancestry direction. The comparison supports projection as a necessary step and supports no claim that the differences are ancestry-like.

## 4. The transfer result, with its denominator

The external result rests on **5 colonies** of known pure *A. m. caucasica*, not on the 9,590 wings of the cross dataset. The other pure lines were assigned correctly without adjustment, so they contribute no evidence of failure.

| principal components | reference accuracy | pure caucasica correct, uncorrected | centred |
|---|---|---|---|
| 6 | 41/41 | 0/5 | 2/5 |
| 8 | 41/41 | 1/5 | 4/5 |
| 10 | 41/41 | 0/5 | 4/5 |
| 12 | 41/41 | 0/5 | 4/5 |
| 16 | 41/41 | 1/5 | 4/5 |
| 20 | 41/41 | 0/5 | 3/5 |

The failure of uncorrected transfer on these colonies is insensitive to the number of principal components across this range, and the reference's own accuracy is not. Reference accuracy of 41 of 41 does not establish that the model is well specified, only that these three subspecies are separable within that collection.

## 5. Full backcross counts

The backcrosses comprise **98** genotype-colony groups across twelve genotypes, not 101 as the revised draft stated.

| genotype | majority subspecies | colonies | carnica | caucasia | mellifera |
|---|---|---|---|---|---|
| BCckc | caucasia | 10 | 5 | 3 | 2 |
| BCckk | carnica | 6 | 6 | 0 | 0 |
| BCcmc | caucasia | 8 | 4 | 4 | 0 |
| BCcmm | mellifera | 5 | 0 | 1 | 4 |
| BCkcc | caucasia | 5 | 1 | 4 | 0 |
| BCkck | carnica | 6 | 6 | 0 | 0 |
| BCkmk | carnica | 16 | 12 | 0 | 4 |
| BCkmm | mellifera | 19 | 0 | 0 | 19 |
| BCmcc | caucasia | 4 | 1 | 3 | 0 |
| BCmcm | mellifera | 10 | 1 | 4 | 5 |
| BCmkk | carnica | 4 | 4 | 0 | 0 |
| BCmkm | mellifera | 5 | 1 | 0 | 4 |

The cross dataset yields 198 genotype-colony groups from 198 distinct colony identifiers; 0 identifiers appear under more than one genotype label . The two identifiers found earlier, 0489_12 (P1kk, P1mm) and 0203_13 (P1mm, BCkmk), are now excluded in step 3 before the centring offset is fitted, so none remain here. Refitting with them excluded changed no assignment relative to removing them from the results afterwards, and moved the cross-dataset offset from 0.02470 to 0.02475.

## 6. Figures

- **Fig. 1** Distribution of Procrustes distances between the two measurements of each candidate pair, with the median and the three-times-median cut marked.

- **Fig. 2** The displacement between measurement sets against the distribution of distances between colony means in the same dataset, with the bootstrap interval shaded.

- **Fig. 3** Assignment of cross-dataset colonies after centring, by genotype group, with counts.

Matched-image overlays could not be produced: the deposits' image archives were not available to this analysis, and auditing the disputed pairs against the images remains outstanding.
