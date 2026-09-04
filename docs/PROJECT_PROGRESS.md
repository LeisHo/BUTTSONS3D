# BUTTSONS3D — Project Progress

**This is a live document, not a log.** It holds only the current picture —
what's being worked on right now, what's recently done, and what's next. It
does **not** accumulate a running history of every past session; that
history already lives in `CHANGELOG.txt` (the append-only, authoritative
record — see CLAUDE.md §4a/§4). When something here is finished and no
longer relevant to understand what's current, remove it from this file
rather than leaving it to pile up. Rewrite the sections below in place at
each real update — don't append a new dated block underneath the old one.

This doc functionally doubles as a handoff document (CLAUDE.md §4c): a
brand-new AI chat with no prior context should be able to read this file
alone and know exactly where the project currently stands, and pick up the
work seamlessly from there.

--------------------------------------------------------------------------------

## Currently working on

Nothing in progress — see What's next.

## Recently completed

- Fixed the screen-space `OutlinePass` outline toggle being invisible: it
  composites edges via `THREE.AdditiveBlending` by default, which is a
  no-op for the project's default black outline color. Forced
  `THREE.NormalBlending` on both `outlinePassBase`/`outlinePassCap`'s
  overlay materials instead.
- Integrated the user's 2nd FBX re-export of `BUTTON MODEL.fbx` — verified
  identical part names and bounding boxes to the prior version, so no code
  changes were needed. Also confirmed Rhino's Active/Archived master-layer
  organization does not survive into the FBX export (only flat object
  names do), answering the user's question about duplicate "Active"
  sublayer names across different master layers.
- (Prior round) Fixed a real interaction bug where a button would
  permanently stop registering clicks after enough presses — root-caused
  to pointer capture on `canvas` conflicting with OrbitControls' own
  capture handling; moved move/up/cancel listeners to `window`.
- (Prior round) Added the geometry-vs-screen-space outline toggle, camera
  OrbitControls rework with saved camera presets, and settings schema
  versioning.

## What's next

No specific next action is currently pending. Likely future work, not yet
requested: wire Save Settings through to the git-tracked settings log
(`data/processed/dev-panel-settings.json` via
`scripts/active/dev_server.py`'s existing `/api/save-settings` route,
currently unused by the client) the way the sibling BUTTSONS 2D project
already does — see PROJECT_SUMMARY.md's Scope section.

## Open questions / blockers

None currently open.
