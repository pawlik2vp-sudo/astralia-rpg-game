# Astralia RPG — build source

This folder holds the canonical, editable source for the game and the
script that builds the deployed `index.html`.

**IMPORTANT — read this before touching the build:** `margonem-mini-rpg.jsx`
is a real ES module (`import ... from '...'` at the top, `export default
function AstraliaRPG()` at the bottom) written for a real bundler. The
deployed page instead runs everything through Babel-in-browser via a plain
`<script type="text/babel">` tag, which **cannot** execute `import`/`export`
at all. If you ever concatenate the raw `.jsx` straight into an HTML page
without stripping those lines, the live site will silently hang forever on
the loading screen with **no console error** — this has happened twice
already. Always build through `build.py`, which strips them automatically.

## Files

- `margonem-mini-rpg.jsx` — the game itself, one big React component.
- `build.py` — strips ES module syntax and assembles `index.html`.
- `full-page-header.html` / `full-page-footer.html` — wrap the game into a
  standalone HTML page for GitHub Pages.
- `preamble.html` / `closing.html` — wrap the game for the claude.ai
  Artifact tool instead (which supplies its own outer skeleton).
- `postamble.jsx` — small script tail appended after the game component
  (mounts it with `createRoot`).

## How to rebuild after editing the game

```
python3 build.py
```

This reads `margonem-mini-rpg.jsx` (one directory up... no — it now lives
in *this* directory when checked out from the repo; adjust `SOURCE` in
`build.py` if you move things around), strips the `import`/`export` lines,
and writes `index.html` next to it. Upload that `index.html` to the repo
root (GitHub Pages serves the root) to deploy.

## Why this folder exists

A previous session hand-built the HTML bundle by concatenating the raw
source without stripping ES module syntax, which broke the live site
(hung on the loading screen, zero console errors, only surfaced by running
the page's own script through `Babel.transform` + `eval` and reading the
thrown `SyntaxError`). The fix was reapplied, but the build script itself
lived only in the ephemeral session workspace and was lost once that
session ended — so the *next* session reconstructed the pipeline from
scratch and reintroduced the exact same bug. Committing the whole pipeline
here means any future session can just read this folder instead of
guessing.
