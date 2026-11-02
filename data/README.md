# Source data

Raw data is not committed to this repository. Each file below is a published
open deposit; download it from its DOI into this directory.

## Required for the reliability analysis

| file in this directory | source | DOI |
|---|---|---|
| `raw_coordinates.xlsx` | Masaquiza & Arenal — images and coordinates of honey bee wings from the central highlands of Ecuador | 10.5281/zenodo.13340594 |
| `EC-raw-coordinates.csv` | Tofilski et al. — re-measurement of the same Masaquiza images, 19 landmarks via IdentiFly | 10.5281/zenodo.14604363 |

These two deposits contain the **same physical wings**, digitized
independently by two groups. That is what makes an inter-team error estimate
possible, and it happens only once in the public record.

## Reference configuration

| source | DOI |
|---|---|
| `Nawrocka_et_al2018.csv` and `Nawrocka_et_al2018-geo-data.csv` — 19-landmark coordinates, 1,832 workers, 187 colonies, 25 subspecies, 4 lineages, from the Morphometric Bee Data Bank, Oberursel | 10.5281/zenodo.7567336 |

## Additional deposits used in the within-colony variance analysis

| region | DOI |
|---|---|
| Europe, 13 countries | 10.5281/zenodo.7244070 |
| Northwestern Europe, 10 countries | 10.5281/zenodo.18845767 |
| Southwestern Asia | 10.5281/zenodo.17075125 |
| Jammu and Kashmir, India | 10.5281/zenodo.8071014 |
| Kazakhstan | 10.5281/zenodo.8128010 |
| Serbia — `RS_21_80-raw-coordinates.csv`, 1,065 bees with both forewings | 10.5281/zenodo.10389960 |
| Tabasco, Mexico | 10.5281/zenodo.13884732 |
| Algeria 2018 — `DZ-2018-raw-coordinates.csv`, 460 bees with **both** forewings | 10.5281/zenodo.18359322 |
| Algeria 2024 — `DZ-2024-raw-coordinates.csv`, 164 bees with both forewings | 10.5281/zenodo.13939415 |
| Algeria 2025 | 10.5281/zenodo.18360081 |
| Queens and drones | 10.5281/zenodo.8396176 |
| Africanized bees, California and Argentina — re-measurement of Calfee et al.; `US-` and `AR-raw-coordinates.csv` mix left and right wings with no bilateral pairs | 10.5281/zenodo.14604479 |
| Africanized bees — original images and ImageJ wing lengths, with individual genomic ancestry (Dryad) | 10.25338/B8T032 |

## Known crosses

| file in this directory | source | DOI |
|---|---|---|
| `oo_404830.txt` | Węgrzynowicz & Łoś — wing venation measurements for *A. m. caucasica*, *A. m. carnica* and *A. m. mellifera*, their hybrids and backcrosses: 9,590 wings, 200 queens, 24 genotypes by instrumental insemination. The only honey bee wing material with known pedigree. | 10.3897/BDJ.8.e53724 |
| `oo_404831.txt` | genotype key for the same data paper | 10.3897/BDJ.8.e53724 |

Released under a Creative Commons Zero public domain waiver.

Note on the file: eight of the twelve backcross genotypes are spelled `Bc...`
and four `BC...`. `scripts/03_known_crosses.py` normalises the case; a naive
prefix filter silently drops two thirds of the backcrosses.

## Licensing

Several deposits are released under the Open Database License v1.0, which
carries a share-alike requirement. Any derived database built from them —
including the tables in `../results/` — must be released under the same
licence, with attribution to the source deposits. Attribution is given by DOI
in this file and in the manuscript.

## Note on wing side

Three deposits hold **both forewings of the same bee** — Algeria 2018 (460
bees, complete pairing), Serbia (1,065 of 1,217 specimens) and Algeria 2024
(164). `scripts/04_paired_wings.py` uses these for an error estimate
independent of the Ecuador pair.

Their left wings were already flipped during image preparation, so no
reflection should be applied; doing so makes left-right distances about fifty
times worse. The script checks this rather than assuming it.

136 Serbia specimens carry no side marker in the filename and are excluded
from the paired analysis. The Calfee re-measurements mix left and right wings
without bilateral pairs: 73 right and 26 left for the United States, 159 right
and 18 left for Argentina.
