# Pali Suttas — Punnaji-Style Trilingual Translations

Translations of Pali suttas into English and Spanish following the psychological translation methodology of Bhante Madawela Punnaji, with the Pali kept accessible alongside every rendering. Renderings not attested in Punnaji's published work are reconstructions in his style, and are labeled as such.

## Repository layout

```
glossary/
  glossary.yaml          # Single source of truth for all term renderings
suttas/
  iti/                   # Collection (Itivuttaka)
    ekakanipata/
      pathamavagga/
        iti001-lobha.yaml   # One YAML file per sutta (source of truth)
scripts/
  build.py               # Generates Markdown/site pages from YAML
  validate.py            # Checks glossary consistency across all suttas
site/                    # MkDocs static site (generated pages land in site/docs)
```

## Data model

Each sutta is one YAML file containing segment-aligned Pali, English, and Spanish (SuttaCentral/Bilara-style segment IDs), plus the per-sutta glossary table and interpretive notes. Segment alignment means every Pali line is permanently paired with its renderings — the site, PDFs, or any future format are generated from this, never hand-edited.

## Workflow

1. Add/extend the sutta YAML (translate with the `punnaji-sutta-translation` Claude Skill).
2. Add any new terms to `glossary/glossary.yaml` with a status flag.
3. Run `python scripts/validate.py` — fails if a settled term is rendered inconsistently or a to-verify term appears in final text.
4. Run `python scripts/build.py` to regenerate site pages.
5. Commit. CI runs validate + build; the site deploys via GitHub Pages.

## Stack

- **Git + GitHub** — versioning, review, issues for term debates
- **YAML** source files — human-editable, diff-friendly, segment-aligned
- **Python** (PyYAML) build/validate scripts
- **MkDocs + Material theme** — trilingual static site, deployed on GitHub Pages
- **GitHub Actions** — validate on every push, deploy on main

## Licensing

Suggested: CC BY-NC-SA 4.0 for translations; Pali source texts are public domain.
