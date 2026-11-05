#!/usr/bin/env python3
"""Build the Journal of Apicultural Research submission.

Journal requirements applied: Original Research Article under 9000 words
including tables, references and figure captions; at most six display items;
order Abstract, Introduction, Materials and Methods, Results, Discussion,
Conclusions; non-structured abstract under 250 words; 5-8 keywords;
continuous line numbering; figures and tables placed within the text;
declarations including generative AI use.
"""
import csv
import os
from collections import Counter

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

OUT = "/home/claude/Chaudhari_Pastagia_JAR.docx"
REPO = "/home/claude/honeybee-wing-reliability-"
FIGS = os.path.join(REPO, "figures_jar")
RES = os.path.join(REPO, "results")

# --------------------------------------------------------------- document
doc = Document()
sec = doc.sections[0]
sec.top_margin = sec.bottom_margin = Cm(2.5)
sec.left_margin = sec.right_margin = Cm(2.5)
ln = OxmlElement("w:lnNumType")
ln.set(qn("w:countBy"), "1")
ln.set(qn("w:restart"), "continuous")
ln.set(qn("w:distance"), "360")
sec._sectPr.append(ln)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.paragraph_format.line_spacing = 2.0
st.paragraph_format.space_after = Pt(0)

I = {"i": True}
B = {"b": True}
N = {}


def para(t="", align=None, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = bold
    if align is not None:
        p.alignment = align
    return p


def rich(parts, align=None):
    p = doc.add_paragraph()
    for t, f in parts:
        r = p.add_run(t)
        r.bold = f.get("b", False)
        r.italic = f.get("i", False)
    if align is not None:
        p.alignment = align
    return p


def h(level, t):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = True
    r.font.size = Pt(13 if level == 1 else 12)
    r.italic = (level == 2)
    return p


def br():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def table(label, caption, hdr, rows):
    para()
    rich([(label + ". ", B), (caption, N)])
    t = doc.add_table(rows=1, cols=len(hdr))
    t.style = "Table Grid"
    for j, cell in enumerate(hdr):
        p = t.rows[0].cells[j].paragraphs[0]
        r = p.add_run(cell)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        p.paragraph_format.line_spacing = 1.0
    for row in rows:
        cs = t.add_row().cells
        for j, v in enumerate(row):
            p = cs[j].paragraphs[0]
            r = p.add_run(str(v))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            p.paragraph_format.line_spacing = 1.0
    para()


def figure(n, caption):
    para()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(FIGS, f"Figure{n}.jpg"), width=Cm(15))
    rich([(f"Figure {n}. ", B), (caption, N)])
    para()


# ------------------------------------------------- genotype counts from data
rows_kc = list(csv.DictReader(
    open(os.path.join(RES, "known_crosses_assignments.csv"))))
EXP = {"cc": "caucasia", "kk": "carnica", "mm": "mellifera"}
PURE = []
for g in ("P0cc", "P1cc", "P0kk", "P1kk", "P0mm", "P1mm"):
    s = [x for x in rows_kc if x["genotype"] == g]
    e = EXP[g[2:]]
    PURE.append([
        g,
        {"cc": "caucasica", "kk": "carnica", "mm": "mellifera"}[g[2:]],
        str(len(s)),
        f"{sum(1 for x in s if x['assigned_raw'] == e)}/{len(s)}",
        f"{sum(1 for x in s if x['assigned_corrected'] == e)}/{len(s)}"])

# =========================================================== title page
para("Measurement disagreement concentrated at two landmarks limits the "
     "transfer of honey bee wing morphometric references",
     align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
para()
para("V. K. Chaudhari and J. J. Pastagia",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para()
para("AINP on Agricultural Acarology, Department of Entomology, N. M. "
     "College of Agriculture, Navsari Agricultural University, Navsari "
     "396450, Gujarat, India", align=WD_ALIGN_PARAGRAPH.CENTER)
para()
para("Corresponding author: V. K. Chaudhari, vkcvaibhav@gmail.com")
para("ORCID: V. K. Chaudhari https://orcid.org/0000-0001-9688-0134")
para()
para("Word count: 4,870 including tables, references and figure captions")
para("Display items: three tables and three figures")
br()

# =============================================================== abstract
h(1, "Abstract")
rich([("Wing geometric morphometrics identifies honey bee (", N),
      ("Apis mellifera", I),
      (" L.) subspecies by comparing landmark coordinates against a "
       "reference dataset, a procedure that assumes a reference produced in "
       "one laboratory applies to wings landmarked in another. That "
       "assumption has not been tested. We tested it using the only case in "
       "the public record in which two groups independently landmarked the "
       "same wing images, and asked whether any disagreement between them "
       "is spread across the configuration, as operator variation would "
       "predict, or concentrated at the two landmarks that published "
       "versions of the configuration define differently. Across 642 "
       "matched candidate pairs, landmarks 7 and 14 carried about 94% of "
       "the squared mean displacement, against roughly 10% expected under "
       "an even spread, and their disagreement was six times the median of "
       "the other seventeen. The disagreement behaved as a constant "
       "displacement rather than random scatter: 0.00875 Procrustes units "
       "(95% CI 0.00844 to 0.00916), unchanged under random re-pairing of "
       "the wings, and 0.44 times the median distance between colony means, "
       "so averaging more wings per colony does not remove it. A classifier "
       "that separated its own subspecies in 41 of 41 colonies assigned "
       "zero or one of five colonies of known pure ", N),
      ("A. m. caucasica", I),
      (" correctly when applied to a dataset produced elsewhere. One of "
       "nine deposits numbered the same landmarks in a different order "
       "without warning. We recommend that wing deposits record the "
       "landmark convention they follow, and that references be calibrated "
       "against shared specimens before transfer.", N)])
para()
rich([("Keywords: ", B),
      ("Apis mellifera", I),
      ("; geometric morphometrics; wing venation; measurement error; "
       "landmark definition; reference dataset; subspecies identification; "
       "standard methods", N)])
br()

# =========================================================== introduction
h(1, "Introduction")
para("Identification of honey bee subspecies from forewing venation is now "
     "the standard low-cost alternative to molecular markers, and its "
     "reference base is large and open. Oleksa et al. (2023) released "
     "26,481 forewing images from 1,725 samples across 13 European "
     "countries, with coordinates for 19 landmarks at vein junctions. "
     "Machlowska et al. (2025) added 17,457 wings from 1,557 colonies in "
     "nine southwestern Asian countries. Further deposits cover Kazakhstan, "
     "Serbia, Algeria, Tabasco, Ecuador, northwestern Europe and Jammu and "
     "Kashmir, all landmarked to the configuration of Nawrocka et al. "
     "(2018). These references are applied at scale: Machlowska et al. "
     "(2026) assigned 1,342 colony samples from ten countries to the four "
     "evolutionary lineages. Oleksa and Tofilski (2015) showed that wing "
     "shape and microsatellites discriminate subspecies similarly well, "
     "which is much of the reason the method is now used in place of "
     "molecular work.")
para("Every one of these applications rests on an assumption that is rarely "
     "stated. A reference dataset is landmarked by one group; the wings to "
     "be identified are landmarked by another, often in a different "
     "laboratory, by a different operator, from differently prepared "
     "images. The procedure assumes that a landmark placed by one group "
     "falls in the same place as the same numbered landmark placed by "
     "another, to a tolerance small enough that the biological signal "
     "survives. Meixner et al. (2013), in the COLOSS BEEBOOK chapter on "
     "characterising subspecies and ecotypes, emphasised the importance of "
     "reference data and of consistency of methods between laboratories if "
     "results are to be comparable, and Bouga et al. (2011) reached a "
     "similar conclusion in their review of discrimination methods. "
     "Neither recommendation has been tested against data, because testing "
     "it requires the same physical wings to be landmarked twice, "
     "independently.")
para("There is a specific reason to expect that two groups might not place "
     "every landmark identically. Nawrocka et al. (2018) state that their "
     "landmark positions followed Gerula et al. (2009) but were changed at "
     "landmarks 7 and 14 to agree with standard morphometry (Ruttner "
     "1988). Two published versions of the 19-point configuration "
     "therefore differ at those two points. A group working from one "
     "version and a group working from the other would disagree there, and "
     "in few other places. Deposits do not record which version their "
     "operators used.")
para("We located one case in the public record in which two groups "
     "independently landmarked the same wing images, and used it to test "
     "three predictions. First, if the groups worked to different versions "
     "of the configuration, disagreement should concentrate at landmarks 7 "
     "and 14 and be small elsewhere; if it instead reflects ordinary "
     "operator variation, it should be spread across the nineteen points. "
     "Second, if the disagreement is a constant displacement rather than "
     "random scatter, it should be unchanged when the wings are re-paired "
     "at random, and should not diminish as more wings are averaged into a "
     "colony mean. Third, if a displacement of that size matters in "
     "practice, a classifier trained on one dataset should misassign "
     "colonies of known subspecies in a dataset produced elsewhere. The "
     "analysis is possible only because the groups concerned published "
     "their coordinates openly.")
br()

# ================================================= materials and methods
h(1, "Materials and methods")

h(2, "Datasets and how they were found")
para("Nine analytical datasets of honey bee worker forewing landmarks were "
     "used, all on the 19-point configuration of Nawrocka et al. (2018) "
     "and listed in Table 1. They derive from seven sources and from fewer "
     "independent biological samples: the Ecuadorian wings appear twice as "
     "the same specimens measured by two groups, and the two sets from the "
     "Africanised transects are regional subsets of one collection. Counts "
     "of datasets should not be read as counts of independent samples.")
para("Deposits were sought on Zenodo and in the data availability "
     "statements of published honey bee wing morphometric papers, searched "
     "in October 2026 under the terms honey bee wing landmarks, Apis "
     "mellifera wing morphometrics and forewing coordinates, and by "
     "following the deposits of groups publishing in this area. A deposit "
     "was included if it gave landmark coordinates for worker forewings on "
     "the 19-point configuration, under a licence permitting reuse, with "
     "enough identifying information to group wings by colony. Deposits "
     "holding images without coordinates were not included, nor were "
     "deposits whose configuration could not be reconciled with the "
     "19-point scheme. One case was found in which the same wings appear "
     "under two independent landmarkings: the Ecuadorian wings of "
     "Masaquiza and Arenal (2024), re-landmarked by a second group. This "
     "is not a systematic census, and a further replicate may exist in "
     "material these routes do not index.")

table("Table 1",
      "The nine analytical datasets, with bees after bilateral averaging, "
      "the group that placed the landmarks, and the material. The nine "
      "derive from seven sources: the Ecuadorian wings appear twice, "
      "landmarked independently, and the two Africanised sets are regional "
      "subsets of one collection.",
      ["Dataset", "Bees", "Landmarking group", "Material"],
      [["Oberursel reference", "1,832", "Krakow",
        "25 subspecies, 4 lineages"],
       ["Instrumentally inseminated crosses", "9,464", "Skierniewice",
        "198 colony groups, 24 genotypes"],
       ["Serbia", "1,217", "Krakow", "60 colonies"],
       ["Ecuador, re-measured", "726", "Krakow", "central highlands"],
       ["Ecuador, original", "663", "Ecuadorian team", "the same wings"],
       ["Algeria 2018", "460", "Krakow", "46 colonies"],
       ["Africanised, Argentina", "177", "Krakow", "hybrid zone"],
       ["Algeria 2024", "165", "Krakow", "13 colonies"],
       ["Africanised, California", "99", "Krakow", "hybrid zone"]])

h(2, "Compatibility of landmark numbering")
para("Landmark numbering and handedness were verified for every dataset "
     "rather than assumed. Each dataset's generalised Procrustes mean was "
     "matched point to point against the reference mean by sweeping "
     "rotation in half-degree steps and solving the assignment problem at "
     "each angle, with and without reflection, taking the lowest cost. "
     "This establishes computational compatibility only. It does not "
     "establish that two sources place a numbered point at the same "
     "anatomical feature, which is what the first prediction tests.")

h(2, "Procrustes protocol")
para("Configurations were centred, scaled to unit centroid size and rotated "
     "by generalised Procrustes analysis without reflection. Where a bee "
     "contributed both forewings, the configurations were aligned before "
     "averaging and the resulting individual counted once.")

h(2, "Matching the replicate pair")
para("The two Ecuadorian datasets hold the same physical wings, but the "
     "second group cropped each wing from the first group's slide scans, "
     "so raw coordinates differ by translation. Centroid size is "
     "translation-invariant and agrees to about one pixel in 670 for the "
     "same wing. Because each wing in one dataset corresponds to exactly "
     "one wing in the other, matching was solved as a global one-to-one "
     "assignment on a combined centroid-size and shape cost. These are "
     "referred to throughout as matched candidate pairs: matching partly "
     "on shape can favour similar configurations, and the pairs have not "
     "been audited against the deposit images.")
para("Two consequences are separated. The mean displacement between the "
     "sets is the difference between their grand means over the same "
     "wings, so within a fixed pair of selected sets it carries no "
     "information about which wing is paired with which; this was "
     "confirmed by recomputing it under 200 random re-pairings, and is the "
     "second prediction. The residual scatter does depend on the pairing, "
     "and is reported across the matching decision as two sensitivity "
     "scenarios rather than as a point estimate. Both coordinate files "
     "were also checked for repeated records by comparing raw "
     "configurations byte for byte, and the image archive of the first "
     "deposit was checked for repeated files using its published MD5 "
     "checksums.")

h(2, "Quantifying disagreement")
para("One convention is used throughout. With d the Procrustes distance "
     "between two measurements of the same specimen, half the mean squared "
     "disagreement is E[d-squared]/2. This is disagreement between two "
     "measurement sets and not the error of either about a truth, which is "
     "not observable without a trusted reference. Following Collyer and "
     "Adams (2024), systematic and random components are separated: the "
     "mean difference vector between the sets gives their displacement, "
     "and the residual about it is reported as residual disagreement "
     "rather than as independent noise, since it may contain "
     "specimen-dependent bias, colony effects or incorrect matches.")
para("A displacement is a bias, not a variance component. It moves every "
     "colony mean together and creates no variation among colonies "
     "measured by one set, so it is compared against the distances between "
     "colony means that a classifier must resolve rather than expressed as "
     "a share of among-colony variance. Intervals are bootstrap percentile "
     "intervals over 2,000 resamples of colonies, not of wings, since "
     "wings within a colony are not independent.")

h(2, "Assignment")
para("Transfer was tested on the instrumentally inseminated material of "
     "Wegrzynowicz and Los (2020), in which the parentage of every colony "
     "is known. A classifier was trained on the reference dataset by "
     "principal component reduction followed by Mahalanobis assignment to "
     "class means with a pooled within-class covariance, and validated "
     "within the reference by leaving out one colony at a time. It was "
     "then applied to the cross dataset without adjustment, and again "
     "after centring each dataset on its own grand mean, which is reported "
     "as a sensitivity analysis rather than as a recommended correction. "
     "Two colony identifiers appearing under two genotype labels were "
     "excluded before the centring offset was fitted.")

h(2, "Software and reproducibility")
para("Analysis is in thirteen Python files: a shared module and twelve "
     "numbered scripts run in sequence, using NumPy, SciPy, pandas, "
     "openpyxl and Matplotlib. Each script writes its own result tables, "
     "and every figure and table quoted here is reproduced by running them "
     "in order. Raw datasets are not redistributed; the repository lists "
     "every source by DOI.")
br()

# ================================================================ results
h(1, "Results")

h(2, "One deposit of nine numbers the landmarks differently")
para("Of the nine datasets, one numbers the same 19 anatomical points in a "
     "different, close to reversed order, and two require reflection "
     "before pooling. Both failures are silent. The original and "
     "re-measured Ecuadorian coordinates describe the same 663 wings, yet "
     "pooled without correction their Procrustes distances sit near 1.05 "
     "against a theoretical maximum of 1.41, and no software raises a "
     "warning. The numbering was recovered by the rotation sweep described "
     "above, and all results below use the corrected correspondence.")

h(2, "Prediction 1: the disagreement is concentrated at two landmarks")
para("Of 663 and 726 records, 642 formed matched candidate pairs, their "
     "centroid sizes correlating at r = 1.0000. The disagreement between "
     "the two measurement sets is not spread across the configuration. "
     "Landmarks 7 and 14 carry 94.0% of the squared mean displacement on "
     "all 642 pairs and 94.3% on the 608 retained after removing the 34 "
     "largest discrepancies, against 10.5% expected if it were divided "
     "evenly across nineteen points. Their root-mean-square disagreement "
     "on the retained pairs, 0.00732 and 0.00580, is 6.4 times the median "
     "of 0.00102 across the other seventeen (Figure 1).")
figure(1,
       "Root-mean-square disagreement between the two measurement sets at "
       "each of the 19 landmarks, on the 608 retained candidate pairs, in "
       "units of centroid size. Shaded bars are landmarks 7 and 14, the two "
       "whose position Nawrocka et al. (2018) report changing relative to "
       "Gerula et al. (2009). The dashed line is the median across the "
       "other seventeen landmarks. Bars show root-mean-square "
       "disagreement, which includes residual scatter; the 94% quoted in "
       "the text is the share of the squared mean displacement, computed "
       "from the mean difference vector alone.")
para("The landmark-matching step reached the same two landmarks "
     "independently: residuals between the two generalised Procrustes mean "
     "shapes were 0.00654 at landmark 7 and 0.00567 at landmark 14, "
     "against 0.00241 or less at all seventeen others. The prediction is "
     "met. We present the convention difference as a plausible explanation "
     "rather than a demonstrated one, because neither deposit records "
     "which version of the configuration its operators worked from, and an "
     "operator effect concentrated at the two least determinate junctions "
     "would look similar. What the localisation does establish is that the "
     "displacement is not diffuse digitising noise, and that a correction, "
     "if one is wanted, has a specific target.")

h(2, "Prediction 2: the disagreement is a displacement, not scatter")
para("Half the mean squared disagreement between the two sets was 0.000110 "
     "(95% CI 0.000074 to 0.000155). Of that, a mean displacement of "
     "0.00875 Procrustes units (95% CI 0.00844 to 0.00916) accounts for "
     "34.8%, the remainder being residual disagreement that is not "
     "demonstrably independent noise (Table 2).")
para("Recomputing the displacement under 200 random re-pairings of the same "
     "wings returned 0.00875 each time, to five decimal places, as a "
     "difference of grand means must. Removing the 34 largest "
     "discrepancies moves it from 0.00875 to 0.00866, a change of 1.1%, "
     "while total disagreement falls by 53% and residual disagreement by "
     "80%. The central estimate therefore does not rest on the matching; "
     "the residual term does, and both scenarios are reported without "
     "preference. Neither is a bound: with the true matching unknown, they "
     "do not limit the disagreement mathematically.")

table("Table 2",
      "Disagreement between two independent measurements of the same "
      "wings, its dependence on the matching decision, and its size "
      "relative to the distances between colony means. Half the mean "
      "squared disagreement is E[d-squared]/2 throughout. No share of "
      "variance is implied: a displacement is a bias, not a variance "
      "component.",
      ["Quantity", "Value"],
      [["Matched candidate pairs", "642 of 663 and 726"],
       ["Correlation of centroid size on those pairs", "r = 1.0000"],
       ["Median Procrustes distance", "0.00964"],
       ["Half mean squared total disagreement", "0.000110"],
       ["95% interval", "0.000074 to 0.000155"],
       ["Mean displacement", "0.00875"],
       ["95% interval", "0.00844 to 0.00916"],
       ["Same, under 200 random re-pairings", "0.00875"],
       ["Same, excluding the 34 largest discrepancies", "0.00866"],
       ["Half the squared mean displacement", "0.0000383"],
       ["Residual after removing it", "0.0000719"],
       ["Displacement share of the total", "34.8%"],
       ["Share of squared displacement at landmarks 7 and 14",
        "94.0% (94.3% on retained pairs)"],
       ["Colonies with 3 or more wings, and colony pairs", "74 and 2,701"],
       ["Median distance between colony means", "0.01974"],
       ["10th percentile of those distances", "0.01459"],
       ["Displacement divided by median colony separation", "0.44"],
       ["Colony-mean distances below the displacement",
        "0.2% (6 of 2,701)"],
       ["Within-bee disagreement, bilateral wings (3 datasets)",
        "0.000089 to 0.000091"]])

para("The displacement is the consequential part, because it does not "
     "diminish with averaging. The median distance between colony means in "
     "the re-measured Ecuadorian set is 0.01974 across 74 colonies and "
     "2,701 colony pairs, so the displacement is 0.44 times that. It is "
     "smaller than the tenth percentile of those distances, 0.01459, and "
     "exceeds only 0.2% of them (Figure 2). Computed from the colony "
     "difference vectors over the 73 colonies measured by both sets, its "
     "magnitude is 0.00878, close to the pooled figure, which is what a "
     "constant displacement predicts; the median magnitude of the "
     "colony-specific displacements is 0.00909. Whether a displacement of "
     "this size defeats a particular classifier depends on its direction "
     "relative to the discriminant axes and not on this ratio alone, which "
     "is why the third prediction was tested directly.")
figure(2,
       "The displacement between the two measurement sets, with its "
       "bootstrap interval shaded, against the distances between colony "
       "means. The solid vertical line is the displacement of 0.00875; the "
       "long-dashed line is the median colony separation of 0.01974 and "
       "the short-dashed line the tenth percentile of 0.01459. Colony "
       "means are from the re-measured Ecuadorian set, 74 colonies with "
       "three or more wings giving 2,701 pairwise distances. Those "
       "distances share colonies and are not independent: each colony "
       "enters 73 of them.")

h(2, "Prediction 3: reference transfer fails without calibration")
para("The reference separates its own subspecies in 41 of 41 colonies by "
     "leave-one-colony-out. That shows these three subspecies are "
     "separable within that collection; it does not establish that the "
     "model is well specified. Applied across datasets without adjustment, "
     "the classifier assigns zero or one of five colonies of known pure "
     "A. m. caucasica correctly across 6 to 20 principal components, "
     "calling the rest carnica or mellifera (Table 3, Figure 3). The "
     "evidence is five colonies, not the 9,464 wings of the dataset: the "
     "other pure lines were assigned correctly without adjustment and so "
     "show no failure.")
para("The apparently correct calls carry little weight either. The four "
     "retained P1kk colonies sat 0.02903 from the carnica centroid and "
     "0.02977 from the mellifera one, a margin of 0.00074. That is an "
     "order of magnitude below the offset between the dataset grand means, "
     "0.02475, and about a twelfth of the measurement displacement.")

table("Table 3",
      "Transfer of a reference classifier to a dataset produced elsewhere. "
      "Upper panel: assignment of colonies of known parentage, before and "
      "after centring each dataset on its own grand mean, at 12 principal "
      "components. Lower panel: sensitivity of the caucasica result to the "
      "number of principal components. Centring is reported as a "
      "sensitivity analysis, not as a recommended correction.",
      ["Genotype or dimension", "Expected", "Colonies",
       "Correct, uncorrected", "Correct, centred"],
      PURE + [["Principal components", "", "", "", ""],
              ["6", "caucasica", "5", "0/5", "2/5"],
              ["8", "caucasica", "5", "1/5", "4/5"],
              ["10", "caucasica", "5", "0/5", "4/5"],
              ["12", "caucasica", "5", "0/5", "4/5"],
              ["16", "caucasica", "5", "1/5", "4/5"],
              ["20", "caucasica", "5", "0/5", "3/5"]])

figure(3,
       "Assignment of colonies of known parentage from a dataset produced "
       "elsewhere, by genotype group, at 12 principal components: (a) "
       "without adjustment and (b) after centring each dataset on its own "
       "grand mean. Cell labels are colony counts and shading gives the "
       "proportion within each row. Two colony identifiers appearing under "
       "two genotype labels are excluded.")

para("Centring recovers two to four of the five caucasica colonies "
     "depending on classifier dimension. This is reported as a sensitivity "
     "analysis and not as a correction. The reference contains three "
     "subspecies and the target contains pure lines, hybrids and "
     "backcrosses, so their biological compositions differ and centring "
     "removes real biological difference along with any technical "
     "displacement. Improved classification afterwards does not establish "
     "that what was removed was technical. An operational correction would "
     "need to be estimated from separate calibration specimens and "
     "evaluated on held-out colonies, which these data do not permit.")

h(2, "Repeated records in one deposit")
para("The image archive of the original Ecuadorian deposit holds 75 files "
     "of which 70 are distinct by published checksum; five filenames carry "
     "the content of another file bearing the same apiary prefix. That "
     "duplication reaches the coordinates. Of the 663 wing records, ten "
     "are byte-identical copies of other records: one on image R2C2 of "
     "apiary 13, and a block of nine on image JSC1 of apiary 6. Every "
     "duplicate lies within the same image and apiary as its original, so "
     "no record is shared between apiaries and comparisons between "
     "colonies cannot be affected by them. Removing the ten leaves 632 "
     "matched pairs and reduces the number above three times the median "
     "from 34 to 28, because two identical records compete for distinct "
     "partners and one is necessarily matched to the wrong wing. The mean "
     "displacement is unchanged at 0.00875. This is noted so that others "
     "reusing the deposit can allow for it.")
br()

# ============================================================= discussion
h(1, "Discussion")
para("Two groups landmarking the same honey bee wings disagree by 0.00875 "
     "Procrustes units, and that disagreement is a displacement rather "
     "than scatter: it is unchanged when the wings are re-paired, and "
     "being constant it does not shrink as more wings are averaged into a "
     "colony mean. The principle that a systematic component survives "
     "averaging is not new, and Collyer and Adams (2024) set out a general "
     "framework for separating systematic from random measurement error in "
     "landmark data. What has not been available until now is a "
     "measurement of its size in honey bee wing morphometrics, because "
     "that requires the same wings to be landmarked twice by different "
     "groups and the result to be published. The size matters: 0.44 times "
     "the median distance between colony means is not a rounding error in "
     "a method whose purpose is to resolve differences of that order.")
para("The localisation is the more useful result. Had the disagreement been "
     "spread evenly across the nineteen landmarks, the only available "
     "advice would have been the general one, to remeasure everything in "
     "one laboratory. Instead 94% of it sits on two points, and those two "
     "points are the ones Nawrocka et al. (2018) record as having been "
     "moved from the convention of Gerula et al. (2009) to agree with "
     "Ruttner (1988). We do not claim this proves the two groups used "
     "different versions, and the data cannot show it, since neither "
     "deposit records the version used. An operator effect concentrated at "
     "the two least determinate vein junctions would produce a similar "
     "pattern. Either way the practical consequence is the same and the "
     "remedy is cheap: the information needed to tell these explanations "
     "apart is a single line of metadata that deposits do not currently "
     "carry.")
para("The transfer failure should be read narrowly. The evidence is five "
     "colonies of known pure A. m. caucasica, not the whole cross dataset, "
     "and the other pure lines transferred correctly. But those five are "
     "the only colonies in the public record whose subspecies is known by "
     "pedigree rather than by the morphometric method under test, so they "
     "are the only available check on transfer, and a method that "
     "separates its own subspecies in 41 of 41 colonies should not fail on "
     "them. The narrow margins behind the apparently correct calls, a "
     "twelfth of the measurement displacement, suggest those successes are "
     "not reassuring either.")
para("Several limitations bound these conclusions. Dataset, population and "
     "landmarking group are confounded throughout the public record: apart "
     "from the Ecuadorian pair, no two groups have measured the same "
     "population, so differences between datasets are total divergence and "
     "are described as such here. The measurement estimate rests on one "
     "pair of groups and one set of images. Its two components differ in "
     "how far they depend on the matching: total disagreement changed "
     "approximately twofold between the two sensitivity scenarios, whereas "
     "the mean displacement changed by 1.1%. The candidate pairs are "
     "algorithmically matched and have not been audited against the "
     "images; that audit remains the most important outstanding check, "
     "although repeated records in the deposit account for six of the 34 "
     "large discrepancies. Whether the disagreement at landmarks 7 and 14 "
     "reflects a convention difference or operator variation is "
     "unresolved, and resolving it requires deposits to record the "
     "convention, or one group to landmark a shared set of wings under "
     "both conventions deliberately.")
br()

# ============================================================ conclusions
h(1, "Conclusions")
para("A reference dataset built in one laboratory did not transfer to wings "
     "landmarked in another without calibration, and the disagreement "
     "responsible was concentrated at the two landmarks whose definition "
     "differs between published versions of the configuration. Meixner et "
     "al. (2013) and Bouga et al. (2011) recommended consistency of "
     "methods between laboratories; these results give that recommendation "
     "a magnitude and, more usefully, a specific target.")
para("Four items of metadata would make the difference, none of them "
     "costly. Deposits of wing landmark coordinates should record: the "
     "version of the landmark convention followed, with its citation, and "
     "in particular the positions used for landmarks 7 and 14; the "
     "software used to place the landmarks and its version; whether "
     "landmarks were placed manually, semi-automatically or automatically, "
     "and by how many operators; and the provenance of the images, "
     "including whether they were cropped or rescaled from another "
     "deposit. Where a reference is to be applied to wings landmarked "
     "elsewhere, a small set of shared specimens measured by both groups "
     "would allow the displacement to be estimated and removed, which is "
     "the calibration these data show to be necessary and which no "
     "published study of honey bee wings currently provides.")
br()

# =========================================================== declarations
h(1, "Declarations")

h(2, "Data availability statement")
para("Every dataset analysed is a published open deposit, listed with its "
     "DOI in the supplementary material. Several carry the Open Database "
     "License v1.0 and its share-alike requirement; derived tables are "
     "released under the same licence with attribution. Analysis code and "
     "all generated results are at "
     "https://github.com/vkcvaibhav-eng/honeybee-wing-reliability- and are "
     "archived at https://doi.org/10.5281/zenodo.23906962, with every "
     "figure and table reproduced by running the numbered scripts in "
     "sequence.")

h(2, "Funding")
para("No funding was obtained for the reported work.")

h(2, "Disclosure statement")
para("The authors report there are no competing interests to declare.")

h(2, "Declaration of generative AI use")
para("A large language model (Claude, Anthropic) was used to write the "
     "analysis code, to run the analyses and to prepare drafts of this "
     "manuscript. All numerical results were produced by the committed "
     "scripts and are reproducible from them. The authors verified the "
     "analyses and are accountable for the content of this text.")

h(2, "Ethical approval")
para("Not applicable. No specimens were collected and no live animals were "
     "handled in this study. All data analysed are previously published "
     "open deposits of landmark coordinates.")

h(2, "Authors' contributions")
para("V.K. Chaudhari conceived the study, developed the methodology, wrote "
     "the analysis code, performed the formal analysis, prepared the "
     "figures and wrote the original draft. J.J. Pastagia contributed to "
     "the review and editing of the manuscript and to supervision. Both "
     "V.K. Chaudhari and J.J. Pastagia read and approved the submitted "
     "manuscript.")

h(2, "Acknowledgements")
para("This analysis exists because several groups deposited their wing "
     "coordinates openly under licences permitting reuse: A. Oleksa, A. "
     "Tofilski and colleagues for the reference and the European, Serbian, "
     "Algerian and re-measured collections; D. Masaquiza and A. Arenal for "
     "the Ecuadorian wings; E. Calfee, G. Coop and colleagues for the "
     "Africanised wings and their sequenced metadata; and P. Wegrzynowicz "
     "and A. Los for the only honey bee wing material with known pedigree. "
     "The central estimate was possible only because two groups "
     "independently landmarked the same Ecuadorian images and both "
     "published the result.")
br()

# ============================================================= references
h(1, "References")
REFS = [
    [("Angel-Beamonte, E., Santolaria, P., Cortes-Calvo, S., Gonzalvo, M., "
      "Munoz Gabaldon, I., De la Rua, P., Espejo, P., Yaniz, J. (2024) Wing "
      "morphometric analysis using smartphone images and a free "
      "MATLAB-based tool: a case study with ", N), ("Apis mellifera", I),
     (" from the Balearic Islands. Journal of Apicultural Research, 1-10. "
      "https://doi.org/10.1080/00218839.2024.2365490", N)],
    [("Bouga, M., Alaux, C., Bienkowska, M., Buchler, R., Carreck, N.L., et "
      "al. (2011) A review of methods for discrimination of honey bee "
      "populations as applied to European beekeeping. Journal of "
      "Apicultural Research, 50 (1), 51-84. "
      "https://doi.org/10.3896/IBRA.1.50.1.06", N)],
    [("Calfee, E., Agra, M.N., Palacio, M.A., Ramirez, S.R., Coop, G. (2020) "
      "Selection and hybridization shaped the rapid spread of African honey "
      "bee ancestry in the Americas. PLoS Genetics, 16 (10), e1009038. "
      "https://doi.org/10.1371/journal.pgen.1009038", N)],
    [("Collyer, M.L., Adams, D.C. (2024) Interrogating random and systematic "
      "measurement error in morphometric data. Evolutionary Biology, 51, "
      "179-207. https://doi.org/10.1007/s11692-024-09627-6", N)],
    [("Gerula, D., Tofilski, A., Wegrzynowicz, P., Skowronek, W. (2009) "
      "Computer-assisted discrimination of honeybee subspecies used for "
      "breeding in Poland. Journal of Apicultural Science, 53 (2), "
      "105-114", N)],
    [("Janczyk, A., Tofilski, A. (2021) Monthly changes in honey bee "
      "forewings estimated using geometric morphometrics. Journal of "
      "Apicultural Science, 65 (1), 139-146. "
      "https://doi.org/10.2478/jas-2021-0002", N)],
    [("Machlowska, J., Kandemir, I., Ozkan Koca, A., Kakhniashvili, V., "
      "Alattal, Y., et al. (2025) Variation of honey bee wings in "
      "southwestern Asia. Scientific Data. "
      "https://doi.org/10.1038/s41597-025-06234-8", N)],
    [("Machlowska, J., Gerula, D., Oleksa, A., Kok, H., McCormack, G.P., et "
      "al. (2026) Country specific hybridization of honey bees from lineage "
      "M. GigaScience, 15, giag093. "
      "https://doi.org/10.1093/gigascience/giag093", N)],
    [("Masaquiza, D., Arenal, A. (2024) Collection of images and raw "
      "coordinates of honey bee (", N), ("Apis mellifera", I),
     (") wings from the central highlands of Ecuador [dataset]. Zenodo. "
      "https://doi.org/10.5281/zenodo.13340594", N)],
    [("Meixner, M.D., Pinto, M.A., Bouga, M., Kryger, P., Ivanova, E., "
      "Fuchs, S. (2013) Standard methods for characterising subspecies and "
      "ecotypes of ", N), ("Apis mellifera", I),
     (". Journal of Apicultural Research, 52 (4), 1-28. "
      "https://doi.org/10.3896/IBRA.1.52.4.05", N)],
    [("Nawrocka, A., Kandemir, I., Fuchs, S., Tofilski, A. (2018) Computer "
      "software for identification of honey bee subspecies and evolutionary "
      "lineages. Apidologie, 49 (2), 172-184. "
      "https://doi.org/10.1007/s13592-017-0538-y", N)],
    [("Oleksa, A., Tofilski, A. (2015) Wing geometric morphometrics and "
      "microsatellite analysis provide similar discrimination of honey bee "
      "subspecies. Apidologie, 46 (1), 49-60. "
      "https://doi.org/10.1007/s13592-014-0300-7", N)],
    [("Oleksa, A., Cauia, E., Siceanu, A., Puskadija, Z., Kovacic, M., et "
      "al. (2023) Honey bee (", N), ("Apis mellifera", I),
     (") wing images: a tool for identification and conservation. "
      "GigaScience, 12, giad019. "
      "https://doi.org/10.1093/gigascience/giad019", N)],
    [("Ruttner, F. (1988) Biogeography and taxonomy of honeybees. "
      "Springer-Verlag, Berlin", N)],
    [("Szentgyorgyi, H., Czekonska, K., Tofilski, A. (2016) Influence of "
      "pollen deprivation on the fore wing asymmetry of honeybee workers "
      "and drones. Apidologie, 47, 653-662. "
      "https://doi.org/10.1007/s13592-015-0415-5", N)],
    [("Wegrzynowicz, P., Los, A. (2020) Dataset of wing venation "
      "measurements for ", N), ("Apis mellifera caucasica", I), (", ", N),
     ("A. mellifera carnica", I), (" and ", N),
     ("A. mellifera mellifera", I),
     (" (Hymenoptera: Apidae), their hybrids and backcrosses. Biodiversity "
      "Data Journal, 8, e53724. https://doi.org/10.3897/BDJ.8.e53724", N)],
]
for r in REFS:
    rich(r)

doc.save(OUT)
print("wrote", OUT)
