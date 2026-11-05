"""HeapLine product appearance model (build123d), TRL 3, kit 1.9 (STANDARDS sections 12 and 24).

Every product part is components(CHOSEN) from cad/src/model.py as it is, in the display layout: the open search
crate with its boards, link plates, probes, shovels, stretcher and wands, and beside it the pumped friction
capstan with its rope, stakes, hammer, sling, clamp and the capstan crate. Only the site is added, as context parts:
the waste pickers' shed wall (reaching below ground) and a 1.75 m mannequin standing on the ground beside the capstan.
Appearance additions not in model.py, recorded in docs/REVIEW.md: the shed wall and the person.
The hero is rendered by .kit/photoreal.py as an outdoor scene on soil, ground level at model z = 0.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the capstan pull set), "internal" (search kit, crates, sling coil, clamp), "context" (shed, person).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P, CAP_AT, bx  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "HeapLine: slide-rescue kit kept at the waste pickers' shed"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=40,-75", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -38, "args": _SITE,
     "note": "Site render from the front right and above (about 24 deg elevation), on bare soil in front of the shed wall: the open "
             "search crate with its drill card, crawl boards, six probes and the sheet stretcher, the pumped friction capstan with "
             "its rope on the right, the closed capstan crate, and a 1.75 m person standing on the ground beside the capstan"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -48,
     "note": "Studio render of the pumped friction capstan from the front right and above (about 24 deg elevation): welded frame "
             "with post and roller, acetal bushes, drum with holding ratchet and pawls, drive ratchet with shear pin, lever head, "
             "bars, keeper, four turns of rope and the anchor shackle"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded pumped friction capstan from the front right and above (about 26 deg elevation): frame, bushes, roller, "
             "drum with ratchet and pawls, shear pin, lever head, bars, keeper and rope"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 28, "az": -35,
     "note": "Detail from the front right and above (about 28 deg elevation): the open search crate with its hinged lid on a stay, "
             "drill card, crawl boards and link plates, probes and stretcher"},
]


def product_parts(P=P):
    out = [dict(p) for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    # site: the shed wall behind the crate, reaching below ground
    out.append(part("Shed wall (site)", bx(-3600.0, 5400.0, 1700.0, 1900.0, -400.0, 2600.0), "concrete", kind="context", group="context"))
    from context_parts import mannequin
    px, py = PERSON_AT
    person = Pos(px, py, 0) * Rot(0, 0, -62) * mannequin(1750, "stand")
    out.append(part("Person, 1.75 m (scale)", person, "skin", kind="context", group="context"))
    return out


PERSON_AT = (CAP_AT[0] + 650.0, CAP_AT[1] + 950.0)


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:18s} vol={s.volume / 1000:9.1f} cm3")
