"""HeapLine product appearance model (build123d), TRL 3, constructable design (HPL-DDR-002, HPL-DDR-003).

For photoreal renders only (.kit/export_views.py, then .kit/photoreal.py on Amish's Mac). Every
part is the model.py solid itself, placed in the display layout of model.py (the kit laid out beside
the open search crate, a reused crate refitted, with the 18 mm probe tips of HPL-DDR-003); colours and
materials are added for the look. The capstan set shown beside it is the one shared set, kept at the
host site in its own crate. Appearance additions not in
model.py, recorded in docs/REVIEW.md: four turns of rope on the drum with a lead to the coil, the
printed drill card on the inside of the lid, and a posed 1.75 m mannequin standing beside the
capstan (never between the camera and the kit). CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos, Rot, Torus  # noqa: E402
from model import PARAMS as P, derived, build_components, bx, rod, CAP_AT  # noqa: E402

TITLE = "HeapLine: slide-rescue kit kept at the waste pickers' shed"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -38,
     "note": "Product render from the front right and above (about 24 deg elevation): the open search crate (a reused crate) with its drill "
             "card, six probes standing in a line, two linked crawl boards, the sheet stretcher and sheet clamp, "
             "shovels and spare boards on the left, and the hand capstan on the right with a person standing beside it"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 22, "az": -45,
     "note": "Exploded hand capstan from the front right and above (about 22 deg elevation): base frame with post, "
             "bushes, drum with holding ratchet, pawls, drive ratchet and shear pin, lever head, bars, keeper, "
             "hold-down roller and stakes"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right and above (about 18 deg elevation): the hand capstan assembled, with four "
             "turns of rope on the drum leading out under the hold-down roller"},
]

LOOK = {  # key: (colour, material, group, exploded offset)
    "frame": ("#1D4ED8", "painted steel", "shell", (0, 0, 0)),
    "roller": ("#15803D", "painted steel", "shell", (-300, 0, 0)),
    "roller_pin": ("#9CA3AF", "bright steel", "shell", (-300, 0, 0)),
    "bushes": ("#F5F5F4", "acetal", "shell", (0, 0, 500)),
    "drum": ("#C2410C", "painted steel", "shell", (0, 0, 650)),
    "drive_ratchet": ("#A16207", "steel", "shell", (0, 0, 1050)),
    "shear_pin": ("#DC2626", "steel", "shell", (0, 0, 1200)),
    "head": ("#111827", "painted steel", "shell", (0, 0, 1350)),
    "hold_pawls": ("#7C3AED", "painted steel", "shell", (0, 0, 250)),
    "drive_pawl": ("#7C3AED", "painted steel", "shell", (0, 0, 1350)),
    "bars": ("#4B5563", "painted steel", "shell", (0, 0, 1350)),
    "bar_pins": ("#9CA3AF", "bright steel", "shell", (0, 0, 1500)),
    "keeper": ("#0E7490", "painted steel", "shell", (0, 0, 1650)),
    "stakes": ("#57534E", "steel", "shell", (0, 0, 0)),
    "box_body": ("#0F766E", "painted timber crate", "internal", (0, 0, 0)),
    "box_lid": ("#115E59", "painted timber crate", "internal", (0, 0, 0)),
    "box_hardware": ("#9CA3AF", "galvanised steel", "internal", (0, 0, 0)),
    "boards": ("#B45309", "plywood", "internal", (0, 0, 0)),
    "links": ("#9CA3AF", "galvanised steel", "internal", (0, 0, 0)),
    "probes": ("#DC2626", "painted steel", "internal", (0, 0, 0)),
    "shovels": ("#6B7280", "steel", "internal", (0, 0, 0)),
    "sheet": ("#FACC15", "HDPE plastic", "internal", (0, 0, 0)),
    "straps": ("#1E3A8A", "polyester webbing", "internal", (0, 0, 0)),
    "clamp_bars": ("#2563EB", "painted steel", "internal", (0, 0, 0)),
    "clamp_bolts": ("#9CA3AF", "zinc plated steel", "internal", (0, 0, 0)),
    "rope": ("#E11D48", "polyester rope", "internal", (0, 0, 0)),
    "sling": ("#F97316", "polyester webbing", "internal", (0, 0, 0)),
    "wands": ("#F97316", "fibreglass", "internal", (0, 0, 0)),
}


def product_parts(P=P):
    D = derived(P)
    C = build_components(P, "display")
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for k, c in C.items():
        color, mat, grp, ex = LOOK[k]
        shape = c.shape
        if k == "stakes":
            shape = shape & bx(-20000, 20000, -20000, 20000, 0, 400)
        add(c.name, shape, color, mat, c.bom, grp, ex)
    # four turns of rope on the drum and a lead to the coil
    cx, cy = CAP_AT
    r = D["r_rope"]
    wraps = None
    for i in range(4):
        t = Pos(cx, cy, 110.0 + i * 15.0) * Torus(r, P["rope_d"] / 2)
        wraps = t if wraps is None else wraps + t
    rx = P["roller"][0]
    lead = (rod((cx, cy - r, 110.0), (cx + rx, cy - r, D["z_rope_out"]), 7.0)
            + rod((cx + rx, cy - r, D["z_rope_out"]), (cx - 50.0, cy - 1300.0 + 260.0, 7.0 + 14 * 3), 7.0))
    add("Rope on the drum", wraps + lead, "#E11D48", "polyester rope", 20, "shell", (0, 0, 650))
    # printed drill card on the inside of the open lid
    L, W, H = P["box"]
    t_ = P["ply"]
    g, sk = P["lid_gap"], P["skirt"]
    Wo = W + 2 * (g + t_)
    zl = P["skid"][1] + H + 3.0
    card = bx(-500, 500, -Wo / 2 + 180, Wo / 2 - 180, zl - 1.0, zl)
    card = Pos(0, Wo / 2, zl) * Rot(-P["lid_open_deg"], 0, 0) * Pos(0, -Wo / 2, -zl) * card
    add("Drill card on the lid", card, "#F9FAFB", "printed vinyl", 27, "internal", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(cx + 1300.0, cy + 700.0, 0) * Rot(0, 0, -62) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, "#D1D5DB", "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:18s} vol={s.volume / 1000:9.1f} cm3")
