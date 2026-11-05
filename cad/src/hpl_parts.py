"""HeapLine helpers for the kit 1.9 model (cad/src/model.py): plain geometry builders, weld beads, ratchet
wheels and pawls, R-clips, wood screws, shackles, crates and other repo-specific parts. The shared parts
library is .kit/cad_parts.py; nothing here changes it. All dimensions in millimetres, Z up, ground at z = 0.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Torus, Vector, extrude,  # noqa: E402
                       Sphere, Sketch, Circle, RectangleRounded, Location)
import cad_parts as cp  # noqa: E402

# Materials this repo needs that the kit library does not list (added at import; the kit file is unchanged)
cp.MATERIALS.setdefault("acetal", ("#E8E4D8", "hdpe", 1410))
cp.MATERIALS.setdefault("fibreglass", ("#F28C28", "painted", 1900))
cp.MATERIALS.setdefault("polyester", ("#F97316", "fabric", 1380))
cp.MATERIALS.setdefault("plywood_painted", ("#0F766E", "painted", 600))
cp.MATERIALS.setdefault("steel_paint_blue", ("#1D4ED8", "painted", 7850))
cp.MATERIALS.setdefault("steel_paint_orange", ("#C2410C", "painted", 7850))
cp.MATERIALS.setdefault("steel_paint_red", ("#B91C1C", "painted", 7850))
cp.MATERIALS.setdefault("steel_paint_green", ("#15803D", "painted", 7850))
cp.MATERIALS.setdefault("webbing", ("#1E3A8A", "fabric", 1000))
cp.MATERIALS.setdefault("hdpe_yellow", ("#FACC15", "hdpe", 950))


def part(name, shape, material, kind="made", bom=None, key=None, group="shell", color=None, explode=(0, 0, 0)):
    """cad_parts.part() plus a legacy component `key` (the drawings and build plan pictures group by it)."""
    d = cp.part(name, shape, material, kind=kind, bom=bom, group=group, color=color, explode=explode)
    d["key"] = key or name
    return d


# ----------------------------------------------------------------------------- plain geometry
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


def ytube(x, z, ro, ri, y0, y1):
    return ycyl(x, z, ro, y0, y1) - ycyl(x, z, ri, y0 - 1, y1 + 1)


def xtube(y, z, ro, ri, x0, x1):
    return xcyl(y, z, ro, x0, x1) - xcyl(y, z, ri, x0 - 1, x1 + 1)


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


def be(shape, r=1.0):
    """Break the edges of a made part (never leaves a bare box)."""
    return cp.break_edges(shape, r)


def place(shape, origin=(0, 0, 0), z_dir=(0, 0, 1), x_dir=None):
    """Put a shape built along +Z onto an axis through `origin` pointing along z_dir."""
    kw = dict(origin=origin, z_dir=z_dir)
    if x_dir is not None:
        kw["x_dir"] = x_dir
    return Plane(**kw).location * shape


def slot_cut(cx, cy, length, width, z0, z1, along="x"):
    """A stadium slot (length overall, width) as a cutting solid, long axis along x or y."""
    r = width / 2
    body = bx(cx - (length / 2 - r), cx + (length / 2 - r), cy - r, cy + r, z0, z1) if along == "x" else \
        bx(cx - r, cx + r, cy - (length / 2 - r), cy + (length / 2 - r), z0, z1)
    dx, dy = ((length / 2 - r), 0) if along == "x" else (0, (length / 2 - r))
    return body + zcyl(cx - dx, cy - dy, r, z0, z1) + zcyl(cx + dx, cy + dy, r, z0, z1)


# ----------------------------------------------------------------------------- welds (fillet beads)
def ring_bead(x, y, z, r, leg, up=True, axis="z"):
    """Fillet weld ring of leg `leg` around a round bar or tube of radius r where it meets a flat face at
    (x, y, z). axis 'z': bar along Z, bead above (up) or below the face; 'x' or 'y': bar along that axis,
    bead on the +side (up) or the -side."""
    cone = Solid.make_cone(r + leg, r, leg, Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))) - Cylinder(r, leg * 3)
    if not up:
        cone = Rot(180, 0, 0) * cone
    if axis == "x":
        cone = Rot(0, 90, 0) * cone
    elif axis == "y":
        cone = Rot(-90, 0, 0) * cone
    return Pos(x, y, z) * cone


def weld_bead(p0, p1, n1, n2, leg):
    """Fillet weld bead of leg `leg` along the line p0 to p1 in the corner whose two faces point toward the
    unit vectors n1 and n2 (both perpendicular to the line)."""
    a, b = Vector(*p0), Vector(*p1)
    d = b - a
    u = d.normalized()
    n1v = Vector(*n1).normalized()
    pl = Plane(origin=a, x_dir=n1v, z_dir=u)
    s = 1.0 if Vector(*n2).dot(pl.y_dir) > 0 else -1.0
    tri = Polygon((0, 0), (leg, 0), (0, s * leg), align=None)
    return extrude(pl * tri, d.length)


def collar_weld(slab, minus, edge=None):
    """A fillet weld all round a joint: a slab that overlaps the joint, less the parts it joins."""
    w = slab
    for m in minus:
        w = w - m
    return cp.break_edges(w, edge) if edge else w


# ----------------------------------------------------------------------------- ratchets and pawls
def ratchet_xy(z0, t, R, r, n, first_deg, bore, sense=1):
    """Ratchet wheel on z (axis at x = y = 0): radial faces, sloping backs."""
    pts = []
    for k in range(n):
        a = math.radians(first_deg + 360.0 * k / n)
        b = math.radians(first_deg + 360.0 * (k + 1) / n)
        pts += [(r * math.cos(a), r * math.sin(a)), (R * math.cos(b - 0.002), R * math.sin(b - 0.002))]
    w = prism_xy(pts, z0, z0 + t)
    if sense < 0:
        w = Rot(180, 0, 0) * w
        w = Pos(0, 0, 2 * z0 + t) * w
    return w - zcyl(0, 0, bore / 2, z0 - 1, z0 + t + 1)


def face_angle(first_deg, n, k):
    return first_deg + 360.0 * (k + 1) / n


def pawl_xy(nose, pivot, z0, t, pin_d=12.0, nose_r=2.0, body_r=12.0):
    pts = hull2d(circle_pts(*pivot, body_r, 32) + circle_pts(*nose, nose_r, 12))
    return prism_xy(pts, z0, z0 + t) - zcyl(pivot[0], pivot[1], pin_d / 2 + 0.5, z0 - 1, z0 + t + 1)


def pawl_points(R, r, n, face_deg, sense, lead=0.12, rn_frac=0.55, pivot_dist=55.0):
    p = 360.0 / n
    a = math.radians(face_deg + sense * lead * p)
    rn = r + rn_frac * (R - r)
    nose = (rn * math.cos(a), rn * math.sin(a))
    tx, ty = -math.sin(a) * sense, math.cos(a) * sense
    ux, uy = math.cos(a), math.sin(a)
    ang = math.radians(30.0)
    dx, dy = tx * math.cos(ang) + ux * math.sin(ang), ty * math.cos(ang) + uy * math.sin(ang)
    pivot = (nose[0] + dx * pivot_dist, nose[1] + dy * pivot_dist)
    return nose, pivot


# ----------------------------------------------------------------------------- small hardware
def rclip(pin_r, along="x", hole_r=1.2):
    """R-clip (hitch pin clip) on a pin of radius pin_r whose axis is z: a 2 mm wire leg through a cross hole
    along `along` (x or y) and the loop that wraps the pin, fused into one solid, centred on z = 0."""
    leg = Rot(0, 90, 0) * Cylinder(1.0, 2 * pin_r + 14) if along == "x" else Rot(90, 0, 0) * Cylinder(1.0, 2 * pin_r + 14)
    ring = Torus(pin_r + 1.15, 1.0)
    return leg + ring


def pin_hole(shape, x, y, z, r, along="x", reach=60):
    cut = xcyl(y, z, r, x - reach, x + reach) if along == "x" else ycyl(x, z, r, y - reach, y + reach)
    return shape - cut


def wood_screw(d, length):
    """Countersunk wood screw, head on top (z 0 to 0.55 d), shank down to -length, pointed."""
    head = Solid.make_cone(d, d * 0.5, d * 0.55, Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))).move(Location((0, 0, 0)))
    head = Pos(0, 0, 0) * head
    shank = Pos(0, 0, -length / 2) * Cylinder(d * 0.5, length - d * 0.5)
    shank = Pos(0, 0, -d * 0.25) * shank
    tip = Solid.make_cone(d * 0.5, 0.2, d * 0.5, Plane(origin=(0, 0, -length), z_dir=(0, 0, 1)))
    return head + shank + tip


def screws(points, d, length, z_top, normal=(0, 0, 1), x_dir=None):
    """A group of identical wood screws as one solid: heads on the face at height z_top, going down -normal.
    points are (x, y) on a horizontal face when normal is +Z; for other faces pass 3-D points via `pts3`."""
    w = wood_screw(d, length)
    return Compound([Pos(x, y, z_top) * w for x, y in points])


def screws3(points3, d, length, normal, x_dir=None):
    """Screws at 3-D points whose axes point along `normal` (head side) onto the face."""
    w = wood_screw(d, length)
    out = []
    for p in points3:
        out.append(place(w, origin=p, z_dir=normal, x_dir=x_dir))
    return Compound(out)


def bolt_parts(d, grip, origin, z_dir, nm_prefix="", x_dir=None, group="shell", bom=None, extra=None, key="bolts"):
    """Bolt, two washers and nut (cad_parts.hex_bolt_set) for a joint whose top face is at `origin` and
    whose axis points (head side) along z_dir. Returns part dicts of kind fastener."""
    out = []
    for nm, sh in cp.hex_bolt_set(d, grip, extra=extra):
        out.append(part((nm_prefix + " " + nm).strip(), place(sh, origin, z_dir, x_dir), "zinc_plated", kind="fastener",
                        group=group, key=key))
    return out


def wing_nut(d):
    """Wing nut for Md: boss with two wings, bore d, from z 0 up to 16."""
    s = cp.ISO[d][0]
    boss = zcyl(0, 0, s * 0.62, 0, 14)
    wing = [Pos(sg * (s * 0.62 + 11), 0, 14) * Box(24, 3.5, 24) for sg in (-1, 1)]
    wing = [w.move(Location((0, 0, 0))) for w in wing]
    w = boss + wing[0] + wing[1]
    return cp.break_edges(w - zcyl(0, 0, d / 2 + 0.1, -1, 20), 0.8)


def bow_shackle(origin, pin_dir, bow_dir, pin_d=19.0, bow_r=36.0, bar_d=16.0):
    """Bow shackle: a ring bow of bar_d bar in the plane normal to pin_dir, reaching out along bow_dir, and a
    pin of pin_d through the two ears (centred on origin). Returns (bow, pin) solids."""
    pin_dir = Vector(*pin_dir).normalized()
    bow_dir = Vector(*bow_dir).normalized()
    pl = Plane(origin=origin, z_dir=pin_dir, x_dir=bow_dir)
    bow = pl.location * (Pos(bow_r, 0, 0) * Torus(bow_r, bar_d / 2))
    keep = pl.location * Pos(bow_r * 0.9, 0, 0) * Box(bow_r * 2.2, bow_r * 2.6, bar_d * 4)
    bow = bow & keep
    ears = pl.location * (Pos(0, 0, 0) * Cylinder(bar_d * 0.85, 2 * (bar_d / 2) * 2 + 22))
    pin = pl.location * Cylinder(pin_d / 2, 2 * bar_d / 2 + 2 * bar_d + 14)
    return fuse([bow, ears]) - pin, pin


def coil(cx, cy, z0, R0, minor, loops, dR=0.0, dz=None):
    """Loops of rope or webbing lying in a stack: tori of decreasing radius, each `dz` higher."""
    dz = dz or 2 * minor
    return Compound([Pos(cx, cy, z0 + minor + k * dz) * Torus(R0 - k * dR, minor) for k in range(loops)])


# ----------------------------------------------------------------------------- label and flag
def flag(x, y, z0, z1, w=150.0, h=100.0):
    return bx(x + 4, x + 4 + w, y - 0.75, y + 0.75, z1 - h, z1)
