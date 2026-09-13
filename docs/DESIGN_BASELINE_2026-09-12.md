# MOMO design baseline — 2026-09-12

## Confirmed scope

- The user confirmed MOMO as the current design baseline on 2026-09-12.
- The user subsequently approved the REQ156 flowing cat mark and authorized AI implementation and remote publication. The AI update was completed on 2026-09-13.
- Source: `current/svg/MOMO_R166_REQ146_PANEL.svg`.
- Nominal panel size: 71.12 × 128.5 mm (14HP, 3U panel height convention).
- Palette: warm white substrate with black, white and neutral gray graphics.
- Source SHA-256: `fd4cf737c08229c734d99ee20ac1dc574023b848899b6895b6fae7874658527d`.

## Illustrator project

- Project: `illustrator/MOMO_R166_REQ146_PANEL.ai`.
- Color mode: RGB.
- Artboard: 201.600006 × 364.251953 pt, corresponding to 71.12 × 128.5 mm.
- Layers: `MOMO_MODULE_LOGO_FLOW_VECTOR`, `MOMO_PANEL_VISIBLE_VECTOR` and `OFFICIAL_BOTTOM_LOCKUP_RASTER`.
- Live close/reopen readback in Illustrator 30.3.0: 218 paths, 5 compound paths, 47 groups, 22 editable text frames, 1 embedded raster item, 0 placed/linked items.
- AI SHA-256: `04e6ca090a848efdd71a9cadf232479fdd99000499f81c995dbb0c2dd39448aa`.

The approved logo was inserted into the existing AI as exact native cubic paths, replacing `req146-cat-profile` with `req156-flow-cat-mark`. Its seven SVG paths contain eight subpaths, represented by eight Illustrator paths and one compound path. Widths, grayscale colors and control points match the approved SVG; the maximum coordinate/width readback error is below 0.000000014 pt. Before/after AI exports at 500% have zero changed pixels outside the logo rectangle. `tools/audit_current.py` passes all 16 checks; evidence is in `verification/CURRENT_BASELINE_AUDIT.json` and `verification/REQ156_AI_LIVE_READBACK.json`.

The original SVG uses CSS classes, `<use>` references, hidden manufacturing groups, SVG filters and an embedded PNG lockup. Illustrator 30.3.0 stalled on the embedded SVG image, so the visible `<use>` geometry was expanded to editable paths and the official bottom lockup was reinserted as one embedded raster layer. The complete SVG remains the authority for hidden manufacturing helper groups.

## Open engineering work

The aesthetic baseline is confirmed. Hole diameters and exact positions, tolerances, panel thickness, component envelopes, PCB alignment, hardware clearance, engraving/print process, supplier DFM and physical fit are provisional until later mechanical review and prototype measurement.
