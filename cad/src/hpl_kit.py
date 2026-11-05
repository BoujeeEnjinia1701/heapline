"""HeapLine search kit, part by part (kit 1.9, D3): reused crate refitted (search crate and capstan crate),
crawl boards with link plates, probes, shovels, sheet stretcher, sheet clamp, lookout marker wands. Each
builder returns cad_parts-style part dicts in the builder's own frame; model.py places them.
"""
from __future__ import annotations

import math

from hpl_parts import *  # noqa: F401,F403
import cad_parts as cp
from build123d import Pos, Rot, Torus, Cylinder, Box, Compound, Plane, Solid, Location


# ----------------------------------------------------------------------------- crates
def crate(P, which="box", open_lid=False, bom=(1, 2, 3), tag="Search crate", key="box"):
    """Boarded crate on skids with a skirted lid, centred on x = y = 0, ground at z = 0. The lid hinges about
    an axis along X behind the lid's skirt; open_lid swings it P['lid_open_deg'] about that axis."""
    L, W, H = P[which]
    t = P["ply"]
    sk_w, sk_h = P["skid"]
    g, sk = P["lid_gap"], P["skirt"]
    zb = sk_h
    ztop = zb + H
    b_body, b_lid, b_hw = bom
    pl = "plywood_painted"
    out = []
    A = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    Lo, Wo = L + 2 * (g + t), W + 2 * (g + t)
    zl = ztop + 3.0
    zh = ztop - 47.0                       # hinge axis height
    yh = Wo / 2 + 1.5 + 4.5                # hinge axis y: knuckle clear of the skirt
    hx = (-0.37 * L, 0.0, 0.37 * L)
    knuckle_cut = lambda: sum([xcyl(yh, zh, 6.4, x - 32, x + 32) for x in hx[1:]], xcyl(yh, zh, 6.4, hx[0] - 32, hx[0] + 32))  # noqa: E731

    floor = bx(-L / 2, L / 2, -W / 2, W / 2, zb, zb + t)
    A(f"{tag} floor, 18 mm plywood", be(floor, 1.5), pl, bom=b_body, key=key + "_body")
    for sg in (-1, 1):
        y0 = W / 2 - t if sg > 0 else -W / 2
        pn = bx(-L / 2, L / 2, y0, y0 + t, zb + t, ztop)
        if sg > 0:                         # hinge pads on the back, relief for the knuckles
            pass
        A(f"{tag} {'back' if sg > 0 else 'front'} panel, 18 mm plywood", be(pn, 1.5), pl, bom=b_body, key=key + "_body")
    for sg in (-1, 1):
        x0 = L / 2 - t if sg > 0 else -L / 2
        A(f"{tag} {'right' if sg > 0 else 'left'} end panel, 18 mm plywood", be(bx(x0, x0 + t, -W / 2 + t, W / 2 - t, zb + t, ztop), 1.5), pl, bom=b_body, key=key + "_body")
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * (L / 2 - t - 22.5), sy * (W / 2 - t - 22.5)
            A(f"{tag} corner batten {'R' if sx > 0 else 'L'}{'B' if sy > 0 else 'F'}, 45 x 45", be(bx(cx - 22.5, cx + 22.5, cy - 22.5, cy + 22.5, zb + t, ztop - 30), 1.0),
              "timber", bom=b_body, key=key + "_body")
    for sy in (-1, 1):
        yc = sy * (W / 2 - 120)
        A(f"{tag} skid {'B' if sy > 0 else 'F'}, 70 x 45", be(bx(-L / 2 + 40, L / 2 - 40, yc - sk_w / 2, yc + sk_w / 2, 0, sk_h), 2.0), "timber", bom=b_body, key=key + "_body")
    for sx in (-1, 1):
        x0 = L / 2 if sx > 0 else -L / 2 - 30
        A(f"{tag} handle cleat {'R' if sx > 0 else 'L'}, hardwood", be(bx(x0, x0 + 30, -150, 150, ztop - 160, ztop - 120), 2.0), "hardwood", bom=b_body, key=key + "_body")
        for sy in (-1, 1):
            xo = L / 2 + 30 + 6 if sx > 0 else -L / 2 - 30 - 6
            A(f"Rope handle {'R' if sx > 0 else 'L'}{'B' if sy > 0 else 'F'}, 12 mm rope", Pos(xo, sy * 75, ztop - 160 - 34) * Rot(0, 90, 0) * Torus(40, 6),
              "rope", kind="bought", bom=b_hw, key=key + "_hw")
    # hinge pads (back), hasp pad (front)
    pad_z0, pad_z1 = ztop - 110, ztop - 48
    for i, x in enumerate(hx):
        pad = bx(x - 40, x + 40, W / 2, Wo / 2, pad_z0, pad_z1) - xcyl(yh, zh, 6.4, x - 41, x + 41)
        A(f"{tag} hinge pad {i + 1}, 20 mm timber", be(pad, 1.0), "timber", bom=b_body, key=key + "_body")
    A(f"{tag} hasp pad, 20 mm timber", be(bx(-40, 40, -Wo / 2, -W / 2, pad_z0 - 10, pad_z1), 1.0), "timber", bom=b_body, key=key + "_body")

    # ---- lid
    lid_parts = []
    top = bx(-Lo / 2, Lo / 2, -Wo / 2, Wo / 2, zl, zl + t)
    lid_parts.append((f"{tag} lid top, 18 mm plywood", be(top, 1.5), pl))
    for sg in (-1, 1):
        y0 = Wo / 2 - t if sg > 0 else -Wo / 2
        strip = bx(-Lo / 2, Lo / 2, y0, y0 + t, zl - sk, zl)
        if sg > 0:
            strip = strip - knuckle_cut()
        lid_parts.append((f"{tag} lid skirt {'back' if sg > 0 else 'front'}, 48 mm", be(strip, 1.0), "timber"))
        x0 = Lo / 2 - t if sg > 0 else -Lo / 2
        lid_parts.append((f"{tag} lid skirt {'right' if sg > 0 else 'left'} end, 48 mm", be(bx(x0, x0 + t, -Wo / 2 + t, Wo / 2 - t, zl - sk, zl), 1.0), "timber"))
    seal = bx(-L / 2 + 4, L / 2 - 4, -W / 2 + 4, W / 2 - 4, ztop, ztop + 3) - bx(-L / 2 + 14, L / 2 - 14, -W / 2 + 14, W / 2 - 14, ztop - 1, ztop + 4)
    # the EPDM seal strip stays on the rim: it is part of the body hardware
    # lid hardware: hasp strap and the lid-side hinge leaves, drill card
    hasp = bx(-15, 15, -Wo / 2 - 3, -Wo / 2, ztop - 98, ztop + 2)
    card = bx(-min(500.0, L / 2 - 60), min(500.0, L / 2 - 60), -Wo / 2 + 180, Wo / 2 - 180, zl - 1.0, zl)

    zax, yax = zh, yh
    if open_lid:
        rot = lambda s_: Pos(0, yax, zax) * Rot(-P["lid_open_deg"], 0, 0) * Pos(0, -yax, -zax) * s_  # noqa: E731
    else:
        rot = lambda s_: s_  # noqa: E731
    for nm, sh, mat in lid_parts:
        A(nm, rot(sh), mat, bom=b_lid, key=key + "_lid")
    A(f"{tag} EPDM seal strip, 10 x 3", seal, "epdm", kind="bought", bom=b_hw, key=key + "_hw")

    # hinges: butt hinges (leaf 62 x 60) on the pads and the lid skirt
    open_deg = 180 - (P["lid_open_deg"] if open_lid else 0)
    for i, x in enumerate(hx):
        h, hp = cp.butt_hinge(60.0, 62.0, 3.0, 6.0, open_deg)
        loc = Plane(origin=(x - 30, yh, zh), z_dir=(1, 0, 0), x_dir=(0, 0, -1)).location
        A(f"Hinge {i + 1}, 62 mm leaves, galvanised", loc * h, "galvanised", kind="bought", bom=b_hw, key=key + "_hw")
        A(f"Hinge pin {i + 1}, 6 mm", loc * hp, "zinc_plated", kind="bought", bom=b_hw, key=key + "_hw")
    A(f"{tag} hasp strap, 30 x 3", be(hasp, 0.6), "galvanised", kind="bought", bom=b_hw, key=key + "_hw")
    st = xcyl(-Wo / 2 - 3 - 7, ztop - 100, 3.5, -22, 22) + zcyl(-22, -Wo / 2 - 3 - 7, 3.5, ztop - 100, ztop - 80) + zcyl(22, -Wo / 2 - 3 - 7, 3.5, ztop - 100, ztop - 80)
    A("Staple, 7 mm rod", st, "galvanised", kind="bought", bom=b_hw, key=key + "_hw")
    A("Combination padlock, shrouded", Pos(0, -Wo / 2 - 3 - 7, ztop - 118) * (be(Box(48, 20, 36), 3.0) + Pos(0, 0, 18) * Rot(90, 0, 0) * Torus(11, 3.0)),
      "brass", kind="bought", bom=b_hw, key=key + "_hw")
    if open_lid:
        # folding lid stay: two rods from a bracket on the body end to a bracket on the lid end, pinned at the knee
        xs_ = L / 2 + 30.0
        lo_p = (xs_, -W / 2 + 250.0, ztop - 80.0)
        lid_pt = (xs_, -Wo / 2 + 250.0, zl - 24.0)
        th = math.radians(-P["lid_open_deg"])
        dy, dz = lid_pt[1] - yax, lid_pt[2] - zax
        up_p = (lid_pt[0], yax + dy * math.cos(th) - dz * math.sin(th), zax + dy * math.sin(th) + dz * math.cos(th))
        knee = ((lo_p[0] + up_p[0]) / 2 + 22.0, (lo_p[1] + up_p[1]) / 2, (lo_p[2] + up_p[2]) / 2)
        A(f"{tag} stay bracket, body, 40 x 30 timber", be(bx(L / 2, L / 2 + 40, lo_p[1] - 15, lo_p[1] + 15, lo_p[2] - 20, lo_p[2] + 20), 1.0), "timber", bom=b_body, key=key + "_body")
        A(f"{tag} stay bracket, lid, 40 x 30 timber", rot(be(bx(L / 2 + 20, L / 2 + 60, lid_pt[1] - 15, lid_pt[1] + 15, lid_pt[2] - 20, lid_pt[2] + 20), 1.0)), "timber", bom=b_lid, key=key + "_lid")
        A("Lid stay lower arm, 8 mm bar", rod(lo_p, knee, 4.0), "galvanised", kind="bought", bom=b_hw, key=key + "_hw")
        A("Lid stay upper arm, 8 mm bar", rod(knee, up_p, 4.0), "galvanised", kind="bought", bom=b_hw, key=key + "_hw")
    A(f"{tag} drill card, printed vinyl", rot(card), "label", kind="bought", bom=27 if which == "box" else b_hw, key=key + "_hw")
    # fixings, as groups of identical screws
    n_ = int(L // 150)
    xs_ = [-L / 2 + 75 + 150 * k for k in range(n_)]
    A(f"{tag} screws, side panels to floor (5 x 60)",
      Compound([Pos(x, sy * (W / 2 - t / 2), zb + t) * wood_screw(5, 40) for x in xs_ for sy in (-1, 1)]),
      "zinc_plated", kind="fastener", key=key + "_body")
    for i, x in enumerate(hx):
        hs = [(x + dx, Wo / 2 + 3.5, zh + dz) for dx in (-24, 24) for dz in (-45, -25)]
        A(f"Screws, hinge {i + 1} to pad (4.5 x 20)", screws3(hs, 4.5, 20, (0, 1, 0), x_dir=(1, 0, 0)), "zinc_plated", kind="fastener", key=key + "_hw")
    return out


# ----------------------------------------------------------------------------- crawl boards
def board_parts(P, tag="Board 1"):
    """One crawl board centred at the origin, length along X, batten feet at z = 0 (BOM 4)."""
    L, W, t = P["board"]
    bw, bd, inset = P["batten"]
    yb = W / 2 - inset - bw / 2
    lw, lt, ll, lp, lpl, lh = P["link"]
    sw, sh, se = P["hand_slot"]
    out = []
    deck = bx(-L / 2, L / 2, -W / 2, W / 2, bd, bd + t)
    for sx in (-1, 1):
        deck = deck - slot_cut(sx * (L / 2 - se - sh / 2), 0, sw, sh, bd - 1, bd + t + 1, along="y")
    for sx in (-1, 1):
        for y in (-yb, yb):
            deck = deck - zcyl(sx * (L / 2 - lh), y, lp / 2 + 0.5, bd - 1, bd + t + 1)
    out.append(part(f"{tag} deck, 15 mm plywood", be(deck, 1.2), "plywood", bom=4, key="board"))
    for i, y in enumerate((-yb, yb)):
        bat = bx(-L / 2, L / 2, y - bw / 2, y + bw / 2, 0, bd)
        for sx in (-1, 1):
            bat = bat - zcyl(sx * (L / 2 - lh), y, lp / 2 + 0.5, -1, bd + 1)
        out.append(part(f"{tag} batten {i + 1}, 45 x 70", be(bat, 1.5), "timber", bom=4, key="board"))
    pts = []
    for y in (-yb, yb):
        for k in range(9):
            pts.append((-600.0 + k * 150, y + (bw / 4 if k % 2 else -bw / 4)))
    out.append(part(f"{tag} screws, deck to battens (5 x 60)", Compound([Pos(x, y, bd + t - 2.75) * wood_screw(5, 60) for x, y in pts]),
                    "zinc_plated", kind="fastener", key="board"))
    return out


def link_plate_part(P, name="Board link plate", x_joint=0.0, y=0.0):
    L, W, t = P["board"]
    bw, bd, inset = P["batten"]
    lw, lt, ll, lp, lpl, lh = P["link"]
    ztop = bd + t
    pl = bx(x_joint - ll / 2, x_joint + ll / 2, y - lw / 2, y + lw / 2, ztop, ztop + lt)
    for xp in (x_joint - lh, x_joint + lh):
        pl = pl + zcyl(xp, y, lp / 2, ztop - lpl, ztop + lt)
    return part(name, be(pl, 0.7), "galvanised", bom=5, key="link")


# ----------------------------------------------------------------------------- probe
def probe_parts(P, tag="Probe 1"):
    """One probe standing on its tip at z = 0, axis on z at x = y = 0 (BOM 6 and 7)."""
    td, tw, tl, n = P["probe_tube"]
    dt, cone, par, spg = P["probe_tip"]
    sd, sl = P["probe_spigot"]
    pd = P["probe_pin"]
    ri = td / 2 - tw
    out = []
    z_t0 = cone + par
    tip = Solid.make_cone(3.0, dt / 2, cone, Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))) + zcyl(0, 0, dt / 2, cone, z_t0) + zcyl(0, 0, ri - 0.1, z_t0, z_t0 + spg)
    out.append(part(f"{tag} tip, 18 mm bar", be(tip, 0.4), "mild_steel", bom=6, key="probe_tip_section"))
    nm = ("lower", "middle", "upper")
    ho, hw, hl = P["probe_handle"]
    for k in range(n):
        z0 = z_t0 + k * tl
        top_z = z0 + tl
        tube = ztube(0, 0, td / 2, ri, z0, top_z)
        if k == n - 1:                       # T handle saddled onto the top of the tube
            zt = top_z + ho / 2 - 2.0
            handle_out = xcyl(0, zt, ho / 2, -hl / 2, hl / 2)
            tube = tube + zcyl(0, 0, td / 2, top_z, zt) - zcyl(0, 0, ri, top_z - 1, zt + 1)
            tube = tube - handle_out
        if k >= 1:
            tube = tube - ycyl(0, z0 + 30.0, pd / 2 + 0.2, -td, td)
        out.append(part(f"{tag} {nm[k]} tube, 16 x 2.0", tube, "mild_steel", bom=6, key=("probe_tip_section", "probe_mid_section", "probe_top_section")[k]))
        if k < n - 1:
            spig = zcyl(0, 0, sd / 2, top_z - sl / 2, top_z + sl / 2)
            spig = spig - ycyl(0, top_z + 30.0, pd / 2 + 0.2, -td, td)
            out.append(part(f"{tag} spigot {k + 1}, 11.5 mm bar", be(spig, 0.4), "mild_steel", bom=6, key=("probe_tip_section", "probe_mid_section")[k]))
            pin = ycyl(0, top_z + 30.0, pd / 2, -td / 2 - 6, td / 2 + 6)
            out.append(part(f"{tag} joint pin {k + 1}, 5 mm", be(pin, 0.4), "zinc_plated", kind="bought", bom=7, key="probe_pins"))
            clip = Pos(0, td / 2 + 3.0, top_z + 30.0) * Rot(0, 0, 0) * Rot(90, 0, 0) * Torus(pd / 2 + 1.2, 0.9)
            out.append(part(f"{tag} R-clip {k + 1}", clip, "zinc_plated", kind="fastener", key="probe_pins"))
    # the handle
    zt = z_t0 + n * tl + ho / 2 - 2.0
    out.append(part(f"{tag} T handle, 26.9 x 2.6 tube", xtube(0, zt, ho / 2, ho / 2 - hw, -hl / 2, hl / 2), "mild_steel", bom=6, key="probe_top_section"))
    zt_top = z_t0 + n * tl
    wh = zcyl(0, 0, td / 2 + 3.0, zt_top - 2.0, zt_top + 8.0) - xcyl(0, zt, ho / 2, -hl / 2, hl / 2) - zcyl(0, 0, td / 2, zt_top - 3, zt_top + 30)
    out.append(part(f"{tag} weld, handle to tube", wh, "mild_steel", kind="weld", key="probe_top_section"))
    out.append(part(f"{tag} weld, tip to tube", ring_bead(0, 0, z_t0, td / 2, 1.0, up=True), "mild_steel", kind="weld", key="probe_tip_section"))
    return out


# ----------------------------------------------------------------------------- shovel (bought, BOM 8)
def shovel_parts(P, tag="Shovel 1"):
    """Round-point shovel lying on its back, blade toward -X, centred on its length."""
    bw, bl, L = P["shovel"]
    blade = prism_xy([(-L / 2, 0), (-L / 2 + 60, -bw / 2), (-L / 2 + bl, -bw / 2), (-L / 2 + bl, bw / 2), (-L / 2 + 60, bw / 2)], 0, 2.0)
    blade = be(blade, 0.6)
    sock = Pos(-L / 2 + bl - 60, 0, 22) * Rot(0, 90, 0) * cp.round_tube(40, 3, 150)
    handle = Pos(-L / 2 + bl + 90, 0, 22) * Rot(0, 90, 0) * cp.round_bar(34, L - bl - 90, 2.0)
    return [part(f"{tag} blade, steel", blade, "mild_steel", kind="bought", bom=8, key="shovel"),
            part(f"{tag} socket, 40 x 3 tube", sock, "mild_steel", kind="bought", bom=8, key="shovel"),
            part(f"{tag} handle, 34 mm fibreglass", handle, "fibreglass", kind="bought", bom=8, key="shovel")]


# ----------------------------------------------------------------------------- stretcher (BOM 23)
def stretcher_parts(P):
    L, W, t = P["sheet"]
    sl, sw, se = P["sheet_slot"]
    out = []
    sh = extrude(Sketch() + RectangleRounded(L, W, 50.0), t)
    for k in range(6):
        cx = -L / 2 + 250 + k * (L - 500) / 5
        for sg in (-1, 1):
            sh = sh - slot_cut(cx, sg * (W / 2 - se - sw / 2), sl, sw, -1, t + 1, along="x")
    out.append(part("Stretcher sheet, 2 mm HDPE", sh, "hdpe_yellow", bom=23, key="sheet"))
    zs = t
    for i, cx in enumerate((-550.0, 0.0, 550.0)):
        w_ = bx(cx - P["strap_w"] / 2, cx + P["strap_w"] / 2, -W / 2 + 40, W / 2 - 40, zs, zs + 2)
        out.append(part(f"Stretcher strap {i + 1}, 50 mm webbing", w_, "webbing", kind="bought", bom=23, key="straps"))
        buck = be(bx(cx - 30, cx + 30, W / 2 - 160, W / 2 - 110, zs + 2, zs + 8), 1.0) - bx(cx - 20, cx + 20, W / 2 - 150, W / 2 - 120, zs + 2.5, zs + 9)
        out.append(part(f"Cam buckle {i + 1}, acetal", buck, "acetal", kind="bought", bom=23, key="straps"))
        riv = Compound([Pos(cx + dx, y, zs + 2.75) * Cylinder(4.0, 1.5) for dx in (-15, 15) for y in (-W / 2 + 60, W / 2 - 60)])
        out.append(part(f"Rivets, strap {i + 1} (4)", riv, "zinc_plated", kind="fastener", key="straps"))
    out.append(part("Head haul strap, 50 mm webbing", bx(L / 2 - 80, L / 2 - 30, -W / 2 + 120, W / 2 - 120, zs, zs + 2), "webbing", kind="bought", bom=23, key="straps"))
    return out


# ----------------------------------------------------------------------------- sheet clamp (BOM 22)
def clamp_parts(P):
    w, t, L = P["clamp"]
    g = P["clamp_gap"]
    xs = [s * x for x in P["clamp_bolts"] for s in (-1, 1)]
    out = []
    lower = bx(-L / 2, L / 2, -w / 2, w / 2, 0, t)
    upper = bx(-L / 2, L / 2, -w / 2, w / 2, t + g, 2 * t + g)
    for x in xs:
        lower = lower - zcyl(x, 0, 6.5, -1, t + 1)
        upper = upper - zcyl(x, 0, 6.5, t + g - 1, 2 * t + g + 1)
    out.append(part("Clamp lower flat, 50 x 8 x 600", be(lower, 1.0), "steel_paint_blue", bom=22, key="clamp_bars"))
    out.append(part("Clamp upper flat, 50 x 8 x 600", be(upper, 1.0), "steel_paint_blue", bom=22, key="clamp_bars"))
    ztop = 2 * t + g
    lug = prism_xz(hull2d([(-45, ztop), (45, ztop)] + circle_pts(0, ztop + 45, 28, 24)), -5, 5) - ycyl(0, ztop + 45, 11.0, -6, 6)
    out.append(part("Clamp lug, 10 mm plate", be(lug, 1.0), "steel_paint_blue", bom=22, key="clamp_bars"))
    out.append(part("Weld, clamp lug to upper flat (2 beads)", weld_bead((-45, -5, ztop), (45, -5, ztop), (0, -1, 0), (0, 0, 1), 3.0) +
                    weld_bead((-45, 5, ztop), (45, 5, ztop), (0, 1, 0), (0, 0, 1), 3.0), "mild_steel", kind="weld", key="clamp_bars"))
    for i, x in enumerate(xs):
        hb = cp.hex_bolt(12, 60)
        out.append(part(f"M12 x 60 bolt {i + 1} (ISO 4017)", Pos(x, 0, -2.5) * Rot(180, 0, 0) * hb, "zinc_plated", kind="fastener", key="clamp_bolts"))
        out.append(part(f"M12 washer under head {i + 1}", Pos(x, 0, 0) * Rot(180, 0, 0) * cp.washer(12), "zinc_plated", kind="fastener", key="clamp_bolts"))
        out.append(part(f"M12 washer under wing nut {i + 1}", Pos(x, 0, ztop) * cp.washer(12), "zinc_plated", kind="fastener", key="clamp_bolts"))
        out.append(part(f"M12 wing nut {i + 1}", Pos(x, 0, ztop + 2.5) * wing_nut(12), "zinc_plated", kind="bought", bom=22, key="clamp_bolts"))
    return out


# ----------------------------------------------------------------------------- lookout kit (BOM 24)
def wand_parts(P, pts):
    out = []
    for i, (x, y) in enumerate(pts):
        out.append(part(f"Marker wand {i + 1}, 8 mm fibreglass", be(zcyl(x, y, 4.0, -200, 1000), 0.8), "fibreglass", kind="bought", bom=24, key="wands"))
        out.append(part(f"Wand flag {i + 1}", bx(x + 4, x + 154, y - 0.75, y + 0.75, 850, 1000), "safety_red", kind="bought", bom=24, key="wands"))
    return out
