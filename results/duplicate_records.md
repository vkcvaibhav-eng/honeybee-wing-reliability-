# Step 12 - duplicate records in the Ecuadorian deposit

The coordinate file holds **663** wing records across **69** source images and **15** apiaries. Of those records, **10** are byte-identical copies of another record.

| duplicate of | record | apiary | image |
|---|---|---|---|
| 198 | 199 | Apiary 13 | R2C2.tif |
| 491 | 535 | Apiary 6 | JSC1.tif |
| 492 | 536 | Apiary 6 | JSC1.tif |
| 493 | 537 | Apiary 6 | JSC1.tif |
| 494 | 538 | Apiary 6 | JSC1.tif |
| 495 | 539 | Apiary 6 | JSC1.tif |
| 496 | 540 | Apiary 6 | JSC1.tif |
| 497 | 541 | Apiary 6 | JSC1.tif |
| 498 | 542 | Apiary 6 | JSC1.tif |
| 499 | 543 | Apiary 6 | JSC1.tif |

Every duplicate lies within the same image and the same apiary as its original: **True**. No record is shared between apiaries, so comparisons between colonies cannot be contaminated by them.

## Effect on the reported estimates

| quantity | as published (663) | duplicates removed (653) |
|---|---|---|
| matched candidate pairs | 642 | 632 |
| median Procrustes distance | 0.00964 | 0.00960 |
| pairs above three times the median | 34 | 28 |
| mean displacement | 0.00875 | 0.00875 |
| half mean squared disagreement, all pairs | 0.000110 | 0.000105 |
| half mean squared disagreement, retained | 0.000052 | 0.000050 |

Removing the duplicates accounts for 6 of the 34 large discrepancies, because two identical records compete for distinct partners and one of them is necessarily matched to the wrong wing. The mean displacement is unchanged at 0.00875. The analysis reported in the manuscript uses the deposit as published, so that it reproduces from the deposited file; this is the sensitivity check.
