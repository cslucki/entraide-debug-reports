#!/usr/bin/env python3
"""Generate GitHub-friendly bug reports from the Obsidian TODO vault."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "Fiche"
CAPTURES_DIR = ROOT / "captures"
BUGS_DIR = ROOT / "bugs"
README = ROOT / "README.md"


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
OBSIDIAN_EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    return data, text[match.end() :]


def github_image_path(obsidian_path: str, from_bugs_dir: bool = True) -> str:
    image_name = obsidian_path.replace("\\", "/").split("/")[-1]
    prefix = "../captures" if from_bugs_dir else "captures"
    return f"{prefix}/{quote(image_name)}"


def convert_body(body: str) -> str:
    def replace_embed(match: re.Match[str]) -> str:
        target = match.group(1)
        label = Path(target.replace("\\", "/")).name
        return f"![{label}]({github_image_path(target)})"

    return OBSIDIAN_EMBED_RE.sub(replace_embed, body).strip() + "\n"


def metadata_table(frontmatter: dict[str, str]) -> str:
    rows = []
    for key in ("statut", "categorie", "priorite", "source", "url", "date_creation"):
        value = frontmatter.get(key)
        if value:
            rows.append(f"| {key} | {value} |")

    if not rows:
        return ""

    return "| Champ | Valeur |\n| --- | --- |\n" + "\n".join(rows) + "\n\n"


def title_for(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def clean_generated_dir() -> None:
    if BUGS_DIR.exists():
        shutil.rmtree(BUGS_DIR)
    BUGS_DIR.mkdir(parents=True, exist_ok=True)


def copy_captures() -> None:
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)


def export_reports() -> list[dict[str, str]]:
    clean_generated_dir()
    copy_captures()

    reports: list[dict[str, str]] = []
    for source in sorted(SOURCE_DIR.glob("*.md")):
        text = source.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)

        if frontmatter.get("type") != "bug":
            continue

        converted_body = convert_body(body)
        title = title_for(source, converted_body)
        output = BUGS_DIR / source.name
        output.write_text(metadata_table(frontmatter) + converted_body, encoding="utf-8")

        reports.append(
            {
                "title": title,
                "filename": output.name,
                "statut": frontmatter.get("statut", "Non classe"),
                "priorite": frontmatter.get("priorite", ""),
            }
        )

    return reports


def link_to_bug(filename: str) -> str:
    return f"bugs/{quote(filename)}"


def write_readme(reports: list[dict[str, str]]) -> None:
    by_status: dict[str, list[dict[str, str]]] = {}
    for report in reports:
        by_status.setdefault(report["statut"], []).append(report)

    lines = [
        "# BouclePro Debug Reports",
        "",
        "Depot genere depuis le vault Obsidian local `_TODO`.",
        "",
        "Les fichiers dans `bugs/` sont adaptes pour GitHub. Les captures liees aux fiches sont dans `captures/`.",
        "",
        "## Resume Par Statut",
        "",
    ]

    status_order = ["A faire", "En cours", "Fait", "Abandonné", "Non classe"]
    for status in status_order:
        items = by_status.get(status, [])
        if not items:
            continue
        lines.append(f"### {status}")
        lines.append("")
        for item in sorted(items, key=lambda item: item["filename"]):
            priority = f" - {item['priorite']}" if item["priorite"] else ""
            lines.append(f"- [{item['title']}]({link_to_bug(item['filename'])}){priority}")
        lines.append("")

    lines.extend(
        [
            "## Convention",
            "",
            "- `Fiche/` reste la source Obsidian locale.",
            "- `bugs/` est la version Markdown compatible GitHub.",
            "- `TODO.base` est volontairement ignore par l'export GitHub.",
            "- L'export est regenere par `python tools/export_github.py`.",
            "",
        ]
    )

    README.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    reports = export_reports()
    write_readme(reports)
    print(f"Export GitHub genere: {len(reports)} fiche(s) dans {BUGS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
