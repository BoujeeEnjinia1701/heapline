"""HeapLine parametric model (build123d), TRL 3, constructable design (HPL-DDR-002).

Run from the repo root:  python cad/src/model.py          (checks, masses and exports)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    heapline-capstan.step / .stl    hand capstan: base frame with post, drum, drive ratchet, lever
                                    head, pawls, bars, bushes, hold-down roller, keeper, stakes
    heapline-probe.step / .stl      one sectional probe (tip section, middle section, top section, pins)
    heapline-board.step / .stl      two crawl boards joined by their link plates
    heapline-box.step / .stl        search crate body and lid (closed), the crate every site keeps
    heapline-capbox.step / .stl     capstan crate body and lid (closed), kept at the host site only
    heapline-stretcher.step / .stl  sheet stretcher laid flat with its straps
    heapline-clamp.step / .stl      sheet clamp with its shackle lug
    heapline-assembly.step          the kit laid out beside the open box (display layout)

Axes: Z is up with the ground at z = 0. The capstan stands on its own frame with the drum axis on
z at x = 0, y = 0; the rope leaves under the hold-down roller toward -X (the load) and the anchor
sling leaves the rear eye toward +X. Probes stand on z with the tip at z = 0. Crawl boards lie
along X with the walking face up.

Constructable design, 2026-10-03 (HPL-DDR-002, decided under Amish's pre-approvals of 2026-10-03):
    the hand capstan is a vertical friction capstan worked by pumping two bars through a quarter turn
    (no walking round): a smooth drum on a fixed post, turned through a drive ratchet and pawl in the
    lever head, held by two pawls on a ratchet ring at its foot, with a 6 mm shear pin between the
    drive ratchet and the drum that limits rope tension to about 6.3 kN; the rope leaves under a
    hold-down roller near the ground and the anchor sling pulls from an eye at the same height;
    probes are three 1 m sections of 16 x 2 mm steel tube on spigots and R-clips with a blunt tip;
    crawl boards are 15 mm plywood decks on two 45 x 70 mm battens, joined end to end by pinned link
    plates.
Amish's requirement decisions of 2026-10-03 (HPL-DDR-003): the probe tip is 18 mm on all six probes
(20A); one capstan set is shared by neighbouring sites and kept at the host site in its own capstan
crate, and each site keeps its search kit in a reused crate or bought job box (23C). The crates are
modelled as boarded crates of the minimum inside size, on skids with an overlapping lid.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (HPL-CAL-001), the drawings (cad/src/sheets.py), the concept media
(cad/src/concept_media.py), the product model and the build plan pictures.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Vector, extrude,
                       export_step, export_stl, Torus)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # ---- capstan base frame (BOM 9): SHS size and wall, frame outer length (X) and width (Y)
    "shs": (40.0, 3.0), "frame_l": 700.0, "frame_w": 440.0,
    "rhs": (100.0, 40.0, 4.0),          # centre cross member, width along X, height, wall
    "post": (60.3, 5.0, 995.0),         # fixed post OD, wall, height above ground
    "stake_tube": (33.7, 3.2, 60.0),
    "stake": (25.0, 500.0, 360.0),      # stake dia, length, depth below ground
    # hold-down roller (BOM 16): axis x, axis z, tube OD x wall, length; cheek plate; pin
    "roller": (-415.0, 75.0, 60.3, 3.6, 200.0), "cheek_t": 8.0, "roller_pin": 20.0,
    "eye": (10.0, 22.0),                # rear anchor eye plate thickness, hole
    # ---- drum (BOM 10): stack heights (z) from the frame top up
    "z_frame": 40.0, "washer_t": 4.0, "ring_t": 6.0, "disc_t": 6.0, "disc_d": 230.0,
    "barrel": (114.3, 3.6, 260.0),      # OD, wall, length between the discs
    "spindle": (76.1, 3.2), "z_flange": 850.0, "flange": (140.0, 8.0),
    "hold_ratchet": (210.0, 186.0, 24),  # OD, root dia, teeth
    "drive_ratchet": (160.0, 136.0, 20, 8.0),
    "shear_pin": (6.0, 60.0),           # dia, radius from the axis (BOM 18)
    # ---- lever head (BOM 12), bars (BOM 14), keeper (BOM 17)
    "sleeve": (88.9, 5.0, 80.0), "socket": (50.0, 3.0, 150.0), "bar": (40.0, 2.5, 900.0),
    "bar_insert": 140.0, "keeper": (80.0, 20.0), "keeper_pin": 10.0,
    "pawl_t": (10.0, 8.0),              # holding pawls, drive pawl plate thickness
    # ---- rope (BOM 20)
    "rope_d": 14.0, "rope_mbs": 40000.0, "rope_len": 30.0,
    # ---- probe (BOM 6): tube OD, wall, section length, number of sections; tip; spigot; handle
    "probe_tube": (16.0, 2.0, 1000.0, 3), "probe_tip": (18.0, 35.0, 20.0, 30.0),  # dia, cone, parallel, spigot (18 mm, HPL-DDR-003)
    "probe_spigot": (11.5, 120.0), "probe_pin": 5.0, "probe_handle": (26.9, 2.6, 450.0),
    # ---- crawl board (BOM 4): deck length, width, ply thickness; battens; link holes; slot
    "board": (1500.0, 450.0, 15.0), "batten": (45.0, 70.0, 30.0),   # width, depth, inset from edge
    "link": (40.0, 6.0, 160.0, 12.0, 75.0, 40.0),   # plate width, thickness, length, pin dia, pin length, hole from end
    "hand_slot": (140.0, 35.0, 75.0),
    # ---- search crate (BOM 1, 2) at every site, and capstan crate (BOM 31) at the host site only:
    #      outer length, width, body height (minimum sizes for a reused crate); boards; skids; lid skirt
    "box": (1640.0, 860.0, 640.0), "cap_box": (940.0, 900.0, 1060.0),
    "ply": 18.0, "skid": (70.0, 45.0), "skirt": 48.0, "lid_gap": 2.0,
    "lid_open_deg": 100.0,
    # ---- stretcher (BOM 23): sheet length, width, thickness; slots; straps
    "sheet": (2000.0, 900.0, 2.0), "sheet_slot": (130.0, 35.0, 60.0), "strap_w": 50.0,
    # ---- sheet clamp (BOM 22): bar width, thickness, length; bolt positions; lug
    "clamp": (50.0, 8.0, 600.0), "clamp_bolts": (100.0, 250.0), "clamp_gap": 3.0,
    # ---- shovel (BOM 8, bought): blade width, length; overall length
    "shovel": (230.0, 290.0, 1450.0),
    # materials (kg per m^3)
    "rho_steel": 7850.0, "rho_ply": 550.0, "rho_timber": 450.0, "rho_hdpe": 950.0, "rho_acetal": 1410.0,
}


# ----------------------------------------------------------------------------- helpers
def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def ycyl(x, z, r, y0, y1):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def xcyl(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def zcyl(x, y, r, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def ztube(x, y, ro, ri, z0, z1):
    return zcyl(x, y, ro, z0, z1) - zcyl(x, y, ri, z0 - 1, z1 + 1)


def _ccw(points):
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]))
    return list(points) if a > 0 else list(points)[::-1]


def prism_xz(points, y0, y1):
    """Polygon given as (x, z) points, extruded from y0 to y1."""
    f = Plane.XZ.offset(-y0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=-(y1 - y0))


def prism_xy(points, z0, z1):
    f = Plane.XY.offset(z0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=z1 - z0)


def rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def hull2d(pts):
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def circle_pts(cx, cy, r, n=40):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out.fuse(s)
    return out.clean() if hasattr(out, "clean") else out


def rot_z(shape, deg, x=0.0, y=0.0):
    return Pos(x, y, 0) * Rot(0, 0, deg) * Pos(-x, -y, 0) * shape


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
    D["r_rope"] = (P["barrel"][0] + P["rope_d"]) / 2          # rope centre radius on the drum
    D["z_bar"] = (D["z_socket"][0] + D["z_socket"][1]) / 2
    D["r_grip"] = P["sleeve"][0] / 2 + 10.0 + P["bar"][2] - P["bar_insert"] - 60.0   # hands 60 mm in from the end
    D["r_bar_end"] = P["sleeve"][0] / 2 + 10.0 + P["bar"][2] - P["bar_insert"]
    rx, rz, ro, _, _ = P["roller"]
    D["z_rope_out"] = rz - ro / 2 - P["rope_d"] / 2          # rope centre line after the roller
    # probe
    td, tw, tl, n = P["probe_tube"]
    dt, cone, par, spg = P["probe_tip"]
    D["probe_len"] = cone + par + n * tl + P["probe_handle"][0] / 2
    return D


# ----------------------------------------------------------------------------- ratchets and pawls
def ratchet_xy(z0, t, R, r, n, first_deg, bore, sense=1):
    """Ratchet wheel on z (axis at x = y = 0). sense = +1: radial faces resist +angle rotation of the
    wheel against a fixed pawl (the slope rises toward +angle); -1: mirror."""
    pts = []
    for k in range(n):
        a = math.radians(first_deg + 360.0 * k / n)
        b = math.radians(first_deg + 360.0 * (k + 1) / n)
        pts += [(r * math.cos(a), r * math.sin(a)), (R * math.cos(b - 0.002), R * math.sin(b - 0.002))]
    w = prism_xy(pts, z0, z0 + t)
    if sense < 0:
        w = Rot(180, 0, 0) * w           # flip over: teeth face the other way
        w = Pos(0, 0, 2 * z0 + t) * w
    return w - zcyl(0, 0, bore / 2, z0 - 1, z0 + t + 1)


def face_angle(first_deg, n, k):
    """Angle (deg) of radial face k for sense +1 (the face at the end of tooth k)."""
    return first_deg + 360.0 * (k + 1) / n


def pawl_xy(nose, pivot, z0, t, pin_d=12.0, nose_r=2.0, body_r=12.0):
    pts = hull2d(circle_pts(*pivot, body_r, 32) + circle_pts(*nose, nose_r, 12))
    return prism_xy(pts, z0, z0 + t) - zcyl(pivot[0], pivot[1], pin_d / 2 + 0.5, z0 - 1, z0 + t + 1)


# Pawl geometry: nose in the gap just past a radial face, pivot along the tangent behind it.
# The nose offset (fraction of a tooth pitch) and pivot angles were chosen so the pawl clears every
# tooth (checked with build123d intersections in checks()).
HOLD_FIRST = 7.5            # first tooth angle of the holding ring (deg)
DRIVE_FIRST = 0.0


def _pawl_points(R, r, n, face_deg, sense, lead=0.12, rn_frac=0.55, pivot_dist=55.0):
    p = 360.0 / n
    a = math.radians(face_deg + sense * lead * p)
    rn = r + rn_frac * (R - r)
    nose = (rn * math.cos(a), rn * math.sin(a))
    # pawl lies along the tangent on the side the face pushes toward, lifted 30 deg outward
    tx, ty = -math.sin(a) * sense, math.cos(a) * sense
    ux, uy = math.cos(a), math.sin(a)
    ang = math.radians(30.0)
    dx, dy = tx * math.cos(ang) + ux * math.sin(ang), ty * math.cos(ang) + uy * math.sin(ang)
    pivot = (nose[0] + dx * pivot_dist, nose[1] + dy * pivot_dist)
    return nose, pivot


# ----------------------------------------------------------------------------- capstan
def capstan_parts(P=PARAMS):
    """Capstan in its own coordinates: drum axis on z at x = y = 0, ground at z = 0, load toward -X."""
    D = derived(P)
    s, w = P["shs"]
    L, W = P["frame_l"], P["frame_w"]
    x0, x1 = -L / 2, L / 2
    yr = W / 2 - s / 2                          # rail centre lines
    out = {}

    def shs_x(xa, xb, y):
        return bx(xa, xb, y - s / 2, y + s / 2, 0, s) - bx(xa - 1, xb + 1, y - s / 2 + w, y + s / 2 - w, w, s - w)

    def shs_y(x, ya, yb_):
        return bx(x - s / 2, x + s / 2, ya, yb_, 0, s) - bx(x - s / 2 + w, x + s / 2 - w, ya - 1, yb_ + 1, w, s - w)

    po, pw_, ph = P["post"]
    rw, rh, rt = P["rhs"]
    frame = [shs_x(x0, x1, -yr), shs_x(x0, x1, yr),
             shs_y(x0 + s / 2, -yr + s / 2, yr - s / 2), shs_y(x1 - s / 2, -yr + s / 2, yr - s / 2)]
    rhs = (bx(-rw / 2, rw / 2, -yr + s / 2, yr - s / 2, 0, rh)
           - bx(-rw / 2 + rt, rw / 2 - rt, -yr + s / 2 - 1, yr - s / 2 + 1, rt, rh - rt))
    frame.append(rhs - zcyl(0, 0, po / 2 + 0.3, -1, rh + 1))
    frame.append(ztube(0, 0, po / 2, po / 2 - pw_, 0, ph) - xcyl(0, D["z_keeper_pin"], P["keeper_pin"] / 2 + 0.5, -40, 40))
    # stake tubes at the four corners, outside the rails
    so, st, sl = P["stake_tube"]
    for sx in (x0 + 40.0, x1 - 40.0):
        for sg in (-1, 1):
            ys = sg * (W / 2 + so / 2)
            frame.append(ztube(sx, ys, so / 2, so / 2 - st, 0, sl))
    # hold-down roller cheeks on the front cross member's outer face
    rx, rz, ro, rtw, rl = P["roller"]
    ct = P["cheek_t"]
    cheeks = []
    for sg in (-1, 1):
        y0 = rl / 2 + 1.0 if sg > 0 else -rl / 2 - 1.0 - ct
        ch = prism_xz(hull2d([(x0, 0), (x0, s + 20)] + circle_pts(rx, rz, 32, 24) + [(rx - 32, 0)]), y0, y0 + ct)
        cheeks.append(ch - ycyl(rx, rz, P["roller_pin"] / 2 + 0.5, y0 - 1, y0 + ct + 1))
    frame += cheeks
    # rear anchor eye: 10 mm plate on the rear cross member's outer face, hole at rope height
    et, eh = P["eye"]
    ze = D["z_rope_out"]
    eye = prism_xz(hull2d([(x1, 0), (x1, s)] + circle_pts(x1 + 50, ze, 26, 24) + [(x1 + 50, 0)]), -et / 2, et / 2)
    frame.append(eye - ycyl(x1 + 50, ze, eh / 2, -et, et))
    # tail cleat: two 12 mm posts and a 16 mm horn on the rear cross member, +Y side
    xc = x1 - s / 2
    for yc in (95.0, 155.0):
        frame.append(zcyl(xc, yc, 6.0, s, s + 34))
    frame.append(rod((xc, 60.0, s + 40), (xc, 190.0, s + 40), 8.0))
    # pawl pivot pins on the RHS top (two holding pawls)
    R, r, n = P["hold_ratchet"][0] / 2, P["hold_ratchet"][1] / 2, P["hold_ratchet"][2]
    pins = []
    for face_k in (4, 16):
        nose, pivot = _pawl_points(R, r, n, face_angle(HOLD_FIRST, n, face_k), +1)
        pins.append(zcyl(pivot[0], pivot[1], 6.0, rh, rh + P["pawl_t"][0] + 8.0))
    frame += pins
    out["frame"] = fuse(frame)

    # hold-down roller tube and pin
    out["roller"] = (ycyl(rx, rz, ro / 2, -rl / 2, rl / 2) - ycyl(rx, rz, ro / 2 - rtw, -rl / 2 - 1, rl / 2 + 1)
                     + ytube_(rx, rz, ro / 2 - rtw, P["roller_pin"] / 2 + 0.5, -rl / 2, -rl / 2 + 15)
                     + ytube_(rx, rz, ro / 2 - rtw, P["roller_pin"] / 2 + 0.5, rl / 2 - 15, rl / 2))
    out["roller_pin"] = ycyl(rx, rz, P["roller_pin"] / 2, -rl / 2 - ct - 12, rl / 2 + ct + 12)

    # bushes and thrust washers (acetal)
    zr0, zr1 = D["z_ring"]
    bushes = [ztube(0, 0, 50.0, po / 2 + 0.2, P["z_frame"], zr0),                 # foot thrust washer
              ztube(0, 0, 37.5, po / 2 + 0.2, zr0, D["z_disc0"][1]),              # foot bush in ring and disc
              ztube(0, 0, P["spindle"][0] / 2 - P["spindle"][1], po / 2 + 0.2, D["z_spindle"][1] - 50, D["z_flange"][1]),
              ztube(0, 0, 44.0, po / 2 + 0.2, D["z_drive"][1], D["z_sleeve"][0]),  # head thrust washer
              ztube(0, 0, P["sleeve"][0] / 2 - P["sleeve"][1], po / 2 + 0.2, *D["z_sleeve"]),
              ztube(0, 0, 44.0, po / 2 + 0.2, D["z_sleeve"][1], D["z_keeper"][0])]
    out["bushes"] = fuse(bushes)

    # drum weldment: holding ratchet ring, foot disc, barrel, top disc, spindle, top flange
    so_, sw_ = P["spindle"]
    drum = [ratchet_xy(zr0, P["ring_t"], R, r, n, HOLD_FIRST, 75.0, +1),
            ztube(0, 0, P["disc_d"] / 2, 37.5, *D["z_disc0"]),
            ztube(0, 0, P["barrel"][0] / 2, P["barrel"][0] / 2 - P["barrel"][1], *D["z_barrel"]),
            ztube(0, 0, P["disc_d"] / 2, so_ / 2 - sw_, *D["z_disc1"]),
            ztube(0, 0, so_ / 2, so_ / 2 - sw_, *D["z_spindle"]),
            ztube(0, 0, P["flange"][0] / 2, so_ / 2 - sw_, *D["z_flange"])]
    sp_d, sp_r = P["shear_pin"]
    out["drum"] = fuse(drum) - zcyl(-sp_r, 0, sp_d / 2 + 0.1, D["z_flange"][0] - 1, D["z_flange"][1] + 1)

    # drive ratchet wheel (pinned to the top flange by the shear pin)
    dR, dr, dn, dt = P["drive_ratchet"]
    dz0 = D["z_drive"][0]
    out["drive_ratchet"] = (ratchet_xy(dz0, dt, dR / 2, dr / 2, dn, DRIVE_FIRST, po + 1.0, +1)
                            - zcyl(-sp_r, 0, sp_d / 2 + 0.1, dz0 - 1, dz0 + dt + 1))
    out["shear_pin"] = zcyl(-sp_r, 0, sp_d / 2, D["z_flange"][0] - 6, dz0 + dt + 6)

    # lever head: sleeve, two radial bar sockets on +-Y, drive pawl bracket and pin on +X
    zs0, zs1 = D["z_sleeve"]
    sr = P["sleeve"][0] / 2
    so2, sw2, sl2 = P["socket"]
    za, zb = D["z_socket"]
    head = [ztube(0, 0, sr, sr - P["sleeve"][1], zs0, zs1)]
    for sg in (-1, 1):
        ya, yb_ = (sr - 6, sr - 6 + sl2) if sg > 0 else (-(sr - 6 + sl2), -(sr - 6))
        sock = bx(-so2 / 2, so2 / 2, ya, yb_, za, zb) - bx(-so2 / 2 + sw2, so2 / 2 - sw2, ya - 1, yb_ + 1, za + sw2, zb - sw2)
        sock = sock - zcyl(0, sg * (sr + 110.0), 6.5, za - 1, zb + 1)          # bar pin hole
        head.append(sock - zcyl(0, 0, sr - P["sleeve"][1] + 0.1, za - 1, zb + 1))
    nose_d, piv_d = _pawl_points(dR / 2, dr / 2, dn, face_angle(DRIVE_FIRST, dn, 0), +1, pivot_dist=45.0)
    bracket = prism_xy(hull2d(circle_pts(0, 0, sr - 1, 32) + circle_pts(piv_d[0], piv_d[1], 16, 24)), zs0, zs0 + 8)
    bracket = bracket - zcyl(0, 0, sr - P["sleeve"][1] + 0.1, zs0 - 1, zs0 + 9)
    head.append(bracket)
    head.append(zcyl(piv_d[0], piv_d[1], 6.0, dz0 - 8, zs0))
    out["head"] = fuse(head)
    # pawls: two holding pawls on the ring (sense +1), one drive pawl on the drive ratchet
    hp = []
    for face_k in (4, 16):
        nose, pivot = _pawl_points(R, r, n, face_angle(HOLD_FIRST, n, face_k), +1)
        hp.append(pawl_xy(nose, pivot, P["rhs"][1], P["pawl_t"][0]))
    out["hold_pawls"] = fuse(hp)
    out["drive_pawl"] = pawl_xy(nose_d, piv_d, dz0, P["pawl_t"][1])

    # bars: 40 x 40 x 2.5 SHS, inserted 140 mm into each socket, pinned
    b, bw, bl = P["bar"]
    bars = []
    for sg in (-1, 1):
        yi = sr - 6 + 10.0
        ya, yb_ = (yi, yi + bl) if sg > 0 else (-(yi + bl), -yi)
        bar = bx(-b / 2, b / 2, ya, yb_, D["z_bar"] - b / 2, D["z_bar"] + b / 2)
        bar = bar - bx(-b / 2 + bw, b / 2 - bw, ya - 1, yb_ + 1, D["z_bar"] - b / 2 + bw, D["z_bar"] + b / 2 - bw)
        bars.append(bar - zcyl(0, sg * (sr + 110.0), 6.5, D["z_bar"] - 30, D["z_bar"] + 30))
    out["bars"] = fuse(bars)
    out["bar_pins"] = fuse([zcyl(0, sg * (sr + 110.0), 6.0, za - 8, zb + 8) for sg in (-1, 1)])
    # keeper collar and its cross pin
    kd, kh = P["keeper"]
    out["keeper"] = fuse([ztube(0, 0, kd / 2, po / 2 + 0.3, *D["z_keeper"]),
                          xcyl(0, D["z_keeper_pin"], P["keeper_pin"] / 2, -48, 48)])
    # ground stakes through the stake tubes
    sd, slen, sdep = P["stake"]
    stakes = []
    for sx in (x0 + 40.0, x1 - 40.0):
        for sg in (-1, 1):
            ys = sg * (W / 2 + so / 2)
            stakes.append(zcyl(sx, ys, sd / 2, sl - slen, sl) + zcyl(sx, ys, 22.0, sl, sl + 10))
    out["stakes"] = fuse(stakes)
    return out


def ytube_(x, z, ro, ri, y0, y1):
    return ycyl(x, z, ro, y0, y1) - ycyl(x, z, ri, y0 - 1, y1 + 1)


# ----------------------------------------------------------------------------- probe
def probe_parts(P=PARAMS):
    """One probe standing on its tip at z = 0, axis on z at x = y = 0."""
    td, tw, tl, n = P["probe_tube"]
    dt, cone, par, spg = P["probe_tip"]
    sd, sl = P["probe_spigot"]
    pd = P["probe_pin"]
    ri = td / 2 - tw
    out = {}
    z_tube0 = cone + par
    tip = (Solid.make_cone(3.0, dt / 2, cone, Plane(origin=(0, 0, 0), z_dir=(0, 0, 1)))
           + zcyl(0, 0, dt / 2, cone, cone + par) + zcyl(0, 0, ri, cone + par, cone + par + spg))
    sections = []
    for k in range(n):
        z0 = z_tube0 + k * tl
        tube = ztube(0, 0, td / 2, ri, z0, z0 + tl)
        parts = [tube]
        if k == 0:
            parts.append(tip)
        if k < n - 1:          # spigot welded into the top, half out
            parts.append(zcyl(0, 0, sd / 2, z0 + tl - sl / 2, z0 + tl + sl / 2))
        if k == n - 1:         # T handle
            ho, hw, hl = P["probe_handle"]
            zt = z0 + tl + ho / 2
            parts.append(xcyl(0, zt, ho / 2, -hl / 2, hl / 2) - xcyl(0, zt, ho / 2 - hw, -hl / 2 - 1, hl / 2 + 1))
        sec = fuse(parts)
        # pin holes 30 mm above each joint (in the upper tube and the spigot below it)
        for zj in (z0, z0 + tl):
            if 0 < zj - z_tube0 < n * tl:
                sec = sec - ycyl(0, zj + 30.0, pd / 2 + 0.2, -td, td)
        sections.append(sec)
    out["probe_tip_section"] = sections[0]
    out["probe_mid_section"] = sections[1]
    out["probe_top_section"] = sections[2]
    out["probe_pins"] = fuse([ycyl(0, z_tube0 + k * tl + 30.0, pd / 2, -td / 2 - 4, td / 2 + 4) for k in range(1, n)])
    return out


def probe_whole(P=PARAMS):
    p = probe_parts(P)
    return Compound([p["probe_tip_section"], p["probe_mid_section"], p["probe_top_section"], p["probe_pins"]])


# ----------------------------------------------------------------------------- crawl board and links
def board(P=PARAMS):
    """One crawl board centred at the origin, length along X, walking face up (z = 0 at the batten feet)."""
    L, W, t = P["board"]
    bw, bd, inset = P["batten"]
    yb = W / 2 - inset - bw / 2
    lw, lt, ll, lp, lpl, lh = P["link"]
    deck = bx(-L / 2, L / 2, -W / 2, W / 2, bd, bd + t)
    sw, sh, se = P["hand_slot"]
    for sx in (-1, 1):
        cx = sx * (L / 2 - se - sh / 2)
        deck = deck - bx(cx - sh / 2, cx + sh / 2, -sw / 2, sw / 2, bd - 1, bd + t + 1)
    battens = [bx(-L / 2, L / 2, y - bw / 2, y + bw / 2, 0, bd) for y in (-yb, yb)]
    b = fuse([deck] + battens)
    for sx in (-1, 1):
        for y in (-yb, yb):
            b = b - zcyl(sx * (L / 2 - lh), y, lp / 2 + 0.5, -1, bd + t + 1)
    return b


def link_plate(P=PARAMS, x_joint=0.0):
    """Link plate across the butt joint at x_joint, on the +Y batten line (mirror for -Y)."""
    L, W, t = P["board"]
    bw, bd, inset = P["batten"]
    yb = W / 2 - inset - bw / 2
    lw, lt, ll, lp, lpl, lh = P["link"]
    ztop = bd + t
    plates = []
    for y in (-yb, yb):
        pl = bx(x_joint - ll / 2, x_joint + ll / 2, y - lw / 2, y + lw / 2, ztop, ztop + lt)
        for xp in (x_joint - lh, x_joint + lh):
            pl = pl + zcyl(xp, y, lp / 2, ztop - lpl, ztop)
        plates.append(pl)
    return fuse(plates)


# ----------------------------------------------------------------------------- crates (search crate, capstan crate)
def box_parts(P=PARAMS, open_lid=False, which="box"):
    """Crate centred on x = y = 0, ground at z = 0; the lid hinges along the back (+Y) top edge.
    which = "box": the search crate every site keeps; "cap_box": the capstan crate at the host site."""
    L, W, H = P[which]
    t = P["ply"]
    sk_w, sk_h = P["skid"]
    zb = sk_h
    body = [bx(-L / 2, L / 2, -W / 2, W / 2, zb, zb + t)]
    ztop = zb + H
    for sg in (-1, 1):
        y0 = W / 2 - t if sg > 0 else -W / 2
        body.append(bx(-L / 2, L / 2, y0, y0 + t, zb + t, ztop))
        x0 = L / 2 - t if sg > 0 else -L / 2
        body.append(bx(x0, x0 + t, -W / 2 + t, W / 2 - t, zb + t, ztop))
    for sx in (-1, 1):                  # corner battens 45 x 45 inside the corners
        for sy in (-1, 1):
            cx = sx * (L / 2 - t - 22.5)
            cy = sy * (W / 2 - t - 22.5)
            body.append(bx(cx - 22.5, cx + 22.5, cy - 22.5, cy + 22.5, zb + t, ztop - 30))
    for sy in (-1, 1):                  # skids
        body.append(bx(-L / 2 + 40, L / 2 - 40, sy * (W / 2 - 120) - sk_w / 2, sy * (W / 2 - 120) + sk_w / 2, 0, sk_h))
    # rope handles: hardwood cleats on the ends
    for sx in (-1, 1):
        x0 = L / 2 if sx > 0 else -L / 2 - 30
        body.append(bx(x0, x0 + 30, -150, 150, ztop - 160, ztop - 120))
    out = {"box_body": fuse(body)}
    g, sk = P["lid_gap"], P["skirt"]
    Lo, Wo = L + 2 * (g + t), W + 2 * (g + t)
    zl = ztop + 3.0                      # 3 mm seal strip on the rim
    lid = [bx(-Lo / 2, Lo / 2, -Wo / 2, Wo / 2, zl, zl + t)]
    for sg in (-1, 1):
        y0 = Wo / 2 - t if sg > 0 else -Wo / 2
        lid.append(bx(-Lo / 2, Lo / 2, y0, y0 + t, zl - sk, zl))
        x0 = Lo / 2 - t if sg > 0 else -Lo / 2
        lid.append(bx(x0, x0 + t, -Wo / 2 + t, Wo / 2 - t, zl - sk, zl))
    lid = fuse(lid)
    seal = (bx(-L / 2, L / 2, -W / 2, W / 2, ztop, zl) - bx(-L / 2 + t, L / 2 - t, -W / 2 + t, W / 2 - t, ztop - 1, zl + 1))
    # hardware: three strap hinges on the back, hasp on the front
    hw = []
    for hx in (-0.37 * L, 0.0, 0.37 * L):
        hw.append(bx(hx - 40, hx + 40, W / 2, W / 2 + 3, ztop - 120, ztop - 50 + 0.0))
    hw.append(bx(-40, 40, -W / 2 - 3, -W / 2, ztop - 130, ztop - 60))
    if open_lid:
        hinge_y, hinge_z = Wo / 2, zl
        ang = P["lid_open_deg"]
        lid = Pos(0, hinge_y, hinge_z) * Rot(-ang, 0, 0) * Pos(0, -hinge_y, -hinge_z) * lid
    out["box_lid"] = lid
    out["box_hardware"] = fuse(hw + [seal])
    return out


# ----------------------------------------------------------------------------- stretcher, clamp, shovel
def stretcher(P=PARAMS):
    """Sheet stretcher laid flat, centred at the origin, length along X."""
    L, W, t = P["sheet"]
    sl, sw, se = P["sheet_slot"]
    sheet = bx(-L / 2, L / 2, -W / 2, W / 2, 0, t)
    for k in range(6):
        cx = -L / 2 + 250 + k * (L - 500) / 5
        for sg in (-1, 1):
            cy = sg * (W / 2 - se - sw / 2)
            sheet = sheet - bx(cx - sl / 2, cx + sl / 2, cy - sw / 2, cy + sw / 2, -1, t + 1)
    straps = []
    for cx in (-550.0, 0.0, 550.0):
        straps.append(bx(cx - P["strap_w"] / 2, cx + P["strap_w"] / 2, -W / 2 + 5, W / 2 - 5, t, t + 2))
        straps.append(bx(cx - 30, cx + 30, W / 2 - 160, W / 2 - 110, t + 2, t + 10))     # buckle
    # head haul strap: a webbing loop across the head end
    straps.append(bx(L / 2 - 80, L / 2 - 30, -W / 2 + 120, W / 2 - 120, t, t + 2))
    return {"sheet": sheet, "straps": fuse(straps)}


def sheet_clamp(P=PARAMS):
    """Sheet clamp on the ground, bars along X, centred at the origin."""
    w, t, L = P["clamp"]
    g = P["clamp_gap"]
    xs = [s * x for x in P["clamp_bolts"] for s in (-1, 1)]
    lower = bx(-L / 2, L / 2, -w / 2, w / 2, 0, t)
    upper = bx(-L / 2, L / 2, -w / 2, w / 2, t + g, 2 * t + g)
    lug = prism_xz(hull2d([(-45, 2 * t + g), (45, 2 * t + g)] + circle_pts(0, 2 * t + g + 45, 28, 24)), -5, 5)
    lug = lug - ycyl(0, 2 * t + g + 45, 11.0, -6, 6)
    for x in xs:
        lower = lower - zcyl(x, 0, 6.5, -1, t + 1)
        upper = upper - zcyl(x, 0, 6.5, t + g - 1, 2 * t + g + 1)
    bolts = []
    for x in xs:
        bolts.append(zcyl(x, 0, 6.0, -12, 2 * t + g + 22) + zcyl(x, 0, 11.0, -20, -12)
                     + bx(x - 28, x + 28, -6, 6, 2 * t + g + 10, 2 * t + g + 22) + zcyl(x, 0, 11.0, 2 * t + g, 2 * t + g + 10))
    return {"clamp_bars": fuse([lower, fuse([upper, lug])]), "clamp_bolts": fuse(bolts)}


def shovel(P=PARAMS):
    """Bought long-handled round-point shovel lying on its back, blade toward -X."""
    bw, bl, L = P["shovel"]
    blade = prism_xy([(-L / 2, 0), (-L / 2 + 60, -bw / 2), (-L / 2 + bl, -bw / 2), (-L / 2 + bl, bw / 2), (-L / 2 + 60, bw / 2)], 0, 2)
    socket = rod((-L / 2 + bl - 20, 0, 18), (-L / 2 + bl + 130, 0, 18), 17.0)
    handle = rod((-L / 2 + bl + 130, 0, 18), (L / 2, 0, 18), 18.0)
    return fuse([blade, socket, handle, bx(-L / 2 + bl - 30, -L / 2 + bl, -15, 15, 2, 18)])


# ----------------------------------------------------------------------------- packed crates
def packed_contents(P=PARAMS):
    """The search kit stowed in the closed search crate (crate centred at the origin). Bags and
    bundles are drawn as their outer envelopes. Returns {name: shape}; checks() confirms nothing
    overlaps. PPE comes from the cooperative's stock and is kept in its bag in this crate."""
    L, W, H = P["box"]
    t = P["ply"]
    z0 = P["skid"][1] + t                         # inside floor
    xi, yi = L / 2 - t, W / 2 - t                 # inside half sizes
    bL, bW, bt = P["board"]
    bd = P["batten"][1]
    out = {}
    # boards flat at the back, four high
    bx_c = -xi + 50 + bL / 2
    yb = yi - 4 - bW / 2
    out["Crawl boards (4), stacked"] = Compound([Pos(bx_c, yb, z0 + k * (bd + bt)) * board(P) for k in range(4)])
    ztop = z0 + 4 * (bd + bt)
    # on the boards: shovels in two layers, then the probe bag
    sh = shovel(P)
    sl = []
    for layer in range(2):
        for k, sg in enumerate((-1, 1)):
            y = yb + sg * 110
            s_ = Pos(bx_c, y, ztop + 1 + layer * 40) * (Rot(0, 0, 180) * sh if k else sh)
            sl.append(s_)
    out["Shovels (4)"] = Compound(sl)
    z2 = ztop + 82
    out["Probe bag (18 sections)"] = Pos(bx_c, yb, z2 + 80) * Rot(0, 90, 0) * Cylinder(80, 1160)
    # bags along the front, the rolled stretcher on top of them
    xl = -xi + 50
    out["Lookout kit and lights bag"] = bx(xl, xl + 275, -yi + 5, -yi + 345, z0, z0 + 300)
    out["PPE bag"] = bx(xl + 280, xl + 980, -yi + 5, -yi + 345, z0, z0 + 300)
    out["Stretcher, rolled"] = Pos(xl + 40 + 450, -yi + 5 + 170, z0 + 305 + 125) * Rot(0, 90, 0) * Cylinder(125, 900)
    return out


def packed_capstan(P=PARAMS):
    """The capstan set stowed in the closed capstan crate at the host site (crate centred at the
    origin): capstan upright with its bars off and stakes out, bars standing in a front corner,
    rope, slings and clamp, and stakes in bags along the front."""
    L, W, H = P["cap_box"]
    t = P["ply"]
    z0 = P["skid"][1] + t
    xi, yi = L / 2 - t, W / 2 - t
    out = {}
    cap = capstan_parts(P)
    keys = [k for k in CAPSTAN_KEYS if k not in ("bars", "bar_pins", "stakes")]
    cy = yi - 5 - (P["frame_w"] / 2 + P["stake_tube"][0])
    out["Capstan, bars off"] = Pos(0.0, cy, z0) * Compound([cap[k] for k in keys])
    xl = -xi + 50                                 # clear of the corner battens
    out["Rope bag"] = bx(xl, xl + 420, -yi + 5, -yi + 345, z0, z0 + 300)
    out["Slings, shackles and sheet clamp bag"] = bx(xl, xl + 420, -yi + 5, -yi + 345, z0 + 305, z0 + 505)
    out["Stakes (4) and mallet"] = bx(xl + 425, xl + 700, -yi + 5, -yi + 345, z0, z0 + 120)
    b = P["bar"][0]
    out["Capstan bars (2), standing"] = Compound([bx(xl + 705 + k * (b + 5), xl + 705 + k * (b + 5) + b, -yi + 5, -yi + 5 + b,
                                                    z0, z0 + P["bar"][2]) for k in range(2)])
    return out


# ----------------------------------------------------------------------------- components and layouts
@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    group: str          # capstan, probe, board, box, stretcher, clamp, kit
    material: str


BOM = {  # key: (BOM line, plain name, material)
    "box_body": (1, "Search crate body", "plywood"),
    "box_lid": (2, "Search crate lid", "plywood"),
    "box_hardware": (3, "Crate hinges, hasp and seal", "steel"),
    "boards": (4, "Crawl boards (4)", "plywood"),
    "links": (5, "Board link plates", "steel"),
    "probe_tip_section": (6, "Probe tip section", "steel"),
    "probe_mid_section": (6, "Probe middle section", "steel"),
    "probe_top_section": (6, "Probe top section with T handle", "steel"),
    "probes": (6, "Probes (6), assembled", "steel"),
    "probe_pins": (7, "Probe joint pins", "steel"),
    "shovels": (8, "Long-handled shovels (4)", "steel"),
    "frame": (9, "Capstan base frame with post", "steel"),
    "drum": (10, "Capstan drum with holding ratchet", "steel"),
    "drive_ratchet": (11, "Drive ratchet wheel", "steel"),
    "head": (12, "Lever head", "steel"),
    "hold_pawls": (13, "Holding pawls (2)", "steel"),
    "drive_pawl": (13, "Drive pawl", "steel"),
    "bars": (14, "Capstan bars (2)", "steel"),
    "bar_pins": (14, "Bar pins (2)", "steel"),
    "bushes": (15, "Bushes and thrust washers", "acetal"),
    "roller": (16, "Hold-down roller", "steel"),
    "roller_pin": (16, "Roller pin", "steel"),
    "keeper": (17, "Keeper collar and pin", "steel"),
    "shear_pin": (18, "Shear pin", "steel"),
    "stakes": (19, "Ground stakes (4)", "steel"),
    "rope": (20, "Capstan rope, 14 mm", "polyester"),
    "sling": (21, "Anchor sling and shackle", "polyester"),
    "clamp_bars": (22, "Sheet clamp bars", "steel"),
    "clamp_bolts": (22, "Sheet clamp bolts", "steel"),
    "sheet": (23, "Sheet stretcher", "HDPE"),
    "straps": (23, "Stretcher straps", "polyester"),
    "wands": (24, "Marker wands and safe-zone sign", "fibreglass"),
}
CAPSTAN_KEYS = ["frame", "roller", "roller_pin", "bushes", "drum", "drive_ratchet", "shear_pin", "head",
                "hold_pawls", "drive_pawl", "bars", "bar_pins", "keeper", "stakes"]

# Display layout: the kit laid out beside the open box (for the hero and the product renders)
CAP_AT = (2350.0, 150.0)
BOARD_Y = -850.0
STRETCH_AT = (-300.0, -1750.0)


def _wands(P, pts):
    ws = []
    for x, y in pts:
        ws.append(zcyl(x, y, 4.0, -200, 1000) + bx(x + 4, x + 154, y - 1, y + 1, 850, 1000))
    return fuse(ws)


def build_components(P=PARAMS, layout="display"):
    """Every component placed. layout 'display': the kit laid out beside the open box;
    'site': deployed at a slide (shortened distances). Returns {key: Comp}."""
    C = {}
    cap = capstan_parts(P)
    if layout == "display":
        cap_loc = Pos(CAP_AT[0], CAP_AT[1], 0) * Rot(0, 0, 0)
    else:
        cap_loc = Pos(3600.0, -1400.0, 0) * Rot(0, 0, 150)
    for k, s in cap.items():
        n, nm, mat = BOM[k][0], BOM[k][1], BOM[k][2]
        C[k] = Comp(nm, cap_loc * s, n, "capstan", mat)
    L, W, t = P["board"]
    bd = P["batten"][1]
    if layout == "display":
        bpos = [Pos(-L / 2, BOARD_Y, 0), Pos(L / 2, BOARD_Y, 0)]
        boards = [p * board(P) for p in bpos]
        links = [Pos(0, BOARD_Y, 0) * link_plate(P, 0.0)]
        # the other two boards stacked on the first pair's left end? stacked beside the box, left
        boards += [Pos(-2550.0, 350.0, 0) * Rot(0, 0, 90) * board(P),
                   Pos(-2550.0, 350.0, bd + t) * Rot(0, 0, 90) * board(P)]
        C["boards"] = Comp(BOM["boards"][1], Compound(boards), 4, "board", "plywood")
        C["links"] = Comp(BOM["links"][1], Compound(links), 5, "board", "steel")
        # probes standing in a line in front of the boards, as they are used
        pr = probe_whole(P)
        probes = [Pos(-1250.0 + 500.0 * k, -1190.0, 0) * Rot(0, 0, 90) * pr for k in range(6)]
        C["probes"] = Comp(BOM["probes"][1], Compound(probes), 6, "probe", "steel")
        sh = shovel(P)
        C["shovels"] = Comp(BOM["shovels"][1], Compound([Pos(-2550.0 + 0.0, -900.0 - k * 260.0, 0) * Rot(0, 0, 0) * sh
                                                         for k in range(4)]), 8, "kit", "steel")
        st = stretcher(P)
        C["sheet"] = Comp(BOM["sheet"][1], Pos(*STRETCH_AT, 0) * st["sheet"], 23, "stretcher", "HDPE")
        C["straps"] = Comp(BOM["straps"][1], Pos(*STRETCH_AT, 0) * st["straps"], 23, "stretcher", "polyester")
        cl = sheet_clamp(P)
        cl_at = Pos(1650.0, -1800.0, 0)
        C["clamp_bars"] = Comp(BOM["clamp_bars"][1], cl_at * cl["clamp_bars"], 22, "clamp", "steel")
        C["clamp_bolts"] = Comp(BOM["clamp_bolts"][1], cl_at * cl["clamp_bolts"], 22, "clamp", "steel")
        # rope coiled in front of the capstan; anchor sling coiled behind it
        rc = (CAP_AT[0] - 50.0, CAP_AT[1] - 1300.0)
        rope = Compound([Pos(rc[0], rc[1], 7 + 14 * i) * Torus(260 - 8 * i, 7) for i in range(4)])
        C["rope"] = Comp(BOM["rope"][1], rope, 20, "kit", "polyester")
        sl = Compound([Pos(CAP_AT[0] + 900.0, CAP_AT[1] - 300.0, 6) * Torus(150, 6),
                       Pos(CAP_AT[0] + 900.0, CAP_AT[1] - 300.0, 18) * Torus(140, 6)])
        C["sling"] = Comp(BOM["sling"][1], sl, 21, "kit", "polyester")
        C["wands"] = Comp(BOM["wands"][1], _wands(P, [(-1700.0, 900.0), (-1550.0, 950.0), (-1400.0, 1000.0)]),
                          24, "kit", "fibreglass")
        bxp = box_parts(P, open_lid=True)
    else:
        # deployed: four boards in a line up the debris (+Y), probes standing in a line at the head
        boards, links = [], []
        for k in range(4):
            boards.append(Pos(0, k * L + L / 2, 0) * Rot(0, 0, 90) * board(P))
            if k:
                links.append(Pos(0, k * L, 0) * Rot(0, 0, 90) * link_plate(P, 0.0))
        C["boards"] = Comp(BOM["boards"][1], Compound(boards), 4, "board", "plywood")
        C["links"] = Comp(BOM["links"][1], Compound(links), 5, "board", "steel")
        pr = probe_whole(P)
        probes = [Pos(-1250.0 + 500.0 * k, 4 * L + 400.0, -1400.0) * pr for k in range(6)]
        C["probes"] = Comp(BOM["probes"][1], Compound(probes), 6, "probe", "steel")
        st = stretcher(P)
        at = Pos(-900.0, 2400.0, 0) * Rot(0, 0, 90)
        C["sheet"] = Comp(BOM["sheet"][1], at * st["sheet"], 23, "stretcher", "HDPE")
        C["straps"] = Comp(BOM["straps"][1], at * st["straps"], 23, "stretcher", "polyester")
        cl = sheet_clamp(P)
        cl_at = Pos(1300.0, 3600.0, 0) * Rot(0, 0, -30)
        C["clamp_bars"] = Comp(BOM["clamp_bars"][1], cl_at * cl["clamp_bars"], 22, "clamp", "steel")
        C["clamp_bolts"] = Comp(BOM["clamp_bolts"][1], cl_at * cl["clamp_bolts"], 22, "clamp", "steel")
        # rope from the hold-down roller to the clamp lug, straight
        D = derived(P)
        rx = P["roller"][0]
        ang = math.radians(150)
        sx = 3600.0 + (rx - 30.0) * math.cos(ang)
        sy = -1400.0 + (rx - 30.0) * math.sin(ang)
        ex, ey = 1300.0, 3600.0
        ez = 2 * P["clamp"][1] + P["clamp_gap"] + 45.0
        C["rope"] = Comp(BOM["rope"][1], rod((sx, sy, D["z_rope_out"]), (ex, ey, ez), P["rope_d"] / 2), 20, "kit", "polyester")
        ex2 = 3600.0 + (P["frame_l"] / 2 + 50.0) * math.cos(ang)
        ey2 = -1400.0 + (P["frame_l"] / 2 + 50.0) * math.sin(ang)
        far = (ex2 - 2500.0 * math.cos(ang), ey2 - 2500.0 * math.sin(ang))
        C["sling"] = Comp(BOM["sling"][1], rod((ex2, ey2, D["z_rope_out"]), (far[0], far[1], D["z_rope_out"] + 40), 12.0),
                          21, "kit", "polyester")
        C["wands"] = Comp(BOM["wands"][1], _wands(P, [(-600.0, 6400.0), (0.0, 6500.0), (600.0, 6400.0)]),
                          24, "kit", "fibreglass")
        bxp = None
    if bxp:
        for k, s in bxp.items():
            C[k] = Comp(BOM[k][1], s, BOM[k][0], "box", BOM[k][2])
    return C


def context_shapes(P=PARAMS, layout="display"):
    """Grey context: for 'display' a shed wall behind the box; for 'site' the debris and an anchor post."""
    if layout == "display":
        return {"shed": bx(-3300.0, 3600.0, 1250.0, 1350.0, 0, 2400.0)}
    ang = math.radians(150)
    ex2 = 3600.0 + (P["frame_l"] / 2 + 50.0) * math.cos(ang)
    ey2 = -1400.0 + (P["frame_l"] / 2 + 50.0) * math.sin(ang)
    far = (ex2 - 2500.0 * math.cos(ang) + 150 * -math.cos(ang), ey2 - 2500.0 * math.sin(ang) + 150 * -math.sin(ang))
    debris = prism_xy([(-2600, 1500), (2600, 1500), (2600, 7500), (-2600, 7500)], -1, 0)
    return {"debris": debris, "anchor_post": zcyl(far[0], far[1], 150.0, 0, 1800.0)}


# ----------------------------------------------------------------------------- checks
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
    """Constructability checks: no two separate parts overlap; every part touches what holds it."""
    cap = capstan_parts(P)
    pr = probe_parts(P)
    res = {"overlaps": [], "floating": []}
    holds = [("bushes", "frame"), ("drum", "bushes"), ("drive_ratchet", "drum"), ("shear_pin", "drum"),
             ("shear_pin", "drive_ratchet"), ("bushes", "head"), ("head", "bushes"), ("hold_pawls", "frame"),
             ("drive_pawl", "head"), ("bar_pins", "head"), ("bar_pins", "bars"),
             ("keeper", "frame"), ("roller_pin", "frame"), ("roller", "roller_pin"), ("stakes", "frame")]
    for a, b in holds:
        d = _dist(cap[a], cap[b])
        if not d <= 0.6:
            res["floating"].append((a, b, round(d, 2)))
    keys = list(cap)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            v = _overlap(cap[a], cap[b])
            if not v < 1.0:
                res["overlaps"].append((a, b, round(v, 1)))
    pk = list(pr)
    for i, a in enumerate(pk):
        for b in pk[i + 1:]:
            v = _overlap(pr[a], pr[b])
            if not v < 1.0:
                res["overlaps"].append((a, b, round(v, 1)))
    for a, b in (("probe_mid_section", "probe_tip_section"), ("probe_top_section", "probe_mid_section"),
                 ("probe_pins", "probe_mid_section")):
        d = _dist(pr[a], pr[b])
        if not d <= 0.6:
            res["floating"].append((a, b, round(d, 2)))
    L = P["board"][0]
    b1, b2 = Pos(-L / 2, 0, 0) * board(P), Pos(L / 2, 0, 0) * board(P)
    lk = link_plate(P, 0.0)
    for nm, v in (("board/board", _overlap(b1, b2)), ("link/board1", _overlap(lk, b1)), ("link/board2", _overlap(lk, b2))):
        if not v < 1.0:
            res["overlaps"].append((nm, round(v, 1)))
    if not _dist(lk, b1) <= 0.6:
        res["floating"].append(("links", "boards", _dist(lk, b1)))
    bxp = box_parts(P)
    for a, b in (("box_body", "box_lid"), ("box_body", "box_hardware"), ("box_lid", "box_hardware")):
        v = _overlap(bxp[a], bxp[b])
        if not v < 1.0:
            res["overlaps"].append((a, b, round(v, 1)))
    pk = packed_contents(P)
    shell = [bxp["box_body"], bxp["box_lid"], bxp["box_hardware"]]
    names = list(pk)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = _overlap(pk[a], pk[b])
            if not v < 1.0:
                res["overlaps"].append(("packed: " + a, b, round(v, 1)))
        for sh_ in shell:
            v = _overlap(pk[a], sh_)
            if not v < 1.0:
                res["overlaps"].append(("packed: " + a, "box", round(v, 1)))
    cbx = box_parts(P, which="cap_box")
    for a, b in (("box_body", "box_lid"), ("box_body", "box_hardware"), ("box_lid", "box_hardware")):
        v = _overlap(cbx[a], cbx[b])
        if not v < 1.0:
            res["overlaps"].append(("capstan crate " + a, b, round(v, 1)))
    pc = packed_capstan(P)
    cshell = [cbx["box_body"], cbx["box_lid"], cbx["box_hardware"]]
    names = list(pc)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = _overlap(pc[a], pc[b])
            if not v < 1.0:
                res["overlaps"].append(("capstan crate: " + a, b, round(v, 1)))
        for sh_ in cshell:
            v = _overlap(pc[a], sh_)
            if not v < 1.0:
                res["overlaps"].append(("capstan crate: " + a, "crate", round(v, 1)))
    # every packed item lies inside its crate's inside space
    for nm, (pk_, which) in {"search crate": (pk, "box"), "capstan crate": (pc, "cap_box")}.items():
        L_, W_, H_ = P[which]
        xi_, yi_ = L_ / 2 - P["ply"], W_ / 2 - P["ply"]
        zf_, zt_ = P["skid"][1] + P["ply"], P["skid"][1] + H_
        for a, sh_ in pk_.items():
            bb = sh_.bounding_box()
            if (bb.min.X < -xi_ - 0.5 or bb.max.X > xi_ + 0.5 or bb.min.Y < -yi_ - 0.5 or bb.max.Y > yi_ + 0.5
                    or bb.min.Z < zf_ - 0.5 or bb.max.Z > zt_ + 0.5):
                res["overlaps"].append((nm + ": " + a, "outside the crate", 0))
    cl = sheet_clamp(P)
    v = _overlap(cl["clamp_bars"], cl["clamp_bolts"])
    if not v < 1.0:
        res["overlaps"].append(("clamp_bars", "clamp_bolts", round(v, 1)))
    if verbose:
        print("overlaps (should be none):", res["overlaps"] or "none")
        print("parts not touching what holds them (should be none):", res["floating"] or "none")
    return res


def masses(P=PARAMS):
    """Mass of each component in kg from model volumes."""
    rho = {"steel": P["rho_steel"], "plywood": P["rho_ply"], "acetal": P["rho_acetal"], "HDPE": P["rho_hdpe"]}
    cap = capstan_parts(P)
    m = {k: cap[k].volume * 1e-9 * (P["rho_acetal"] if k == "bushes" else P["rho_steel"]) for k in cap}
    stakes_head = m["stakes"]
    pr = probe_parts(P)
    m["probe"] = sum(v.volume for v in pr.values()) * 1e-9 * P["rho_steel"]
    # board: plywood deck and timber battens separately
    L, W, t = P["board"]
    bw, bd, _ = P["batten"]
    bvol = board(P).volume
    batt = 2 * L * bw * bd
    m["board"] = (bvol - batt) * 1e-9 * P["rho_ply"] + batt * 1e-9 * P["rho_timber"]
    m["link"] = link_plate(P).volume * 1e-9 * P["rho_steel"] / 2
    bxp = box_parts(P)
    m["box_body"] = bxp["box_body"].volume * 1e-9 * P["rho_ply"]
    m["box_lid"] = bxp["box_lid"].volume * 1e-9 * P["rho_ply"]
    cbx = box_parts(P, which="cap_box")
    m["cap_box_body"] = cbx["box_body"].volume * 1e-9 * P["rho_ply"]
    m["cap_box_lid"] = cbx["box_lid"].volume * 1e-9 * P["rho_ply"]
    st = stretcher(P)
    m["stretcher"] = st["sheet"].volume * 1e-9 * P["rho_hdpe"] + 0.6       # straps and buckles about 0.6 kg
    cl = sheet_clamp(P)
    m["clamp"] = (cl["clamp_bars"].volume + cl["clamp_bolts"].volume) * 1e-9 * P["rho_steel"]
    m["stakes"] = stakes_head
    return m


def export(P=PARAMS):
    root = Path(__file__).resolve().parents[2]
    (root / "cad" / "step").mkdir(parents=True, exist_ok=True)
    (root / "cad" / "stl").mkdir(parents=True, exist_ok=True)
    cap = capstan_parts(P)
    pr = probe_parts(P)
    L = P["board"][0]
    bxp = box_parts(P)
    st = stretcher(P)
    cl = sheet_clamp(P)
    groups = {"capstan": Compound([cap[k] for k in CAPSTAN_KEYS]),
              "probe": Compound(list(pr.values())),
              "board": Compound([Pos(-L / 2, 0, 0) * board(P), Pos(L / 2, 0, 0) * board(P), link_plate(P, 0.0)]),
              "box": Compound(list(bxp.values())),
              "capbox": Compound(list(box_parts(P, which="cap_box").values())),
              "stretcher": Compound(list(st.values())),
              "clamp": Compound(list(cl.values()))}
    for g, cmp in groups.items():
        export_step(cmp, str(root / "cad" / "step" / f"heapline-{g}.step"))
        export_stl(cmp, str(root / "cad" / "stl" / f"heapline-{g}.stl"), tolerance=0.5, angular_tolerance=0.3)
    C = build_components(P, "display")
    export_step(Compound([c.shape for c in C.values()]), str(root / "cad" / "step" / "heapline-assembly.step"))
    print("exported STEP and STL to cad/step and cad/stl")


if __name__ == "__main__":
    D = derived()
    print({k: (tuple(round(x, 1) for x in v) if isinstance(v, tuple) else round(v, 1)) for k, v in D.items()})
    checks()
    for k, v in sorted(masses().items()):
        print(f"{k:16s} {v:6.2f} kg")
    if "--check" not in sys.argv:
        export()
