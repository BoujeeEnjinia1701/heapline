"""HeapLine drawing sheets: HPL-DWG-001 Rev P2, HPL-DWG-002 Rev P3 (TRL 3, HPL-DDR-002 and HPL-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/HPL-DWG-001 (hand capstan, general arrangement) and HPL-DWG-002 (search crate
and capstan crate, packed arrangement) as SVG, PDF and PNG from cad/src/model.py with .kit/drawing.py. Overall sizes
are dimensioned by the kit; main dimensions and interfaces are listed in the notes, taken from
PARAMS and derived(). The concept blueprint in media/ is HPL-DWG-010; the making sketches for the
build plan are HPL-DWG-101 onward (cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet  # noqa: E402
from build123d import Pos  # noqa: E402
from model import PARAMS as P, capstan_parts, box_parts, packed_contents, packed_capstan, derived, CAPSTAN_KEYS  # noqa: E402

DATE = "2026-10-03"
REVS = [("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
        ("P2", "HPL-DDR-002: design for construction", DATE, "AC")]
REVS_BOX = REVS + [("P3", "HPL-DDR-003: search crate at every site, capstan crate at the host site", DATE, "AC")]


def safe_project_views(part, workdir, line_weight=0.35):
    """Front, top, right and iso views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except Exception:  # noqa: BLE001  (degenerate or unconvertible edge)
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def capstan_sheet():
    cap = capstan_parts(P)
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views1"
    from model import bx
    shapes = [cap[k] if k != "stakes" else cap[k] & bx(-2000, 2000, -2000, 2000, 0, 400) for k in CAPSTAN_KEYS]
    views = safe_project_views(Compound(shapes), work)
    s = Sheet(project="HeapLine", title="Hand capstan: general arrangement", dwg_no="HPL-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE, scale=1 / 20, theme="technical",
              material="Steel weldments, acetal bushes, bought rope and lifting gear per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; seen from the front right; stakes shown above ground")
    s.add_notes("Main dimensions and interfaces (mm)", [
        "Frame 700 x 440, 40 x 40 x 3 SHS; centre member 100 x 40 x 4 (9)",
        "Post 60.3 x 5.0, 995 tall, welded through the centre member (9)",
        f"Drum barrel 114.3 x 3.6, {P['barrel'][2]:.0f} long, 230 discs; spindle 76.1 x 3.2 (10)",
        f"Rope 14 at {D['r_rope']:.1f} radius, four turns, tailed by hand (20)",
        "Holding ring 24 teeth, 210 OD; two holding pawls on 12 pins (13)",
        "Drive ratchet 20 teeth, 160 OD, on the top flange (11)",
        "6 mm S275 shear pin on a 60 radius: about 6.4 kN rope (18)",
        f"Lever head sleeve 88.9 x 5.0; bars 40 x 40 x 2.5 x 900 at {D['z_bar']:.0f} up (12, 14)",
        f"Rope leaves under the roller at {D['z_rope_out']:.0f} up; anchor eye at the same height",
        "Acetal bushes on the post (15); keeper collar and pin on top (17)",
        "Third-angle; front view from -Y; load toward -X; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "HPL-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


def box_sheet():
    bxp = box_parts(P)
    pk = packed_contents(P)
    cbx = box_parts(P, which="cap_box")
    pc = packed_capstan(P)
    dx = P["box"][0] / 2 + P["cap_box"][0] / 2 + 400.0       # capstan crate drawn to the right of the search crate
    work = ROOT / "cad" / "drawings" / "_views2"
    shapes = ([bxp["box_body"], bxp["box_hardware"]] + list(pk.values())
              + [Pos(dx, 0, 0) * s_ for s_ in [cbx["box_body"], cbx["box_hardware"]] + list(pc.values())])
    views = safe_project_views(Compound(shapes), work, line_weight=0.25)
    work2 = ROOT / "cad" / "drawings" / "_views2b"
    iso = safe_project_views(Compound(list(bxp.values()) + [Pos(dx, 0, 0) * s_ for s_ in cbx.values()]), work2, line_weight=0.25)["iso"]
    Lb, Wb, Hb = P["box"]
    Lc, Wc, Hc = P["cap_box"]
    t = P["ply"]
    s = Sheet(project="HeapLine", title="Search crate and capstan crate: packed arrangement", dwg_no="HPL-DWG-002", rev="P3",
              author="Amish Chadha", date=DATE, scale=1 / 25, theme="technical",
              material="Reused timber crates (or bought job boxes) of at least these sizes; contents per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS_BOX)
    s.add_ortho(views)
    s.add_svg(iso, 276, 32, 140, 92, label="Isometric view, lids closed", sublabel="Not to scale; search crate left, capstan crate right")
    s.add_notes("Packing and crates (mm)", [
        f"Search crate, every site: outside {Lb:.0f} x {Wb:.0f} x {Hb:.0f} on skids (1, 2)",
        f"Inside at least {Lb - 2 * t:.0f} x {Wb - 2 * t:.0f} x {Hb - t:.0f}; corner battens 45",
        "Back: four crawl boards flat; shovels, probe bag on top (4 to 8)",
        "Front: lookout and lights bag, PPE bag, stretcher roll on top",
        f"Capstan crate, host site only: outside {Lc:.0f} x {Wc:.0f} x {Hc:.0f} (31)",
        f"Inside at least {Lc - 2 * t:.0f} x {Wc - 2 * t:.0f} x {Hc - t:.0f}",
        "Capstan upright at the back, bars off, stakes out (9 to 17)",
        "Front: rope, slings and clamp, stakes, two bars standing",
        "Lids: drill card inside, stop rule outside (27)",
        "Combination padlock on each front hasp (3)",
        "Third-angle; front view from -Y; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "HPL-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(work2, ignore_errors=True)
    print("wrote", out)


if __name__ == "__main__":
    which = sys.argv[1:] or ["capstan", "box"]
    if "capstan" in which:
        capstan_sheet()
    if "box" in which:
        box_sheet()
