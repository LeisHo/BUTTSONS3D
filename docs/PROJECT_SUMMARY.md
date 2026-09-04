BUTTSONS3D -- PROJECT SUMMARY
================================================================================

Status: working single-page Three.js prototype -- a grid of real Rhino-
modeled 3D buttons, press/hold-to-grow-or-shrink interaction, a dev panel
with two selectable outline-rendering techniques, as of 2026-09-04. See
PROJECT_PROGRESS.md for what's actively being worked on right now, and
CHANGELOG.txt for the full historical log -- this file stays a mid-altitude
snapshot, not a duplicate of either.

--------------------------------------------------------------------------------
OBJECTIVE

A 3D reimplementation of the BUTTSONS 2D project's interaction model: a grid
of button-shaped objects that grow permanently taller with a quick click and
shrink permanently shorter with a click-and-hold, using a real Rhino-modeled
button (base, exterior shell, and swappable unpressed/pressed interior)
loaded from an FBX file rather than procedural primitives. No backend, no
auth, no build step -- a single `index.html` loading Three.js from a CDN via
an import map, matching this workspace's no-build-system convention.

--------------------------------------------------------------------------------
SCOPE

In scope: the 3D scene/interaction (grid layout, camera, lighting, press/
hold gain mechanics, outline rendering), the dev panel (CLAUDE.md §12) for
tuning all of it live, and integrating whatever FBX re-exports the user
produces from the Rhino source file.

Out of scope / dormant: git-tracked Save Settings write-through (CLAUDE.md
§12l) -- the dev panel's Save Settings is currently localStorage-only for
this project; the panel says so directly ("Local-only for now -- git-tracked
sync not wired up yet for this project"). `scripts/active/dev_server.py` has
a `/api/save-settings` POST route that writes to
`data/processed/dev-panel-settings.json`, but nothing in the client currently
calls it -- wiring that up (plus the Vercel/GitHub write-through the sibling
BUTTSONS 2D project already has) is a real gap, not yet started.

Audience / how it's used: single-user prototype, iterated on live via the
dev panel and direct feedback from the user (who also maintains the source
Rhino model).

--------------------------------------------------------------------------------
CURRENT STATE

Real Rhino-modeled geometry (`data/BUTTON MODEL.fbx`, currently on its 2nd
user-provided re-export) is loaded once at startup via `FBXLoader` and
cloned per grid cell; the button/base/extension-cylinder dimensions are
scale factors applied on top of the model's authored size (measured
constants `NATURAL_BASE_RADIUS = 2.03125`, `NATURAL_BASE_HEIGHT = 1`,
`NATURAL_EXTERIOR_RADIUS = 1.5`), not literal primitive dimensions. Camera
is a full OrbitControls mouse orbit/pan/zoom rig, with position/target
sliders acting as a "jump to this view" default and a saved-camera-presets
system (Save/Use/Delete, a resizable multi-row list) for storing named
views. Press/hold interaction mirrors the 2D BUTTSONS project's gain
mechanics exactly, with window-level (not canvas-level) pointer listeners
so OrbitControls' own pointer-capture handling on the same canvas can't
starve a button of its release event.

Two independently toggleable outline-rendering techniques exist: the
default per-mesh inverted-hull (BackSide-culled child meshes, geometry-
based, always renders correctly regardless of color) and an alternative
screen-space `OutlinePass` (EffectComposer/RenderPass/OutlinePass/
OutputPass, two separate pass instances so base and button/cap keep an
independent silhouette with a visible seam). As of 2026-09-04 the
OutlinePass's overlay material is forced to `THREE.NormalBlending` (see
Known Limitations) so it renders correctly with the project's default black
outline color.

--------------------------------------------------------------------------------
DECISIONS

- Model geometry is loaded from a real FBX export rather than built
  procedurally -- the user maintains the authoritative shape in Rhino;
  button/base sliders are scale factors on the authored geometry, not
  independent primitive dimensions, so they can never drift out of
  proportion with the model.
- Two separate `OutlinePass` instances (base vs. cap/button) instead of one
  shared selection -- a single shared selection merges any two touching
  selected objects into one silhouette with no line at their seam, which
  would hide the base/button boundary that a single geometry-outline pair
  of child meshes naturally preserves.
- Pointer listeners for move/up/cancel are attached to `window`, not
  `canvas` -- OrbitControls does its own pointer-capture handling on that
  same canvas element, and depending on capture correctly redirecting the
  up-event back to canvas caused buttons to get permanently stuck pressed
  after enough clicks (fixed 2026-09-04, see CHANGELOG).
- Settings persistence is localStorage-only for now, with an explicit
  schema-version gate (`SETTINGS_SCHEMA_VERSION`) that discards an
  incompatible old save wholesale rather than attempting a semantic merge,
  after a scale-factor meaning change silently corrupted an old save once.

--------------------------------------------------------------------------------
KNOWN LIMITATIONS

- Save Settings is localStorage-only (see Scope) -- not git-tracked, unlike
  the sibling BUTTSONS 2D project.
- `OutlinePass`'s default compositing is `THREE.AdditiveBlending`, which
  makes a black edge color a no-op (adding black changes nothing) -- fixed
  by forcing `THREE.NormalBlending` on both pass instances' overlay
  material (2026-09-04); worth remembering if either pass is ever
  reconstructed or replaced, since the fix lives on the pass instance, not
  in Three.js's own defaults.
- No automated test suite -- all verification this project has had is
  direct live-browser testing (real dispatched pointer events, screenshots,
  direct property/value checks), not a repeatable test harness.

--------------------------------------------------------------------------------
NEXT ACTION

No specific next action is currently pending -- the most recently reported
bug (invisible OutlinePass outline) and the 2nd FBX model update are both
resolved and committed. Likely future work, not yet requested: wiring Save
Settings through to the git-tracked settings log the way the sibling
BUTTSONS 2D project already does.
