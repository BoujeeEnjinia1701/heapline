"""Option B, six-part rope tackle (kit 1.9, D3). No machine: two triple blocks reeved six-part, an anchor picket,
a shear link in series with the load, a rope grab on the tail and five rope handles.  Part names carry the
words the contact list allows for ropes (Tackle rope) and handles (Rope handle)."""
import math

from build123d import Compound, Cylinder, Pos, Rot, Torus

import cad_parts as cp
import hpl_parts as H
from hpl_parts import be, bx, fuse, hull2d, part, prism_xz, rod, xcyl, ycyl, zcyl

SHEAVE_R = 62.5
Z0 = 490.0                      # axle height above the ground
PITCH = 26.0                    # sheave pitch along the axle (Y)
PLATE_T = 6.0
GAP = 80.0                      # clear width between the plates


def _plate(name, y_in, y_out, eye_dir, key, bom=None):
    """One block side plate in the XZ plane, axle at the origin, eye on the eye_dir side, with its holes."""
    ex = 125.0 * eye_dir
    pts = H.circle_pts(0.0, 0.0, 78.0) + H.circle_pts(ex, 0.0, 30.0)
    pl = prism_xz(hull2d(pts), y_in, y_out)
    pl = pl - ycyl(0.0, 0.0, 8.3, y_in - 1, y_out + 1) - ycyl(ex, 0.0, 8.3, y_in - 1, y_out + 1)
    return part(name, be(pl, 1.0), "painted_steel", bom=bom, key=key)


def block(tag, fx, eye_dir, key):
    """Triple block with its axle along Y at x = fx, z = Z0 (all in world coordinates)."""
    out = []
    y_a = GAP / 2
    for s, nm in ((-1, "near"), (1, "far")):
        y0, y1 = (s * y_a, s * (y_a + PLATE_T)) if s > 0 else (s * (y_a + PLATE_T), s * y_a)
        p = _plate(f"{tag} side plate {nm}, 6 mm", y0, y1, eye_dir, key)
        p["shape"] = Pos(fx, 0, Z0) * p["shape"]
        out.append(p)
    for i in (-1, 0, 1):
        y = i * PITCH
        sh = H.ytube(0.0, 0.0, SHEAVE_R, 10.0, y - 10.5, y + 10.5)
        groove = Rot(90, 0, 0) * Torus(SHEAVE_R + 2.0, 8.0)
        sh = be(sh - Pos(0, y, 0) * groove, 0.8)
        out.append(part(f"{tag} sheave {i + 2}, 125 mm", Pos(fx, 0, Z0) * sh, "cast_aluminium", key=key))
        bush = H.ytube(0.0, 0.0, 9.95, 8.15, y - 10.5, y + 10.5)
        out.append(part(f"{tag} sheave bush {i + 2}, acetal", Pos(fx, 0, Z0) * be(bush, 0.5), "acetal", key=key))
    # axle: a pin through plates and bushes, one M16 bolt set holds the pack
    out += H.bolt_parts(16, GAP + 2 * PLATE_T, (fx, y_a + PLATE_T, Z0), (0, 1, 0), nm_prefix=f"{tag} axle", key=key)
    return out


def _picket(px, key):
    tube = cp.round_tube(60.3, 4.0, 870.0)
    tube = Pos(px, 0, -450.0) * tube
    eye = bx(px - 30.0, px + 30.0, -5.0, 5.0, 400.0, Z0 + 30.0)
    eye = eye - ycyl(px, Z0, 8.3, -10, 10)
    body = be(fuse([tube, eye]), 1.0)
    return [part("Anchor picket weldment, 60.3 x 4 tube and eye plate", body, "galvanised", bom=None, key=key)]


def _clipped_pin(name, clip_name, x, z, r, half, d_clip, key, y_c=0.0):
    """Plain pin along Y with a cross hole near each... one end and a split pin through it."""
    yh = y_c + half - 2.0
    pin = ycyl(x, z, r, y_c - half, y_c + half) - xcyl(yh, z, 1.35, x - 10.0, x + 10.0)
    sk = Pos(x + max(0.0, r - 4.0), yh, z) * cp.split_pin(8.0)
    return [part(name, be(pin, 0.4), "mild_steel", key=key),
            part(clip_name, sk, "zinc_plated", kind="fastener", key=key)]


def option_b(P, layout, common):
    B = P["B"]
    out = list(common)
    key = "tackle"
    if layout == "display":
        ox, oy, yaw = 2350.0, 150.0, 0.0
    else:
        ox, oy, yaw = 3600.0, -1400.0, 150.0
    pull = []
    px = 0.0
    fx = px + 125.0                    # fixed block eye pinned to the picket eye plate
    mx = fx + 1500.0
    pull += _picket(px, key)
    pull += block("Fixed block", fx, -1, key)
    pull += block("Moving block", mx, 1, key)
    # picket eye plate carries the fixed block eye bolt (grip is the 24 mm gap + 2 x 6 mm plates)
    pull += H.bolt_parts(16, GAP + 2 * PLATE_T, (fx - 125.0, GAP / 2 + PLATE_T, Z0), (0, 1, 0), nm_prefix="Fixed block eye", key=key)
    # moving block eye pinned to the shear link
    lk = bx(0.0, 200.0, -6.0, 6.0, -20.0, 20.0)
    notch = bx(60.0, 120.0, -7.0, 7.0, 10.0, 21.0) + bx(60.0, 120.0, -7.0, 7.0, -21.0, -10.0)
    lk = lk - notch - ycyl(15.0, 0.0, 8.3, -10, 10) - ycyl(185.0, 0.0, 4.1, -10, 10)
    lk = Pos(mx + 125.0 - 15.0, 0, Z0) * lk
    pull.append(part("Shear link plate, 40 x 12 mild steel, notched", be(lk, 1.0), "mild_steel", key=key))
    pull += H.bolt_parts(16, GAP + 2 * PLATE_T, (mx + 125.0, GAP / 2 + PLATE_T, Z0), (0, 1, 0), nm_prefix="Moving block eye", key=key)
    # clevis that takes the shear pin and the sling
    cx = mx + 125.0 - 15.0 + 185.0
    for s, nm in ((-1, "near"), (1, "far")):
        y0, y1 = (6.5, 12.5) if s > 0 else (-12.5, -6.5)
        ch = prism_xz(hull2d(H.circle_pts(cx, Z0, 22.0) + H.circle_pts(cx + 90.0, Z0, 22.0)), y0, y1)
        ch = ch - ycyl(cx, Z0, 4.1, y0 - 1, y1 + 1) - ycyl(cx + 90.0, Z0, 6.6, y0 - 1, y1 + 1)
        pull.append(part(f"Sling clevis cheek {nm}, 6 mm", be(ch, 1.0), "painted_steel", key=key))
    pull += _clipped_pin("Shear pin, 8 mm, mild steel", "Split pin, 2.5 x 20", cx, Z0, 4.0, 17.0, 8.0, key)
    # sling from the clevis to a load stake at the debris
    lx = cx + 90.0
    pull.append(part("Load stake, 25 mm bar", be(zcyl(lx + 380.0, 0.0, 12.5, -360.0, 140.0), 1.0), "mild_steel", key=key))
    pull.append(part("Tackle rope, 14 mm, load sling to the stake", rod((lx, 0.0, Z0), (lx + 380.0, 0.0, 120.0), 6.8),
                     "rope", kind="bought", key=key))
    # six-part reeving: runs between the blocks, wraps on the sheaves, tail leaving the fixed block
    ys = [-PITCH, 0.0, PITCH]
    zt, zb = Z0 + SHEAVE_R + 3.0, Z0 - SHEAVE_R - 3.0
    runs = [((fx, ys[0], zb), (mx, ys[0], zb)), ((mx, ys[0], zt), (fx, ys[0], zt)),
            ((fx, ys[0], zb), (mx, ys[1], zb)), ((mx, ys[1], zt), (fx, ys[1], zt)),
            ((fx, ys[1], zb), (mx, ys[2], zb)), ((mx, ys[2], zt), (fx, ys[2], zt))]
    for k, (a, b) in enumerate(runs):
        pull.append(part(f"Tackle rope, 14 mm, run {k + 1}", rod(a, b, 6.8), "rope", kind="bought", key=key))
    for nm, x in (("fixed", fx), ("moving", mx)):
        for i, y in enumerate(ys):
            ring = Pos(x, y, Z0) * (Rot(90, 0, 0) * Torus(SHEAVE_R + 2.0, 6.8))
            pull.append(part(f"Tackle rope, wrap on {nm} sheave {i + 1}", ring, "rope", kind="bought", key=key))
    tail_end = fx - 3000.0
    pull.append(part("Tackle rope, 14 mm, tail", rod((fx, ys[2], zb), (tail_end, ys[2], zb), 6.8), "rope", kind="bought", key=key))
    for k in range(6):  # six handles: HPL-DDR-006 (five gave more than 200 N each)
        x = fx - 700.0 - k * 450.0
        hd = H.xtube(ys[2], zb, 20.0, 8.0, x, x + 160.0)
        pull.append(part(f"Rope handle {k + 1}, 40 mm HDPE", be(hd, 2.0), "hdpe_yellow", kind="bought", key=key))
    # rope grab: two plates, a toothed cam, pivot and spring pin, on the tail near the fixed block
    gx = fx - 420.0
    gz = zb
    for s, nm in ((-1, "near"), (1, "far")):
        y0, y1 = (ys[2] + 9.0, ys[2] + 14.0) if s > 0 else (ys[2] - 14.0, ys[2] - 9.0)
        g = prism_xz(hull2d(H.circle_pts(gx, gz, 30.0) + H.circle_pts(gx + 150.0, gz, 30.0)), y0, y1)
        g = g - ycyl(gx + 60.0, gz + 12.0, 6.1, y0 - 1, y1 + 1) - ycyl(gx + 150.0, gz, 6.1, y0 - 1, y1 + 1)
        pull.append(part(f"Rope grab plate {nm}, 5 mm", be(g, 1.0), "painted_steel", key=key))
    cam = prism_xz(hull2d(H.circle_pts(gx + 60.0, gz + 12.0, 22.0) + H.circle_pts(gx + 100.0, gz + 4.0, 10.0)),
                   ys[2] - 8.0, ys[2] + 8.0)
    cam = cam - ycyl(gx + 60.0, gz + 12.0, 6.1, ys[2] - 9.0, ys[2] + 9.0)
    pull.append(part("Rope grab cam, toothed", be(cam, 1.0), "mild_steel", key=key))
    pull += _clipped_pin("Rope grab pivot pin, 12 mm", "Rope grab pivot split pin", gx + 60.0, gz + 12.0, 6.0, 18.5, 12.0, key, y_c=ys[2])
    pull += _clipped_pin("Rope grab tie pin, 12 mm", "Rope grab tie split pin", gx + 150.0, gz, 6.0, 18.5, 12.0, key, y_c=ys[2])
    loc = Pos(ox, oy, 0) * Rot(0, 0, yaw)
    for p in pull:
        out.append(dict(p, shape=loc * p["shape"], group="shell"))
    return out
