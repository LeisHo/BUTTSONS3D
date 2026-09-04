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
POST route (`/api/save-settings`, currently unused by the client — see
`docs/PROJECT_SUMMARY.md`'s Known Limitations). Then open
`http://localhost:8938/index.html`. Three.js itself loads from a CDN via an
import map in `index.html` — no `npm install` needed.

## Project structure

```
BUTTSONS3D/
├── index.html                 single-file app: scene, model loading,
│                               interaction, dev panel — see docs/CODE_SUMMARY.md
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
