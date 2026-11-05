"""HeapLine option A pull set, part by part (kit 1.9, D3): the pumped friction capstan, its rope, anchor
sling and shackle, the sheet clamp and the ground stakes. Built in the capstan's own frame: drum axis on z
at x = y = 0, ground at z = 0, load toward -X, anchor sling toward +X. Called from model.py.
"""
from __future__ import annotations

import math

from hpl_parts import *  # noqa: F401,F403
import cad_parts as cp
from build123d import Pos, Rot, Torus, Cylinder, Box, Compound

HOLD_FIRST = 7.5
DRIVE_FIRST = 0.0


def capstan(P, D):
    s, w = P["shs"]
    L, W = P["frame_l"], P["frame_w"]
    x0, x1 = -L / 2, L / 2
    yr = W / 2 - s / 2
    po, pw_, ph = P["post"]
    rw, rh, rt = P["rhs"]
    leg = P["weld_leg"]
    out = []
    A = lambda *a, **k: out.append(part(*a, bom=k.pop("bom", None), **k))  # noqa: E731

    # ---- frame (BOM 9): stock sections, then the weld beads that join them
    rail = lambda y: Pos(x0, y, s / 2) * Rot(0, 90, 0) * cp.shs(s, w, L)  # noqa: E731
    A("Frame rail -Y, 40 x 40 x 3 SHS", rail(-yr), "steel_paint_blue", bom=9, key="frame")
    A("Frame rail +Y, 40 x 40 x 3 SHS", rail(yr), "steel_paint_blue", bom=9, key="frame")
    cl = 2 * (yr - s / 2)
    cross = lambda x: Pos(x, -cl / 2, s / 2) * Rot(-90, 0, 0) * cp.shs(s, w, cl)  # noqa: E731
    A("Frame cross member, front", cross(x0 + s / 2), "steel_paint_blue", bom=9, key="frame")
    A("Frame cross member, rear", cross(x1 - s / 2), "steel_paint_blue", bom=9, key="frame")
    rhs = Pos(0, -cl / 2, rh / 2) * Rot(-90, 0, 0) * cp.rhs(rw, rh, rt, cl)
    rhs = rhs - zcyl(0, 0, po / 2 + 0.3, -1, rh + 1)
    for _k, _fk in enumerate((4, 16)):
        _n, _pv = pawl_points(P["hold_ratchet"][0] / 2, P["hold_ratchet"][1] / 2, P["hold_ratchet"][2], face_angle(HOLD_FIRST, P["hold_ratchet"][2], _fk), +1)
        rhs = rhs - zcyl(_pv[0], _pv[1], 6.1, rh - rt - 1, rh + 1)
    A("Frame centre member, 100 x 40 x 4 RHS", rhs, "steel_paint_blue", bom=9, key="frame")
    post = ztube(0, 0, po / 2, po / 2 - pw_, 0, ph)
    post = post - xcyl(0, D["z_keeper_pin"], P["keeper_pin"] / 2 + 0.25, -40, 40)
    A("Post, 60.3 x 5.0 tube", post, "steel_paint_blue", bom=9, key="frame")
    so, st, sl = P["stake_tube"]
    stake_pos = [(a_, b_) for a_ in (x0 + 40.0, x1 - 40.0) for b_ in (-1, 1)]
    stube = []
    for i, (sx, sg) in enumerate(stake_pos):
        t_ = ztube(sx, sg * (W / 2 + so / 2), so / 2, so / 2 - st, 0, sl)
        stube.append(t_)
        A(f"Stake tube {i + 1}, 33.7 x 3.2", t_, "steel_paint_blue", bom=9, key="frame")
    rx, rz, ro, rtw, rl = P["roller"]
    ct = P["cheek_t"]
    cheeks = []
    for sg in (-1, 1):
        y0 = rl / 2 + 1.0 if sg > 0 else -rl / 2 - 1.0 - ct
        ch = prism_xz(hull2d([(x0, 0), (x0, s + 20)] + circle_pts(rx, rz, 32, 24) + [(rx - 32, 0)]), y0, y0 + ct)
        ch = be(ch - ycyl(rx, rz, P["roller_pin"] / 2 + 0.25, y0 - 1, y0 + ct + 1), 1.0)
        cheeks.append((ch, y0))
        A(f"Roller cheek {'+Y' if sg > 0 else '-Y'}, 8 mm plate", ch, "steel_paint_blue", bom=9, key="frame")
    et, eh = P["eye"]
    ze = D["z_rope_out"]
    eye = prism_xz(hull2d([(x1, 0), (x1, s)] + circle_pts(x1 + 50, ze, 26, 24) + [(x1 + 50, 0)]), -et / 2, et / 2)
    eye = be(eye - ycyl(x1 + 50, ze, eh / 2, -et, et), 1.0)
    A("Anchor eye plate, 10 mm, 22 mm hole", eye, "steel_paint_blue", bom=9, key="frame")
    xc = x1 - s / 2
    for j, yc in enumerate((95.0, 155.0)):
        A(f"Tail cleat post {j + 1}, 12 mm bar", cp.break_edges(zcyl(xc, yc, 6.0, s, s + 32), 0.8), "steel_paint_blue", bom=9, key="frame")
    A("Tail cleat horn, 16 mm bar", cp.break_edges(rod((xc, 60.0, s + 40), (xc, 190.0, s + 40), 8.0), 1.0), "steel_paint_blue", bom=9, key="frame")
    R, r, n = P["hold_ratchet"][0] / 2, P["hold_ratchet"][1] / 2, P["hold_ratchet"][2]
    pt, pt_d = P["pawl_t"]
    hold_pivots = []
    zph = rh
    for k, face_k in enumerate((4, 16)):
        nose, pivot = pawl_points(R, r, n, face_angle(HOLD_FIRST, n, face_k), +1)
        hold_pivots.append((nose, pivot))
        pin = zcyl(pivot[0], pivot[1], 6.0, rh - rt - 6.0, rh + 23.5)
        pin = pin - xcyl(pivot[1], rh + 19.0, 1.2, pivot[0] - 20, pivot[0] + 20)
        A(f"Holding pawl pin {k + 1}, 12 mm bar", cp.break_edges(pin, 0.8), "mild_steel", bom=9, key="frame")

    wk = dict(kind="weld", key="frame")
    for nm, xs, ci in (("front", x0 + s / 2, 2), ("rear", x1 - s / 2, 3)):
        for sg in (-1, 1):
            yj = sg * (yr - s / 2)
            ya, yb_ = (yj - leg, yj) if sg > 0 else (yj, yj + leg)
            slab = bx(xs - s / 2 - leg, xs + s / 2 + leg, ya, yb_, 0.0, s + leg)
            wd = collar_weld(slab, [out[ci]["shape"], out[0 if sg < 0 else 1]["shape"]], 0.9)
            A(f"Weld, {nm} cross member to {'+Y' if sg > 0 else '-Y'} rail", wd, "mild_steel", **wk)
    for sg in (-1, 1):
        yj = sg * (yr - s / 2)
        ya, yb_ = (yj - leg, yj) if sg > 0 else (yj, yj + leg)
        slab = bx(-rw / 2 - leg, rw / 2 + leg, ya, yb_, 0, rh + leg)
        A(f"Weld, centre member to {'+Y' if sg > 0 else '-Y'} rail", collar_weld(slab, [rhs, out[0 if sg < 0 else 1]["shape"]], 0.9), "mild_steel", **wk)
    A("Weld, post to centre member, top face", ring_bead(0, 0, rh, po / 2, leg, up=True), "mild_steel", **wk)
    A("Weld, post to centre member, underside", ring_bead(0, 0, 0, po / 2, leg, up=False), "mild_steel", **wk)
    for k, (nose, pivot) in enumerate(hold_pivots):
        A(f"Weld, holding pawl pin {k + 1} to centre member (inside)", ring_bead(pivot[0], pivot[1], rh - rt, 6.0, 3.0, up=False), "mild_steel", **wk)
    for i, (sx, sg) in enumerate(stake_pos):
        ya, yb_ = (W / 2, W / 2 + 3.0) if sg > 0 else (-W / 2 - 3.0, -W / 2)
        slab = bx(sx - 12, sx + 12, ya, yb_, 6, sl - 6)
        A(f"Weld, stake tube {i + 1} to rail (stitch)", slab - stube[i] - out[0 if sg < 0 else 1]["shape"], "mild_steel", **wk)
    for (ch, y0), sg in zip(cheeks, (-1, 1)):
        slab = bx(x0 - leg, x0, y0, y0 + ct, 0, s + 20)
        A(f"Weld, roller cheek {'+Y' if sg > 0 else '-Y'} to front member", slab - ch - out[2]["shape"], "mild_steel", **wk)
    A("Weld, anchor eye to rear member", collar_weld(bx(x1, x1 + leg, -et / 2 - leg, et / 2 + leg, 0, s), [eye]), "mild_steel", **wk)
    for j, yc in enumerate((95.0, 155.0)):
        A(f"Weld, tail cleat post {j + 1} to rear member", ring_bead(xc, yc, s, 6.0, 3.0, up=True), "mild_steel", **wk)

    # ---- roller (BOM 16): tube, two end bushes, pin, R-clips
    rtube = ytube(rx, rz, ro / 2, ro / 2 - rtw, -rl / 2, rl / 2)
    A("Hold-down roller, 60.3 x 3.6 tube", rtube, "steel_paint_green", bom=16, key="roller")
    for sg in (-1, 1):
        y0, y1 = (-rl / 2, -rl / 2 + 15) if sg < 0 else (rl / 2 - 15, rl / 2)
        A(f"Roller end bush {'+Y' if sg > 0 else '-Y'}, acetal", ytube(rx, rz, ro / 2 - rtw - 0.1, P["roller_pin"] / 2 + 0.25, y0, y1),
          "acetal", bom=16, key="roller")
    pin = ycyl(rx, rz, P["roller_pin"] / 2, -rl / 2 - ct - 12, rl / 2 + ct + 12)
    for sg in (-1, 1):
        pin = pin - xcyl(sg * (rl / 2 + ct + 6), rz, 1.2, rx - 30, rx + 30)
    A("Roller pin, 20 mm bar", cp.break_edges(pin, 0.8), "mild_steel", bom=16, key="roller_pin")
    for sg in (-1, 1):
        cl_ = Pos(rx, sg * (rl / 2 + ct + 6), rz) * Rot(-90, 0, 0) * rclip(P["roller_pin"] / 2, "x")
        A(f"R-clip, roller pin {'+Y' if sg > 0 else '-Y'}", cl_, "zinc_plated", kind="fastener", key="roller_pin")

    # ---- bushes (BOM 15)
    zr0, zr1 = D["z_ring"]
    bk = dict(bom=15, key="bushes")
    A("Foot thrust washer, acetal 4 mm", ztube(0, 0, 50.0, 30.25, P["z_frame"], zr0), "acetal", **bk)
    A("Foot bush, acetal 12 mm", ztube(0, 0, 37.5, 30.25, zr0, D["z_disc0"][1]), "acetal", **bk)
    A("Spindle bush, acetal 58 mm", ztube(0, 0, P["spindle"][0] / 2 - P["spindle"][1] - 0.1, 30.25, D["z_spindle"][1] - 50, D["z_flange"][1]), "acetal", **bk)
    A("Head thrust washer, acetal 2 mm", ztube(0, 0, 44.0, 30.25, D["z_drive"][1], D["z_sleeve"][0]), "acetal", **bk)
    A("Head bush, acetal 80 mm", ztube(0, 0, P["sleeve"][0] / 2 - P["sleeve"][1] - 0.1, 30.25, *D["z_sleeve"]), "acetal", **bk)
    A("Top thrust washer, acetal 2 mm", ztube(0, 0, 44.0, 30.25, D["z_sleeve"][1], D["z_keeper"][0]), "acetal", **bk)

    # ---- drum weldment (BOM 10)
    so_, sw_ = P["spindle"]
    dk = dict(bom=10, key="drum")
    A("Holding ratchet ring, 24 teeth, 6 mm", ratchet_xy(zr0, P["ring_t"], R, r, n, HOLD_FIRST, 75.0, +1), "steel_paint_orange", **dk)
    A("Drum foot disc, 6 mm", be(ztube(0, 0, P["disc_d"] / 2, 37.5, *D["z_disc0"]), 1.0), "steel_paint_orange", **dk)
    A("Drum barrel, 114.3 x 3.6 tube", ztube(0, 0, P["barrel"][0] / 2, P["barrel"][0] / 2 - P["barrel"][1], *D["z_barrel"]), "steel_paint_orange", **dk)
    A("Drum top disc, 6 mm", be(ztube(0, 0, P["disc_d"] / 2, so_ / 2, *D["z_disc1"]), 1.0), "steel_paint_orange", **dk)
    A("Drum spindle, 76.1 x 3.2 tube", ztube(0, 0, so_ / 2, so_ / 2 - sw_, *D["z_spindle"]), "steel_paint_orange", **dk)
    sp_d, sp_r = P["shear_pin"]
    fl = ztube(0, 0, P["flange"][0] / 2, so_ / 2, *D["z_flange"]) - zcyl(-sp_r, 0, sp_d / 2 + 0.1, D["z_flange"][0] - 1, D["z_flange"][1] + 1)
    A("Drum top flange, 8 mm, shear pin hole", be(fl, 1.0), "steel_paint_orange", **dk)
    bo = P["barrel"][0] / 2
    A("Weld, barrel to foot disc", ring_bead(0, 0, D["z_barrel"][0], bo, 3.0, up=True), "mild_steel", kind="weld", key="drum")
    A("Weld, barrel to top disc", ring_bead(0, 0, D["z_barrel"][1], bo, 3.0, up=False), "mild_steel", kind="weld", key="drum")
    A("Weld, spindle to top disc", ring_bead(0, 0, D["z_disc1"][1], so_ / 2, 3.0, up=True), "mild_steel", kind="weld", key="drum")
    A("Weld, spindle to flange", ring_bead(0, 0, D["z_flange"][0], so_ / 2, 3.0, up=False), "mild_steel", kind="weld", key="drum")
    A("Weld, holding ring to foot disc (stitch)",
      (zcyl(0, 0, 40.0, zr0 - 3, zr0) - zcyl(0, 0, 37.5, zr0 - 4, zr0 + 1)), "mild_steel", kind="weld", key="drum")

    # ---- drive ratchet (BOM 11), shear pin (BOM 18), split pin
    dR, dr, dn, dt = P["drive_ratchet"]
    dz0 = D["z_drive"][0]
    dr_ = ratchet_xy(dz0, dt, dR / 2, dr / 2, dn, DRIVE_FIRST, po + 1.0, +1) - zcyl(-sp_r, 0, sp_d / 2 + 0.1, dz0 - 1, dz0 + dt + 1)
    A("Drive ratchet wheel, 20 teeth, 8 mm", dr_, "steel_paint_orange", bom=11, key="drive_ratchet")
    zp0, zp1 = D["z_flange"][0] - 8, dz0 + dt + 8
    spin = cp.break_edges(zcyl(-sp_r, 0, sp_d / 2, zp0, zp1), 0.4) - xcyl(0, zp0 + 4, 1.1, -sp_r - 10, -sp_r + 10)
    A("Shear pin, 6 mm S275, 32 mm", spin, "mild_steel", kind="bought", bom=18, key="shear_pin")
    sp = cp.split_pin(sp_d)
    A("Split pin, shear pin", Pos(-sp_r, 0, zp0 + 4) * sp, "zinc_plated", kind="fastener", key="shear_pin")

    # ---- lever head (BOM 12)
    zs0, zs1 = D["z_sleeve"]
    sr = P["sleeve"][0] / 2
    so2, sw2, sl2 = P["socket"]
    za, zb = D["z_socket"]
    A("Head sleeve, 88.9 x 5.0 tube", ztube(0, 0, sr, sr - P["sleeve"][1], zs0, zs1), "steel_paint_blue", bom=12, key="head")
    sleeve_out = zcyl(0, 0, sr, zs0 - 1, zs1 + 1)
    socks = []
    for sg in (-1, 1):
        ya, yb_ = (20.0, sr + sl2) if sg > 0 else (-(sr + sl2), -20.0)
        sock = Pos(0, ya, (za + zb) / 2) * Rot(-90, 0, 0) * cp.shs(so2, sw2, yb_ - ya)
        sock = sock - sleeve_out - zcyl(0, sg * (sr + 110.0), 6.6, za - 1, zb + 1)
        socks.append(sock)
        A(f"Bar socket {'+Y' if sg > 0 else '-Y'}, 50 x 50 x 3 SHS", sock, "steel_paint_blue", bom=12, key="head")
        slab = bx(-so2 / 2 - leg, so2 / 2 + leg, (sr - 1) if sg > 0 else -(sr + leg + 4), (sr + leg + 4) if sg > 0 else -(sr - 1), za - leg, zb + leg)
        A(f"Weld, socket {'+Y' if sg > 0 else '-Y'} to sleeve", collar_weld(slab, [sock, sleeve_out], 0.9), "mild_steel", **wk | {"key": "head"})
    nose_d, piv_d = pawl_points(dR / 2, dr / 2, dn, face_angle(DRIVE_FIRST, dn, 0), +1, pivot_dist=45.0)
    lug = prism_xy(hull2d(circle_pts(0, 0, sr - 1, 32) + circle_pts(piv_d[0], piv_d[1], 16, 24)), zs0, zs0 + 8) - zcyl(0, 0, sr + 0.0, zs0 - 1, zs0 + 9)
    A("Pawl bracket lug, 8 mm plate", be(lug, 0.8), "steel_paint_blue", bom=12, key="head")
    A("Weld, pawl bracket to sleeve", ring_bead(0, 0, zs0, sr, 0.0 + 3.0, up=False) if False else
      (zcyl(0, 0, sr + 3.0, zs0 + 8, zs0 + 11) - zcyl(0, 0, sr, zs0 + 7, zs0 + 12) - lug), "mild_steel", **wk | {"key": "head"})
    dpin = zcyl(piv_d[0], piv_d[1], 6.0, dz0 - 12, zs0) - xcyl(piv_d[1], dz0 - 9.0, 1.2, piv_d[0] - 20, piv_d[0] + 20)
    A("Drive pawl pin, 12 mm bar", cp.break_edges(dpin, 0.8), "mild_steel", bom=12, key="head")
    A("Weld, drive pawl pin to bracket", ring_bead(piv_d[0], piv_d[1], zs0, 6.0, 2.0, up=False), "mild_steel", **wk | {"key": "head"})

    # ---- pawls (BOM 13): profile cut, with washer, spring and R-clip on each pin
    pk = dict(bom=13, key="hold_pawls")
    for k, (nose, pivot) in enumerate(hold_pivots):
        A(f"Holding pawl {k + 1}, 10 mm plate", be(pawl_xy(nose, pivot, zph, pt), 0.8), "steel_paint_red", **pk)
        A(f"Pawl spring {k + 1}", ztube(pivot[0], pivot[1], 10.0, 6.5, zph + pt, zph + pt + 4), "zinc_plated", kind="bought", **pk)
        A(f"Washer 12, holding pawl {k + 1}", Pos(pivot[0], pivot[1], zph + pt + 4) * cp.washer(12), "zinc_plated", kind="fastener", key="hold_pawls")
        A(f"R-clip, holding pawl pin {k + 1}", Pos(pivot[0], pivot[1], rh + 19.0) * rclip(6.0, "x"), "zinc_plated", kind="fastener", key="hold_pawls")
    A("Drive pawl, 8 mm plate", be(pawl_xy(nose_d, piv_d, dz0, pt_d), 0.8), "steel_paint_red", bom=13, key="drive_pawl")
    A("Pawl spring, drive pawl", ztube(piv_d[0], piv_d[1], 10.0, 6.5, dz0 - 6.5, dz0 - 2.5), "zinc_plated", kind="bought", bom=13, key="drive_pawl")
    A("Washer 12, drive pawl", Pos(piv_d[0], piv_d[1], dz0 - 2.5) * cp.washer(12), "zinc_plated", kind="fastener", key="drive_pawl")
    A("R-clip, drive pawl pin", Pos(piv_d[0], piv_d[1], dz0 - 9.0) * rclip(6.0, "x"), "zinc_plated", kind="fastener", key="drive_pawl")

    # ---- bars (BOM 14)
    b, bw, bl = P["bar"]
    for sg in (-1, 1):
        yi = sr - 6 + 10.0
        ya, yb_ = (yi, yi + bl) if sg > 0 else (-(yi + bl), -yi)
        bar = Pos(0, ya, D["z_bar"]) * Rot(-90, 0, 0) * cp.shs(b, bw, bl)
        bar = bar - zcyl(0, sg * (sr + 110.0), 6.6, D["z_bar"] - 30, D["z_bar"] + 30)
        nm = '+Y' if sg > 0 else '-Y'
        A(f"Capstan bar {nm}, 40 x 40 x 2.5 SHS", bar, "steel_paint_blue", bom=14, key="bars")
        capl = Pos(0, 0, -7) * Box(b - 2 * bw - 4.0, b - 2 * bw - 4.0, 14) + Pos(0, 0, 1.5) * Box(b + 2, b + 2, 3)
        A(f"End cap {nm}, plastic", place(be(capl, 0.6), (0, yb_ if sg > 0 else ya, D["z_bar"]), (0, sg, 0)),
          "hdpe_black", kind="bought", bom=14, key="bars")
        pn = zcyl(0, sg * (sr + 110.0), 6.0, za - 8, zb + 8) - xcyl(sg * (sr + 110.0), zb + 4, 1.2, -20, 20)
        A(f"Bar pin {nm}, 12 mm bar", cp.break_edges(pn, 0.8), "mild_steel", bom=14, key="bar_pins")
        A(f"R-clip, bar pin {nm}", Pos(0, sg * (sr + 110.0), zb + 4) * rclip(6.0, "x"), "zinc_plated", kind="fastener", key="bar_pins")

    # ---- keeper (BOM 17)
    kd, kh = P["keeper"]
    A("Keeper collar, 80 OD x 61 bore x 20", be(ztube(0, 0, kd / 2, 30.5, *D["z_keeper"]), 0.8), "steel_paint_blue", bom=17, key="keeper")
    kp = xcyl(0, D["z_keeper_pin"], P["keeper_pin"] / 2, -48, 48) - ycyl(40.0, D["z_keeper_pin"], 1.2, -20, 20)
    A("Keeper pin, 10 mm bar, 96 mm", cp.break_edges(kp, 0.6), "mild_steel", bom=17, key="keeper")
    A("R-clip, keeper pin", Pos(40.0, 0, D["z_keeper_pin"]) * Rot(0, 90, 0) * rclip(5.0, "y"), "zinc_plated", kind="fastener", key="keeper")

    # ---- stakes (BOM 19)
    sd, slen, sdep = P["stake"]
    for i, (sx, sg) in enumerate([(a, b_) for a in (x0 + 40.0, x1 - 40.0) for b_ in (-1, 1)]):
        ys = sg * (W / 2 + so / 2)
        ztop = sl + 4.0
        stake = zcyl(sx, ys, sd / 2, ztop - slen + 40.0, ztop) + Pos(sx, ys, 0) * Solid.make_cone(0.5, sd / 2, 40.0, Plane(origin=(0, 0, ztop - slen), z_dir=(0, 0, 1)))
        A(f"Ground stake {i + 1}, 25 mm bar, pointed", stake, "mild_steel", bom=19, key="stakes")
        wsh = ztube(sx, ys, 22.0, sd / 2 + 0.2, sl, ztop)
        A(f"Stake head washer {i + 1}, 44 mm", wsh, "mild_steel", bom=19, key="stakes")
        A(f"Weld, stake head washer {i + 1}", ring_bead(sx, ys, ztop, sd / 2, 3.0, up=True) - zcyl(sx, ys, sd / 2, ztop - 1, ztop + 5), "mild_steel", kind="weld", key="stakes")
    return out


