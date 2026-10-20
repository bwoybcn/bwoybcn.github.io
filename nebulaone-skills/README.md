# nebulaONE Skills Library

The page at `/nebulaone-skills/` lists released nebulaONE skills, each with an explanation, how it works, what it's good for, and a download.

- `index.html` renders everything from `skills.json`, so adding a skill never means editing the page.
- `downloads/<name>.txt` is the exact skill file people download. nebulaONE doesn't take Markdown, so skills ship as plain text.
- `coming_soon` in `skills.json` lists skills still in development (no download).

## Adding a skill

Only add a skill once it has passed verification and is marked Released in the project's skill register.

1. Copy `tools/entry-template.json` to `<name>.entry.json` and fill it in. Write for staff, not developers: short sentences, no jargon. `family` must be a key in `families` in `skills.json` (add a new one there if needed).
2. Run:
   ```
   python3 tools/add_skill.py path/to/<name>.txt path/to/<name>.entry.json
   python3 tools/check_catalogue.py
   ```
   This copies the text file into `downloads/`, adds or replaces the entry, removes any matching "coming soon" item and bumps the `updated` date.
3. Commit and open a pull request.

To update a skill, run the same command with the new text file and a raised `version`. To withdraw one, delete its entry from `skills.json` and its file from `downloads/`.

Each skill card can be linked to directly: `/nebulaone-skills/#<name>` opens it with the details expanded.
