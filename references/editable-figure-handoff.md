# Editable Figure Handoff

Use this reference when the user asks for editable SVG or mentions AutoFigure-Edit.

## Positioning

AutoFigure-Edit can be an optional local post-processing path after a raster draft has been generated. Treat it as a local integration hook, not a guaranteed built-in conversion feature.

## What It Can Help With

- Generating or refining editable SVG scientific figures.
- Reconstructing structure, placeholders, and icon regions.
- Keeping a figure editable after a first-pass draft.

## Limitation

The upstream AutoFigure-Edit workflow is primarily `method text -> draft figure -> editable SVG`. It may support reference images and SVG reconstruction internally, but direct `existing Banana raster -> editable SVG` depends on local wrappers or custom setup.

## Suggested Local Variables

- `AUTOFIGURE_EDIT_ROOT`
- `AUTOFIGURE_EDIT_PYTHON`
- `AUTOFIGURE_EDIT_OUTPUT_DIR`
- `AUTOFIGURE_EDIT_ENABLED=1`

## Handoff Artifacts

- `figure.png`
- `prompt.txt`
- `method.txt`
- optional `handoff.json` with language, figure type, output paths, and editable-output intent

## Conservative Wording

Use wording like:

`This figure can optionally be handed off to a local AutoFigure-Edit deployment for editable SVG reconstruction or refinement if that pipeline is available on this machine.`
