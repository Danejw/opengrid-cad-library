"""Parametric, pitch-aligned printable object primitives for openGrid projects.

This module does NOT reproduce or certify official snap geometry. Production
snap-in parts must use official publisher-authored models, see docs/INTERFACES.md.
Inputs in inches where named *_in; CAD library models internally in mm.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import cadquery as cq

MM_PER_IN = 25.4
GRID_MM = 28.0
GRID_IN = GRID_MM / MM_PER_IN


def inch(value: float) -> float:
    return float(value) * MM_PER_IN


def grid_span(cells: int) -> float:
    if not isinstance(cells, int) or cells < 1:
        raise ValueError('cells must be a positive integer')
    return GRID_MM * cells


def centered_grid_locations(cells: int) -> list[float]:
    """Zero-centered *cell centers* in mm, not accessory snap profiles."""
    span = grid_span(cells)
    return [(-span / 2 + (i + .5) * GRID_MM) for i in range(cells)]


def mounting_pattern(width_cells: int, height_cells: int):
    """Hole centers in inches, useful for external native connector placement."""
    return [(round(x / MM_PER_IN, 4), round(y / MM_PER_IN, 4))
            for x in centered_grid_locations(width_cells)
            for y in centered_grid_locations(height_cells)]


def test_pitch_coupon(cells_w=3, cells_h=2, aperture_in=.78, thickness_in=.16):
    """Calibration plate with square clearance windows, NOT official openGrid.

    Use it to verify printer pitch and dimensions; do not test native snap fit
    on this coupon. Native openGrid board geometry is more sophisticated.
    """
    if aperture_in >= GRID_IN - .15 or aperture_in < .3:
        raise ValueError('aperture should leave at least .15in of surrounding frame')
    part = cq.Workplane('XY').box(grid_span(cells_w), grid_span(cells_h), inch(thickness_in), centered=(True, True, False))
    for x in centered_grid_locations(cells_w):
        for y in centered_grid_locations(cells_h):
            cutter = (cq.Workplane('XY').box(inch(aperture_in), inch(aperture_in), inch(thickness_in)+2,
                                                centered=(True, True, False))
                      .translate((x, y, -1)))
            part = part.cut(cutter)
    return part


def grid_tray(width_cells=4, depth_cells=3, height_in=1.75, wall_in=.12,
              backplate_in=.22, mounting_hole_in=.17):
    """Working printable desk/storage tray + integrated rear mounting tab.

    Rear tab holes are on the openGrid 28mm grid pitch. Selecting an actual
    wall attachment requires verified upstream snap + fastener geometry.
    Standalone tray can be placed on a desk without mounting.
    """
    if min(width_cells, depth_cells) < 2:
        raise ValueError('tray requires at least two grid cells in each direction')
    w,d,h,t = grid_span(width_cells),grid_span(depth_cells),inch(height_in),inch(wall_in)
    if 2*t >= min(w,d) or h <= 2*t:
        raise ValueError('wall too thick for selected tray size')
    tray = cq.Workplane('XY').box(w,d,h, centered=(True,True,False))
    inner = (cq.Workplane('XY').box(w-2*t,d-2*t,h+2, centered=(True,True,False))
             .translate((0,0,t)))
    tray = tray.cut(inner)
    # Rear upright tab, printable together as part of the tray. The two hole
    # centers are exactly two openGrid cells apart.
    tab_h = min(h, inch(1.25))
    tab = (cq.Workplane('XY').box(w, inch(backplate_in), tab_h,
                                  centered=(True,True,False))
           .translate((0, -d/2 - inch(backplate_in)/2, h-tab_h)))
    tray = tray.union(tab)
    for x in (-GRID_MM, GRID_MM):
        # Bores travel front-to-back through the mounting tab.
        bore=(cq.Workplane('XZ').center(x,h-tab_h/2)
             .circle(inch(mounting_hole_in)/2).extrude(inch(backplate_in)+2)
             .translate((0,-d/2+1,0)))
        tray=tray.cut(bore)
    return tray


def vented_crate(width_cells=4, depth_cells=3, height_cells=3,
                  wall_in=.16, bottom_in=.20, vent_in=.70):
    """A one-piece reusable crate with 28mm-spaced windows in four faces.

    Crate windows are intentionally smaller than real openGrid openings for
    structural reasons. Only the *pitch* is shared; these are not a snap-fit
    openGrid accessory surface.
    """
    w,d,h=grid_span(width_cells),grid_span(depth_cells),grid_span(height_cells)
    t=inch(wall_in); bottom=inch(bottom_in); vent=inch(vent_in)
    if not (0 < vent < GRID_MM-2*t):
        raise ValueError('vent must leave structurally usable lattice rails')
    body=cq.Workplane('XY').box(w,d,h, centered=(True,True,False))
    cavity=(cq.Workplane('XY').box(w-2*t,d-2*t,h-bottom+2,centered=(True,True,False))
            .translate((0,0,bottom)))
    body=body.cut(cavity)
    # Wall cutouts, pitch-aligned and with walls left around openings.
    for x in centered_grid_locations(width_cells):
        for z in centered_grid_locations(height_cells):
            for yy in (-d/2,d/2):
                cutter=(cq.Workplane('XY').box(vent, t+2, vent, centered=(True,True,True))
                        .translate((x,yy,z)))
                body=body.cut(cutter)
    for y in centered_grid_locations(depth_cells):
        for z in centered_grid_locations(height_cells):
            for xx in (-w/2,w/2):
                cutter=(cq.Workplane('XY').box(t+2, vent, vent, centered=(True,True,True))
                        .translate((xx,y,z)))
                body=body.cut(cutter)
    return body


def adapter_blank(width_cells=3, height_cells=2, thickness_in=.19,
                  bolt_hole_in=.17):
    """Flat, printable mounting blank with standardized interface center marks.

    Attach upstream native openGrid mounting snaps to this part in CAD, or
    mount with independently specified fasteners after verification. Geometry
    is a blank adapter; it contains no counterfeit snap interface.
    """
    w,h,t=grid_span(width_cells),grid_span(height_cells),inch(thickness_in)
    plate=cq.Workplane('XY').box(w,h,t,centered=(True,True,False))
    for x in centered_grid_locations(width_cells):
        for y in centered_grid_locations(height_cells):
            hole=(cq.Workplane('XY').center(x,y).circle(inch(bolt_hole_in)/2)
                  .extrude(t+2).translate((0,0,-1)))
            plate=plate.cut(hole)
    return plate


def export_model(model: cq.Workplane, stem: Path):
    stem=Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(model, str(stem)+'.step')
    cq.exporters.export(model, str(stem)+'.stl', tolerance=0.12, angularTolerance=0.25)
    return stem


BUILDERS = {'pitch_coupon':test_pitch_coupon,'grid_tray':grid_tray,
            'vented_crate':vented_crate, 'adapter_blank':adapter_blank}
