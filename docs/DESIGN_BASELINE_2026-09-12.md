# MOMO design baseline — 2026-09-12

## Confirmed scope

- The user confirmed MOMO as the current design baseline on 2026-09-12.
- Source: `current/svg/MOMO_R166_REQ146_PANEL.svg`.
- Nominal panel size: 71.12 × 128.5 mm (14HP, 3U panel height convention).
- Palette: warm white substrate with black, white and neutral gray graphics.
- Source SHA-256: `679f2137d3d8e626e4cc08ec8788a06e4362b5139e525aef3b2e3195598b673f`.

## Illustrator project

- Project: `illustrator/MOMO_R166_REQ146_PANEL.ai`.
- Color mode: RGB.
- Artboard: 201.600006 × 364.251953 pt, corresponding to 71.12 × 128.5 mm.
- Layers: `MOMO_PANEL_VISIBLE_VECTOR` and `OFFICIAL_BOTTOM_LOCKUP_RASTER`.
- Live close/reopen readback in Illustrator 30.3.0: 238 paths, 8 compound paths, 47 groups, 22 editable text frames, 1 embedded raster item, 0 placed/linked items.

The original SVG uses CSS classes, `<use>` references, hidden manufacturing groups, SVG filters and an embedded PNG lockup. Illustrator 30.3.0 stalled on the embedded SVG image, so the visible `<use>` geometry was expanded to editable paths and the official bottom lockup was reinserted as one embedded raster layer. The complete SVG remains the authority for hidden manufacturing helper groups.

## Open engineering work

The aesthetic baseline is confirmed. Hole diameters and exact positions, tolerances, panel thickness, component envelopes, PCB alignment, hardware clearance, engraving/print process, supplier DFM and physical fit are provisional until later mechanical review and prototype measurement.
