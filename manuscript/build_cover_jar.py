#!/usr/bin/env python3
"""Cover letter for the Journal of Apicultural Research submission."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.paragraph_format.line_spacing = 1.15
st.paragraph_format.space_after = Pt(10)
for s in doc.sections:
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(2.5)


def p(t="", bold=False, align=None):
    par = doc.add_paragraph()
    r = par.add_run(t)
    r.bold = bold
    if align is not None:
        par.alignment = align
    return par


p("V. K. Chaudhari", bold=True)
p("AINP on Agricultural Acarology, Department of Entomology")
p("N. M. College of Agriculture, Navsari Agricultural University")
p("Navsari 396450, Gujarat, India")
p("vkcvaibhav@gmail.com")
p()
p("6 November 2026")
p()
p("The Editor")
p("Journal of Apicultural Research")
p()
p("Dear Editor,")

p("We submit for consideration as an Original Research Article a manuscript "
  "entitled “Measurement disagreement concentrated at two landmarks "
  "limits the transfer of honey bee wing morphometric references”.")

p("Identification of honey bee subspecies from forewing venation now rests "
  "on large open reference datasets, and almost every application of them "
  "assumes that a reference landmarked in one laboratory applies to wings "
  "landmarked in another. Meixner et al. (2013), in the COLOSS BEEBOOK "
  "chapter on characterising subspecies and ecotypes, emphasised the "
  "importance of consistency of methods between laboratories if results are "
  "to be comparable, and Bouga et al. (2011) reached the same conclusion. "
  "Neither recommendation has been tested against data, because testing it "
  "requires the same physical wings to be landmarked twice, independently, "
  "and both results published. We located the one case in the public record "
  "where that has happened.")

p("The study is built around three stated predictions rather than a "
  "description of a dataset. If the two groups worked to different versions "
  "of the 19-point configuration, disagreement should concentrate at "
  "landmarks 7 and 14, the two that Nawrocka et al. (2018) record as having "
  "been moved from the convention of Gerula et al. (2009); if it reflects "
  "ordinary operator variation it should be spread across the nineteen "
  "points. If the disagreement is a constant displacement rather than "
  "random scatter it should survive random re-pairing of the wings and not "
  "diminish with averaging. And if a displacement of that size matters in "
  "practice, a reference classifier should misassign colonies of known "
  "parentage in a dataset produced elsewhere. All three predictions were "
  "met: about 94% of the squared mean displacement falls on those two "
  "landmarks against roughly 10% expected under an even spread; the "
  "displacement of 0.00875 Procrustes units is unchanged under 200 random "
  "re-pairings; and a classifier that separated its own subspecies in 41 of "
  "41 colonies assigned zero or one of five colonies of known pure Apis "
  "mellifera caucasica correctly across 6 to 20 principal components.")

p("We present the convention difference as a plausible explanation rather "
  "than a demonstrated one, since no deposit records which version its "
  "operators used. That is itself the practical point, and the manuscript "
  "ends with four items of metadata that would settle it and that cost "
  "nothing to record.")

p("The work is entirely a reanalysis of published open deposits and exists "
  "only because several groups released their coordinates under licences "
  "permitting reuse. We have framed it as a measurement question the field "
  "has itself raised, not as a criticism of any dataset or group. Analysis "
  "code and all generated results are archived at "
  "https://doi.org/10.5281/zenodo.23906962, and every figure and table is "
  "reproduced by running the deposited scripts in sequence.")

p("The manuscript is 4,870 words including tables, references and figure "
  "captions, and contains three tables and three figures. It uses "
  "continuous line numbering. It is original, is not under consideration "
  "elsewhere, and both authors have read and approved the submitted "
  "version. We declare no competing interests and no funding was obtained. "
  "Use of a large language model in preparing the analysis code and "
  "manuscript drafts is disclosed in the Declarations. No specimens were "
  "collected and no live animals were handled.", )

p("Suggested reviewers.", bold=True)
p("The researchers most expert in honey bee wing morphometrics are "
  "themselves the producers of the deposits reanalysed here, so we have not "
  "named them, to avoid a conflict of interest. We would have no objection "
  "should the editorial office consider any of them appropriate. The three "
  "below are independent of the datasets analysed:")
p("1. Prof. Tiago Mauricio Francoy, Escola de Artes, Ciências e "
  "Humanidades, Universidade de São Paulo, Brazil (tfrancoy@usp.br). "
  "Works on geometric morphometrics of bee wings for subspecies and species "
  "identification, including Africanised honey bees, and publishes in this "
  "journal.")
p("2. Prof. Dean C. Adams, Department of Ecology, Evolution and Organismal "
  "Biology, Iowa State University, USA (dcadams@iastate.edu). Co-author of "
  "the framework for separating random from systematic measurement error in "
  "landmark data that this analysis applies.")
p("3. Dr Andrea Cardini, Dipartimento di Scienze Chimiche e Geologiche, "
  "Università di Modena e Reggio Emilia, Italy "
  "(andrea.cardini@unimore.it). Works specifically on measurement error and "
  "landmark digitisation in two-dimensional Procrustes data.")

p("Thank you for considering our manuscript.")
p()
p("Yours sincerely,")
p()
p()
p("V. K. Chaudhari", bold=True)
p("On behalf of both authors")

out = "/home/claude/Chaudhari_Pastagia_JAR_cover_letter.docx"
doc.save(out)
print("wrote", out)
