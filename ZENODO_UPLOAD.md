# Depositing the analysis on Zenodo

Two separate things can be deposited. Do the first; the second only if you
want the derived tables citable on their own.

## 1. The code and results repository (do this one)

This gives the repository a DOI you can cite in the manuscript's Data
availability statement. Zenodo can archive a GitHub release automatically,
so you never upload files by hand.

1. Sign in at https://zenodo.org with your GitHub account
   (Log in -> Log in with GitHub, then Authorize).
2. Go to https://zenodo.org/account/settings/github/
3. Find `vkcvaibhav-eng/honeybee-wing-reliability-` in the repository list
   and switch the toggle to **On**.
   If it is not listed, press **Sync now**. Only repositories you own appear.
4. In GitHub, open the repository -> **Releases** -> **Create a new release**.
   - Tag: `v1.0.0`
   - Title: `Analysis code for Chaudhari & Pastagia, Apidologie submission`
   - Description: one or two lines on what the code does.
   - Press **Publish release**.
5. Zenodo picks up the release within a few minutes and mints a DOI.
   Refresh https://zenodo.org/account/settings/github/ and the DOI badge
   appears next to the repository.
6. Open the new Zenodo record and press **Edit** to correct the metadata,
   which Zenodo guesses from GitHub and usually gets partly wrong:
   - **Authors**: V. K. Chaudhari (Navsari Agricultural University) and
     J. J. Pastagia (Navsari Agricultural University). Add ORCID iDs if you
     have them.
   - **Title**: as above, not the bare repository name.
   - **Description**: the abstract of the paper, or a short summary.
   - **Licence**: choose one that is compatible with the deposits you reuse.
     Several carry the Open Database License v1.0 with a share-alike
     requirement, so for the derived tables use **ODbL-1.0**; for the code
     itself **MIT** or **GPL-3.0** is fine. If in doubt, ODbL-1.0 for the
     whole record is the safe choice.
   - **Related identifiers**: add each source deposit DOI with the relation
     **"is derived from"**, and the Apidologie article DOI once you have it,
     with **"is supplement to"**.
   - **Keywords**: Apis mellifera, geometric morphometrics, wing
     morphometrics, measurement error, reference dataset.
7. Press **Publish**. Zenodo gives you two DOIs: a *concept DOI* that always
   points at the newest version, and a *version DOI* for this release. Cite
   the **concept DOI** in the paper.

## 2. Derived tables as a dataset record (optional)

Only if you want the result tables citable separately from the code.

1. https://zenodo.org/uploads/new
2. Upload the files you want to share — for this paper, the contents of
   `results/` is the sensible set.
3. Upload type: **Dataset**.
4. Fill in title, authors, description, licence (**ODbL-1.0**, because of the
   share-alike requirement on several sources) and the same related
   identifiers as above.
5. Publish.

## What to put in the manuscript

Once you have the DOI, replace the GitHub URL in the Data availability
statement with both, for example:

> Analysis code and all generated results are at
> https://github.com/vkcvaibhav-eng/honeybee-wing-reliability- and are
> archived at https://doi.org/10.5281/zenodo.XXXXXXX

Tell me the DOI and I will put it into the manuscript and rebuild.

## Two cautions

- Publishing on Zenodo is permanent. A record can be given a new version but
  not deleted, so check the author list and licence before pressing Publish.
- Do not upload the raw deposits of other groups. The repository already
  avoids this and lists every source by DOI instead; redistributing them
  could breach the share-alike and attribution terms.
