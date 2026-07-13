#!/usr/bin/env python3
"""Validate glossary consistency across all sutta files.

Checks:
1. Every sutta YAML parses and has required fields.
2. Terms listed in a sutta's `terms_used` exist in the glossary.
3. Settled terms' English/Spanish renderings actually appear in the
   sutta text where the term is declared used (soft check, warns on miss).
4. No sutta declares use of a `to-verify` term.
Exit code 1 on any hard failure.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "glossary" / "glossary.yaml"
SUTTAS = ROOT / "suttas"

REQUIRED_FIELDS = ["id", "name_pali", "title_en", "title_es", "segments"]


def load_glossary():
    data = yaml.safe_load(GLOSSARY.read_text(encoding="utf-8"))
    return {t["pali"]: t for t in data.get("terms", [])}


def full_text(sutta, lang):
    return " ".join(seg.get(lang, "") for seg in sutta.get("segments", []))


def main():
    glossary = load_glossary()
    errors, warnings = [], []

    files = sorted(SUTTAS.rglob("*.yaml"))
    if not files:
        print("No sutta files found.")
        return 0

    for f in files:
        try:
            sutta = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"{f.name}: YAML parse error: {e}")
            continue

        for field in REQUIRED_FIELDS:
            if field not in sutta:
                errors.append(f"{f.name}: missing required field '{field}'")

        en_text = full_text(sutta, "en").lower()
        es_text = full_text(sutta, "es").lower()

        for pali in sutta.get("terms_used", []):
            term = glossary.get(pali)
            if term is None:
                errors.append(f"{f.name}: term '{pali}' not in glossary")
                continue
            if term.get("status") == "to-verify":
                errors.append(
                    f"{f.name}: uses '{pali}' which is still to-verify — resolve before finalizing"
                )
            if term.get("status") == "settled":
                if term["en"].lower() not in en_text:
                    warnings.append(
                        f"{f.name}: settled EN rendering '{term['en']}' for '{pali}' not found in text"
                    )
                if term["es"].lower() not in es_text:
                    warnings.append(
                        f"{f.name}: settled ES rendering '{term['es']}' for '{pali}' not found in text"
                    )

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(files)} sutta file(s) checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
