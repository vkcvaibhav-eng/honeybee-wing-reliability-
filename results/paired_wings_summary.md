# Independent error estimate from paired left and right forewings

Three deposits digitized both forewings of the same bee. The left-right difference within a bee contains fluctuating asymmetry and within-session digitizing error together, bounding each from above. This route involves no specimen matching and no cross-dataset comparison, so it is independent of step 2.

## Reflection check

The left wings were already flipped during image preparation, so no reflection is applied here. Applying one makes left-right distances far worse, which is the check rather than an assumption.

| deposit | median L-R, as deposited | median L-R, left reflected | ratio |
|---|---|---|---|
| DZ-2018 | 0.01303 | 0.69272 | 53x worse |
| RS_21_80 | 0.01286 | 0.71247 | 55x worse |
| DZ-2024 | 0.01276 | 0.68394 | 54x worse |

## Variance decomposition

| deposit | paired bees | median L-R | among-individual | directional asymmetry | within-individual (FA + error) |
|---|---|---|---|---|---|
| DZ-2018 | 460 | 0.01303 | 0.000534 | 0.00000058 | 0.000046 |
| RS_21_80 | 1065 | 0.01286 | 0.000341 | 0.00000036 | 0.000045 |
| DZ-2024 | 164 | 0.01276 | 0.000523 | 0.00000115 | 0.000044 |

## What this gives

Across **1689 paired bees** in 3 deposits, within-individual variance is 0.000044 to 0.000046. Step 2, from two teams digitizing the same images, gives 0.000047.

Two independent methods on four deposits therefore agree to within about 5%. Neither depends on the other: step 2 rests on specimen matching across deposits, this step on bilateral pairs within one deposit. That convergence is the main reason to prefer the median-based estimator in step 2 over a mean-based one, which the outlier pairs there inflate roughly twofold.

**Directional asymmetry in shape is essentially zero** in all three deposits. That independently confirms, on this many bees, the published finding that honey bee forewing shape does not differ between body sides while size does.

**Fluctuating asymmetry cannot be separated from within-session digitizing error here.** The left-right variance contains both and is indistinguishable from the step 2 estimate, so it is an upper bound on each. Separating them needs repeated digitization of the same wing, which in the public record exists only for the Ecuador pair — and those deposits hold no bilateral pairs.
