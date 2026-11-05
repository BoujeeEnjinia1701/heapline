"""HeapLine concept media (TRL 3, constructable design HPL-DDR-002 with HPL-DDR-003), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py [web]
With `web` it writes only media/model.glb and viewer.html (the web model stays under about 20 MB).
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
import model as M  # noqa: E402
from model import PARAMS as P, CAP_AT, bx, by_key, EXPLODE, KEYNAME  # noqa: E402

# Every concept picture is made from the kit 1.9 D3 model of option A (cad/src/model.py): the parts are grouped by
# component (key) so the callouts match the BOM lines; colours are those of the real materials.
RAW = [p for p in M.components("A", "display") if p["kind"] != "context"]
FIRST = {}
for p_ in RAW:
    FIRST.setdefault(p_["key"], p_)
parts = []
for key, shape in by_key(RAW).items():
    f = FIRST[key]
    if key == "stakes":                       # show only the parts above ground in the pictures
        shape = shape & bx(-20000, 20000, -20000, 20000, 0, 400)
    parts.append(Part(KEYNAME.get(key, f["name"]), shape, f["color"], f["bom"], EXPLODE.get(key, (0, 0, 0))))

person = human_figure(1750.0, x=CAP_AT[0] + 1300.0, y=CAP_AT[1] + 700.0, z=0.0)
context = [person]

flow = {"title": "capstan energy per metre of rope at 5 kN, kJ (HPL-CAL-001 estimates)", "unit": "kJ",
        "stages": [("Four people at the bars", 5.35), ("Drum", 5.0), ("Load moved 1 m", 5.0),
                   ("Sheeting or timber off the dig", "5 kN pull")],
        "losses": [(0, "Bush friction on the post", 0.35)]}

WEB_ONLY = len(sys.argv) > 1 and sys.argv[1] == "web"
outs = {} if WEB_ONLY else render_all(
    parts, project="HeapLine", title="Dumpsite slide-rescue kit concept", dwg_no="HPL-DWG-010",
    key_figures=["Search crate 1.68 x 0.90 x 0.71 m, reused; stays at the shed",
                 "Six 3.07 m probes, 18 mm tips; 2.6 m deep with two people",
                 "Four 1.5 x 0.45 m crawl boards, 9.7 kg; 44 mm sinkage",
                 "Capstan: 5 kN with four people at 114 N each",
                 "Shear pin releases at about 6.4 kN; drum held by two pawls",
                 "Two waves: search kit 21.5 kg each, capstan 21.4 kg each",
                 "USD 827 a site; shared capstan set USD 547 a group"],
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
