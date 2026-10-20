#!/usr/bin/env python3
"""Add or update a released skill in the catalogue.

    python3 tools/add_skill.py path/to/<name>.txt path/to/<name>.entry.json

Copies the skill text to downloads/<name>.txt and puts the entry into
skills.json (replacing any entry with the same name, and removing a
matching "coming soon" item). Run check_catalogue.py afterwards.
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(txt, entry_path):
    txt, entry_path = Path(txt), Path(entry_path)
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    name = entry.get("name") or txt.stem
    if txt.stem != name:
        sys.exit(f"File name {txt.name} doesn't match entry name {name}")
    entry["name"] = name

    shutil.copyfile(txt, ROOT / "downloads" / f"{name}.txt")

    cat_path = ROOT / "skills.json"
    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    cat["skills"] = [s for s in cat["skills"] if s["name"] != name] + [entry]
    cat["skills"].sort(key=lambda s: s["title"].lower())
    cat["coming_soon"] = [c for c in cat.get("coming_soon", [])
                          if c["title"].lower() != entry["title"].lower()]
    cat["updated"] = datetime.date.today().isoformat()
    cat_path.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {name} ({entry.get('version', 'no version')})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
