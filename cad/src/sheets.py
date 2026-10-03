"""HeapLine drawing sheets, Rev P2 (TRL 3, constructable design HPL-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/HPL-DWG-001 (hand capstan, general arrangement) and HPL-DWG-002 (site box,
packed arrangement) as SVG, PDF and PNG from cad/src/model.py with .kit/drawing.py. Overall sizes
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
from model import PARAMS as P, capstan_parts, box_parts, packed_contents, derived, CAPSTAN_KEYS  # noqa: E402

DATE = "2026-10-03"
REVS = [("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
        ("P2", "HPL-DDR-002: design for construction", DATE, "AC")]


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
    work = ROOT / "cad" / "drawings" / "_views2"
    views = safe_project_views(Compound([bxp["box_body"], bxp["box_hardware"]] + list(pk.values())), work, line_weight=0.25)
    work2 = ROOT / "cad" / "drawings" / "_views2b"
    iso = safe_project_views(Compound(list(bxp.values())), work2, line_weight=0.25)["iso"]
    s = Sheet(project="HeapLine", title="Site box: packed arrangement", dwg_no="HPL-DWG-002", rev="P2",
              author="Amish Chadha", date=DATE, scale=1 / 20, theme="technical",
              material="18 mm exterior plywood box; contents per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(iso, 276, 32, 140, 92, label="Isometric view, lid closed", sublabel="Not to scale; seen from the front right")
    s.add_notes("Packing and box (mm)", [
        "Box outside 1700 x 1020 x 1060 on skids; lid 1740 x 1060 (1, 2)",
        "Inside 1664 x 984 x 1042; corner battens 45 x 45",
        "Back: four crawl boards flat, 340 high (4)",
        "On the boards: four shovels, probe bag, bars, rolled stretcher",
        "Front right: capstan upright, bars off, stakes out (9 to 17)",
        "Front left: rope, slings and clamp, stakes, lookout and PPE bags",
        "Lid: drill card inside, stop rule outside (27)",
        "Combination padlock on the front hasp (3)",
        "Lid closed in the views; contents shown inside (top view)",
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
