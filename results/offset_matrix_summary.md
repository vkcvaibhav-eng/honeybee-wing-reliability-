# Pairwise offsets between deposits

Every deposit is checked for landmark numbering and handedness against the Oberursel reference, then all are placed in one Procrustes frame and the distance between each pair of grand means is reported. Where a bee contributed both forewings they are averaged first, so no bee is counted twice.

## Compatibility audit

| deposit | bees | reflection needed | landmarks remapped |
|---|---|---|---|
| Nawrocka reference | 1832 | no | 0 |
| Ecuador (re-meas.) | 726 | no | 0 |
| Serbia | 1217 | no | 0 |
| Algeria 2018 | 460 | no | 0 |
| Algeria 2024 | 165 | no | 0 |
| Calfee USA (re-m.) | 99 | no | 0 |
| Calfee Arg. (re-m.) | 177 | no | 0 |
| Masaquiza original | 663 | yes | 18 |
| Wegrzynowicz | 9590 | yes | 0 |

One of the nine uses a different landmark numbering. Pooling it uncorrected produces Procrustes distances near the theoretical maximum of 1.41 and raises no error, so this check is not optional.

## Offsets by how much the deposits share

| comparison | pairs | median offset | range |
|---|---|---|---|
| same group, same region | 1 | 0.01256 | 0.01256 - 0.01256 |
| same group, other region | 20 | 0.01711 | 0.00780 - 0.02458 |
| different group | 15 | 0.02398 | 0.00891 - 0.03451 |

For scale, the reference's own between-subspecies distances run 0.01941 to 0.03216, and its random colony split-halves give 0.00550.

## Every pair

| deposit A | deposit B | offset | comparison |
|---|---|---|---|
| Calfee USA (re-m.) | Calfee Arg. (re-m.) | 0.00780 | same group, other region |
| Ecuador (re-meas.) | Masaquiza original | 0.00891 | different group |
| Nawrocka reference | Calfee Arg. (re-m.) | 0.00978 | same group, other region |
| Algeria 2018 | Algeria 2024 | 0.01256 | same group, same region |
| Algeria 2018 | Calfee Arg. (re-m.) | 0.01259 | same group, other region |
| Nawrocka reference | Algeria 2018 | 0.01286 | same group, other region |
| Serbia | Calfee USA (re-m.) | 0.01295 | same group, other region |
| Nawrocka reference | Calfee USA (re-m.) | 0.01377 | same group, other region |
| Nawrocka reference | Ecuador (re-meas.) | 0.01406 | same group, other region |
| Algeria 2018 | Calfee USA (re-m.) | 0.01521 | same group, other region |
| Nawrocka reference | Algeria 2024 | 0.01657 | same group, other region |
| Algeria 2024 | Calfee Arg. (re-m.) | 0.01682 | same group, other region |
| Serbia | Calfee Arg. (re-m.) | 0.01740 | same group, other region |
| Ecuador (re-meas.) | Algeria 2018 | 0.01767 | same group, other region |
| Nawrocka reference | Masaquiza original | 0.01827 | different group |
| Ecuador (re-meas.) | Calfee Arg. (re-m.) | 0.01860 | same group, other region |
| Masaquiza original | Wegrzynowicz | 0.01879 | different group |
| Ecuador (re-meas.) | Calfee USA (re-m.) | 0.01947 | same group, other region |
| Nawrocka reference | Serbia | 0.01966 | same group, other region |
| Serbia | Algeria 2018 | 0.02049 | same group, other region |
| Algeria 2024 | Calfee USA (re-m.) | 0.02088 | same group, other region |
| Algeria 2018 | Masaquiza original | 0.02132 | different group |
| Ecuador (re-meas.) | Algeria 2024 | 0.02152 | same group, other region |
| Ecuador (re-meas.) | Wegrzynowicz | 0.02193 | different group |
| Ecuador (re-meas.) | Serbia | 0.02274 | same group, other region |
| Calfee Arg. (re-m.) | Masaquiza original | 0.02275 | different group |
| Algeria 2024 | Masaquiza original | 0.02351 | different group |
| Calfee USA (re-m.) | Masaquiza original | 0.02398 | different group |
| Serbia | Algeria 2024 | 0.02458 | same group, other region |
| Serbia | Masaquiza original | 0.02636 | different group |
| Nawrocka reference | Wegrzynowicz | 0.02654 | different group |
| Algeria 2018 | Wegrzynowicz | 0.02950 | different group |
| Algeria 2024 | Wegrzynowicz | 0.03044 | different group |
| Calfee Arg. (re-m.) | Wegrzynowicz | 0.03312 | different group |
| Serbia | Wegrzynowicz | 0.03410 | different group |
| Calfee USA (re-m.) | Wegrzynowicz | 0.03451 | different group |

## What the structure shows

Offsets grow as deposits share less: 0.01256 within one group and region, 0.01711 for the same group elsewhere, 0.02398 across groups. The last of these falls inside the between-subspecies range the method exists to resolve.

## Four controls that separate method from biology

| control | deposits | offset | what varies |
|---|---|---|---|
| same wings, two groups | Ecuador re-measurement vs Masaquiza original | **0.00891** | digitizing only; biology identical |
| two continents, one group and batch | Calfee California vs Argentina | **0.00780** | geography only |
| one group, one region, two collection years | Algeria 2018 vs 2024 | **0.01256** | collection and preparation |
| overlapping subspecies, two groups | Oberursel reference vs Wegrzynowicz | **0.02654** | group, with subspecies shared |

The first is pure method: the same physical wings landmarked by two groups. It is the second smallest offset in the whole matrix, so landmarking alone accounts for about a quarter of the largest cross-group figures.

The second is the smallest offset of all 36, and it spans two continents. The fourth is among the largest, and the two deposits there share all three subspecies, since the Oberursel reference contains carnica, caucasia and mellifera. Taken together: **the digitizing group matters more than geography or biology.**

Every one of the eight largest offsets in the matrix involves the one deposit measured by a different group.

Region and digitizing group are confounded in the public record: no two groups have measured the same population, apart from the Ecuador pair used in step 2. So these offsets are total divergence, not pure method error, and only the split-half baseline is purely sampling and measurement. The ordering is still informative, and the Ecuador pair shows that landmarking alone accounts for well under half of the cross-group figure.
