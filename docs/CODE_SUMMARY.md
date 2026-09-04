BUTTSONS3D -- CODE SUMMARY
================================================================================

Status: see ../README.md for the project-structure layout and how to run it;
this file is a quick orientation pointer into the actual code, not a
duplicate of the README's tree.

--------------------------------------------------------------------------------
FILE MAP

- `index.html` -- the entire app: scene setup, model loading, interaction,
  dev panel, all in one file (single-file architecture, no build step --
  matches this workspace's CLAUDE.md §11 exception for small projects).
  Loads Three.js from jsdelivr CDN via an `<script type="importmap">`.
- `data/BUTTON MODEL.fbx` (+ `.fbxbak`) -- the Rhino-exported button model
  `index.html` loads at runtime via `FBXLoader`. `.3dm`/`.3dm.rhl`/
  `.3dmbak`/`.gts` are the Rhino source/backup files, kept for reference,
  not read by the app.
- `scripts/active/dev_server.py` -- local static-file dev server (port
  8938, distinct from the sibling BUTTSONS project's 8937), with
  no-cache response headers and one POST route (`/api/save-settings`,
  writes to `data/processed/dev-panel-settings.json`) that the client does
  not currently call -- see PROJECT_SUMMARY.md's Known Limitations.
- `data/processed/`, `data/raw/` -- present per the CLAUDE.md §11 project
  skeleton, currently empty; no data pipeline exists for this project.
- `config/`, `models/`, `src/`, `tests/`, `logs/`, `results/`,
  `scripts/results/`, `datalog/` -- present from the project skeleton or
  created incidentally; not used by `index.html` or `dev_server.py`. Not
  verified empty/unused beyond a directory listing -- flagged here rather
  than silently treated as live.

--------------------------------------------------------------------------------
ARCHITECTURE

Single IIFE inside `index.html`'s `<script type="module">`. Rough data
flow:

1. `DEFAULT_SETTINGS` + `loadSavedDefaults()` establish the live `settings`
   object (schema-version-gated localStorage load, falling back to
   `DEFAULT_SETTINGS` on any version mismatch or absence).
2. Scene/renderer/camera/OrbitControls/EffectComposer are constructed once
   at module load. Two `OutlinePass` instances (base, cap) are added to the
   composer alongside a `RenderPass` and `OutputPass`, but stay `enabled =
   false` until the geometry outline is administratively swapped for the
   screen-space one (see `refreshOutlines()`).
3. `loadButtonModel()` asynchronously loads the FBX once, extracts and
   caches each of the 4 named parts' geometry (rotated from Rhino's Z-up to
   the scene's Y-up), and resolves a promise. Nothing that depends on the
   model (`regenerateGrid()`, `applyAllSettings()`) runs before this
   resolves — `regenerateGrid()` itself also no-ops via a `modelReady`
   guard as a second safety net.
4. `regenerateGrid()` builds one cell per grid position by cloning the
   cached geometries into new meshes (base, exterior, unpressed/pressed
   interior, a procedural gap-fill extension cylinder), grouping the
   cap-related meshes (`capGroup`) so they can move as one rigid unit
   relative to the fixed `baseMesh`, and populating both outline systems'
   object references.
5. Per-frame (`animate()`): tween any active cell's `capGroup.position.y`
   toward its press/release target, re-stretch each cell's extension
   cylinder to bridge the (fixed) base top to the (moving) cap bottom
   exactly, update OrbitControls, then render via either
   `composer.render()` (screen-space outline active) or
   `renderer.render(scene, camera)` (geometry outline / no outline).
6. Pointer interaction is entirely separate from the render loop:
   `pointerdown` on `canvas` starts a visual press and raycast-picks the
   cell; `pointermove`/`pointerup`/`pointercancel` are on `window` (not
   `canvas` — see Gotchas) and resolve into a permanent height gain
   (quick click = up, held past a threshold = down) or a cancel (dragged
   past a small pixel threshold, treated as an orbit/pan gesture instead).
7. The dev panel (`buildPanelContent()` and friends) reads/writes the same
   `settings` object; every control's `cfg.regen`/`cfg.camera`/
   `cfg.light`/`cfg.material`/`cfg.outline`/`cfg.scene` flags determine
   which of the functions above `applySetting()` calls after a change,
   rather than the panel code duplicating any scene logic itself.

Deliberately one-directional: the dev panel only ever calls into the scene-
setup functions above: it does not hold its own parallel copy of scene
state, and the scene-setup functions never read from panel DOM directly
(they only read `settings`).

--------------------------------------------------------------------------------
UNTOUCHABLE SYSTEMS

None formally designated yet.

--------------------------------------------------------------------------------
GOTCHAS

- **Pointer listeners must stay on `window`, not `canvas`, for
  move/up/cancel.** OrbitControls attaches its own pointer-capture handling
  to the same canvas element used for button picking. Scoping those three
  listeners to `canvas` makes them depend entirely on pointer capture
  correctly redirecting the up-event back to canvas; when it doesn't, a
  cell's `pressed` flag never clears, and `pressCell()`'s own re-entry
  guard then silently no-ops every future click on that one cell — matches
  the real "button stops clicking after multiple presses" bug fixed
  2026-09-04ish (prior round). `pointerdown` itself stays on `canvas` since
  raycasting needs the click's own origin coordinates regardless of
  capture.
- **`OutlinePass` composites edges with `THREE.AdditiveBlending` by
  default.** With this project's default black `outlineColor`, additive
  blending adds `(0,0,0)` to the scene — a no-op, so the pass renders every
  frame but produces zero visible change. Both `outlinePassBase` and
  `outlinePassCap` have `overlayMaterial.blending` forced to
  `THREE.NormalBlending` at construction specifically to avoid this; don't
  remove that without re-testing with the default black outline color.
- **`baseRadius`/`baseHeight`/`buttonRadius`/`buttonHeight` are scale
  factors, not literal dimensions.** They multiply the model's authored
  size (`NATURAL_BASE_RADIUS`/`NATURAL_BASE_HEIGHT`/
  `NATURAL_EXTERIOR_RADIUS`, measured directly from the FBX, not guessed)
  via `mesh.scale.set(...)` — this changed from an earlier version where
  these were literal cylinder dimensions for a procedural primitive, which
  is why `SETTINGS_SCHEMA_VERSION` exists: an old saved value under the old
  meaning would otherwise be silently reinterpreted under the new one.
- **The extension cylinder's radius is derived from `buttonRadius *
  NATURAL_EXTERIOR_RADIUS` directly**, not an independent slider — it must
  always match the exterior's actual scaled radius to visually bridge the
  gap without a mismatch at the seam.
- **Rhino's FBX export does not preserve Active/Archived (or any other)
  master-layer structure** — only flat object-level names
  (`BUTTON_BASE`, `BUTTON_EXTERIOR`, `BUTTON_INTERIOR_-_UNPRESSED`,
  `BUTTON_INTERIOR_-_PRESSED`) survive into the exported file. Confirmed by
  direct FBXLoader scene-graph inspection, not assumed from Rhino/FBX
  documentation.
