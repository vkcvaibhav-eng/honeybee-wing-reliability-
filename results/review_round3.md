# Step 10 - matching signature and remaining corrections

## 1. Where the disagreement sits, and what it does not depend on

Nawrocka et al. (2018) state that their landmark positions followed Gerula et al. (2009) but were changed for landmarks 7 and 14 to agree with standard morphometry (Ruttner 1988). Two published versions of the convention therefore differ at those two landmarks, and a group working to one version would disagree with a group working to the other there and almost nowhere else.

| pair set | n | share of squared displacement at LM7+LM14 | RMS LM7 | RMS LM14 | median RMS, other 17 |
|---|---|---|---|---|---|
| all 642 candidate pairs | 642 | 94.0% | 0.00840 | 0.00599 | 0.00215 |
| 608 retained (d <= 3x median) | 608 | 94.3% | 0.00732 | 0.00580 | 0.00102 |
| 34 disputed (d > 3x median) | 34 | 56.4% | 0.01934 | 0.00869 | 0.00808 |

Even division across 19 landmarks would be 10.5%. On the retained pairs the two landmarks carry 94.3% of the squared displacement, and their RMS disagreement is 6.4 times the median of the other seventeen. The landmark-map step reached the same two landmarks independently: residuals between the two mean shapes were 0.00654 at landmark 7 and 0.00567 at landmark 14, against 0.00241 or less at all seventeen others.

### What the estimate does not depend on

- mean displacement on the matching as fitted: **0.00875**
- the same quantity under 200 random re-pairings of the same wings: median **0.00875**, range 0.00875 to 0.00875

The displacement is the difference between the two grand means, so which wing is paired with which leaves it unchanged. The central estimate therefore does not rest on the matching being correct, and no claim here is made that the per-landmark profile identifies correct matches: it does not, because the profile of a mean difference is also invariant to the pairing. What does rest on the matching is the residual scatter, reported as a range in section 3.

## 2. Displacement against colony-mean distances

- colonies with 3 or more wings: **74**
- pairwise distances between their means: **2701** (not independent; each colony enters 73 of them)
- median distance between colony means: **0.01974**
- 10th percentile: **0.01459**
- mean displacement between measurement sets: **0.00875**
- ratio: **0.44**
- proportion of colony-mean distances below the displacement: **0.2%** (6 of 2701)

- colonies measured by both sets with 3+ wings: **73**
- median magnitude of their colony-specific displacement: **0.00909**
- magnitude of the mean of the colony-specific difference vectors: **0.00878** (computed from the colony vectors, not carried over from the pooled-wing figure of 0.00875)

## 2a. Total and residual disagreement

| quantity | all 642 | retained 608 |
|---|---|---|
| half mean squared total disagreement | 0.000110 | 0.000052 |
| half the squared mean displacement | 0.0000383 | 0.0000375 |
| residual after removing it | 0.0000719 | 0.0000146 |
| displacement share of the total | 34.8% | 72.0% |

Excluding the 34 reduces total disagreement by 53% and residual disagreement by 80%. These are two sensitivity scenarios, not bounds: neither establishes a mathematical limit on disagreement under an unknown true matching.

## 3. Excluding the 34 disputed matches

- half mean squared disagreement: **0.000052** (95% CI 0.000048 to 0.000056)
- mean displacement: **0.00866**, against 0.00875 on all 642
- the displacement moves by 1.1% when the 34 are removed, while the variance changes by 53%.

## 4. The two conflicting colony identifiers

Both appear under two genotype labels. The wing counts identify which entry is spurious:

| colony | genotype | wings | raw | centred |
|---|---|---|---|---|

| genotype | all entries | excluding the two |
|---|---|---|
| P0cc | 0/2 raw, 2/2 centred | 0/2 raw, 2/2 centred |
| P1cc | 0/3 raw, 2/3 centred | 0/3 raw, 2/3 centred |
| P0kk | 1/1 raw, 1/1 centred | 1/1 raw, 1/1 centred |
| P1kk | 4/4 raw, 4/4 centred | 4/4 raw, 4/4 centred |
| P0mm | 1/1 raw, 1/1 centred | 1/1 raw, 1/1 centred |
| P1mm | 6/6 raw, 6/6 centred | 6/6 raw, 6/6 centred |

The single colony that centring fails to recover, P1mm 0489_12, is represented by one wing and also appears as P1kk with 41 wings. Excluded, the centred pure-line result is 4 of 5 caucasica colonies and 12 of 12 for the other lines. The earlier statement that neither identifier is a pure parental line was wrong.
