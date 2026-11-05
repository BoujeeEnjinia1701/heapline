"""Option C, lever rope-grip puller (kit 1.9, D3). No drum: the rope runs straight through the machine. A fixed
cam holds the rope; a traveller carrying a second cam is driven along two slotted side plates by a long
lever, gripping the rope on the pull stroke and sliding free on the return. The machine stands on two RHS
rails with four ground stakes and an anchor shackle; the rope runs to a load stake. Axis of the rope: X."""
import math

from build123d import Pos, Rot

import cad_parts as cp
import hpl_parts as H
from hpl_parts import be, bx, fuse, hull2d, part, prism_xz, rod, xcyl, ycyl, zcyl

ZR = 200.0                        # rope height above ground
Y_IN, PT = 60.0, 10.0             # plate inner face and thickness
KEY = "puller"
LEVER = 1600.0                    # mm, pivot to grips: HPL-DDR-006 (1100 mm gave more than 150 N each)


def _pin(name, clip_name, x, z, r, half, y_c=0.0):
    """Pin along Y with a cross hole near each end and a split pin through each."""
    yh = half - 3.5
    pin = ycyl(x, z, r, y_c - half, y_c + half)
    for sy in (-1, 1):
        pin = pin - xcyl(y_c + sy * yh, z, 1.35, x - 10.0, x + 10.0)
    out = [part(name, be(pin, 0.4), "mild_steel", key=KEY)]
    for i, sy in enumerate((-1, 1)):
        out.append(part(f"{clip_name} {i + 1}", Pos(x + max(0.0, r - 4.0), y_c + sy * yh, z) * cp.split_pin(8.0), "zinc_plated",
                        kind="fastener", key=KEY))
    return out


def _cam(name, pivot, toe):
    c = prism_xz(hull2d(H.circle_pts(pivot[0], pivot[1], 18.0) + H.circle_pts(toe[0], toe[1], 9.0)), -40.0, 40.0)
    c = c - ycyl(pivot[0], pivot[1], 8.1, -50, 50)
    return part(name, be(c, 0.8), "mild_steel", key=KEY)


def option_c(P, layout, common):
    leg = P["weld_leg"]
    out = list(common)
    w = []
    # ---- rails with stake sleeves, ground stakes, anchor eye
    for xr in (-200.0, 250.0):
        r = Rot(90, 0, 0) * cp.rhs(80.0, 40.0, 4.0, 520.0)
        bb = r.bounding_box().center()
        r = Pos(xr - bb.X, -bb.Y, 20.0 - bb.Z) * r
        sl = [Pos(xr, sy * 245.0, 0.0) * cp.round_tube(33.7, 3.2, 60.0) for sy in (-1, 1)]
        shapes = [r] + sl
        if xr > 0:
            shapes.append(bx(xr + 30.0, xr + 120.0, -10.0, 10.0, 0.0, 70.0))
        body = fuse(shapes)
        for sy in (-1, 1):
            body = body - zcyl(xr, sy * 245.0, 13.2, -10.0, 70.0)
        if xr > 0:
            body = body - ycyl(xr + 95.0, 35.0, 8.3, -20, 20)
        w.append(part(f"Base rail weldment, 80 x 40 x 4 RHS with two stake sleeves {'rear' if xr < 0 else 'front, with anchor eye'}",
                      be(body, 1.0), "painted_steel", key=KEY))
        for sy in (-1, 1):
            w.append(part("Ground stake, 25 mm bar, 500 mm", be(zcyl(xr, sy * 245.0, 12.5, -360.0, 140.0), 1.5), "mild_steel",
                          kind="bought", key=KEY))
    bow, pin = H.bow_shackle((345.0, 0.0, 35.0), (0, 1, 0), (1, 0, 0), pin_d=16.0, bow_r=30.0, bar_d=12.0)
    w.append(part("Shackle bow, anchor eye, WLL 1 t", bow, "galvanised", kind="bought", key=KEY))
    w.append(part("Shackle pin, 16 mm", pin, "zinc_plated", kind="bought", key=KEY))
    # ---- side plates
    corners = [(-230.0, 60.0), (280.0, 60.0), (-230.0, 360.0), (280.0, 360.0)]
    pts = [q for cx, cz in corners for q in H.circle_pts(cx, cz, 20.0, 16)]
    slot = hull2d(H.circle_pts(-10.0, ZR - 35.0, 8.4, 20) + H.circle_pts(110.0, ZR - 35.0, 8.4, 20))
    holes = [(-175.0, ZR - 35.0, 6.2), (-85.0, ZR - 35.0, 6.2), (-130.0, ZR + 45.0, 8.3), (140.0, 260.0, 8.3)]
    for s, nm in ((-1, "near"), (1, "far")):
        y0, y1 = (Y_IN, Y_IN + PT) if s > 0 else (-Y_IN - PT, -Y_IN)
        pl = prism_xz(hull2d(pts), y0, y1)
        for hx, hz, hr in holes:
            pl = pl - ycyl(hx, hz, hr, y0 - 1, y1 + 1)
        pl = pl - prism_xz(slot, y0 - 1, y1 + 1)
        w.append(part(f"Puller side plate {nm}, 10 mm", be(pl, 1.0), "painted_steel", key=KEY))
    wi = 0
    for s in (-1, 1):
        for yf, ny in ((s * Y_IN, -s), (s * (Y_IN + PT), s)):
            for x0 in (-240.0, 160.0):
                wi += 1
                b = H.weld_bead((x0, yf, 40.0), (x0 + 80.0, yf, 40.0), (0, 0, 1), (0, ny, 0), leg)
                w.append(part(f"Weld bead {wi}, plate to rail, 4 mm leg", b, "mild_steel", kind="weld", key=KEY))
    # ---- fixed bed and cam
    groove = lambda x0, x1: xcyl(0.0, ZR, 7.5, x0 - 1, x1 + 1)  # noqa: E731
    bed = bx(-200.0, -60.0, -59.0, 59.0, ZR - 70.0, ZR) - groove(-200.0, -60.0)
    for hx in (-175.0, -85.0):
        bed = bed - ycyl(hx, ZR - 35.0, 6.2, -70, 70)
    w.append(part("Fixed bed block, 140 x 118 x 70, grooved", be(bed, 1.0), "mild_steel", key=KEY))
    for hx in (-175.0, -85.0):
        for p_ in H.bolt_parts(12, 140.0, (hx, 70.0, ZR - 35.0), (0, 1, 0), nm_prefix=f"Bed bolt x{hx:.0f}", key=KEY):
            w.append(p_)
    w.append(_cam("Fixed cam, holds the rope", (-130.0, ZR + 45.0), (-112.0, ZR + 16.0)))
    w += _pin("Fixed cam pin, 16 mm", "Fixed cam pin split pin", -130.0, ZR + 45.0, 8.0, 82.0)
    # ---- traveller: bed with two cheeks, cam, cam pin, drive pin
    tr = fuse([bx(-20.0, 120.0, -40.0, 40.0, ZR - 70.0, ZR), bx(-20.0, 120.0, 42.0, 50.0, ZR - 70.0, ZR + 70.0),
               bx(-20.0, 120.0, -50.0, -42.0, ZR - 70.0, ZR + 70.0), bx(-20.0, 120.0, 38.0, 44.0, ZR - 70.0, ZR - 30.0),
               bx(-20.0, 120.0, -44.0, -38.0, ZR - 70.0, ZR - 30.0)])
    tr = tr - groove(-20.0, 120.0) - ycyl(50.0, ZR + 45.0, 8.1, -60, 60) - ycyl(50.0, ZR - 35.0, 8.3, -60, 60)
    w.append(part("Traveller weldment, grooved bed and two cheeks", be(tr, 1.0), "painted_steel", key=KEY))
    w.append(_cam("Traveller cam, grips the rope", (50.0, ZR + 45.0), (68.0, ZR + 16.0)))
    pin = ycyl(50.0, ZR + 45.0, 8.0, -55.0, 55.0)
    for sy in (-1, 1):
        pin = pin - xcyl(sy * 52.5, ZR + 45.0, 1.35, 40.0, 60.0)
    w.append(part("Traveller cam pin, 16 mm", be(pin, 0.4), "mild_steel", key=KEY))
    for i, sy in enumerate((-1, 1)):
        w.append(part(f"Traveller cam pin split pin {i + 1}", Pos(54.0, sy * 52.5, ZR + 45.0) * cp.split_pin(8.0), "zinc_plated",
                      kind="fastener", key=KEY))
    # ---- lever with its pivot and the drive pin in its slot
    pv = (140.0, 260.0)
    dp = (50.0, ZR - 35.0)
    ux, uz = pv[0] - dp[0], pv[1] - dp[1]
    ln = math.hypot(ux, uz)
    ux, uz = ux / ln, uz / ln
    he = (pv[0] + ux * LEVER, pv[1] + uz * LEVER)
    st = (dp[0] - ux * 40.0, dp[1] - uz * 40.0)
    en = (dp[0] + ux * 40.0, dp[1] + uz * 40.0)
    bars = []
    for sy in (-1, 1):
        y0, y1 = (72.0, 80.0) if sy > 0 else (-80.0, -72.0)
        b = prism_xz(hull2d(H.circle_pts(st[0], st[1], 24.0, 24) + H.circle_pts(he[0], he[1], 17.0, 24)), y0, y1)
        b = b - ycyl(pv[0], pv[1], 8.3, y0 - 1, y1 + 1) - prism_xz(hull2d(H.circle_pts(st[0], st[1], 8.4, 20) + H.circle_pts(en[0], en[1], 8.4, 20)), y0 - 1, y1 + 1)
        bars.append(b)
    cross = H.ytube(he[0], he[1], 19.0, 16.0, -200.0, 200.0)
    lever = fuse(bars + [cross])
    w.append(part("Lever weldment, two 8 mm bars and a 38 x 3 cross tube", be(lever, 0.8), "painted_steel", key=KEY))
    for sy, nm in ((-1, "near"), (1, "far")):
        g = H.ytube(he[0], he[1], 22.0, 19.1, sy * 100.0 - 50.0, sy * 100.0 + 50.0)
        w.append(part(f"Lever grip {nm}, HDPE", be(g, 2.0), "hdpe_yellow", kind="bought", key=KEY))
    w += _pin("Lever pivot pin, 16 mm", "Lever pivot pin split pin", pv[0], pv[1], 8.0, 86.5)
    w += _pin("Drive pin, 16 mm", "Drive pin split pin", dp[0], dp[1], 8.0, 86.5)
    # ---- rope through the machine to the load stake
    rd = 14.0
    w.append(part("Puller rope, 14 mm, load to the tail", rod((-1500.0, 0.0, ZR), (700.0, 0.0, ZR), rd / 2 - 0.2), "rope", kind="bought", key=KEY))
    w.append(part("Load stake, 25 mm bar", be(zcyl(-1500.0, 0.0, 12.5, -360.0, ZR), 1.0), "mild_steel", kind="bought", key=KEY))
    loc = Pos(2350.0, 150.0, 0) if layout == "display" else Pos(3600.0, -1400.0, 0) * Rot(0, 0, 150)
    for p in w:
        out.append(dict(p, shape=loc * p["shape"], group="shell"))
    return out
