#!/usr/bin/env python3
"""Build the revised Apidologie submission after editorial review."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

OUT = "/home/claude/Chaudhari_Pastagia_Apidologie_v10.docx"
doc = Document()

sec = doc.sections[0]
for a in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sec, a, Cm(3))
ln = OxmlElement("w:lnNumType")
ln.set(qn("w:countBy"), "1")
ln.set(qn("w:restart"), "continuous")
sec._sectPr.append(ln)
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run()
b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin")
i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = " PAGE "
e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end")
for el in (b, i, e):
    run._r.append(el)
run.font.name = "Times New Roman"; run.font.size = Pt(12)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(12)
st._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.line_spacing = 2.0
st.paragraph_format.space_after = Pt(0)
for nm, bold, ital in (("Heading 1", True, False), ("Heading 2", True, True),
                       ("Heading 3", False, True)):
    s = doc.styles[nm]
    s.font.name = "Times New Roman"; s.font.size = Pt(12)
    s.font.bold = bold; s.font.italic = ital; s.font.color.rgb = None
    s.paragraph_format.line_spacing = 2.0
    s.paragraph_format.space_before = Pt(12)
    s.paragraph_format.space_after = Pt(0)


def para(t="", align=None, italic=False, bold=False):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    if t:
        r = p.add_run(t); r.italic = italic; r.bold = bold
    return p


def rich(segs):
    p = doc.add_paragraph()
    for t, f in segs:
        r = p.add_run(t); r.italic = f.get("i", False); r.bold = f.get("b", False)
    return p


def h(lv, t):
    p = doc.add_paragraph(style=f"Heading {lv}"); p.add_run(t); return p


def br():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


import csv as _csv
from collections import Counter as _Counter
_LET = {"c": "caucasica", "k": "carnica", "m": "mellifera"}
_rows = list(_csv.DictReader(open(
    "/home/claude/honeybee-wing-reliability-/results/"
    "known_crosses_assignments.csv")))
_BADID = {"0489_12", "0203_13"}
_rows = [x for x in _rows if x["colony"] not in _BADID]
_EXP = {"cc": "caucasia", "kk": "carnica", "mm": "mellifera"}
_QD = {"c": "caucasica", "k": "carnica", "m": "mellifera"}
PURE_ROWS, F1_ROWS = [], []
for _g in ("P0cc", "P1cc", "P0kk", "P1kk", "P0mm", "P1mm"):
    _s = [x for x in _rows if x["genotype"] == _g]
    _e = _EXP[_g[2:]]
    _c = _Counter(x["assigned_corrected"] for x in _s)
    PURE_ROWS.append([
        _g, {"cc": "caucasica", "kk": "carnica", "mm": "mellifera"}[_g[2:]],
        str(len(_s)),
        f"{round(100*sum(1 for x in _s if x['assigned_raw']==_e)/max(len(_s),1))}%",
        f"{round(100*sum(1 for x in _s if x['assigned_corrected']==_e)/max(len(_s),1))}%"])
    F1_ROWS.append([_g, _QD[_g[2]], _QD[_g[3]], str(len(_s))] +
                   [str(_c.get(k, 0)) for k in ("carnica", "caucasia",
                                                "mellifera")])
for _g in ("F1ck", "F1kc", "F1cm", "F1mc", "F1km", "F1mk"):
    _s = [x for x in _rows if x["genotype"] == _g]
    _c = _Counter(x["assigned_corrected"] for x in _s)
    F1_ROWS.append([_g, _QD[_g[2]], _QD[_g[3]], str(len(_s))] +
                   [str(_c.get(k, 0)) for k in ("carnica", "caucasia",
                                                "mellifera")])
_bc = [x for x in _rows if x["genotype"].startswith("BC")]
BC_ROWS = []
for _g in sorted({x["genotype"] for x in _bc}):
    _sub = [x for x in _bc if x["genotype"] == _g]
    _c = _Counter(x["assigned_corrected"] for x in _sub)
    BC_ROWS.append([_g, _LET[_g[4]], str(len(_sub))] +
                   [str(_c.get(k, 0)) for k in ("carnica", "caucasia",
                                                "mellifera")])

N_BC = sum(int(r[2]) for r in BC_ROWS)

I = {"i": True}
B = {"b": True}
N = {}

# ---------------------------------------------------------------- title page
para("Disagreement between independently produced honey bee wing datasets "
     "is localized at two landmarks and limits reference transfer",
     align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
para()
para("V. K. Chaudhari (1) and J. J. Pastagia (2)",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para()
para("(1) AINP on Agricultural Acarology, Department of Entomology, N. M. "
     "College of Agriculture, Navsari Agricultural University, Navsari "
     "396450, Gujarat, India", align=WD_ALIGN_PARAGRAPH.CENTER)
para("(2) Department of Entomology, N. M. College of Agriculture, Navsari "
     "Agricultural University, Navsari 396450, Gujarat, India",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para()
para("Corresponding author: V. K. Chaudhari, vkcvaibhav@gmail.com")
para("Co-author: J. J. Pastagia, jayeshpastagia@nau.in")
para()
rich([("Short title: ", B), ("Localized disagreement in wing datasets", N)])
rich([("Running title: ", B), ("Wing reference transfer", N)])
para()
rich([("Author contributions. ", B),
      ("Conceptualization, methodology, software, formal analysis, data "
       "curation, visualization and writing of the original draft: "
       "V. K. Chaudhari. Writing, review and editing, and supervision: "
       "J. J. Pastagia. Both authors read and approved the submitted "
       "manuscript.", N)])
br()

# ------------------------------------------------------------------ abstract
h(1, "Abstract")
rich([("Two groups independently landmarked the same ", N),
      ("Apis mellifera", I),
      (" forewing images, the only such replicate in a search of public "
       "deposits. The two measurements differ by a mean displacement of "
       "0.00875 Procrustes units (95% CI 0.00844 to 0.00916), 0.44 times "
       "the median distance between colony means. Being a difference of "
       "grand means it is unchanged under re-pairing within the sets, and "
       "being constant it does not shrink as wings are averaged. It is "
       "localized: about 94% of the squared mean displacement falls on two "
       "of the nineteen landmarks, the two the reference configuration "
       "records as moved from an earlier convention. A classifier "
       "separating its own subspecies in 41 of 41 colonies assigned zero or "
       "one of five known pure ", N),
      ("A. m. caucasica", I),
      (" colonies correctly in a dataset produced elsewhere. Reference "
       "transfer needs the landmark convention stated.", N)])
para()
rich([("Keywords: ", B), ("Apis mellifera", I),
      (", geometric morphometrics, measurement error, observer effects, "
       "reference dataset", N)])
br()

# -------------------------------------------------------------- introduction
h(1, "1. Introduction")
para("Wing geometric morphometrics is the standard low-cost method for "
     "identifying honey bee subspecies and evolutionary lineages, and its "
     "reference base is now large and open. Oleksa et al. (2023) released "
     "26,481 forewing images from 1,725 samples across 13 European countries, "
     "with coordinates for 19 landmarks at vein junctions. Machlowska et al. "
     "(2025) added 17,457 wings from 1,557 colonies in nine southwestern "
     "Asian countries. Further deposits cover Kazakhstan, Serbia, Algeria, "
     "Tabasco, Ecuador, northwestern Europe and Jammu and Kashmir, all "
     "landmarked to the configuration of Nawrocka et al. (2018). These "
     "references are applied at scale: Machlowska et al. (2026) assigned "
     "1,342 colony samples from ten countries to the four evolutionary "
     "lineages. The analysis reported here is possible only because these "
     "groups published their coordinates openly.")
para("Oleksa et al. (2023) noted that identification always requires a "
     "reference dataset, which is often inadequate, and hoped future studies "
     "would make images freely available to expand it. Pooling across "
     "collections is therefore the intended direction of travel, and it rests "
     "on an assumption that has not been tested: that a reference built from "
     "one collection applies to material prepared and measured elsewhere.")
para("Measurement reliability is the component of that assumption most often "
     "named and least often quantified. Machlowska et al. (2025) observed "
     "that alcohol concentration and wing hydration at measurement differed "
     "between earlier studies and could affect shape. Szentgyorgyi et al. "
     "(2016) found, while testing pollen deprivation, that differences due to "
     "replication exceeded those due to the treatment. Quantification of "
     "measurement error in geometric morphometric datasets, and of its effect "
     "on results, remains uncommon.")
para("This study asks three questions of data already in the public record. "
     "First, are the landmark configurations in circulation computationally "
     "and anatomically compatible? Second, how much disagreement arises when "
     "two groups digitize verified identical images, and how much of it is "
     "random rather than systematic? Third, does a reference classifier "
     "transfer to colonies measured elsewhere, tested where the correct "
     "answer is known from controlled crosses?")
para("The distinction between random and systematic disagreement carries the "
     "practical weight. Published practice averages wings within a colony "
     "before comparing to a reference, which suppresses random error in "
     "proportion to sample size. A constant displacement between two groups "
     "survives that averaging unchanged.")

# ------------------------------------------------------------------- methods
h(1, "2. Materials and methods")

h(2, "2.1. Datasets")
rich([("Nine analytical datasets of ", N), ("Apis mellifera", I),
      (" worker forewing landmarks were used, all on the 19-point "
       "configuration of Nawrocka et al. (2018), listed in Table I. They "
       "derive from seven sources and from fewer independent biological "
       "samples: the Ecuadorian wings appear twice as the same specimens "
       "measured by two groups, and the two Calfee sets are regional subsets "
       "of one collection. Counts of datasets should not be read as counts of "
       "independent samples.", N)])
para("One feature of the public record carries the central analysis. The "
     "Ecuadorian wings were digitized twice and independently: Masaquiza and "
     "Arenal (2024) deposited their own coordinates, and a second group later "
     "landmarked the same images. Across the whole public record this occurs "
     "once. Separately, three datasets digitized both forewings of the same "
     "bee, giving 1,689 bilateral pairs.")

h(3, "2.1.1. How the deposits were found")
para("Deposits were sought on Zenodo and in the data-availability statements "
     "of published honey bee wing morphometric papers, searched in October "
     "2026 under the terms honey bee wing landmarks, Apis mellifera wing "
     "morphometrics and forewing coordinates, and by following the "
     "deposits of groups publishing in this area. A deposit was included if "
     "it gave landmark coordinates for worker forewings on the 19-point "
     "configuration, under a licence permitting reuse, with enough "
     "identifying information to group wings by colony. Deposits holding "
     "images without coordinates were not included, nor were deposits whose "
     "configuration could not be reconciled with the 19-point scheme. One "
     "case was found in which the same wings appear under two independent "
     "landmarkings. This is not a systematic census, and a further replicate "
     "may exist in material these routes do not index.")

h(2, "2.2. Compatibility of landmark configurations")
para("Landmark numbering and handedness were verified for every dataset "
     "rather than assumed. Each dataset's generalized Procrustes mean was "
     "matched point-to-point against the reference mean by sweeping rotation "
     "in half-degree steps and solving the assignment problem at each angle, "
     "with and without reflection, taking the lowest cost.")
para("This establishes computational compatibility only. It does not "
     "establish that two sources place a numbered point at the same "
     "anatomical feature. There is a documented reason to expect that they "
     "may not. Nawrocka et al. (2018) state that their landmark positions "
     "followed Gerula et al. (2009) but were changed at landmarks 7 and 14 "
     "to agree with standard morphometry (Ruttner 1988). Two published "
     "versions of the configuration therefore differ at those two points, "
     "and a group working from one version would disagree with a group "
     "working from the other at those landmarks and in few other places. "
     "Disagreement is reported per landmark for that reason.")

h(2, "2.3. Procrustes protocol")
para("Configurations were centred, scaled to unit centroid size and rotated "
     "by generalized Procrustes analysis without reflection. Where a bee "
     "contributed both forewings, the configurations were aligned before "
     "averaging, and the resulting individual counted once.")

h(2, "2.4. Matching the replicate pair")
para("The two Ecuadorian datasets hold the same physical wings, but the "
     "second group cropped each wing from the first group's slide scans, so "
     "raw coordinates differ by translation. Centroid size is "
     "translation-invariant and agrees to about one pixel in 670 for the same "
     "wing. Because each wing in one dataset corresponds to exactly one wing "
     "in the other, matching was solved as a global one-to-one assignment on "
     "a combined centroid-size and shape cost. These are referred to "
     "throughout as algorithmically matched candidate pairs: matching partly "
     "on shape can favour similar configurations, and the pairs have not "
     "been audited against the images. Both the original scans and the "
     "cropped re-measurement images are publicly deposited; they could not "
     "be retrieved in the environment used for this analysis, whose network "
     "policy refused connections to the host, and the audit is named as "
     "outstanding rather than claimed.")
para("Before matching, both coordinate files were checked for repeated "
     "records by comparing the raw configurations byte for byte, and the "
     "image archive of the first deposit was checked for repeated files by "
     "comparing the MD5 checksums published with it. What this found is "
     "reported in the Results and treated as a sensitivity analysis: the "
     "analysis itself uses the deposit as published, so that it reproduces "
     "from the deposited file without alteration.")
para("Two consequences are separated. The mean displacement between the "
     "sets is the difference between their grand means over the same wings, "
     "so within a fixed pair of selected sets it carries no information about "
     "which wing is paired with which. This was confirmed by recomputing it "
     "under 200 random re-pairings. The invariance is to re-pairing within "
     "the selected sets; selecting the 642 records is itself a matching "
     "step, and the conclusion is qualified accordingly. "
     "The residual scatter does depend on the pairing, and is reported "
     "across the matching decision as a range rather than as a point "
     "estimate. Large discrepancies are retained rather than discarded.")

h(2, "2.5. Disagreement between measurement sets")
para("One convention is used throughout. With d the Procrustes distance "
     "between two measurements of the same specimen, half the mean squared "
     "disagreement is E[d-squared]/2. This is disagreement between two "
     "measurement sets and not the error of either about a truth, which is "
     "not observable without a trusted reference. The mean difference vector "
     "between the sets gives their displacement; the residual about it is "
     "reported as residual disagreement rather than as independent noise, "
     "since it may contain specimen-dependent bias, colony effects or "
     "incorrect matches.")
para("A displacement is a bias, not a variance component: it moves every "
     "colony mean together and creates no variation among colonies measured "
     "by one set. It is therefore compared against the distances between "
     "colony means that a classifier must resolve, not expressed as a share "
     "of among-colony variance.")
para("Intervals are bootstrap percentile intervals over 2,000 resamples of "
     "colonies, not of wings, since wings within a colony are not "
     "independent.")

h(2, "2.6. Assignment")
para("Subspecies assignment used discriminant analysis on shape reduced to 12 "
     "principal components, with class means and a pooled within-class "
     "covariance, assigning by Mahalanobis distance. Colony means were used, "
     "as in published practice. Accuracy on the reference was measured by "
     "leave-one-colony-out. Full assignment counts are reported for every "
     "genotype rather than a modal class.")

h(2, "2.7. An exploratory ancestry scale")
para("Shape was regressed on genome-wide African ancestry across 268 wings "
     "joined to Calfee et al. (2020) by image filename, giving a direction in "
     "shape space and a rate along it. Differences between datasets were "
     "projected onto that direction before conversion. This scale is "
     "exploratory and is evaluated against a measured ancestry difference in "
     "the Results.")

h(2, "2.8. Code and use of large language models")
para("Analysis is in thirteen Python files: a shared module and twelve "
     "numbered scripts run in sequence, using NumPy, SciPy, pandas, openpyxl "
     "for the spreadsheet deposits and Matplotlib for the figures. Each "
     "script writes its own result tables, and every figure and table quoted "
     "here is reproduced by running them in order. Raw datasets are not "
     "redistributed; the repository lists every source by DOI.")
para("A large language model (Claude, Anthropic) was used to write the "
     "analysis code, to run the analyses, and to prepare drafts of this "
     "manuscript. All numerical results were produced by the committed "
     "scripts and are reproducible from them. The authors verified the "
     "analyses and are accountable for the content of this text.")

# ------------------------------------------------------------------- results
h(1, "3. Results")

h(2, "3.1. One dataset of nine is computationally incompatible")
para("Of the nine datasets, one numbers the same 19 anatomical points in a "
     "different, close to reversed order, and two require reflection before "
     "pooling. Both failures are silent. The Masaquiza and re-measured "
     "Ecuadorian coordinates describe the same 663 wings, yet pooled without "
     "correction their Procrustes distances sit near 1.05 against a "
     "theoretical maximum of 1.41, and no software raises a warning.")
para("This is a computational result and the limit of what these data "
     "support. Establishing that two sources place a numbered point at the "
     "same anatomical feature requires their published definitions, not a "
     "coordinate matching. That matters for interpretation: the largest "
     "between-group disagreements in this study fall on landmarks 7 and 14, "
     "and Nawrocka et al. (2018) describe altering the positions of two "
     "landmarks relative to an earlier convention. A difference of convention "
     "would produce exactly the pattern observed, so these points are not "
     "reported here as unreliable. Resolving the question requires annotated "
     "images of the definitions used by each source.")

h(2, "3.2. Systematic and residual disagreement")
para("Of 663 and 726 records, 642 formed algorithmically matched candidate "
     "pairs, their centroid sizes correlating at r = 1.0000. All figures "
     "below are computed on these pairs.")
para("Half the mean squared disagreement between the two sets was 0.000110, "
     "with a 95% interval of 0.000074 to 0.000155 (Table II). Of that, 34.8% "
     "is a mean displacement of 0.00875 Procrustes units (95% CI 0.00844 to "
     "0.00916) and the remainder is residual disagreement, which is not "
     "demonstrably independent noise.")
para("The residual term depends on the matching, so two sensitivity "
     "scenarios are reported. Excluding the 34 pairs whose distance exceeds "
     "three times the median, the median distance is 0.00952 and half the "
     "mean squared disagreement falls to 0.000052 (95% CI 0.000048 to "
     "0.000056). Those pairs could be correct matches with real "
     "disagreement, incorrect matches, or a difference of landmark "
     "definition. Neither scenario is preferred, and neither is a bound: "
     "with the true matching unknown, they do not limit the disagreement "
     "mathematically. The distribution, including the four largest distances "
     "up to 0.134, is shown in Fig. 1.")
para("Total and residual disagreement are distinguished. Half the mean "
     "squared disagreement is a total; removing half the squared mean "
     "displacement leaves the residual. On all 642 pairs that is 0.000110 "
     "total, 0.0000383 displacement and 0.0000719 residual; on the retained "
     "608 it is 0.000052, 0.0000375 and 0.0000146. The displacement share "
     "rises from 34.8% to 72.0%, because excluding the 34 removes residual "
     "scatter and leaves the displacement almost untouched (Table II).")
rich([("The displacement is the consequential part, because it does not "
       "diminish with averaging", B),
      (". A displacement is a bias and not a variance component, so it is "
       "compared against the distances a classifier must resolve rather than "
       "expressed as a share of variance. In this dataset the median distance "
       "between colony means is 0.01974 across 74 colonies and 2,701 colony "
       "pairs, so the displacement is 0.44 times that. It is smaller than "
       "the tenth percentile of those distances, 0.01459, and exceeds only "
       "0.2% of them, 6 of 2,701 (Table III, Fig. 2). Two colony-level "
       "summaries are distinguished. The magnitude of the average "
       "displacement vector over the 73 colonies measured by both sets, "
       "computed from the colony difference vectors, is 0.00878, close to "
       "the pooled figure of 0.00875, which is what a constant displacement "
       "predicts; the median magnitude of the colony-specific displacements "
       "is 0.00909, a median of lengths rather than the length of a mean.",
       N)])
para("Whether a displacement of this size defeats a particular classifier "
     "depends on its direction relative to the discriminant axes and not on "
     "this ratio alone. The ratio is a scale comparison; the transfer test "
     "in Section 3.4 is the evidence.")

h(3, "3.2.1. The disagreement is localized at two landmarks")
para("The disagreement is not spread across the configuration. Landmarks 7 "
     "and 14 carry 94.0% of the squared mean displacement on all 642 "
     "candidate pairs and 94.3% on the 608 retained, against 10.5% if it "
     "were divided evenly. The localization therefore holds with the "
     "disputed pairs included. Their RMS disagreement on the retained pairs, "
     "0.00732 and 0.00580, is 6.4 times the median of 0.00102 across the "
     "other seventeen (Fig. 4). The landmark-matching step of "
     "Section 2.2 reached the same two landmarks independently: residuals "
     "between the two mean shapes were 0.00654 at landmark 7 and 0.00567 at "
     "landmark 14, against 0.00241 or less at all seventeen others.")
para("These are the two landmarks whose position Nawrocka et al. (2018) "
     "report changing relative to Gerula et al. (2009). The pattern is what "
     "a difference in landmark convention would produce. It is not proof of "
     "one: neither deposit records which version of the configuration its "
     "operators worked from, and an operator effect concentrated at the two "
     "least determinate junctions would look similar. What the localization "
     "does establish is that the displacement is not diffuse digitizing "
     "noise, and that a correction, if one is wanted, has a specific target.")
para("Recomputing the displacement under 200 random re-pairings of the same "
     "wings returned 0.00875 each time, to five decimal places. The "
     "displacement is a difference of grand means and carries no information "
     "about which wing is paired with which, so the central estimate does "
     "not rest on the matching. Removing the 34 largest discrepancies moves "
     "it from 0.00875 to 0.00866, a change of 1.1%, while total disagreement "
     "falls by 53% and residual disagreement by 80%.")

h(3, "3.2.2. Part of the matching uncertainty is explained by repeated "
      "records")
para("The image archive of the first Ecuadorian deposit holds 75 files of "
     "which 70 are distinct by published checksum; five filenames carry the "
     "content of another file bearing the same apiary prefix. That "
     "duplication reaches the coordinates. Of the 663 wing records, ten are "
     "byte-identical copies of other records: one on image R2C2 of apiary "
     "13, and a block of nine on image JSC1 of apiary 6, re-entered as "
     "records 535 to 543. Every duplicate lies within the same image and "
     "apiary as its original, so no record is shared between apiaries and "
     "comparisons between colonies cannot be affected by them.")
para("Removing the ten and repeating the analysis leaves 632 matched "
     "candidate pairs and reduces the number above three times the median "
     "from 34 to 28, because two identical records compete for distinct "
     "partners and one of them is necessarily matched to the wrong wing. Six "
     "of the large discrepancies are therefore an artefact of repeated "
     "records rather than digitizing disagreement. The mean displacement is "
     "unchanged at 0.00875 and half the mean squared disagreement moves from "
     "0.000110 to 0.000105 (Table III). This is noted so that others reusing "
     "the deposit can allow for it, and it narrows but does not close the "
     "question of the remaining 28.")

h(3, "3.2.3. Bilateral wings estimate a different component")
para("The 1,689 bilateral pairs give variances of 0.000091, 0.000089 and "
     "0.000089 in Algeria 2018, Serbia and Algeria 2024 respectively, with "
     "narrow intervals (Table II). These figures are of the same order as the "
     "between-group estimate but are not a replicate of it: a left-right "
     "difference contains fluctuating asymmetry as well as within-session "
     "digitizing error, so it bounds each from above. No agreement between "
     "the two routes is claimed, and separating asymmetry from digitizing "
     "error would require repeated digitization of bilateral wings, which none "
     "of the deposits located here provides.")
para("The estimated directional asymmetry of shape was small in all three "
     "datasets. No test of absence is offered: a small estimate does not "
     "establish that no side difference exists, and the published position is "
     "divided. Janczyk and Tofilski (2021) report that forewing shape does "
     "not differ between body sides while size does, whereas Szentgyorgyi et "
     "al. (2016) report significant, though dissimilar, shape differences "
     "between sides in workers and drones. These estimates are consistent "
     "with a small effect and do not resolve the disagreement.")

h(2, "3.3. Differences between datasets")
para("With all nine datasets in one Procrustes fit, differences between grand "
     "means increase as the datasets share less (Table IV). These are "
     "differences between datasets, not measurement effects: the datasets "
     "also differ in population, subspecies composition, breeding history, "
     "geography and collection year, and no decomposition of those causes is "
     "available here.")
para("Two reference points frame the scale. Two hundred random splits of the "
     "reference's own colonies into halves gave a median difference of "
     "0.00559, with a 2.5th to 97.5th percentile range of 0.00316 to 0.01064. "
     "Differences between subspecies within that reference run 0.01941 to "
     "0.03216. The split-half interval is wide enough to overlap the "
     "systematic displacement of section 3.2, so the lower tiers in Table IV "
     "are not cleanly separated.")
para("Two pairs are informative about cause. The same candidate pairs "
     "landmarked by two groups differ by 0.00875, which is measurement "
     "disagreement alone. The Californian and Argentine transects, measured "
     "in one batch by one group, differ by 0.00780 across two continents. Six "
     "of the eight largest differences involve the single dataset measured by "
     "another group. These observations are consistent with measurement "
     "contributing materially; they do not establish that it outweighs "
     "biology, and no decomposition is claimed.")

h(2, "3.4. Classification does not transfer without calibration")
rich([("The Wegrzynowicz material tests transfer where the answer is known: "
       "9,590 wings from 200 queens in 24 genotypes by instrumental "
       "insemination, of which 9,464 wings in 198 colony groups remain after "
       "the two conflicting identifiers are excluded, covering pure lines, "
       "six reciprocal F1 combinations and twelve backcrosses of ", N), ("A. m. carnica", I), (", ", N),
      ("A. m. caucasica", I), (" and ", N), ("A. m. mellifera", I),
      (". Those three subspecies lie in three lineages, so every cross is a "
       "between-lineage cross.", N)])
para("Two colony identifiers, 0489_12 and 0203_13, appear under two "
     "genotype labels each, which cannot both be right for one "
     "instrumentally inseminated queen. In both cases one entry carries the "
     "bulk of the wings and the other is sparse: 0489_12 has 41 wings as "
     "P1kk and one as P1mm, and 0203_13 has 59 as P1mm and 25 as BCkmk. "
     "Both identifiers are excluded before the centring offset is fitted, "
     "and the cross-dataset analysis was rerun rather than filtered "
     "afterwards. Refitting changed no assignment and moved the offset "
     "between dataset grand means from 0.02470 to 0.02475. The exclusion "
     "removes one of the two pure-line colonies that centring had failed to "
     "recover, the one-wing P1mm entry; the other, a P1cc colony, remains "
     "misassigned and is the reason the centred caucasica result is four of "
     "five rather than five of five (Table V).")
para("The reference separates its own subspecies in 41 of 41 colonies by "
     "leave-one-colony-out. That shows these three subspecies are separable "
     "within that collection; it does not establish that the model is well "
     "specified, and it carries no uncertainty estimate of its own.")
rich([("Applied across datasets without adjustment, the classifier assigns "
       "zero or one of five colonies of known pure ", N),
      ("A. m. caucasica", I),
      (" correctly across 6 to 20 principal components, calling the rest ",
       N), ("carnica", I), (" or ", N), ("mellifera", I),
      (" (Tables V and VI). The evidence is five colonies, two of P0cc and "
       "three of P1cc, not the 9,464 wings analysed: the other pure "
       "lines were assigned correctly without adjustment and so show no "
       "failure. Centring recovers two to four of five (Table VI). The apparently correct calls "
       "carry little weight either: the four retained P1kk colonies sat "
       "0.02903 from "
       "the ", N), ("carnica", I), (" centroid and 0.02977 from the ", N),
      ("mellifera", I),
      (" one, a margin of 0.00074. That is an order of magnitude below the "
       "offset between the dataset grand means, 0.02475, and about a twelfth "
       "of the measurement displacement of 0.00875.", N)])

h(3, "3.4.1. Grand-mean centering, as a sensitivity analysis")
para("Centring each dataset on its own grand mean recovers two to four of "
     "the five caucasica colonies depending on classifier dimension "
     "(Table VI). This is reported as a sensitivity analysis and not as a "
     "recommended correction. The reference contains three subspecies and the "
     "target contains pure lines, hybrids and backcrosses, so their "
     "biological compositions differ and centring removes real biological "
     "difference along with any technical displacement. Improved "
     "classification afterwards does not establish that what was removed was "
     "technical. An operational correction would need to be estimated from "
     "separate calibration specimens and evaluated on held-out colonies, "
     "which these data do not permit.")

h(3, "3.4.2. Hybrids are forced into pure classes")
para("Assignment counts for the pure lines and the six F1 genotypes are in "
     "Table VII, and for all twelve backcross genotypes, comprising 98 "
     "genotype-colony groups, in Table VIII. Fig. 3 summarises the "
     "assignments by genotype group. Across 83 F1 colonies, 36.1% were "
     "assigned to the queen's subspecies and 55.4% to the drone's. "
     "Reciprocal pairs of the same expected ancestry proportions were "
     "assigned differently, and one genotype, F1mc, produced an exact "
     "three-way tie of four colonies to each class.")
para("This is reported as a limitation of forcing hybrids into pure classes "
     "when the reference contains no hybrid class, not as evidence about "
     "parental direction. Reciprocal crosses share expected ancestry "
     "proportions but not nuclear genotypes: different parental individuals, "
     "maternal effects and cytoplasmic inheritance all remain in play. "
     "Wegrzynowicz et al. (2019) found hybrid wing shape closer to the "
     "maternal than the paternal colony when compared with those colonies "
     "directly, which is a different comparison from the one made here. "
     "Backcrosses at 3:1 composition matched their majority subspecies at a "
     "median of 80% across the twelve genotypes, with a range from 30% to "
     "100% (Table VIII).")

h(2, "3.5. An exploratory scale, and its limits")
para("Procrustes units are hard to judge, so differences were projected onto "
     "a direction fitted to genome-wide African ancestry in 268 sequenced "
     "bees. Measured ancestry explains 5.7% of shape variation, at 0.02252 "
     "Procrustes units per unit ancestry.")
para("The scale can be checked against a known quantity, and it partly "
     "fails. Measured African ancestry averages 20.33% in the Californian "
     "bees and 40.74% in the Argentine ones, a difference of 20.4 percentage "
     "points. The projection returns 31% for that pair, overstating the "
     "measured difference by about half. Converted equivalents for the other "
     "comparisons are given in Table IX and should be read as exploratory "
     "only. Projection is nevertheless necessary rather than optional. The "
     "median absolute cosine between a dataset difference and the ancestry "
     "direction is 0.237, against a median of 0.118 for directions drawn at "
     "random in 34 dimensions. That reference distribution is simulated from "
     "random directions and is not a permutation of the observed data, so it "
     "describes a scale and supports no test. No significance is claimed for "
     "any individual comparison, and the 36 comparisons are not independent, "
     "since each dataset enters eight of them. Alignments vary widely across "
     "the set, from near-orthogonal to 0.889 (Table IX). Using unprojected "
     "lengths inflates the equivalents about fourfold.")
para("Size could not be assessed. ImageJ wing length measured by one group "
     "correlates with Procrustes centroid size measured by another at 0.50 "
     "across all 268 wings but 0.82 within a single imaging session, because "
     "that dataset records no image resolution and centroid size is in pixels "
     "on a changing scale. Tip-to-base length and the centroid size of 19 "
     "landmarks are in any case different quantities.")

h(2, "3.6. Within-colony variance: a descriptive observation")
para("Within-colony shape variance was compared across datasets of known "
     "mating structure, and the comparison is reported as descriptive only. "
     "Colonies inseminated with semen from a single drone showed the highest "
     "raw within-colony variance of the three datasets, 0.000483 against "
     "0.000273 in Serbia and 0.000425 in Algeria 2018; these are descriptive "
     "variances with no error floor subtracted. Mating structure and dataset "
     "are completely confounded here, and single-drone colonies still contain "
     "genetically variable workers because the queen transmits different "
     "alleles. The comparison therefore supports no inference about either "
     "polyandry or measurement, and within-colony variance is not recommended "
     "as a quantity to compare between datasets.")

# ---------------------------------------------------------------- discussion
h(1, "4. Discussion")
para("Wing geometric morphometrics performs well within the dataset on which "
     "it was calibrated. The reference separates its own subspecies without "
     "error, and nothing here questions the method on that ground. What this "
     "study bears on is transfer.")
para("That a systematic error survives averaging while a random one does "
     "not is an elementary statistical fact and is not offered as a finding. "
     "The contribution here is empirical: a measurement of how large that "
     "systematic part is between two groups working independently on the same "
     "honey bee wing images, which has not previously been quantified. About "
     "a third of their disagreement is a constant displacement, and that "
     "displacement is 0.44 times the median distance between colony means in "
     "the same dataset.")
para("Machlowska et al. (2025) reached the practical conclusion already, "
     "recommending remeasurement by the same person or algorithm in order to "
     "avoid systematic measurement error. The present result puts a number on "
     "what that recommendation guards against, and shows it to be of the same "
     "order as the signal a classifier must resolve.")
para("The misassignment of known pure lines in a separately produced dataset "
     "is consistent with such a displacement, and the Ecuadorian comparison "
     "shows that a displacement of sufficient size occurs. It does not "
     "establish that a displacement caused those misassignments: the two "
     "results come from different datasets and different measurement "
     "comparisons, and the cross dataset offers no replicate measurement of "
     "its own. The mechanism is plausible and untested.")
para("Three practical consequences follow.")
rich([("Verify landmark configurations before pooling. ", B),
      ("One dataset of nine was computationally incompatible and the failure "
       "was silent. Computational matching is necessary but not sufficient: "
       "anatomical definitions should be compared from the source "
       "publications, with annotated images.", N)])
rich([("Treat reference transfer as requiring calibration. ", B),
      ("Applied across datasets without adjustment, the classifier failed on "
       "specimens whose identity was not in doubt. Grand-mean centring "
       "recovered them but cannot be recommended on this evidence, because it "
       "removes biological difference alongside technical displacement. "
       "Calibration specimens measured by both parties would be the "
       "defensible route.", N)])
rich([("Do not expect averaging to solve it. ", B),
      ("A displacement is unaffected by sample size, so a single pooled "
       "disagreement figure understates the risk to colony means. Report the "
       "displacement and the residual separately.", N)])

h(2, "4.1. Scope")
para("The risk identified here falls on a specific class of analysis. "
     "Machlowska et al. (2026) assigned 1,342 colony samples from ten "
     "countries to the four lineages, using material prepared and measured by "
     "the same group as the reference. Differences between that reference and "
     "five of six other datasets from its own group ran 0.00978 to 0.01657, "
     "below the 0.01941 to 0.03216 range separating subspecies within it. "
     "These results do not call such within-group conclusions into question; "
     "they bound the conditions under which they hold. The exposure lies with "
     "analyses combining a reference with material another group prepared and "
     "measured, and with pooling datasets of mixed provenance into a single "
     "reference.")

h(2, "4.2. Limitations")
para("Dataset, population and digitizing group are confounded throughout the "
     "public record. Apart from the Ecuadorian pair, no two groups have "
     "measured the same population, so differences between datasets are total "
     "divergence and are described as such. Only the Ecuadorian comparison "
     "isolates measurement, and only the split-half baseline is purely "
     "sampling; that baseline's interval is wide enough to overlap the "
     "measurement displacement.")
para("The measurement estimate rests on one pair of groups and one set of "
     "images. Its two components differ in how far they depend on the "
     "matching: total disagreement changed approximately twofold between the "
     "two sensitivity scenarios, whereas the mean displacement changed by "
     "1.1%. The pairs are algorithmically matched and have not been audited "
     "against the images; that audit remains the most important outstanding "
     "check, although repeated records in the deposit account for six of "
     "the 34 large discrepancies. "
     "Fluctuating asymmetry and within-session digitizing error remain "
     "confounded. The ancestry scale overstates a measured difference by half "
     "and is exploratory. Whether the disagreement on landmarks 7 and 14 "
     "reflects observer variation or a difference of convention is unresolved.")

h(2, "4.3. What would settle it")
para("A replicated observer experiment would separate what this study cannot: "
     "several observers independently digitizing a shared image panel twice, "
     "with blinded identities and randomized order, analysed as variance "
     "components for specimen, observer and repeatability. Isolating "
     "preparation effects additionally requires shared physical specimens "
     "prepared and imaged under controlled comparison. Neither is expensive, "
     "and neither appears in the deposits located by the search described in "
     "the Methods. The Ecuadorian pair exists only because two groups "
     "happened to measure the same material without coordinating.")
para("Until then the practical reading is narrow. Shared personnel and "
     "protocols reduce the risk of displacement but do not guarantee "
     "transferable classification, and independent validation on held-out "
     "colonies is advisable even within one group. Applying a reference to "
     "material another group prepared requires calibration against shared "
     "specimens, and cannot rely on averaging more wings.")

# ------------------------------------------------------------ back matter
h(1, "Acknowledgements")
para("This analysis exists because several groups deposited their wing "
     "coordinates openly under licences permitting reuse: A. Oleksa, A. "
     "Tofilski and colleagues for the reference and the European, Serbian, "
     "Algerian and re-measured collections; D. Masaquiza and A. Arenal for "
     "the Ecuadorian wings; E. Calfee, G. Coop and colleagues for the "
     "Africanized wings and their sequenced metadata; and P. Wegrzynowicz and "
     "A. Los for the only honey bee wing material with known pedigree. The "
     "central estimate was possible only because two groups independently "
     "landmarked the same Ecuadorian images and both published the result.")

h(1, "Declarations")
rich([("Funding. ", B), ("No specific funding was received.", N)])
rich([("Competing interests. ", B),
      ("The authors declare no competing interests.", N)])
rich([("Ethics approval. ", B),
      ("Not applicable. No specimens were collected and no live animals "
       "handled; all data analysed are published open deposits.", N)])
rich([("Consent. ", B), ("Not applicable.", N)])
rich([("Data availability. ", B),
      ("Every dataset analysed is a published open deposit, listed with its "
       "DOI in Table X. Several carry the Open Database License v1.0 and "
       "its share-alike requirement; derived tables are released under the "
       "same licence with attribution. Analysis code and all generated "
       "results are at https://github.com/vkcvaibhav-eng/"
       "honeybee-wing-reliability- and are archived at "
       "https://doi.org/10.5281/zenodo.23906962, with every figure and table "
       "reproduced by running the numbered scripts in sequence.", N)])

h(1, "References")
REFS = [
    [("Calfee, E., Agra, M.N., Palacio, M.A., Ramirez, S.R., Coop, G. (2020) "
      "Selection and hybridization shaped the rapid spread of African honey "
      "bee ancestry in the Americas. PLoS Genet. 16 (10), e1009038. "
      "https://doi.org/10.1371/journal.pgen.1009038", N)],
    [("Janczyk, A., Tofilski, A. (2021) Monthly changes in honey bee "
      "forewings estimated using geometric morphometrics. J. Apic. Sci. 65 "
      "(1), 139-146. https://doi.org/10.2478/jas-2021-0002", N)],
    [("Machlowska, J., Kandemir, I., Ozkan Koca, A., Kakhniashvili, V., "
      "Alattal, Y., et al. (2025) Variation of honey bee wings in "
      "southwestern Asia. Sci. Data. "
      "https://doi.org/10.1038/s41597-025-06234-8", N)],
    [("Machlowska, J., Gerula, D., Oleksa, A., Kok, H., McCormack, G.P., et "
      "al. (2026) Country specific hybridization of honey bees from lineage "
      "M. Gigascience 15, giag093. "
      "https://doi.org/10.1093/gigascience/giag093", N)],
    [("Masaquiza, D., Arenal, A. (2024) Collection of images and raw "
      "coordinates of honey bee (", N), ("Apis mellifera", I),
     (") wings from the central highlands of Ecuador [dataset]. Zenodo. "
      "https://doi.org/10.5281/zenodo.13340594", N)],
    [("Gerula, D., Tofilski, A., Wegrzynowicz, P., Skowronek, W. (2009) "
      "Computer-assisted discrimination of honeybee subspecies used for "
      "breeding in Poland. Journal of Apicultural Science 53 (2), 105-114",
      N)],
    [("Nawrocka, A., Kandemir, I., Fuchs, S., Tofilski, A. (2018) Computer "
      "software for identification of honey bee subspecies and evolutionary "
      "lineages. Apidologie 49 (2), 172-184. "
      "https://doi.org/10.1007/s13592-017-0538-y", N)],
    [("Oleksa, A., Tofilski, A. (2015) Wing geometric morphometrics and "
      "microsatellite analysis provide similar discrimination of honey bee "
      "subspecies. Apidologie 46 (1), 49-60. "
      "https://doi.org/10.1007/s13592-014-0300-7", N)],
    [("Oleksa, A., Cauia, E., Siceanu, A., Puskadija, Z., Kovacic, M., et al. "
      "(2023) Honey bee (", N), ("Apis mellifera", I),
     (") wing images: a tool for identification and conservation. "
      "Gigascience 12, giad019. "
      "https://doi.org/10.1093/gigascience/giad019", N)],
    [("Ruttner, F. (1988) Biogeography and taxonomy of honeybees. "
      "Springer-Verlag, Berlin", N)],
    [("Szentgyorgyi, H., Czekonska, K., Tofilski, A. (2016) Influence of "
      "pollen deprivation on the fore wing asymmetry of honeybee workers and "
      "drones. Apidologie 47, 653-662. "
      "https://doi.org/10.1007/s13592-015-0415-5", N)],
    [("Wegrzynowicz, P., Los, A. (2020) Dataset of wing venation measurements "
      "for ", N), ("Apis mellifera caucasica", I), (", ", N),
     ("A. mellifera carnica", I), (" and ", N),
     ("A. mellifera mellifera", I),
     (" (Hymenoptera: Apidae), their hybrids and backcrosses. Biodivers. "
      "Data J. 8, e53724. https://doi.org/10.3897/BDJ.8.e53724", N)],
    [("Wegrzynowicz, P., Gerula, D., Tofilski, A., Panasiuk, B., Bienkowska, "
      "M. (2019) Maternal inheritance in hybrids of three honey bee "
      "subspecies. J. Apic. Sci. 63 (1). "
      "https://doi.org/10.2478/jas-2019-0010", N)],
]
for r in REFS:
    p = rich(r)
    p.paragraph_format.first_line_indent = Cm(-1)
    p.paragraph_format.left_indent = Cm(1)

# --------------------------------------------------------- captions + tables
CAPS = [
    ("Table I.", "The nine analytical datasets, with bees after bilateral "
     "averaging, digitizing group and material. They derive from seven "
     "sources; the Ecuadorian wings appear twice and the two Calfee sets are "
     "subsets of one collection."),
    ("Table II.", "Disagreement between two measurement sets of the same "
     "candidate pairs, and within-bee disagreement from bilateral wings. Half "
     "the mean squared disagreement is E[d-squared]/2 throughout. Intervals "
     "are bootstrap percentile intervals over colonies."),
    ("Table III.", "The displacement between measurement sets, its dependence "
     "on the matching, its localization and its separation from residual "
     "disagreement, against the distances between colony means. The two "
     "matching scenarios are sensitivity analyses, not bounds. No share of "
     "variance is implied: a displacement is a bias, not a variance "
     "component."),
    ("Table IV.", "Differences between dataset grand means. These are "
     "differences between datasets, which differ in population and "
     "provenance as well as measurement."),
    ("Table V.", "Assignment of known pure parental lines, uncorrected and "
     "after grand-mean centring, at 12 principal components, with the two "
     "conflicting colony identifiers excluded. Percentages are colonies "
     "assigned to the expected subspecies."),
    ("Table VI.", "Sensitivity of the transfer result to classifier "
     "dimension. The five colonies are the two P0cc and three P1cc colonies "
     "of known pure A. m. caucasica."),
    ("Table VII.", "Assignment counts for the pure lines and the six "
     "reciprocal F1 genotypes, after centring, with the two conflicting "
     "colony identifiers excluded. No modal class is reported."),
    ("Table VIII.", "Assignment counts for all twelve backcross genotypes, "
     "after centring, with the two conflicting colony identifiers excluded."),
    ("Table IX.", "Dataset differences converted to apparent African "
     "ancestry after projection. Exploratory: the scale returns 31% for a "
     "pair whose measured difference is 20.4 percentage points."),
    ("Table X.", "Published deposits analysed, with DOIs."),
]
FIGCAPS = [
    ("Fig. 1", "Distribution of Procrustes distances between the two "
     "measurements of each algorithmically matched candidate pair (n = 642). "
     "a, linear scale to 0.04. b, the complete distribution on a logarithmic "
     "scale, including the four distances above 0.04 and the maximum of "
     "0.134. Solid line, median 0.00964; dashed line, three times the "
     "median, the cut used for the sensitivity analysis, above which 34 "
     "pairs fall."),
    ("Fig. 2", "The displacement between the two measurement sets, with its "
     "bootstrap interval shaded, against the distances between colony means. "
     "Colony means are from the re-measured Ecuadorian set, 74 colonies with "
     "three or more wings giving 2,701 pairwise distances. Those distances "
     "share colonies and are not independent: each colony enters 73 of them. "
     "Values correspond to Table III."),
    ("Fig. 3", "Assignment of cross-dataset colonies by genotype group at 12 "
     "principal components, a before and b after grand-mean centring, with "
     "the two conflicting colony identifiers excluded. Cell labels are "
     "colony counts; shading gives the proportion within each row."),
    ("Fig. 4", "Root-mean-square disagreement between the two measurement "
     "sets at each landmark, on the 608 retained pairs, in units of centroid "
     "size. Landmarks 7 and 14, shaded, are the two whose position Nawrocka "
     "et al. (2018) report changing relative to Gerula et al. (2009). "
     "Dashed line, the median across the other seventeen. The bars are RMS "
     "disagreement, which includes residual scatter; the 94% quoted in the "
     "text is the share of the squared mean displacement, a different "
     "quantity computed from the mean difference vector alone."),
]
br()
h(1, "Figure captions")
for lab, txt in FIGCAPS:
    rich([(lab + " ", B), (txt, N)])

TABLES = [
    ("Table I.", ["Dataset", "Bees", "Digitizing group", "Material"], [
        ["Oberursel reference", "1,832", "Krakow", "25 subspecies, 4 lineages"],
        ["Wegrzynowicz crosses", "9,464 of 9,590", "Skierniewice",
         "200 queens, 24 genotypes, instrumental insemination"],
        ["Serbia", "1,217", "Krakow", "60 colonies"],
        ["Ecuador, re-measured", "726", "Krakow", "central highlands"],
        ["Masaquiza, original", "663", "Ecuador team", "the same wings"],
        ["Algeria 2018", "460", "Krakow", "46 colonies"],
        ["Calfee Argentina, re-measured", "177", "Krakow", "hybrid zone"],
        ["Algeria 2024", "165", "Krakow", "13 colonies"],
        ["Calfee California, re-measured", "99", "Krakow", "hybrid zone"],
    ]),
    ("Table II.", ["Comparison", "n", "Median d", "Half mean squared "
                   "disagreement", "95% CI", "Mean displacement"], [
        ["Two measurement sets, all candidate pairs", "642", "0.00964",
         "0.000110", "0.000074 to 0.000155", "0.00875 (0.00844 to 0.00916)"],
        ["Two measurement sets, excluding 34 largest", "608", "0.00952",
         "0.000052", "0.000048 to 0.000056", "0.00866"],
        ["Algeria 2018, within bee (bilateral)", "460", "0.01303", "0.000091",
         "0.000087 to 0.000095", "small"],
        ["Serbia, within bee (bilateral)", "1,065", "0.01286", "0.000089",
         "0.000087 to 0.000092", "small"],
        ["Algeria 2024, within bee (bilateral)", "164", "0.01276", "0.000089",
         "0.000081 to 0.000095", "small"],
    ]),
    ("Table III.", ["Quantity", "Value"], [
        ["Mean displacement between measurement sets", "0.00875"],
        ["95% interval on that displacement", "0.00844 to 0.00916"],
        ["Same, under 200 random re-pairings of the same wings", "0.00875"],
        ["Same, excluding the 34 largest discrepancies", "0.00866"],
        ["Share of the squared mean displacement at landmarks 7 and 14, "
         "all 642 / retained 608", "94.0% / 94.3%"],
        ["Colonies with 3 or more wings / pairwise distances", "74 / 2,701"],
        ["Median distance between colony means", "0.01974"],
        ["10th percentile of those distances", "0.01459"],
        ["Displacement / median colony separation", "0.44"],
        ["Colony-mean distances below the displacement", "0.2% (6 of 2,701)"],
        ["Length of the mean of the 73 colony difference vectors", "0.00878"],
        ["Median length of the colony-specific displacements", "0.00909"],
        ["Half mean squared total disagreement, all 642 / retained 608",
         "0.000110 / 0.000052"],
        ["Half the squared mean displacement, all 642 / retained 608",
         "0.0000383 / 0.0000375"],
        ["Residual after removing it, all 642 / retained 608",
         "0.0000719 / 0.0000146"],
        ["Displacement share of the total, all 642 / retained 608",
         "34.8% / 72.0%"],
        ["Byte-identical duplicate records in the 663 deposited", "10"],
        ["Pairs above three times the median, as published / duplicates "
         "removed", "34 / 28"],
        ["Mean displacement, as published / duplicates removed",
         "0.00875 / 0.00875"],
    ]),
    ("Table IV.", ["Comparison", "Pairs", "Median difference", "Range"], [
        ["Same group, same region", "1", "0.01256", "-"],
        ["Same group, other region", "20", "0.01711", "0.00780 to 0.02458"],
        ["Different group", "15", "0.02398", "0.00891 to 0.03451"],
        ["Reference split-half baseline", "200 splits", "0.00559",
         "0.00316 to 0.01064"],
        ["Between subspecies within the reference", "3", "-",
         "0.01941 to 0.03216"],
        ["Same candidate pairs, two groups (measurement)", "1", "0.00875",
         "0.00844 to 0.00916"],
    ]),
    ("Table V.", ["Genotype", "Expected", "Colonies", "Uncorrected",
                  "Centred"], PURE_ROWS),
    ("Table VI.", ["Principal components", "Reference accuracy",
                   "Pure caucasica correct, uncorrected", "After centring"], [
        ["6", "41/41", "0/5", "2/5"],
        ["8", "41/41", "1/5", "4/5"],
        ["10", "41/41", "0/5", "4/5"],
        ["12", "41/41", "0/5", "4/5"],
        ["16", "41/41", "1/5", "4/5"],
        ["20", "41/41", "0/5", "3/5"],
    ]),
    ("Table VII.", ["Genotype", "Queen", "Drone", "Colonies", "carnica",
                    "caucasica", "mellifera"], F1_ROWS),
    ("Table VIII.", ["Genotype", "Majority subspecies", "Colonies",
                     "carnica", "caucasica", "mellifera"], BC_ROWS),
    ("Table IX.", ["Comparison", "Difference", "Alignment",
                   "Apparent A ancestry"], [
        ["Same candidate pairs, two groups (measurement)", "0.00875", "0.216",
         "9%"],
        ["Two continents, one group and batch", "0.00780", "0.889", "31%"],
        ["Measured ancestry difference for that pair", "-", "-",
         "20.4 points"],
        ["One group and region, two collection years", "0.01256", "0.337",
         "19%"],
        ["Median across all 36 dataset pairs", "-", "-", "21%"],
    ]),
    ("Table X.", ["Deposit", "DOI"], [
        ["Oberursel reference", "10.5281/zenodo.7567336"],
        ["Wegrzynowicz and Los, crosses and backcrosses",
         "10.3897/BDJ.8.e53724"],
        ["Serbia", "10.5281/zenodo.10389960"],
        ["Algeria 2018", "10.5281/zenodo.18359322"],
        ["Algeria 2024", "10.5281/zenodo.13939415"],
        ["Masaquiza and Arenal, Ecuador", "10.5281/zenodo.13340594"],
        ["Ecuador, re-measured", "10.5281/zenodo.14604363"],
        ["Calfee et al., re-measured", "10.5281/zenodo.14604479"],
        ["Calfee et al., wing images", "10.25338/B8T032"],
        ["Europe, 13 countries", "10.5281/zenodo.7244070"],
        ["Northwestern Europe", "10.5281/zenodo.18845767"],
        ["Southwestern Asia", "10.5281/zenodo.17075125"],
    ]),
]

br()
h(1, "Tables")
for k, (lab, hdr, rows) in enumerate(TABLES):
    cap = next(c for l, c in CAPS if l == lab)
    rich([(lab + " ", B), (cap, N)])
    t = doc.add_table(rows=1, cols=len(hdr)); t.style = "Table Grid"
    for j, cell in enumerate(hdr):
        p = t.rows[0].cells[j].paragraphs[0]
        r = p.add_run(cell); r.bold = True
        r.font.name = "Times New Roman"; r.font.size = Pt(10)
        p.paragraph_format.line_spacing = 1.0
    for row in rows:
        cs = t.add_row().cells
        for j, v in enumerate(row):
            p = cs[j].paragraphs[0]
            r = p.add_run(v)
            r.font.name = "Times New Roman"; r.font.size = Pt(10)
            p.paragraph_format.line_spacing = 1.0
    if k < len(TABLES) - 1:
        br()

doc.save(OUT)
print("wrote", OUT)
