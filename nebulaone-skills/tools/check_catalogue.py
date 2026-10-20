#!/usr/bin/env python3
"""Check skills.json and downloads/ agree. Exits non-zero on any error.

    python3 tools/check_catalogue.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["name", "title", "family", "version", "summary", "what_it_does",
            "how_it_works", "good_for", "try_saying"]
LISTS = ["how_it_works", "good_for", "not_for", "try_saying"]


def main():
    errors = []
    cat = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
    families = cat.get("families", {})
    names = set()
    for s in cat.get("skills", []):
        label = s.get("name", "<no name>")
        for field in REQUIRED:
            if not s.get(field):
                errors.append(f"{label}: missing {field}")
        for field in LISTS:
            if field in s and not isinstance(s[field], list):
                errors.append(f"{label}: {field} should be a list")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", label):
            errors.append(f"{label}: name should be lowercase words joined by hyphens")
        if label in names:
            errors.append(f"{label}: listed twice")
        names.add(label)
        if s.get("family") not in families:
            errors.append(f"{label}: family '{s.get('family')}' isn't in families")
        if len(s.get("summary", "")) > 160:
            errors.append(f"{label}: summary is over 160 characters")
        txt = ROOT / "downloads" / f"{label}.txt"
        if not txt.exists():
            errors.append(f"{label}: downloads/{label}.txt is missing")
        elif not txt.read_text(encoding="utf-8").strip():
            errors.append(f"{label}: downloads/{label}.txt is empty")
    for txt in (ROOT / "downloads").glob("*.txt"):
        if txt.stem not in names:
            errors.append(f"downloads/{txt.name} isn't listed in skills.json")
    for c in cat.get("coming_soon", []):
        if c.get("family") not in families:
            errors.append(f"coming soon '{c.get('title')}': unknown family")

    for e in errors:
        print("ERROR", e)
    print(f"{len(names)} released skill(s), {len(cat.get('coming_soon', []))} coming soon, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
