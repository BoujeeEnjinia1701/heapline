"""HeapLine parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every concept option.

Run from the repo root:  python cad/src/model.py          (counts, masses, constructability checks, STL)
                         python cad/src/model.py --check  (no STL)
The kit check is  python .kit/cad_check.py --export  (STEP per made or bought part of option A, assembly STEP
per option, cad/fidelity.json).

Interface read by the kit and by the repo's scripts:
    PARAMS         every main dimension, in mm (docs/04-calcs/sizing.py, the drawings and the build plan read it)
    OPTIONS        key -> name of each concept option (docs/02a-concept-options.md, HPL-OPT-001)
    PRINCIPLES     key -> one-line working principle
    CHOSEN         "A", the current design (the option carried to the drawings, BOM and build plan; not a
                   decision by Amish, see HPL-DEC-001)
    OPTION_VIEWS   render elevation, azimuth and scale figure for the options picture
    ALLOWED_CONTACTS  part-name pairs that may touch or overlap (fused welds, pins in their own bores)
    components(option)  list of cad_parts.part() dicts for the whole kit with that option's pull set

Every option is the whole kit: the search kit (crate, boards, link plates, probes, shovels, stretcher, lookout
wands; BOM lines 1 to 8, 23, 24, 27) is common, and the pull set that removes sheeting, timber and debris from a
mark differs:
    A  Pumped friction capstan with shear pin and holding pawls (the current design, BOM 9 to 22, 31)
    B  Six-part block-and-tackle purchase with a rope grab and a shear link (opt_b.py)
    C  Lever rope-grip puller: the rope runs straight through two cams worked by a long lever, no drum (opt_c.py)

Axes: Z is up with the ground at z = 0. Display layout: the kit laid out beside the open search crate, the
capstan on the right, the capstan crate behind it, the way the hero is drawn. 'site' layout (build plan steps):
the kit deployed at a slide.

Design changes since the kit 1.7 model are modelling only and are listed in HPL-DDR-005 (docs/decisions).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Cylinder, Plane, Pos, Rot, Solid, Torus, Vector, export_stl as _export_stl  # noqa: E402
import cad_parts as cp  # noqa: E402
from hpl_parts import (part, bx, ycyl, xcyl, zcyl, ztube, ytube, prism_xz, prism_xy, rod, hull2d, circle_pts, fuse,  # noqa: E402
                       bow_shackle, coil, be)
import hpl_capstan as HC  # noqa: E402
import hpl_kit as HK  # noqa: E402

TITLE = "HeapLine"

# Top-level parameters (mm). Edit these, not the geometry.
PARAMS = {
    # ---- capstan base frame (BOM 9): SHS size and wall, frame outer length (X) and width (Y)
    "shs": (40.0, 3.0), "frame_l": 700.0, "frame_w": 440.0,
    "rhs": (100.0, 40.0, 4.0),          # centre cross member, width along X, height, wall
    "post": (60.3, 5.0, 995.0),         # fixed post OD, wall, height above ground
    "stake_tube": (33.7, 3.2, 60.0),
    "stake": (25.0, 500.0, 360.0),      # stake dia, length, depth below ground
    "roller": (-415.0, 75.0, 60.3, 3.6, 200.0), "cheek_t": 8.0, "roller_pin": 20.0,
    "eye": (10.0, 22.0),
    # ---- drum (BOM 10): stack heights (z) from the frame top up
    "z_frame": 40.0, "washer_t": 4.0, "ring_t": 6.0, "disc_t": 6.0, "disc_d": 230.0,
    "barrel": (114.3, 3.6, 260.0),
    "spindle": (76.1, 3.2), "z_flange": 850.0, "flange": (140.0, 8.0),
    "hold_ratchet": (210.0, 186.0, 24),
    "drive_ratchet": (160.0, 136.0, 20, 8.0),
    "shear_pin": (6.0, 60.0),
    # ---- lever head (BOM 12), bars (BOM 14), keeper (BOM 17)
    "sleeve": (88.9, 5.0, 80.0), "socket": (50.0, 3.0, 150.0), "bar": (40.0, 2.5, 900.0),
    "bar_insert": 140.0, "keeper": (80.0, 20.0), "keeper_pin": 10.0,
    "pawl_t": (10.0, 8.0),
    # ---- rope (BOM 20)
    "rope_d": 14.0, "rope_mbs": 40000.0, "rope_len": 30.0,
    # ---- probe (BOM 6)
    "probe_tube": (16.0, 2.0, 1000.0, 3), "probe_tip": (18.0, 35.0, 20.0, 30.0),
    "probe_spigot": (11.5, 120.0), "probe_pin": 5.0, "probe_handle": (26.9, 2.6, 450.0),
    # ---- crawl board (BOM 4)
    "board": (1500.0, 450.0, 15.0), "batten": (45.0, 70.0, 30.0),
    "link": (40.0, 6.0, 160.0, 12.0, 75.0, 40.0),
    "hand_slot": (140.0, 35.0, 75.0),
    # ---- search crate (BOM 1, 2) and capstan crate (BOM 31)
    "box": (1640.0, 860.0, 640.0), "cap_box": (940.0, 900.0, 1060.0),
    "ply": 18.0, "skid": (70.0, 45.0), "skirt": 48.0, "lid_gap": 2.0, "lid_open_deg": 100.0,
    # ---- stretcher (BOM 23)
    "sheet": (2000.0, 900.0, 2.0), "sheet_slot": (130.0, 35.0, 60.0), "strap_w": 50.0,
    # ---- sheet clamp (BOM 22)
    "clamp": (50.0, 8.0, 600.0), "clamp_bolts": (100.0, 250.0), "clamp_gap": 3.0,
    # ---- shovel (BOM 8, bought)
    "shovel": (230.0, 290.0, 1450.0),
    # ---- modelling (kit 1.9): fillet weld leg on 3 mm tube
    "weld_leg": 4.0,
    # materials (kg per m^3), as used by sizing.py
    "rho_steel": 7850.0, "rho_ply": 550.0, "rho_timber": 450.0, "rho_hdpe": 950.0, "rho_acetal": 1410.0,
    # ---- option B: six-part tackle (opt_b.py)
    "B": {"sheave_d": 125.0, "sheave_w": 22.0, "plate_t": 6.0, "n_parts": 6, "rope_d": 14.0, "pin_d": 16.0,
          "grab": (60.0, 260.0), "link_pin": 8.0, "stroke": 3.0},
    # ---- option C: lever rope-grip puller (opt_c.py)
    "C": {"rope_height": 200.0, "stroke": 120.0, "lever_ratio": 12.2, "lever_len": 1600.0, "pin_d": 16.0, "rope_d": 14.0}
}

OPTIONS = {"A": "Pumped friction capstan", "B": "Six-part rope tackle", "C": "Lever rope-grip puller"}
PRINCIPLES = {
    "A": "Four people pump two bars through a quarter turn; a ratchet turns a smooth drum on which four turns of rope "
         "grip by friction, a shear pin limits the pull and two pawls hold the drum.",
    "B": "No machine: a six-part block-and-tackle multiplies the pull of six people on a tail rope, a rope grab holds "
         "each gain and a shear link in series limits the load.",
    "C": "No drum: the rope runs straight through the machine; a fixed cam holds it, and a traveller with a second cam is "
         "driven along slotted plates by a long lever, gripping the rope on the pull stroke and sliding free on the return.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 24, "az": -48, "scale": "person", "ground_z": 0.0} for k in OPTIONS}
# welds are fused metal; pins sit in their own bores; ropes lie on their drums and through eyes, handles through cleats
ALLOWED_CONTACTS = [
    ("Weld", ""), ("weld", ""),
    ("Rope handle", ""), ("Capstan rope", ""), ("Puller rope", ""), ("Rope coil", ""), ("Tackle rope", ""),
    ("Shackle", ""), ("shackle", ""), ("Lid stay", ""), ("Combination padlock", ""), ("Staple", ""),
    ("Sling", ""), ("Hinge", "Hinge pin"), ("screws", ""), ("Screws", ""),
]

# Display layout of the kit (mm)
CAP_AT = (2350.0, 150.0)
BOARD_Y = -850.0
STRETCH_AT = (-300.0, -1750.0)
CAPCRATE_AT = (3750.0, 780.0)

EXPLODE = {   # legacy key -> exploded offset (mm) for the capstan in the exploded view
    "frame": (0, 0, 0), "roller": (-300, 0, 0), "roller_pin": (-300, 0, 0), "bushes": (0, 0, 500), "drum": (0, 0, 650),
    "drive_ratchet": (0, 0, 1050), "shear_pin": (0, 0, 1200), "head": (0, 0, 1350), "hold_pawls": (0, 0, 250),
    "drive_pawl": (0, 0, 1350), "bars": (0, 0, 1350), "bar_pins": (0, 0, 1500), "keeper": (0, 0, 1650),
    "stakes": (0, 0, 0), "rope": (0, 0, 650),
}
CAPSTAN_KEYS = ["frame", "roller", "roller_pin", "bushes", "drum", "drive_ratchet", "shear_pin", "head",
                "hold_pawls", "drive_pawl", "bars", "bar_pins", "keeper", "stakes"]


# ----------------------------------------------------------------------------- derived numbers
def derived(P=PARAMS):
    D = {}
    zf = P["z_frame"]
    D["z_ring"] = (zf + P["washer_t"], zf + P["washer_t"] + P["ring_t"])
    D["z_disc0"] = (D["z_ring"][1], D["z_ring"][1] + P["disc_t"])
    D["z_barrel"] = (D["z_disc0"][1], D["z_disc0"][1] + P["barrel"][2])
    D["z_disc1"] = (D["z_barrel"][1], D["z_barrel"][1] + P["disc_t"])
    D["z_spindle"] = (D["z_disc1"][1], P["z_flange"])
    D["z_flange"] = (P["z_flange"], P["z_flange"] + P["flange"][1])
    D["z_drive"] = (D["z_flange"][1], D["z_flange"][1] + P["drive_ratchet"][3])
    D["z_sleeve"] = (D["z_drive"][1] + 2.0, D["z_drive"][1] + 2.0 + P["sleeve"][2])
    D["z_socket"] = ((D["z_sleeve"][0] + D["z_sleeve"][1]) / 2 - P["socket"][0] / 2,
                     (D["z_sleeve"][0] + D["z_sleeve"][1]) / 2 + P["socket"][0] / 2)
    D["z_keeper"] = (D["z_sleeve"][1] + 2.0, D["z_sleeve"][1] + 2.0 + P["keeper"][1])
    D["z_keeper_pin"] = D["z_keeper"][1] + 12.0
    D["r_rope"] = (P["barrel"][0] + P["rope_d"]) / 2
    D["z_bar"] = (D["z_socket"][0] + D["z_socket"][1]) / 2
    D["r_grip"] = P["sleeve"][0] / 2 + 10.0 + P["bar"][2] - P["bar_insert"] - 60.0
    D["r_bar_end"] = P["sleeve"][0] / 2 + 10.0 + P["bar"][2] - P["bar_insert"]
    rx, rz, ro, _, _ = P["roller"]
    D["z_rope_out"] = rz - ro / 2 - P["rope_d"] / 2
    td, tw, tl, n = P["probe_tube"]
    dt, cone, par, spg = P["probe_tip"]
    D["probe_len"] = cone + par + n * tl + P["probe_handle"][0] / 2
    return D


# ----------------------------------------------------------------------------- placing parts
def _place(parts, loc, group=None, suffix=""):
    out = []
    for p in parts:
        q = dict(p, shape=loc * p["shape"])
        if group:
            q["group"] = group
        if suffix:
            q["name"] = p["name"] + suffix
        out.append(q)
    return out


# ----------------------------------------------------------------------------- the common search kit
def search_kit(P, layout="display"):
    """Search crate, boards, link plates, probes, shovels, stretcher, clamp-free lookout wands, in the layout."""
    L, W, t = P["board"]
    bd = P["batten"][1]
    yb = W / 2 - P["batten"][2] - P["batten"][0] / 2
    out = []
    if layout == "display":
        out += _place(HK.crate(P, "box", open_lid=True, bom=(1, 2, 3), tag="Search crate", key="box"), Pos(0, 0, 0), "internal")
        out += _place(HK.board_parts(P, "Board 1"), Pos(-L / 2, BOARD_Y, 0), "internal")
        out += _place(HK.board_parts(P, "Board 2"), Pos(L / 2, BOARD_Y, 0), "internal")
        out += _place(HK.board_parts(P, "Board 3"), Pos(-2550.0, 350.0, 0) * Rot(0, 0, 90), "internal")
        out += _place(HK.board_parts(P, "Board 4"), Pos(-2550.0, 350.0, bd + t) * Rot(0, 0, 90), "internal")
        for i, y in enumerate((-yb, yb)):
            lp = HK.link_plate_part(P, f"Board link plate {i + 1}", 0.0, BOARD_Y + y)
            lp["group"] = "internal"
            out.append(lp)
        for k in range(6):
            out += _place(HK.probe_parts(P, f"Probe {k + 1}"), Pos(-1250.0 + 500.0 * k, -1190.0, 0) * Rot(0, 0, 90), "internal")
        for k in range(4):
            out += _place(HK.shovel_parts(P, f"Shovel {k + 1}"), Pos(-2550.0, -900.0 - k * 260.0, 0), "internal")
        out += _place(HK.stretcher_parts(P), Pos(STRETCH_AT[0], STRETCH_AT[1], 0), "internal")
        out += _place(HK.wand_parts(P, [(-1700.0, 900.0), (-1550.0, 950.0), (-1400.0, 1000.0)]), Pos(0, 0, 0), "internal")
    else:
        # deployed: four boards in a line up the debris (+Y), probes pushed 1.4 m into it, stretcher alongside
        for k in range(4):
            out += _place(HK.board_parts(P, f"Board {k + 1}"), Pos(0, k * L + L / 2, 0) * Rot(0, 0, 90), "internal")
        for k in range(3):
            for i, y in enumerate((-yb, yb)):
                lp = HK.link_plate_part(P, f"Board link plate {k + 1}{'AB'[i]}", 0.0, y)
                lp = dict(lp, shape=Pos(0, (k + 1) * L, 0) * Rot(0, 0, 90) * lp["shape"], group="internal")
                out.append(lp)
        for k in range(6):
            out += _place(HK.probe_parts(P, f"Probe {k + 1}"), Pos(-1250.0 + 500.0 * k, 4 * L + 400.0, -1400.0), "internal")
        out += _place(HK.stretcher_parts(P), Pos(-900.0, 2400.0, 0) * Rot(0, 0, 90), "internal")
        out += _place(HK.wand_parts(P, [(-600.0, 6400.0), (0.0, 6500.0), (600.0, 6400.0)]), Pos(0, 0, 0), "internal")
    return out


# ----------------------------------------------------------------------------- option A pull set
def _hammer():
    head = Pos(0, 0, 25) * Rot(90, 0, 0) * Cylinder(25.0, 100.0)
    handle = Pos(162.5, 0, 25) * Box(275.0, 28.0, 28.0)
    return [part("Club hammer head, 1.8 kg", be(head, 2.0), "mild_steel", kind="bought", bom=19, key="stakes"),
            part("Club hammer handle", be(handle, 3.0), "timber", kind="bought", bom=19, key="stakes")]


def option_a(P, layout="display"):
    D = derived(P)
    out = search_kit(P, layout)
    cap = HC.capstan(P, D)
    for p in cap:
        p["explode"] = EXPLODE.get(p["key"], (0, 0, 0))
    r = D["r_rope"] + 0.1
    rd = P["rope_d"]
    turns = Compound([Pos(0, 0, 110.0 + i * (rd + 0.2)) * Torus(r, rd / 2 - 0.05) for i in range(4)])
    cap.append(part("Capstan rope, 14 mm, four turns on the drum", turns, "rope", kind="bought", bom=20, key="rope", explode=EXPLODE["rope"]))
    rx, rz = P["roller"][0], P["roller"][1]
    lead = rod((0, -r, 110.0 + 3 * (rd + 0.2)), (rx, -r, D["z_rope_out"]), rd / 2 - 0.1)
    cap.append(part("Capstan rope, 14 mm, lead under the roller", lead, "rope", kind="bought", bom=20, key="rope", explode=EXPLODE["rope"]))
    xe = P["frame_l"] / 2 + 50.0
    ze = D["z_rope_out"]
    bow, pin = bow_shackle((xe, 0, ze), (0, 1, 0), (1, 0, 0), pin_d=19.0, bow_r=34.0, bar_d=15.0)
    cap.append(part("Shackle bow, anchor eye, WLL 2 t", bow, "galvanised", kind="bought", bom=21, key="sling"))
    cap.append(part("Shackle pin, 19 mm", pin, "zinc_plated", kind="bought", bom=21, key="sling"))
    cap += _hammer_at()
    if layout == "display":
        out += _place(cap, Pos(CAP_AT[0], CAP_AT[1], 0), "shell")
        cx, cy = CAP_AT
        out += _rope_coil_parts(P, D, layout)
        out += _place(HK.clamp_parts(P), Pos(1650.0, -1800.0, 0), "internal")
        sl = coil(CAP_AT[0] + 900.0, CAP_AT[1] - 300.0, 0.0, 150.0, 6.0, 2, 10.0, 12.0)
        out.append(part("Round sling, WLL 2 t, coiled", sl, "polyester", kind="bought", bom=21, key="sling", group="internal"))
        out += _place(HK.crate(P, "cap_box", open_lid=False, bom=(31, 31, 31), tag="Capstan crate", key="capbox"),
                      Pos(CAPCRATE_AT[0], CAPCRATE_AT[1], 0), "internal")
    else:
        ang = 150
        loc = Pos(3600.0, -1400.0, 0) * Rot(0, 0, ang)
        out += _place(cap, loc, "shell")
        out += _rope_coil_parts(P, D, layout)
        out += _place(HK.clamp_parts(P), Pos(1300.0, 3600.0, 0) * Rot(0, 0, -30), "internal")
    return out


def _hammer_at():
    ps = _hammer()
    return [dict(p, shape=Pos(500.0, -700.0, 0) * Rot(0, 0, 20) * p["shape"]) for p in ps]


def _rope_coil_parts(P, D, layout):
    rd = P["rope_d"]
    rx = P["roller"][0]
    r = D["r_rope"] + 0.1
    if layout == "display":
        ex = (CAP_AT[0] + rx, CAP_AT[1] - r, D["z_rope_out"])
        rc = (CAP_AT[0] - 50.0, CAP_AT[1] - 1300.0)
        lay = rod(ex, (rc[0] - 260.0 + 20.0, rc[1], rd / 2), rd / 2 - 0.1)
        cl = Compound([Pos(rc[0], rc[1], rd / 2 + (rd + 0.2) * i) * Torus(260 - 9 * i, rd / 2 - 0.05) for i in range(4)])
        return [part("Rope coil, 14 mm, lead on the ground", lay, "rope", kind="bought", bom=20, key="rope", group="internal"),
                part("Rope coil, 14 mm, 4 loops", cl, "rope", kind="bought", bom=20, key="rope", group="internal")]
    ang = math.radians(150)
    sx = 3600.0 + (rx - 30.0) * math.cos(ang)
    sy = -1400.0 + (rx - 30.0) * math.sin(ang)
    ez = 2 * P["clamp"][1] + P["clamp_gap"] + 45.0
    lay = rod((sx, sy, D["z_rope_out"]), (1300.0, 3600.0, ez), rd / 2 - 0.1)
    xe = 3600.0 + (P["frame_l"] / 2 + 50.0) * math.cos(ang)
    ye = -1400.0 + (P["frame_l"] / 2 + 50.0) * math.sin(ang)
    far = (xe - 2500.0 * math.cos(ang), ye - 2500.0 * math.sin(ang))
    sling = rod((xe, ye, D["z_rope_out"]), (far[0], far[1], D["z_rope_out"] + 40), 12.0)
    return [part("Rope, capstan to sheet clamp", lay, "rope", kind="bought", bom=20, key="rope", group="internal"),
            part("Round sling, capstan to anchor", sling, "polyester", kind="bought", bom=21, key="sling", group="internal")]


# ----------------------------------------------------------------------------- components
def components(option=CHOSEN, layout="display"):
    """Parts of one option, the whole kit, as cad_parts.part() dicts."""
    if option == "A":
        return option_a(PARAMS, layout)
    if option == "B":
        import opt_b
        return opt_b.option_b(PARAMS, layout, search_kit(PARAMS, layout))
    if option == "C":
        import opt_c
        return opt_c.option_c(PARAMS, layout, search_kit(PARAMS, layout))
    raise KeyError(option)


# ----------------------------------------------------------------------------- views for the calculations, drawings and pictures
def by_key(parts, only=None):
    d = {}
    for p in parts:
        if p["kind"] == "context":
            continue
        d.setdefault(p["key"], []).extend(p["shape"].solids())
    return {k: Compound(v) for k, v in d.items() if only is None or k in only}


@dataclass
class Comp:
    name: str
    shape: object
    bom: object
    group: str
    material: str


def build_components(P=PARAMS, layout="display"):
    """Option A as {key: Comp}, one Compound per legacy component key (drawings, concept media, build plan)."""
    parts = components("A", layout)
    names, bom, grp, mat = {}, {}, {}, {}
    for p in parts:
        k = p["key"]
        names.setdefault(k, KEYNAME.get(k, p["name"]))
        bom.setdefault(k, p["bom"])
        grp.setdefault(k, p["group"])
        mat.setdefault(k, p["material_name"])
    return {k: Comp(names[k], sh, bom[k], grp[k], mat[k]) for k, sh in by_key(parts).items()}


KEYNAME = {
    "box_body": "Search crate body", "box_lid": "Search crate lid", "box_hw": "Search crate hinges, hasp and seal",
    "board": "Crawl boards (4)", "link": "Board link plates", "probe_tip_section": "Probes (6)", "probe_mid_section": "Probes (6)",
    "probe_top_section": "Probes (6)", "probe_pins": "Probes (6)", "shovel": "Long-handled shovels (4)",
    "frame": "Capstan base frame with post", "drum": "Capstan drum with holding ratchet", "drive_ratchet": "Drive ratchet wheel",
    "head": "Lever head", "hold_pawls": "Holding pawls", "drive_pawl": "Drive pawl", "bars": "Capstan bars (2)",
    "bar_pins": "Bar pins (2)", "bushes": "Bushes and thrust washers", "roller": "Hold-down roller", "roller_pin": "Roller pin",
    "keeper": "Keeper collar and pin", "shear_pin": "Shear pin", "stakes": "Ground stakes (4) and mallet", "rope": "Capstan rope, 14 mm",
    "sling": "Anchor sling and shackle", "clamp_bars": "Sheet clamp", "clamp_bolts": "Sheet clamp bolts", "sheet": "Sheet stretcher",
    "straps": "Stretcher straps", "wands": "Marker wands", "capbox_body": "Capstan crate body", "capbox_lid": "Capstan crate lid",
    "capbox_hw": "Capstan crate hardware",
}


def capstan_parts(P=PARAMS):
    """Capstan as {key: Compound} in its own frame (drum axis at x = y = 0, ground at z = 0): what the build
    plan pictures and sheets draw. Built from the kit 1.9 parts (welds, bolts and clips included)."""
    D = derived(P)
    ps = HC.capstan(P, D)
    r = D["r_rope"] + 0.1
    return by_key(ps)


def probe_parts(P=PARAMS):
    return by_key(HK.probe_parts(P))


def board(P=PARAMS):
    return Compound([s for p in HK.board_parts(P) for s in p["shape"].solids()])


def link_plate(P=PARAMS, x_joint=0.0):
    L, W, t = P["board"]
    yb = W / 2 - P["batten"][2] - P["batten"][0] / 2
    return Compound([s for y in (-yb, yb) for s in HK.link_plate_part(P, "L", x_joint, y)["shape"].solids()])


def box_parts(P=PARAMS, open_lid=False, which="box"):
    bom = (1, 2, 3) if which == "box" else (31, 31, 31)
    ps = HK.crate(P, which, open_lid=open_lid, bom=bom, tag="Search crate" if which == "box" else "Capstan crate",
                  key="box" if which == "box" else "capbox")
    d = by_key(ps)
    k = "box" if which == "box" else "capbox"
    return {"box_body": d[k + "_body"], "box_lid": d[k + "_lid"], "box_hardware": d[k + "_hw"]}


def stretcher(P=PARAMS):
    d = by_key(HK.stretcher_parts(P))
    return {"sheet": d["sheet"], "straps": d["straps"]}


def sheet_clamp(P=PARAMS):
    d = by_key(HK.clamp_parts(P))
    return {"clamp_bars": d["clamp_bars"], "clamp_bolts": d["clamp_bolts"]}


def shovel(P=PARAMS):
    return Compound([s for p in HK.shovel_parts(P) for s in p["shape"].solids()])


# ----------------------------------------------------------------------------- packed crates (envelopes of bags, real boards and capstan)
def packed_contents(P=PARAMS):
    """The search kit stowed in the closed search crate (crate centred at the origin). Boards and shovels are the
    real parts, bags and bundles their outer envelopes. PPE comes from the cooperative's stock."""
    L, W, H = P["box"]
    t = P["ply"]
    z0 = P["skid"][1] + t
    xi, yi = L / 2 - t, W / 2 - t
    bL, bW, bt = P["board"]
    bd = P["batten"][1]
    out = {}
    bx_c = -xi + 50 + bL / 2
    yb = yi - 4 - bW / 2
    b1 = board(P)
    out["Crawl boards (4), stacked"] = Compound([Pos(bx_c, yb, z0 + k * (bd + bt)) * b1 for k in range(4)])
    ztop = z0 + 4 * (bd + bt)
    sh = shovel(P)
    sl = []
    for layer in range(2):
        for k, sg in enumerate((-1, 1)):
            y = yb + sg * 110
            sl.append(Pos(bx_c, y, ztop + 1 + layer * 40) * (Rot(0, 0, 180) * sh if k else sh))
    out["Shovels (4)"] = Compound(sl)
    z2 = ztop + 82
    out["Probe bag (18 sections)"] = Pos(bx_c, yb, z2 + 80) * Rot(0, 90, 0) * Cylinder(80, 1160)
    xl = -xi + 50
    out["Lookout kit and lights bag"] = bx(xl, xl + 275, -yi + 5, -yi + 345, z0, z0 + 300)
    out["PPE bag"] = bx(xl + 280, xl + 980, -yi + 5, -yi + 345, z0, z0 + 300)
    out["Stretcher, rolled"] = Pos(xl + 40 + 450, -yi + 5 + 170, z0 + 305 + 125) * Rot(0, 90, 0) * Cylinder(125, 900)
    return out


def packed_capstan(P=PARAMS):
    L, W, H = P["cap_box"]
    t = P["ply"]
    z0 = P["skid"][1] + t
    xi, yi = L / 2 - t, W / 2 - t
    out = {}
    cap = capstan_parts(P)
    keys = [k for k in CAPSTAN_KEYS if k not in ("bars", "bar_pins", "stakes")]
    cy = yi - 5 - (P["frame_w"] / 2 + P["stake_tube"][0])
    out["Capstan, bars off"] = Pos(0.0, cy, z0) * Compound([s for k in keys for s in cap[k].solids()])
    xl = -xi + 50
    out["Rope bag"] = bx(xl, xl + 420, -yi + 5, -yi + 345, z0, z0 + 300)
    out["Slings, shackles and sheet clamp bag"] = bx(xl, xl + 420, -yi + 5, -yi + 345, z0 + 305, z0 + 505)
    out["Stakes (4) and mallet"] = bx(xl + 425, xl + 700, -yi + 5, -yi + 345, z0, z0 + 120)
    b = P["bar"][0]
    out["Capstan bars (2), standing"] = Compound([bx(xl + 705 + k * (b + 5), xl + 705 + k * (b + 5) + b, -yi + 5, -yi + 5 + b,
                                                    z0, z0 + P["bar"][2]) for k in range(2)])
    return out


def context_shapes(P=PARAMS, layout="display"):
    if layout == "display":
        return {"shed": bx(-3300.0, 5000.0, 1250.0, 1350.0, -400.0, 2400.0)}
    ang = math.radians(150)
    ex2 = 3600.0 + (P["frame_l"] / 2 + 50.0) * math.cos(ang)
    ey2 = -1400.0 + (P["frame_l"] / 2 + 50.0) * math.sin(ang)
    far = (ex2 - 2500.0 * math.cos(ang) + 150 * -math.cos(ang), ey2 - 2500.0 * math.sin(ang) + 150 * -math.sin(ang))
    debris = prism_xy([(-2600, 1500), (2600, 1500), (2600, 7500), (-2600, 7500)], -1, 0)
    return {"debris": debris, "anchor_post": zcyl(far[0], far[1], 150.0, -300.0, 1800.0)}


# ----------------------------------------------------------------------------- masses and checks
def masses(P=PARAMS):
    """Mass of each legacy component in kg from the model volumes and the repo's material densities
    (sizing.py reads this). Fasteners, welds and bought rope are counted with their component."""
    rho = {"steel": P["rho_steel"], "plywood": P["rho_ply"], "timber": P["rho_timber"], "hdpe": P["rho_hdpe"], "acetal": P["rho_acetal"]}

    def dens(p):
        m = p["material_name"]
        if m == "acetal":
            return rho["acetal"]
        if m in ("plywood", "plywood_painted"):
            return rho["plywood"]
        if m in ("timber", "hardwood"):
            return rho["timber"]
        if m.startswith("hdpe"):
            return rho["hdpe"]
        return cp.MATERIALS[m][2] if m in ("rope", "polyester", "webbing", "fibreglass") else rho["steel"]
    D = derived(P)
    m = {}

    def add(k, p, scale=1.0):
        m[k] = m.get(k, 0.0) + p["shape"].volume * 1e-9 * dens(p) * scale
    for p in HC.capstan(P, D):
        if p["kind"] != "context":
            add(p["key"], p)
    pr = HK.probe_parts(P)
    m["probe"] = sum(p["shape"].volume * 1e-9 * dens(p) for p in pr)
    bp = HK.board_parts(P)
    m["board"] = sum(p["shape"].volume * 1e-9 * dens(p) for p in bp if p["kind"] != "fastener")
    m["link"] = HK.link_plate_part(P)["shape"].volume * 1e-9 * P["rho_steel"]
    for which, pre in (("box", ""), ("cap_box", "cap_")):
        cr = HK.crate(P, which, bom=(1, 2, 3))
        m[pre + "box_body"] = sum(p["shape"].volume * 1e-9 * dens(p) for p in cr if p["key"].endswith("_body") and p["kind"] != "fastener")
        m[pre + "box_lid"] = sum(p["shape"].volume * 1e-9 * dens(p) for p in cr if p["key"].endswith("_lid"))
    st = HK.stretcher_parts(P)
    m["stretcher"] = st[0]["shape"].volume * 1e-9 * P["rho_hdpe"] + 0.6
    cl = HK.clamp_parts(P)
    m["clamp"] = sum(p["shape"].volume * 1e-9 * P["rho_steel"] for p in cl if p["kind"] != "weld")
    m["clamp"] = sum(p["shape"].volume * 1e-9 * P["rho_steel"] for p in cl)
    return m


def _dist(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


def _overlap(a, b):
    ba, bb_ = a.bounding_box(), b.bounding_box()
    if (ba.min.X > bb_.max.X or bb_.min.X > ba.max.X or ba.min.Y > bb_.max.Y or bb_.min.Y > ba.max.Y
            or ba.min.Z > bb_.max.Z or bb_.min.Z > ba.max.Z):
        return 0.0
    try:
        i = a & b
        return 0.0 if i is None else i.volume
    except Exception:
        return float("nan")


def checks(P=PARAMS, verbose=True):
    """Packing checks beyond the kit's: nothing packed overlaps another packed item or its crate, and every
    packed item lies inside its crate's inside space (HPL-DWG-002)."""
    res = {"overlaps": []}
    for nm, (pk, which) in {"search crate": (packed_contents(P), "box"), "capstan crate": (packed_capstan(P), "cap_box")}.items():
        cb = box_parts(P, which=which)
        shell = [cb["box_body"], cb["box_lid"], cb["box_hardware"]]
        names = list(pk)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                v = _overlap(pk[a], pk[b])
                if not v < 5.0:
                    res["overlaps"].append((nm + ": " + a, b, round(v, 1)))
            for sh_ in shell:
                v = _overlap(pk[a], sh_)
                if not v < 5.0:
                    res["overlaps"].append((nm + ": " + a, "crate", round(v, 1)))
        L_, W_, H_ = P[which]
        xi_, yi_ = L_ / 2 - P["ply"], W_ / 2 - P["ply"]
        zf_, zt_ = P["skid"][1] + P["ply"], P["skid"][1] + H_
        for a, sh_ in pk.items():
            bb = sh_.bounding_box()
            if (bb.min.X < -xi_ - 0.5 or bb.max.X > xi_ + 0.5 or bb.min.Y < -yi_ - 0.5 or bb.max.Y > yi_ + 0.5
                    or bb.min.Z < zf_ - 0.5 or bb.max.Z > zt_ + 0.5):
                res["overlaps"].append((nm + ": " + a, "outside the crate", 0))
    if verbose:
        print("packing overlaps (should be none):", res["overlaps"] or "none")
    return res


def export_stl(P=PARAMS):
    """STL of option A by group (0.2 mm chord tolerance): capstan, probe, board pair, crates, stretcher, clamp."""
    root = HERE.parents[1]
    (root / "cad" / "stl").mkdir(parents=True, exist_ok=True)
    parts = [p for p in components("A") if p["kind"] != "context"]
    groups = {
        "capstan": lambda p: p["group"] == "shell",
        "probe": lambda p: p["name"].startswith("Probe 1 "),
        "board": lambda p: p["name"].startswith(("Board 1 ", "Board 2 ", "Board link")),
        "box": lambda p: p["key"].startswith("box_") or p["name"].startswith("Rope handle"),
        "capbox": lambda p: p["key"].startswith("capbox_"),
        "stretcher": lambda p: p["key"] in ("sheet", "straps"),
        "clamp": lambda p: p["key"] in ("clamp_bars", "clamp_bolts"),
    }
    for g, f in groups.items():
        sel = [s for p in parts if f(p) for s in p["shape"].solids()]
        _export_stl(Compound(sel), str(root / "cad" / "stl" / f"heapline-{g}.stl"), tolerance=0.2, angular_tolerance=0.3)
    print("exported STL to cad/stl")


if __name__ == "__main__":
    for o in OPTIONS:
        ps = [p for p in components(o) if p["kind"] != "context"]
        print(f"option {o}: {len(ps)} parts, {sum(cp.mass_kg(p) for p in ps):.1f} kg")
    checks()
    for k, v in sorted(masses().items()):
        print(f"{k:16s} {v:6.2f} kg")
    if "--check" not in sys.argv:
        export_stl()
