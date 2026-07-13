#!/usr/bin/env python3
"""Generate Markdown pages (for MkDocs) from sutta YAML files and the glossary."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SUTTAS = ROOT / "suttas"
GLOSSARY = ROOT / "glossary" / "glossary.yaml"
OUT = ROOT / "site" / "docs"


def render_sutta(sutta, glossary):
    lines = [
        f"# {sutta['name_pali']} — {sutta['title_en']} / {sutta['title_es']}",
        "",
        f"*{sutta.get('collection','')} {sutta['id']} · {sutta.get('nipata','')}, {sutta.get('vagga','')}*",
        "",
    ]
    if sutta.get("translator_note"):
        lines += [f"> {sutta['translator_note'].strip()}", ""]

    # Interleaved trilingual view, segment by segment
    lines += ["## Text", ""]
    for seg in sutta["segments"]:
        lines += [
            f'<span class="segid">{seg["id"]}</span>',
            "",
            f'**Pāli** — {seg.get("pali","")}',
            "",
            f'**English** — {seg.get("en","")}',
            "",
            f'**Español** — {seg.get("es","")}',
            "",
            "---",
            "",
        ]

    # Per-sutta glossary table
    used = [glossary[p] for p in sutta.get("terms_used", []) if p in glossary]
    if used:
        lines += ["## Glossary", "", "| Pali | English | Español | Conventional | Status |", "|---|---|---|---|---|"]
        for t in used:
            lines.append(
                f"| {t['pali']} | {t['en']} | {t['es']} | {t.get('conventional_en','')} | {t.get('status','')} |"
            )
        lines.append("")

    for key, heading in (("notes_en", "Notes"), ("notes_es", "Notas")):
        if sutta.get(key):
            lines += [f"## {heading}", "", sutta[key].strip(), ""]
    return "\n".join(lines)


def render_glossary(glossary):
    lines = [
        "# Glossary / Glosario",
        "",
        "| Pali | English | Español | Conventional | Status | First used |",
        "|---|---|---|---|---|---|",
    ]
    for t in glossary.values():
        lines.append(
            f"| {t['pali']} | {t['en']} | {t['es']} | {t.get('conventional_en','')} "
            f"| {t.get('status','')} | {t.get('first_used','')} |"
        )
    return "\n".join(lines) + "\n"


def main():
    glossary = {
        t["pali"]: t
        for t in yaml.safe_load(GLOSSARY.read_text(encoding="utf-8"))["terms"]
    }
    OUT.mkdir(parents=True, exist_ok=True)

    for f in sorted(SUTTAS.rglob("*.yaml")):
        sutta = yaml.safe_load(f.read_text(encoding="utf-8"))
        rel = f.relative_to(SUTTAS).with_suffix(".md")
        out_path = OUT / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_sutta(sutta, glossary), encoding="utf-8")
        print(f"built {out_path.relative_to(ROOT)}")

    (OUT / "glossary.md").write_text(render_glossary(glossary), encoding="utf-8")
    print("built site/docs/glossary.md")


if __name__ == "__main__":
    main()
