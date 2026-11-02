# Deposit offsets expressed as apparent African ancestry

268 wings join the landmark re-measurement to Calfee et al.'s sequenced metadata on the image filename. Ancestry spans A = 0.00 to 0.79.

## The ancestry axis

| quantity | value |
|---|---|
| shape change per unit A ancestry | 0.02252 Procrustes units |
| shape variance explained by measured A | 5.7% |
| rate within California (96 bees) | 0.02732 |
| rate within Argentina (172 bees) | 0.02102 |

Measured ancestry explains 5.7% of shape variation, so wing shape tracks sequenced ancestry but most shape variation is something else. 
The rate is similar on the two transects (ratio 1.30), measured in one batch by one group.

## Are the offsets aligned with the ancestry axis?

| quantity | value |
|---|---|
| median absolute cosine, 36 deposit pairs | 0.237 |
| expected by chance in 34 dimensions | 0.171 |
| range | 0.016 - 0.889 |

Mostly not aligned — barely above chance. The exception validates the axis: the most aligned pair of all 36 is **Calfee USA (re-m.) vs Calfee Arg. (re-m.)** at 0.889, and those are the two transects that genuinely differ in African ancestry.

Because alignment is weak, an offset's full length must be projected onto the ancestry axis before conversion. Using the unprojected length would give a median of 87% instead of 21%, overstating it 4.1-fold.

## The controls, converted

| control | offset | alignment | apparent difference in A ancestry |
|---|---|---|---|
| same wings, two groups: pure method | 0.00891 | 0.216 | **9%** |
| two continents, one group and batch | 0.00780 | 0.889 | **31%** |
| one group and region, two collection years | 0.01256 | 0.337 | **19%** |
| overlapping subspecies, two groups | 0.02654 | 0.199 | **23%** |
| largest offset in the matrix | 0.03410 | 0.254 | **38%** |

Across all 36 pairs the median is **21%** and the largest **73%**.

Read the first two rows together. The same physical wings landmarked by two groups imitate a 9% difference in African ancestry, from landmarking alone. The genuine ancestry difference between the Californian and Argentine hybrid zones registers as 31%. And a typical pair of deposits, differing by method and population together, imitates 21%.

**So a methodological offset between deposits can imitate an apparent ancestry difference of the same order as the real difference between two continents' hybrid zones.** That is the practical cost of comparing deposits without correcting the offset.

Two cautions. The rate is estimated inside two hybrid zones and need not hold in the native range. And these are apparent-ancestry equivalents for interpreting the offsets, not ancestry estimates for any deposit.

## Size: a concordance check, and a data-completeness problem

ImageJ wing length by one group against Procrustes centroid size by another, on the same 268 wings.

| scope | correlation |
|---|---|
| all wings pooled | **0.497** |
| imaging session 05-30-19 (71 wings) | 0.789 |
| imaging session 05-01-19 (40 wings) | 0.854 |
| imaging session 05-15-19 (36 wings) | 0.676 |
| imaging session 03-14-19 (33 wings) | 0.692 |
| imaging session 02-15-19 (23 wings) | 0.865 |
| imaging session 01-25-20 (19 wings) | 0.912 |
| median within session | **0.821** |

Pooled, the correlation is 0.50; within an imaging session it is 0.82. **The deposit records no image resolution**, so centroid size is in pixels and the scale differs between sessions. Anyone wanting real size from these landmark coordinates cannot recover it, and pooling sessions destroys the signal.

This is therefore not a fifth estimate of measurement error. ImageJ tip-to-base length and the centroid size of 19 landmarks are different quantities, so even perfect measurement would not give r = 1. It is reported as a concordance, and as a caution about that deposit.
