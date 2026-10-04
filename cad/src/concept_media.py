"""HeapLine concept media (TRL 3, constructable design HPL-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes every component from cad/src/model.py in the display layout (the kit laid out beside the
open site box) and renders the media set with .kit/concept.py: hero, exploded view with BOM
callouts, concept blueprint, capstan energy flow, and the web model (model.glb with viewer.html).
Coloured parts carry the BOM line numbers of bom/bom.csv; the grey 1.75 m person beside the
capstan is context only. Figures on the sheet and in the flow diagram come from
docs/04-calcs/sizing.py (HPL-CAL-001). CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound, Color, export_gltf  # noqa: E402
import matplotlib.colors as mc  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
import drawing  # noqa: E402
from sheets import safe_project_views  # noqa: E402

# The rope coils are tori whose B-spline edges the kit's SVG export cannot convert; project the
# blueprint views edge by edge and skip any edge that fails (sheets.safe_project_views).
drawing.project_views = lambda part, workdir, line_weight=0.35, center_lines=True: safe_project_views(part, workdir, line_weight)
from model import PARAMS as P, build_components, CAP_AT, bx  # noqa: E402

C = build_components(P, "display")

STYLE = {  # key: (colour, exploded offset in mm)
    "box_body": ("#0F766E", (0, 0, 0)),
    "box_lid": ("#115E59", (0, 0, 0)),
    "box_hardware": ("#374151", (0, 0, 0)),
    "boards": ("#B45309", (0, 0, 0)),
    "links": ("#374151", (0, 0, 250)),
    "probes": ("#DC2626", (0, 0, 0)),
    "shovels": ("#6B7280", (0, 0, 0)),
    "frame": ("#1D4ED8", (0, 0, 0)),
    "roller": ("#15803D", (-250, 0, 0)),
    "roller_pin": ("#374151", (-250, 0, 0)),
    "bushes": ("#F5F5F4", (0, 0, 600)),
    "drum": ("#C2410C", (0, 0, 600)),
    "drive_ratchet": ("#A16207", (0, 0, 1050)),
    "shear_pin": ("#DC2626", (0, 0, 1150)),
    "head": ("#111827", (0, 0, 1300)),
    "hold_pawls": ("#7C3AED", (0, 0, 300)),
    "drive_pawl": ("#7C3AED", (0, 0, 1300)),
    "bars": ("#4B5563", (0, 0, 1300)),
    "bar_pins": ("#111827", (0, 0, 1450)),
    "keeper": ("#0E7490", (0, 0, 1600)),
    "stakes": ("#57534E", (0, 0, 0)),
    "rope": ("#E11D48", (0, 0, 0)),
    "sling": ("#F97316", (0, 0, 0)),
    "clamp_bars": ("#2563EB", (0, 0, 0)),
    "clamp_bolts": ("#111827", (0, 0, 150)),
    "sheet": ("#FACC15", (0, 0, 0)),
    "straps": ("#1E3A8A", (0, 0, 150)),
    "wands": ("#F97316", (0, 0, 0)),
}
parts = []
for key, comp in C.items():
    color, off = STYLE[key]
    shape = comp.shape
    if key == "stakes":                       # show only the parts above ground in the pictures
        shape = shape & bx(-20000, 20000, -20000, 20000, 0, 400)
    parts.append(Part(comp.name, shape, color, comp.bom, off))

person = human_figure(1750.0, x=CAP_AT[0] + 1300.0, y=CAP_AT[1] + 700.0, z=0.0)
context = [person]

flow = {"title": "capstan energy per metre of rope at 5 kN, kJ (HPL-CAL-001 estimates)", "unit": "kJ",
        "stages": [("Four people at the bars", 5.35), ("Drum", 5.0), ("Load moved 1 m", 5.0),
                   ("Sheeting or timber off the dig", "5 kN pull")],
        "losses": [(0, "Bush friction on the post", 0.35)]}

outs = render_all(
    parts, project="HeapLine", title="Dumpsite slide-rescue kit concept", dwg_no="HPL-DWG-010",
    key_figures=["Site box: reused crate or 1.74 x 1.06 x 1.13 m plywood box; stays at the shed",
                 "Six 3.07 m probes, 18 mm tip, in three 1 m sections",
                 "Four 1.5 x 0.45 m crawl boards, 9.7 kg; 44 mm sinkage",
                 "Capstan: 5 kN with four people at 114 N each",
                 "Shear pin releases at about 6.4 kN; drum held by two pawls",
                 "Carried in two waves: 21.5 kg each for four, then 21.7 kg each for three",
                 "Parts USD 830 a site plus a share of the USD 449 capstan set (target USD 1,800)"],
    scale_figure=False, context=context, cut=False, web_model=False, flow=flow)

# Web model at a coarse tessellation (a few MB), with the kit's viewer page
md = ROOT / "media"
kids = []
for p in parts:
    sh = p.shape
    sh.color = Color(*mc.to_rgb(p.color))
    sh.label = p.name
    kids.append(sh)
export_gltf(Compound(kids), str(md / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
(md / "viewer.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>HeapLine: dumpsite slide-rescue kit concept</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}model-viewer{width:100vw;height:100vh}
.tag{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="HeapLine: dumpsite slide-rescue kit concept" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 65deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
print({k: str(v) for k, v in outs.items()}, "model.glb", round((md / "model.glb").stat().st_size / 1e6, 2), "MB")
