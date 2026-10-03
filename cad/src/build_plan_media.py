"""HeapLine prototype build plan pictures (HPL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png       every component pulled apart, numbered in build order
    cad/drawings/HPL-DWG-101 to 116       making sketches for the made components
    docs/05-build-plan/joint-NN.png       close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png        one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Compound, Pos, Rot, Torus  # noqa: E402
from model import (PARAMS as P, derived, capstan_parts, probe_parts, board, link_plate, box_parts,  # noqa: E402
                   stretcher, sheet_clamp, shovel, packed_contents, build_components, context_shapes,
                   bx, zcyl, ycyl, xcyl, fuse, CAPSTAN_KEYS)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
CAP = capstan_parts(P)
PR = probe_parts(P)
BX = box_parts(P)
ST = stretcher(P)
CL = sheet_clamp(P)
L_B = P["board"][0]

COL = {"frame": "#1D4ED8", "drum": "#C2410C", "drive_ratchet": "#A16207", "shear_pin": "#DC2626",
       "head": "#111827", "hold_pawls": "#7C3AED", "drive_pawl": "#7C3AED", "bars": "#4B5563",
       "bar_pins": "#0F172A", "bushes": "#A8A29E", "roller": "#15803D", "roller_pin": "#374151",
       "keeper": "#0E7490", "stakes": "#57534E", "board": "#B45309", "link": "#374151",
       "probe_tip_section": "#DC2626", "probe_mid_section": "#EF4444", "probe_top_section": "#B91C1C",
       "probe_pins": "#111827", "box_body": "#0F766E", "box_lid": "#115E59", "box_hardware": "#374151",
       "sheet": "#EAB308", "straps": "#1E3A8A", "clamp_bars": "#2563EB", "clamp_bolts": "#111827",
       "shovel": "#6B7280", "rope": "#E11D48", "sling": "#F97316", "shackle": "#9CA3AF", "bag": "#9CA3AF"}


def part(name, shape, key, explode=(0, 0, 0)):
    return Part(name, shape, COL[key], None, tuple(explode))


def crop(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def shackle(x, y, z, axis="y"):
    """Bow shackle with a 19 mm pin, pin along the given axis through (x, y, z)."""
    pin = ycyl(x, z, 9.5, y - 30, y + 30) if axis == "y" else xcyl(y, z, 9.5, x - 30, x + 30)
    bow = Pos(x + 45, y, z) * Rot(90, 0, 0) * Torus(38, 8) if axis == "y" else Pos(x, y + 45, z) * Rot(0, 90, 0) * Torus(38, 8)
    return fuse([pin, bow & bx(x - 5, x + 200, y - 60, y + 60, z - 60, z + 60) if axis == "y" else bow])


# ----------------------------------------------------------------- overview
def overview():
    probe = Compound([PR["probe_tip_section"], PR["probe_mid_section"], PR["probe_top_section"]])
    lay = lambda s: Rot(0, 90, 0) * s  # noqa: E731   probe laid along +X
    items = [
        ("Crawl board (make 4)", Pos(-2600, 1600, 0) * board(P), "board", (0, 0, 0)),
        ("Board link plate (make 8)", Pos(-2600, 2300, 0) * link_plate(P, 0.0), "link", (0, 0, 120)),
        ("Probe sections (make 6 sets)", Pos(-3800, 600, 150) * lay(probe), "probe_mid_section", (0, 0, 0)),
        ("Capstan base frame with post", CAP["frame"], "frame", (0, 0, 0)),
        ("Drum with holding ratchet", CAP["drum"], "drum", (0, 0, 900)),
        ("Drive ratchet wheel", CAP["drive_ratchet"], "drive_ratchet", (0, 0, 1600)),
        ("Lever head", CAP["head"], "head", (0, 0, 2300)),
        ("Pawls (3)", CAP["hold_pawls"] + CAP["drive_pawl"], "hold_pawls", (0, -450, 300)),
        ("Capstan bars (2)", CAP["bars"], "bars", (0, 0, 2900)),
        ("Bushes and thrust washers", CAP["bushes"], "bushes", (450, 0, 500)),
        ("Hold-down roller, pin and keeper", CAP["roller"] + CAP["roller_pin"] + CAP["keeper"], "roller", (-600, 0, 0)),
        ("Ground stakes (4)", CAP["stakes"] & bx(-2000, 2000, -2000, 2000, 0, 200), "stakes", (0, 0, 150)),
        ("Sheet clamp", Pos(1600, -1300, 0) * (CL["clamp_bars"] + CL["clamp_bolts"]), "clamp_bars", (0, 0, 0)),
        ("Sheet stretcher", Pos(-1200, -1700, 0) * (ST["sheet"] + ST["straps"]), "sheet", (0, 0, 0)),
        ("Site box body", Pos(-5600, 900, 0) * BX["box_body"], "box_body", (0, 0, 0)),
        ("Site box lid", Pos(-5600, 900, 0) * BX["box_lid"], "box_lid", (0, 0, 700)),
        ("Shear pins, bought", CAP["shear_pin"], "shear_pin", (0, 400, 1900)),
        ("Shovels (4), bought", Pos(1800, 2200, 0) * shovel(P), "shovel", (0, 0, 0)),
    ]
    parts = [part(n, s, k, e) for n, s, k, e in items]
    bv.overview(parts, OUT / "overview.png", "HeapLine prototype: every component in build order",
                subtitle="Made parts first (1 to 16), then bought parts; rope, slings and bags not shown",
                key=True, size=(11, 7.5))


# ----------------------------------------------------------------- making sketches
def sheets():
    cap_grey = [Part(k, v, "#D1D5DB") for k, v in CAP.items() if k != "stakes"]
    b1, b2 = Pos(-L_B / 2, 0, 0) * board(P), Pos(L_B / 2, 0, 0) * board(P)
    lk = link_plate(P, 0.0)
    probe_side = Compound([Pos(0, 0, 0) * PR["probe_tip_section"], Pos(80, 0, -1000) * PR["probe_mid_section"],
                           Pos(160, 0, -2000) * PR["probe_top_section"]])
    probe_all = [Part(k, v, "#D1D5DB") for k, v in PR.items()]
    clamp_nb = [Part("bolts", CL["clamp_bolts"], "#D1D5DB")]
    S = [
        ("HPL-DWG-101", "Crawl board: making sketch", b1, "board", [Part("next board", b2, "#D1D5DB"), Part("links", lk, "#D1D5DB")],
         "15 mm exterior plywood; 45 x 70 mm treated timber", None,
         ["Deck 1500 x 450 x 15 plywood; battens 45 x 70, 1500 long",
          "Battens 30 in from each long edge, flush with the ends",
          "Glue and screw: 5 x 60 stainless screws every 150 into each batten",
          "Hand slot 140 x 35, centred 75 from each end, between the battens",
          "Four 13 mm holes, 40 from each end on the batten centre lines, right through",
          "Round all edges 3 mm; anti-slip grit paint on the deck",
          "Make 4. Check: flat within 5 mm; a link plate drops in at both ends"]),
        ("HPL-DWG-102", "Board link plate: making sketch", lk, "link", [Part("boards", b1 + b2, "#D1D5DB")],
         "40 x 6 mm steel flat; 12 mm round bar", None,
         ["Plate 40 x 6 x 160; two pins 12 mm dia, 75 long",
          "Pins 80 apart, each 40 from the plate's middle, square to the plate",
          "Weld each pin under the plate all round; grind flush on top",
          "Round the plate corners; chamfer the pin ends 1 mm",
          "Galvanise or paint",
          "Make 8 (two per joint, four spare). Check: drops into two butted boards"]),
        ("HPL-DWG-103", "Probe sections: making sketch", Compound(list(PR.values())), "probe_mid_section", [],
         "16 x 2.0 steel tube; 11.5 and 22 mm bright bar; 26.9 x 2.6 tube", probe_side,
         ["Three sections of 16 x 2.0 tube, each 1000 long, ends square",
          "Spigot 11.5 dia x 120 into the top of the tip and middle sections, 60 in; plug weld",
          "Tip from 22 bar: cone 35 long to a 3 mm rounded point, 20 parallel, 30 x 12 spigot",
          "T handle 26.9 x 2.6 x 450 welded square across the top section",
          "5 mm cross hole 30 above each joint, through tube and spigot together",
          "Paint a band every 250 from the tip; R-clip on a lanyard at each joint",
          "Make 6 sets. Check: assembled 3068 long, straight within 10 mm"]),
        ("HPL-DWG-104", "Capstan base frame with post: making sketch", CAP["frame"], "frame", cap_grey,
         "40 x 40 x 3 SHS; 100 x 40 x 4 RHS; 60.3 x 5.0 tube; 8, 10 mm plate", None,
         ["Frame 700 x 440 outside: two rails, two cross members, 40 x 40 x 3",
          "Centre member 100 x 40 x 4 across the middle; 61 mm hole top and bottom",
          "Post 60.3 x 5.0 x 995 through the centre member, square, welded top and bottom",
          "Roller cheeks 8 mm on the front, 20.5 hole at 75 up, 65 ahead of the frame",
          "Anchor eye 10 mm on the rear, 22 hole at 38 up; tail cleat on the rear member",
          "Two 12 mm pawl pins on the centre member; four stake tubes at the corners",
          "10.5 mm cross hole through the post at 982 up",
          "Check: post square to the frame within 1 mm over 900"]),
        ("HPL-DWG-105", "Capstan drum: making sketch", CAP["drum"], "drum", cap_grey,
         "114.3 x 3.6 and 76.1 x 3.2 tube; 6 and 8 mm plate", None,
         ["Barrel 114.3 x 3.6 x 260 between two 6 mm discs, 230 OD",
          "Foot disc bore 75; holding ring 24 teeth, 210 OD, 6 mm, welded under it",
          "Spindle 76.1 x 3.2 x 528 on the top disc; flange 140 OD x 8 on its top",
          "6.2 mm shear pin hole in the flange on a 60 radius",
          "Weld in short stitches, turning the drum, to keep it straight",
          "Grind the barrel smooth where the rope runs; paint",
          "Check: spins true on a 60 mm bar within 1.5 mm at the discs"]),
        ("HPL-DWG-106", "Drive ratchet wheel: making sketch", CAP["drive_ratchet"], "drive_ratchet", cap_grey,
         "8 mm steel plate, laser or plasma cut", None,
         ["20 teeth, 160 OD, 136 root; radial faces, sloping backs",
          "Bore 61.3 to slide over the post",
          "6.2 mm shear pin hole on a 60 radius",
          "Deburr the teeth; no hardening",
          "Check: the pin hole lines up with the drum flange's"]),
        ("HPL-DWG-107", "Lever head: making sketch", CAP["head"], "head", cap_grey,
         "88.9 x 5.0 tube; 50 x 50 x 3 SHS; 8 mm plate; 12 mm bar", None,
         ["Sleeve 88.9 x 5.0 x 80",
          "Two sockets 50 x 50 x 3 x 150, opposite, welded to the sleeve",
          "13 mm pin hole down through each socket, 154 from the axis",
          "Pawl bracket 8 mm under the sleeve's foot; 12 mm pawl pin hanging down",
          "Check: the sleeve slides on a 60.3 tube with its bush; sockets in line"]),
        ("HPL-DWG-108", "Pawls: making sketch", CAP["hold_pawls"] + CAP["drive_pawl"], "hold_pawls", cap_grey,
         "10 and 8 mm steel plate, profile cut", None,
         ["Two holding pawls from 10 mm plate, one drive pawl from 8 mm",
          "12.5 mm pivot hole; nose 2 mm radius; body 24 wide at the pivot",
          "Light torsion spring on each pivot pin keeps the nose on the teeth",
          "Washer and R-clip on each pin",
          "Check: each nose drops into every tooth gap"]),
        ("HPL-DWG-109", "Capstan bars and pins: making sketch", CAP["bars"] + CAP["bar_pins"], "bars", cap_grey,
         "40 x 40 x 2.5 SHS; 12 mm bright bar", None,
         ["Two bars 40 x 40 x 2.5 x 900; plastic end caps",
          "13 mm cross hole 110 from the inner end",
          "Pins 12 mm, 66 long, with an R-clip hole",
          "Bar slides 140 into its socket and is pinned",
          "Check: slides in by hand; pin drops through"]),
        ("HPL-DWG-110", "Bushes and thrust washers: making sketch", CAP["bushes"], "bushes", cap_grey,
         "Acetal (POM) tube and plate", None,
         ["Foot thrust washer 100 OD x 60.5 ID x 4",
          "Foot bush 75 OD x 60.5 ID x 12, pressed into the ring and disc",
          "Spindle bush 69.7 OD x 60.5 ID x 58, pressed into the spindle top",
          "Head bush 78.9 OD x 60.5 ID x 80, pressed into the sleeve",
          "Two washers 88 OD x 60.5 ID x 2 above and below the head",
          "Check: drum and head turn freely on a 60.3 tube"]),
        ("HPL-DWG-111", "Hold-down roller, pin and keeper: making sketch",
         CAP["roller"] + CAP["roller_pin"] + CAP["keeper"], "roller", cap_grey,
         "60.3 x 3.6 tube; 20 mm bar; 80 mm bar for the collar", None,
         ["Roller 60.3 x 3.6 x 200 with two acetal end bushes",
          "Pin 20 dia x 240 with R-clip holes",
          "Keeper collar 80 OD x 61 bore x 20; pin 10 x 96 with an R-clip",
          "Check: roller turns freely between the cheeks"]),
        ("HPL-DWG-112", "Ground stake: making sketch", CAP["stakes"] & bx(-1000, -200, -1000, 0, -600, 200), "stakes",
         [Part("frame", CAP["frame"], "#D1D5DB")],
         "25 mm round bar; 44 mm washer", None,
         ["Four stakes, 25 bar 500 long, ground to a point",
          "44 mm washer welded on top as a head",
          "Driven through the stake tubes; head rests on the tube",
          "They stop the frame turning and skating; the sling is the anchor",
          "Check: straight within 3 mm"]),
        ("HPL-DWG-113", "Sheet clamp: making sketch", CL["clamp_bars"], "clamp_bars", clamp_nb,
         "50 x 8 mm steel flat; 10 mm plate; M12 bolts", None,
         ["Two flats 50 x 8 x 600; four 13 mm holes at 100 and 250 each side of the middle",
          "Lug 10 mm plate on the upper flat's middle, 22 mm hole 45 above it",
          "M12 x 60 bolts up from below with wing nuts on top",
          "Check: closes flat on a 3 mm sheet; lug square to the bars"]),
        ("HPL-DWG-114", "Sheet stretcher: making sketch", ST["sheet"] + ST["straps"], "sheet", [],
         "2 mm UV-stabilised HDPE; 50 mm polyester webbing", None,
         ["Sheet 2000 x 900 x 2; round the corners 50 radius",
          "Twelve hand slots 130 x 35, six each side, 60 in from the edge",
          "Three straps with cam buckles at 550 spacing; head haul strap",
          "Rivet straps with large washers both sides",
          "Check: rolls to 250 dia; a 100 kg dummy rides on it"]),
        ("HPL-DWG-115", "Site box body: making sketch", BX["box_body"], "box_body", [Part("lid", BX["box_lid"], "#D1D5DB")],
         "18 mm exterior plywood; 45 x 45 and 70 x 45 mm treated timber", None,
         ["Outside 1700 x 1020; sides 1060 high above the skids",
          "Base on two skids 70 x 45, 120 in from the long edges",
          "Corner battens 45 x 45 inside each corner; glue and screw",
          "Hardwood handle cleats on each end; rope handles through them",
          "Seal strip on the rim; prime and paint every face",
          "Check: diagonals within 3 mm; lid sits evenly on the seal"]),
        ("HPL-DWG-116", "Site box lid: making sketch", BX["box_lid"], "box_lid", [Part("body", BX["box_body"], "#D1D5DB")],
         "18 mm exterior plywood", None,
         ["Top 1740 x 1060 x 18; skirt 48 deep all round",
          "Skirt 2 mm clear of the body on every side",
          "Three strap hinges on the back, hasp on the front, folding stay",
          "Drill card inside, stop rule outside",
          "Check: closes over the seal; padlock fits the hasp"]),
    ]
    for dwg, title, shape, key, nb, mat, vshape, notes in S:
        nbs = nb if nb else []
        kw = {"view_shape": vshape} if vshape is not None else {}
        nb_use = [n for n in (nbs if nbs else probe_all if key.startswith("probe") else []) if n.name != key][:12]
        bv.component_sheet(Part(title, shape, COL[key]), nb_use, "HeapLine", dwg, title, mat, notes, DATE,
                           out_dir=str(DWG), **kw)
        print("sheet", dwg)


# ----------------------------------------------------------------- joints
def joints(only=None):
    yb = P["board"][1] / 2 - P["batten"][2] - P["batten"][0] / 2
    b1, b2 = Pos(-L_B / 2, 0, 0) * board(P), Pos(L_B / 2, 0, 0) * board(P)
    r1 = (-150, 150, yb - 60, yb + 60, -10, 120)
    bv.joint([part("Board 1 deck and batten", crop(b1, *r1), "board"),
              part("Board 2 deck and batten", crop(b2, *r1), "board"),
              part("Link plate and pins", crop(link_plate(P, 0.0), *r1), "link")],
             OUT / "joint-01.png", "Joint 1: link plate across two boards", "Cut through the pins: each 12 mm pin sits in a 13 mm hole, 75 deep", cut="-Y")
    zj = P["probe_tip"][1] + P["probe_tip"][2] + P["probe_tube"][2]
    r2 = (-30, 30, -30, 30, zj - 90, zj + 90)
    bv.joint([part("Lower section with spigot", crop(PR["probe_tip_section"], *r2), "probe_tip_section"),
              part("Upper section", crop(PR["probe_mid_section"], *r2), "probe_mid_section"),
              part("R-clip pin, 5 mm", crop(PR["probe_pins"], *r2), "probe_pins")],
             OUT / "joint-02.png", "Joint 2: probe sections on their spigot", "Cut open: tube ends bear on each other; the pin only stops them pulling apart", cut="-X", elev=12)
    r3 = (-30, 30, -30, 30, -5, 130)
    bv.joint([part("Tip, 22 mm", crop(PR["probe_tip_section"], -30, 30, -30, 30, -5, 56), "probe_tip_section"),
              part("Bottom of the tip section tube", crop(PR["probe_tip_section"], -30, 30, -30, 30, 56, 130), "probe_mid_section")],
             OUT / "joint-03.png", "Joint 3: tip in the bottom section", "Cut open: 12 mm spigot 30 deep, plug welded; tip 3 mm wider than the tube each side", cut="-X", elev=12)
    r4 = (-80, 80, -120, 120, -5, 120)
    bv.joint([part("Centre member 100 x 40 x 4", crop(CAP["frame"], -50, 50, -120, 120, -5, 41), "frame"),
              part("Post 60.3 x 5.0", crop(CAP["frame"], -31, 31, -31, 31, 41, 120) + crop(CAP["frame"], -31, 31, -31, 31, -1, 40), "drum")],
             OUT / "joint-04.png", "Joint 4: post through the centre member", "Cut open: welded all round at the top and bottom faces", cut="-Y", elev=18)
    zr0 = D["z_ring"][0]
    r5 = (-140, 140, -10, 200, 35, 70)
    bv.joint([part("Centre member and pawl pin", crop(CAP["frame"], -140, 140, -10, 200, 35, 70), "frame"),
              part("Holding ring under the drum", crop(CAP["drum"], *r5), "drum"),
              part("Holding pawl", crop(CAP["hold_pawls"], *r5), "hold_pawls"),
              part("Foot thrust washer and bush", crop(CAP["bushes"], *r5), "bushes")],
             OUT / "joint-05.png", "Joint 5: holding pawl on the ring", "Seen from above: the pawl's nose sits behind a radial tooth face", elev=70, azim=-90)
    zf = D["z_flange"][0]
    r6 = (-130, 150, -130, 130, zf - 30, D["z_drive"][1] + 12)
    bv.joint([part("Drum spindle and top flange", crop(CAP["drum"], *r6), "drum"),
              part("Drive ratchet", crop(CAP["drive_ratchet"], *r6), "drive_ratchet"),
              part("Shear pin, 6 mm", crop(CAP["shear_pin"], *r6), "shear_pin"),
              part("Foot of the lever head and pawl bracket", crop(CAP["head"], *r6), "head"),
              part("Drive pawl", crop(CAP["drive_pawl"], *r6), "drive_pawl"),
              part("Bushes", crop(CAP["bushes"], *r6), "bushes")],
             OUT / "joint-06.png", "Joint 6: shear pin and drive ratchet", "Lever head cut off just above its foot: only the 6 mm pin joins the drive ratchet to the drum", elev=38, azim=-150)
    sr = P["sleeve"][0] / 2
    r7 = (-60, 60, sr - 10, sr + 260, D["z_bar"] - 60, D["z_bar"] + 60)
    bv.joint([part("Socket on the lever head", crop(CAP["head"], *r7), "head"),
              part("Bar 40 x 40 x 2.5", crop(CAP["bars"], *r7), "bars"),
              part("Bar pin, 12 mm", crop(CAP["bar_pins"], *r7), "bar_pins")],
             OUT / "joint-07.png", "Joint 7: bar in its socket", "Bar slides in 140 mm; a 12 mm pin drops through both", cut="+X")
    rx, rz = P["roller"][0], P["roller"][1]
    r8 = (rx - 80, -330, -130, 130, -5, 140)
    from model import rod
    rope = rod((rx - 200, -40, D["z_rope_out"]), (rx, -40, D["z_rope_out"]), 7.0) + rod((rx, -40, D["z_rope_out"]), (-60, -40, 130.0), 7.0)
    bv.joint([part("Roller cheeks on the frame", crop(CAP["frame"], *r8), "frame"),
              part("Hold-down roller", crop(CAP["roller"], *r8), "roller"),
              part("Roller pin, 20 mm", crop(CAP["roller_pin"], *r8), "roller_pin"),
              part("Rope passes under the roller", crop(rope, rx - 200, -330, -130, 130, -5, 140), "rope")],
             OUT / "joint-08.png", "Joint 8: rope under the hold-down roller", "The rope leaves 38 mm above the ground, level with the anchor eye", azim=-30)
    xe = P["frame_l"] / 2 + 50
    ze = D["z_rope_out"]
    r9 = (P["frame_l"] / 2 - 60, xe + 200, -90, 90, -5, 110)
    sl = rod((xe + 70, 0, ze), (xe + 400, 0, ze), 12.0)
    bv.joint([part("Anchor eye on the rear member", crop(CAP["frame"], *r9), "frame"),
              part("Bow shackle, 19 mm pin", shackle(xe, 0, ze, "y"), "shackle"),
              part("Round sling to the anchor", crop(sl, *r9), "sling")],
             OUT / "joint-09.png", "Joint 9: anchor sling on the rear eye", "The sling pulls level with the rope, so the capstan cannot tip", azim=-40)
    t = P["clamp"][1] + P["clamp_gap"] + P["clamp"][1]
    sheet = bx(-500, 500, -300, 300, P["clamp"][1] + 0.3, P["clamp"][1] + P["clamp_gap"] - 0.3)
    r10 = (-330, 330, -120, 120, -30, 120)
    bv.joint([part("Clamp bars and lug", crop(CL["clamp_bars"], *r10), "clamp_bars"),
              part("M12 bolts and wing nuts", crop(CL["clamp_bolts"], *r10), "clamp_bolts"),
              part("Plastic sheeting gripped", crop(sheet, *r10) - CL["clamp_bolts"], "sheet")],
             OUT / "joint-10.png", "Joint 10: sheet clamp on plastic sheeting", "Sheet between the flats; wing nuts hand tight; shackle on the lug")
    Lx, W, H = P["box"]
    rb = (-200, 200, W / 2 - 80, W / 2 + 60, 45 + H - 140, 45 + H + 40)
    bv.joint([part("Box back panel and corner batten", crop(BX["box_body"], *rb), "box_body"),
              part("Lid top and skirt", crop(BX["box_lid"], *rb), "box_lid"),
              part("Seal strip and strap hinge", crop(BX["box_hardware"], *rb), "box_hardware")],
             OUT / "joint-11.png", "Joint 11: lid over the box rim", "Cut open: the skirt laps 48 mm over the body, 2 mm clear; seal on the rim", cut="+X", elev=10, azim=-70)


# ----------------------------------------------------------------- steps
def steps(site_only=False):
    n = 11 if site_only else 0
    g = lambda n, k, e=(0, 0, 0): Part(n, CAP[k], COL[k], None, e)  # noqa: E731
    fr = g("Frame", "frame")
    bu = Part("Bushes and washers", CAP["bushes"], COL["bushes"])
    dr = g("Drum", "drum")
    hp = g("Holding pawls", "hold_pawls")
    dra = g("Drive ratchet", "drive_ratchet")
    sp = g("Shear pin", "shear_pin")
    hd = g("Lever head", "head")
    dp = g("Drive pawl", "drive_pawl")
    kp = g("Keeper collar and pin", "keeper")
    ro = Part("Roller and pin", CAP["roller"] + CAP["roller_pin"], COL["roller"])
    ba = g("Bars", "bars")
    bp = g("Bar pins", "bar_pins")

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, e)
    S = [
        ([fr], [mv(bu, (0, 0, 600))], "Step 1: bushes and washers onto the post",
         "Foot washer down first; the other bushes are pressed into the drum and head"),
        ([fr, bu], [mv(dr, (0, 0, 1000))], "Step 2: lower the drum over the post",
         "Two people; grease the post; the ring's teeth face as drawn"),
        ([fr, bu, dr], [mv(hp, (0, 0, 250))], "Step 3: holding pawls onto their pins",
         "Spring, pawl, washer, R-clip; noses on the ring"),
        ([fr, bu, dr, hp], [mv(dra, (0, 0, 300)), mv(sp, (0, 0, 450))], "Step 4: drive ratchet and shear pin",
         "Line up the holes; 6 mm S275 pin and split pin"),
        ([fr, bu, dr, hp, dra, sp], [mv(hd, (0, 0, 350)), mv(dp, (0, 0, 350))], "Step 5: lever head onto the post",
         "Drive pawl hung on its pin first; nose on the teeth"),
        ([fr, bu, dr, hp, dra, sp, hd, dp], [mv(kp, (0, 0, 250))], "Step 6: keeper collar and pin",
         "Collar over the post top; 10 mm pin and R-clip"),
        ([fr, bu, dr, hp, dra, sp, hd, dp, kp], [mv(ro, (-300, 0, 0))], "Step 7: hold-down roller between the cheeks",
         "Pin through cheek, roller, cheek; R-clips"),
        ([fr, bu, dr, hp, dra, sp, hd, dp, kp, ro], [mv(ba, (0, 0, 250)), mv(bp, (0, 0, 400))], "Step 8: bars into the sockets",
         "Slide in 140 mm; pin and R-clip each"),
    ]
    for done, new, title, sub in ([] if site_only else S):
        n += 1
        bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, label_done=False, size=(8, 6))
    # probes and boards
    if not site_only:
        n = _workshop_steps(n)
    _site_steps(n)


def _workshop_steps(n):
    n += 1
    t, m, tp, pins = (PR[k] for k in ("probe_tip_section", "probe_mid_section", "probe_top_section", "probe_pins"))
    lay = lambda s: Rot(0, 90, 0) * s  # noqa: E731
    bv.step([Part("Tip section", lay(t), COL["probe_tip_section"])],
            [Part("Middle section", lay(m), COL["probe_mid_section"], None, (300, 0, 0)),
             Part("Top section with handle", lay(tp), COL["probe_top_section"], None, (600, 0, 0)),
             Part("R-clip pins", lay(pins), COL["probe_pins"], None, (0, 0, 120))],
            OUT / f"step-{n:02d}.png", "Step 9: join the probe sections", "Spigot into tube, R-clip through the cross hole; ends tight together",
            label_done=True, size=(9, 4.5), elev=28, azim=-75)
    n += 1
    b1, b2 = Pos(-L_B / 2, 0, 0) * board(P), Pos(L_B / 2, 0, 0) * board(P)
    bv.step([Part("Board 1", b1, COL["board"]), Part("Board 2", b2, COL["board"])],
            [Part("Link plates (2)", link_plate(P, 0.0), COL["link"], None, (0, 0, 250))],
            OUT / f"step-{n:02d}.png", "Step 10: link two boards end to end", "Butt the ends; drop a link plate into each pair of holes",
            label_done=True, size=(9, 5))
    n += 1
    pk = packed_contents(P)
    body = Part("Site box body", BX["box_body"], COL["box_body"])
    order = list(pk)
    new = []
    for k_, nm in enumerate(order):
        new.append(Part(nm, pk[nm], "#0F766E" if "Capstan" in nm else ("#B45309" if "boards" in nm else "#9CA3AF"), None,
                        (0, 0, 900)))
    bv.step([body], new, OUT / f"step-{n:02d}.png", "Step 11: pack the site box",
            "Boards at the back, capstan front right, bags front left, long items on the boards", label_done=False, size=(9, 6.5), pull=0.6)
    return n


def _site_steps(n):
    # site steps (deployed, shortened)
    C = build_components(P, "site")
    X = context_shapes(P, "site")
    deb = [Part("Slide debris (site)", X["debris"], "#E7E5E4")]
    sp_ = lambda k, nm=None, e=(0, 0, 0): Part(nm or C[k].name, C[k].shape, COL.get(k, "#0F766E") if k not in ("boards", "links", "probes") else  # noqa: E731
                                              {"boards": COL["board"], "links": COL["link"], "probes": COL["probe_mid_section"]}[k], None, e)
    above = lambda s: s & bx(-20000, 20000, -20000, 20000, 0, 3000)  # noqa: E731
    cap_done = [sp_(k) if k != "stakes" else Part(C[k].name, above(C[k].shape), COL[k]) for k in CAPSTAN_KEYS]
    probes_above = Part("Probes (6) in a line", above(C["probes"].shape), COL["probe_mid_section"], None, (0, 0, 900))
    wands = Part("Lookout's marker wands and safe-zone sign", C["wands"].shape, "#F97316", None, (0, 0, 600))
    site = [
        ([], [sp_("boards", "Crawl boards, linked", (0, -1500, 0)), sp_("links", "Link plates", (0, -1500, 300)), wands],
         "Step 12: lookout posted, boards laid", "Lookout on stable ground above; boards laid out from firm ground, linked"),
        ([sp_("boards"), sp_("links")], [probes_above],
         "Step 13: probe line from the boards", "Probes 0.5 m apart, pushed straight down; mark every strike with a wand"),
        ([sp_("boards"), sp_("links"), Part("Probes", above(C["probes"].shape), "#D1D5DB")],
         [Part(c.name, c.shape, c.color, None, (0, 0, 500)) for c in cap_done] + [sp_("sling", e=(-600, 0, 0))],
         "Step 14: set the capstan on firm ground", "Stakes in; sling from the rear eye to a sound anchor, level"),
        ([sp_("boards"), sp_("links"), Part("Probes", above(C["probes"].shape), "#D1D5DB")] + cap_done + [sp_("sling")],
         [sp_("clamp_bars", e=(0, 0, 400)), sp_("clamp_bolts", e=(0, 0, 400)), sp_("rope", e=(0, 0, 200)),
          sp_("sheet", e=(0, 0, 300)), sp_("straps", e=(0, 0, 300))],
         "Step 15: rig the clamp; stretcher alongside", "Clamp on the sheeting, rope to the capstan; stretcher on the boards' side"),
    ]
    for done, new, title, sub in site:
        n += 1
        bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, context=deb, label_done=False, size=(9, 6))
    print("steps", n)


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    OUT.mkdir(parents=True, exist_ok=True)
    for w in what:
        globals()[w]()
