#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.paragraph_format.line_spacing = 1.15
st.paragraph_format.space_after = Pt(10)
for s in doc.sections:
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(2.5)

def p(t="", align=None, bold=False, italic=False):
    par = doc.add_paragraph(); r = par.add_run(t)
    r.bold = bold; r.italic = italic
    if align is not None: par.alignment = align
    return par

p("V. K. Chaudhari", bold=True)
p("AINP on Agricultural Acarology, Department of Entomology")
p("N. M. College of Agriculture, Navsari Agricultural University")
p("Navsari 396450, Gujarat, India")
p("vkcvaibhav@gmail.com")
p()
p("3 November 2026")
p()
p("The Editor-in-Chief")
p("Apidologie")
p()
p("Dear Editor,")

p("We submit for your consideration an original research article entitled "
  "“Disagreement between independently produced honey bee wing datasets "
  "is localized at two landmarks and limits reference transfer”.")

p("Wing geometric morphometrics has become the standard low-cost method for "
  "identifying honey bee subspecies, and its reference base is now large and "
  "open. That base is only useful if a reference built by one group can be "
  "applied to wings landmarked by another. Our paper asks whether it can, "
  "using the one case in the public record where two groups independently "
  "landmarked the same images.")

p("The two measurement sets differ by a mean displacement of 0.00875 "
  "Procrustes units, 0.44 times the median distance between colony means in "
  "the same dataset. Because this is a difference of grand means it does not "
  "shrink as more wings are averaged, so it is a bias rather than a variance "
  "component and cannot be reduced by sampling more bees per colony. A "
  "classifier that separated its own three subspecies in 41 of 41 colonies by "
  "leave-one-colony-out assigned zero or one of five colonies of known pure "
  "Apis mellifera caucasica correctly when applied to a dataset produced "
  "elsewhere, across 6 to 20 principal components.")

p("The result we think most useful to your readers is where the disagreement "
  "sits. About 94% of the squared mean displacement falls on landmarks 7 and "
  "14 alone, against roughly 10% if it were spread evenly, and these are "
  "precisely the two landmarks whose position Nawrocka et al. (2018) record "
  "as having been moved from the earlier convention of Gerula et al. (2009) "
  "to agree with Ruttner (1988). We present this as a plausible explanation "
  "rather than a demonstrated one, since neither deposit records which "
  "version of the configuration its operators used. The practical "
  "implication is specific and inexpensive: deposits should state the "
  "landmark convention they follow, and references should be calibrated "
  "against shared specimens before transfer.")

p("Analysis code and all generated results are openly archived at "
  "https://doi.org/10.5281/zenodo.23906962, and every figure and table in "
  "the manuscript is reproduced by running the deposited scripts in "
  "sequence.")

p("The work is entirely a reanalysis of published open deposits, and it "
  "exists only because several groups released their coordinates under "
  "licences permitting reuse. We have been careful to frame it as a "
  "measurement question that the field itself has raised, not as a criticism "
  "of any dataset or group. All analysis code and generated results are "
  "openly available.")

p("We confirm that this manuscript is original, has not been published "
  "elsewhere, and is not under consideration by another journal. Both "
  "authors have read and approved the submitted version and agree to its "
  "submission to Apidologie. We declare no competing interests, and no "
  "specific funding was received. Use of a large language model in preparing "
  "the analysis code and manuscript drafts is disclosed in the Methods; the "
  "authors verified the analyses and are accountable for the content.")

p("No specimens were collected and no live animals were handled, so ethics "
  "approval is not applicable.")

p("Thank you for considering our manuscript. We would be glad to supply any "
  "further information the editorial office requires.")

p()
p("Yours sincerely,")
p()
p()
p("V. K. Chaudhari", bold=True)
p("On behalf of both authors")

out = "/home/claude/Chaudhari_Pastagia_Apidologie_cover_letter.docx"
doc.save(out); print("wrote", out)
