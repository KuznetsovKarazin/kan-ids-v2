# ACM DTRAP submission sources

This is the current manuscript. The earlier `review_extension/manuscript`
directory retains the previous article and the numerical asset generators;
its article PDFs are superseded by this directory.

The supplied ACM primary template is acmart 2.20 (2026-08-16), unchanged.
Initial submission uses `manuscript,review,anonymous`; DTRAP's production
format is `acmlarge`, to be applied after acceptance with ACM's rights data.
No journal DOI, acceptance date or copyright assignment is invented here.

Build with a complete TeX Live installation (including texlive-fonts-extra):

```sh
make all
```

- `main.pdf`: anonymous main article for peer review.
- `supplement.pdf`: anonymous supplementary material.
- `author-version.pdf`: full author version with affiliations and declarations.
- `supplement-author.pdf`: full author supplementary material.
- `editor-letter.pdf`: cover letter and author/title information for editors.

The anonymous PDFs exclude author names, affiliations, funding/interest
disclosures and the public repository URL. The numerical-evidence ZIP is
separate from the identified reproduction package. Do not upload the full
author version or integration materials as an anonymous reviewer file.

Generated tables and figures are supplied. No raw data or experiment rerun is
needed to build the paper. In the repository, `refresh_assets.py` refreshes
these assets after the evidence analysis; the standalone LaTeX ZIP contains
the resulting assets and does not require that helper.

The corresponding author must complete the ordinary submission attestations
and obtain every author's approval. Current CRediT records only documented
contributions: Frontoni's intellectual contribution and responsibility still
require confirmation; a writing role must not be added merely to satisfy a
policy. A permanent archival DOI has not yet been registered. The prepared
deposit metadata and immutable package can be deposited after author approval.

Official author requirements can change; check the submission portal's current
fields before upload: https://mc.manuscriptcentral.com/dtrap
