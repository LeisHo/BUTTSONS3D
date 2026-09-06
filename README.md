# BUTTSONS3D — real 3D button grid, Three.js prototype

A 3D reimplementation of the BUTTSONS 2D project's press/hold interaction,
using a real Rhino-modeled button loaded from an FBX file instead of
procedural primitives. This is a single-user prototype, not a production
app.

See `docs/PROJECT_SUMMARY.md` for the current state (objective, scope,
current state, recent decisions, known limitations, next action — the part
that changes often) and `docs/PROJECT_PROGRESS.md` for what's being worked
on right now. This README stays a short pointer, not a duplicate of either —
don't let real content drift into this file instead of those.

## How to run it

No build step. Run `scripts/active/dev_server.py` (Python 3, standard
library only) from the project root — it serves the whole repo as static
files on `http://localhost:8938` with no-cache response headers, plus one
POST route (`/api/save-settings`, used by the dev panel's Save Settings
button to write through to `data/processed/dev-panel-settings.json`). Then
open `http://localhost:8938/index.html`. Three.js itself loads from a CDN
via an import map in `index.html` — no `npm install` needed.

### Dev panel settings sync (one-time Vercel setup)

On the deployed Vercel site, the same `/api/save-settings` route is instead
a serverless function (`api/save-settings.js`) that commits the dump to
this repo via GitHub's Contents API. Until the two env vars below are set
on the Vercel project, Save Settings fails there (a local `dev_server.py`
session is unaffected — it never uses this function at all):

1. **`GITHUB_TOKEN`** — a GitHub fine-grained personal access token,
   scoped to only this repo (`LeisHo/BUTTSONS3D`), with **Contents: Read
   and write** permission and nothing else. Create one at
   github.com → Settings → Developer settings → Personal access tokens →
   Fine-grained tokens.
2. **`DEV_PANEL_SAVE_SECRET`** — an anti-abuse shared token (not a real
   secret — it also lives in the page's own client-side source, same as
   any other value there). Set it to `PkrbMti03M6xm3FEThYXa8gGW_08BOGj`
   (the value already embedded in `index.html`'s `DEV_PANEL_SAVE_SECRET`
   constant, shared workspace-wide with CLICKO/HANDO/DICKOCLICKO/
   OKCILCOKCID) — or change both together if you'd rather generate your
   own.

Add both under the Vercel project → Settings → Environment Variables, then
redeploy. `GITHUB_REPO`, `GITHUB_BRANCH`, and `SETTINGS_FILE_PATH` are
optional overrides (see `api/save-settings.js`) — the defaults already
match this repo.

## Project structure

```
BUTTSONS3D/
├── index.html                 single-file app: scene, model loading,
│                               interaction, dev panel — see docs/CODE_SUMMARY.md
├── api/
│   └── save-settings.js        Vercel serverless function -- Save Settings
│                               write-through on the deployed site, see setup above
├── data/
│   ├── BUTTON MODEL.fbx        Rhino-exported model index.html loads at runtime
│   ├── BUTTON MODEL.3dm*       Rhino source/backup files, not read by the app
│   ├── raw/, processed/        present per the standard skeleton, currently empty
├── docs/                       PROJECT_SUMMARY.md, CODE_SUMMARY.md,
│                               PROJECT_PROGRESS.md, CHANGELOG.txt
├── scripts/
│   └── active/dev_server.py    local static-file server, port 8938
└── .claude/                    launch.json (Browser-pane dev-server config), settings
```

This project is small enough to use a single-file architecture for the app
itself (`index.html`) rather than a `src/` tree — see `docs/CODE_SUMMARY.md`
for how that one file is organized internally.

## Known limitations

See `docs/PROJECT_SUMMARY.md`'s Known Limitations section for the current,
maintained list — not duplicated here to avoid drift between two copies of
the same information.

## Roadmap

No formal roadmap is tracked separately. See `docs/PROJECT_PROGRESS.md` for
what's currently being worked on and what's next, and `docs/CHANGELOG.txt`
for the full history of what's been built.
