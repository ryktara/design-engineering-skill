# Install

Requirements: Claude Code (any client) and Python 3.10+ on PATH (`python` on Windows, `python3` elsewhere). No packages, no network.

## Personal skill (recommended)

Link or copy this directory to `~/.claude/skills/design-engineering`. A link keeps the workspace as the single source of truth.

Windows (PowerShell, no admin needed):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\design-engineering" -Target "D:\indigo pro\MYownSkills\design-engineering"
```

macOS / Linux:

```bash
ln -s "/path/to/MYownSkills/design-engineering" ~/.claude/skills/design-engineering
```

Copy instead of link if you want a frozen version:

```bash
cp -r design-engineering ~/.claude/skills/design-engineering
```

## Project skill

Copy or link to `<repo>/.claude/skills/design-engineering` to scope it to one repository.

## Verify

```bash
python ~/.claude/skills/design-engineering/scripts/validate_skill.py
python ~/.claude/skills/design-engineering/evals/run_evals.py
```

Both must report OK. Start a new Claude Code session; the skill appears as `/design-engineering` and is auto-selected for UI/UX requests. Claude Code picks up SKILL.md edits live within a session.

## Uninstall

Remove the junction/symlink or directory: `Remove-Item "$HOME\.claude\skills\design-engineering"` (junction) or `rm -rf ~/.claude/skills/design-engineering`.
