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

p("The study asks one question with two possible answers rather than "
  "describing a dataset. If the disagreement between two groups arises "
  "from a definable difference in where a numbered landmark is placed, it "
  "should be localised; if it arises from general imprecision in "
  "digitising, it should be spread across the configuration. It proved "
  "sharply localised: about 94% of the squared mean displacement falls on "
  "landmarks 7 and 14, whose root-mean-square disagreement is six times "
  "the median of the other seventeen, and the landmark-matching step "
  "reached the same two points independently. Those are the two landmarks "
  "that Nawrocka et al. (2018) record as having been moved from the "
  "convention of Gerula et al. (2009). We then quantified the "
  "disagreement, separating the mean displacement of 0.00875 Procrustes "
  "units, which averaging wings within a colony cannot remove, from the "
  "residual term, of which averaging reduces whatever part is "
  "independent and zero-mean. Separately, we assessed how a reference "
  "classifier built on one collection performs on colonies of known "
  "parentage in another: it assigned zero or one of five colonies of "
  "known pure Apis mellifera caucasica correctly across 6 to 20 principal "
  "components.")

p("We are careful about what this does and does not establish. Two "
  "explanations predict the localisation we see, a convention difference "
  "or digitising error concentrated at the two least determinate "
  "junctions, and these data cannot separate them because no deposit "
  "records the convention used. The measurement result and the "
  "classification result also come from different datasets, so we present "
  "them as complementary rather than as cause and effect. Measurement "
  "error in honey bee wings has been quantified before, by Machlowska et "
  "al. (2025), but within a single operator; the between-group quantity "
  "reported here is what a single-operator design cannot produce. The "
  "manuscript ends with four items of metadata that would settle the open "
  "question and that cost nothing to record.")

p("The work is entirely a reanalysis of published open deposits and exists "
  "only because several groups released their coordinates under licences "
  "permitting reuse. We have framed it as a measurement question the field "
  "has itself raised, not as a criticism of any dataset or group. Analysis "
  "code and all generated results are archived at "
  "https://doi.org/10.5281/zenodo.23906962, and every figure and table is "
  "reproduced by running the deposited scripts in sequence.")

p("The manuscript is 5,200 words including tables, references and figure "
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
