# Epimoni MicroQuest — Round 2 pitch deck

Live: https://epimoni-r2-pitch.vercel.app

## Editing the speaker script (students)

1. Open `index.html` on GitHub → pencil icon (Edit).
2. Search for `const NOTES=` — each slide's script is the `script:[...]` list under its `tag:` (e.g. `'S5 · DEMO'`).
3. Edit the quoted lines. Keep `[bracketed cues]` — they're stage directions, not spoken.
4. Commit — Vercel redeploys automatically in ~30s. Check the live link after.

Also editable: `who:` (speaker initials), `time:` (target), `cue:` and `tip:` (presenter-only notes).

## Files

- `index.html` — the deck (single self-contained file — this is what you edit)
- `epimoni-round2-pitch-v2.html` — same deck under its real name (keep in sync if you edit)
- `src/build-v2.py` — generator used to build the deck (optional; edits made directly to index.html are fine for the pitch)
- `src/pitch-script.md` — printable rehearsal script (regenerate after script edits, or edit by hand)

## Controls

→/← or click sides: navigate · N/S: script panel · T: rehearsal timer · O: overview · F: fullscreen · H: shortcut hints
