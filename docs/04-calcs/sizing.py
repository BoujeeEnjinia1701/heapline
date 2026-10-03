"""HeapLine sizing calculations (HPL-CAL-001), TRL 3.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every figure quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on, and
writes docs/04-calcs/results.csv (one row per requirement). Geometry and masses come from
cad/src/model.py (PARAMS, derived(), masses()); costs from bom/bom.csv; the value-engineering
target from project.yaml. First-principles estimates for a paper proof of concept, not test results.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src")]
from model import PARAMS as P, derived, masses  # noqa: E402

D = derived(P)
M = masses(P)
g = 9.81
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    print(line)
    OUT.append(line)


# ------------------------------------------------------------------ assumptions
A = dict(
    mu_bush=0.15,            # acetal on painted steel post, dry or dusty
    mu_rope=0.20,            # polyester rope on a painted steel drum (low side)
    turns=4,                 # rope turns on the drum while hauling
    tau_pin=258e6,           # Pa, ultimate shear strength of S275 bar (0.6 x 430 MPa)
    pin_scatter=0.20,        # +- spread of shear pin release over a batch
    design_T=8000.0,         # N, all capstan parts sized on this rope tension (above the pin's upper bound)
    push_sustained=150.0,    # N, sustained push or pull per person on a bar, short bouts
    stroke_deg=90.0, strokes_per_min=15.0,
    # probe penetration in loosened slide debris of mixed waste (no direct data: wide ranges)
    qc_central=0.40e6, fs_central=1.0e3,     # Pa, cone resistance and sleeve friction, central case
    qc_stiff=1.0e6, fs_stiff=3.0e3,          # Pa, stiffer, more compact debris
    push_one=350.0, push_two=650.0,          # N, sustained downward push by one or two people on the T handle
    # crawl board
    m_person=100.0, dyn=1.5, k_debris=0.10e6,   # kg; dynamic factor; N/m^3 subgrade modulus (very loose, low side)
    void_span=0.80,          # m, void the board must bridge
    f_timber=16e6, E_timber=8.0e9,           # Pa, C16 bending strength and modulus
    f_ply=20e6, knee_w=0.15,                 # Pa; m, width of deck taking a knee load
    # stretcher
    m_casualty=100.0, mu_debris=0.50, mu_boards=0.30, slope_deg=15.0,
    haul_sustained=200.0,    # N, sustained pull per hauler on a strap over a short distance
    # sheet clamp
    bolt_preload=2.5e3, mu_sheet=0.30,
    # carrying and deployment
    carry_limit=25.0,        # kg per person for a 100 m carry over rough ground
    run_mps=2.5, carry_mps=0.8, open_s=30.0, boards_s=60.0, probe_assemble_s=30.0, lookout_s=20.0,
    distance=100.0,
)

# ------------------------------------------------------------------ A. capstan
r = D["r_rope"] / 1000
r_b = (P["post"][0] / 2) / 1000
f_bush = A["mu_bush"] * r_b           # friction torque per newton of rope tension (foot bush carries it)
T_req = 5000.0
M_req = T_req * (r + f_bush)
r_grip = D["r_grip"] / 1000
F_end = M_req / 2 / r_grip            # two bar ends, one bar on each side
say("A1", f"Rope centre radius on the drum {r * 1000:.1f} mm; bush friction adds {f_bush * 1000:.1f} mm of lever per newton")
say("A2", f"5,000 N rope pull needs {M_req:.0f} N m at the head: {F_end:.0f} N at each bar end ({F_end / 2:.0f} N each with "
          f"two people per end, four in all; {F_end:.0f} N each with one per end), hands {r_grip * 1000:.0f} mm from the axis")
tail = T_req / math.exp(A["mu_rope"] * A["turns"] * 2 * math.pi)
say("A3", f"Tailer holds {tail:.0f} N on the tail with {A['turns']} turns at a friction coefficient of {A['mu_rope']}")
pd, pr = P["shear_pin"]
F_pin = A["tau_pin"] * math.pi * (pd / 1000) ** 2 / 4
M_pin = F_pin * pr / 1000
T_rel = M_pin / (r + f_bush)
T_lo, T_hi = T_rel * (1 - A["pin_scatter"]), T_rel * (1 + A["pin_scatter"])
say("A4", f"Shear pin {pd:.0f} mm S275 on a {pr:.0f} mm radius releases at {F_pin / 1000:.2f} kN, {M_pin:.0f} N m: rope tension "
          f"{T_rel:.0f} N ({T_lo:.0f} to {T_hi:.0f} N over a +-{A['pin_scatter'] * 100:.0f} % batch spread)")
mbs_spliced = P["rope_mbs"] * 0.9
say("A5", f"Rope 14 mm, {P['rope_mbs'] / 1000:.0f} kN, {mbs_spliced / 1000:.0f} kN through the splice: factor {mbs_spliced / T_req:.1f} "
          f"at 5,000 N and {mbs_spliced / A['design_T']:.1f} at the {A['design_T']:.0f} N design tension")
# post bending at the centre member: rope at mid wraps about 130 mm up, member top 40 mm
z_rope = 130.0
th = math.atan((z_rope - D["z_rope_out"]) / (abs(P["roller"][0]) - D["r_rope"]))
Hx = A["design_T"] * math.cos(th)
Mpost = Hx * (z_rope - P["z_frame"]) / 1000          # N m
do, wt = P["post"][0], P["post"][1]
I_post = math.pi * (do ** 4 - (do - 2 * wt) ** 4) / 64
Z_post = I_post / (do / 2)
say("A6", f"Rope leaves the drum {math.degrees(th):.0f} deg down to the hold-down roller; post moment {Mpost / 1000:.2f} kN m at "
          f"{A['design_T']:.0f} N; 60.3 x 5.0 tube Z = {Z_post:.0f} mm3: {Mpost * 1000 / Z_post:.0f} MPa (S355 yield 355)")
# ratchets: holding ring tooth and drive ratchet tooth
Rh, rh, nh = P["hold_ratchet"]
M_des = A["design_T"] * (r + f_bush)
F_hold = M_des / ((Rh + rh) / 4000)
hh = (Rh - rh) / 2
say("A7", f"Holding pawl force {F_hold / 1000:.1f} kN at the design tension (one pawl taking it all): tooth face "
          f"{hh:.0f} x {P['ring_t']:.0f} mm, bearing {F_hold / (hh * P['ring_t']):.0f} MPa; pawl pin 12 mm single shear "
          f"{F_hold / (math.pi * 36):.0f} MPa")
Rd, rd, nd, td = P["drive_ratchet"]
F_drive = M_pin / ((Rd + rd) / 4000)
say("A8", f"Drive pawl force at pin release {F_drive / 1000:.1f} kN: tooth face {(Rd - rd) / 2:.0f} x {td:.0f} mm, bearing "
          f"{F_drive / ((Rd - rd) / 2 * td):.0f} MPa")
b, bw, bl = P["bar"]
I_bar = (b ** 4 - (b - 2 * bw) ** 4) / 12
Z_bar = I_bar / (b / 2)
M_bar = M_pin / 2
say("A9", f"Bar 40 x 40 x 2.5: Z = {Z_bar:.0f} mm3; at pin release each bar carries {M_bar:.0f} N m at the socket: "
          f"{M_bar * 1000 / Z_bar:.0f} MPa")
rate = r * math.radians(A["stroke_deg"]) * A["strokes_per_min"]
say("A10", f"Quarter-turn strokes: {r * math.radians(A['stroke_deg']) * 1000:.0f} mm of rope a stroke; about {rate:.1f} m/min at "
           f"{A['strokes_per_min']:.0f} strokes a minute")
say("A11", f"Rope leaves under the roller at {D['z_rope_out']:.0f} mm and the sling pulls from the eye at the same height: no "
           f"overturning moment; stakes only resist turning and skating")
F_eye = A["design_T"] / (19 * P["eye"][0])
say("A12", f"Anchor eye 10 mm plate, 22 mm hole: shackle pin bearing {F_eye:.0f} MPa at {A['design_T']:.0f} N; round sling "
           f"WLL 19.6 kN, factor {19.6e3 / A['design_T']:.1f} on WLL at the design tension")

# ------------------------------------------------------------------ B. probe
td_, tw_, tl_, n_ = P["probe_tube"]
dt_ = P["probe_tip"][0]
A_tip = math.pi * (dt_ / 1000) ** 2 / 4
per_m = math.pi * td_ / 1000
I_p = math.pi * (td_ ** 4 - (td_ - 2 * tw_) ** 4) / 64
E = 210e3
usable = (D["probe_len"] - 500) / 1000            # m, with the handle at chest height above the surface


def pcr(free_m):
    return math.pi ** 2 * E * I_p / (free_m * 1000) ** 2


def reach_depth(qc, fs, push):
    """Deepest point where the push needed is within both the people's push and the probe's buckling load."""
    d = 0.0
    while d < usable:
        need = qc * A_tip + fs * per_m * d
        if need > min(push, pcr(D["probe_len"] / 1000 - d)):
            return d
        d += 0.01
    return usable


reach = {}
for case in ("central", "stiff"):
    qc, fs = A[f"qc_{case}"], A[f"fs_{case}"]
    tipF = qc * A_tip
    for who in ("one", "two"):
        reach[(case, who)] = reach_depth(qc, fs, A[f"push_{who}"])
    F25 = tipF + fs * per_m * 2.5
    say(f"B1{case[0]}", f"{case.capitalize()} debris (cone {qc / 1e6:.1f} MPa, sleeve {fs / 1e3:.0f} kPa): tip {tipF:.0f} N, "
                        f"friction {fs * per_m:.0f} N/m; {F25:.0f} N to push to 2.5 m; reach {reach[(case, 'one')]:.1f} m "
                        f"for one person and {reach[(case, 'two')]:.1f} m for two (push capped at the probe's buckling load)")
# options for R2 (decision for Amish): a smaller 18 mm tip, with one or two people
A_tip0 = A_tip
A_tip = math.pi * 0.018 ** 2 / 4
opt18 = {(c, w): reach_depth(A[f"qc_{c}"], A[f"fs_{c}"], A[f"push_{w}"]) for c in ("central", "stiff") for w in ("one", "two")}
A_tip = A_tip0
say("B4", f"Option, 18 mm tip: stiff debris reach {opt18[('stiff', 'one')]:.1f} m for one person, {opt18[('stiff', 'two')]:.1f} m for two; "
          f"central {opt18[('central', 'one')]:.1f} m for one")
for Lp in (1.0, 2.0, 3.0):
    Pcr = math.pi ** 2 * E * I_p / (Lp * 1000) ** 2
    say(f"B2-{Lp:.0f}", f"Probe tube 16 x 2.0 buckling, {Lp:.0f} m free, pinned ends: {Pcr:.0f} N")
say("B3", f"Probe {D['probe_len']:.0f} mm assembled, {M['probe']:.2f} kg; tip 22 mm with a 3 mm rounded point; usable depth about "
          f"{usable:.1f} m with the handle at chest height above the surface")

# ------------------------------------------------------------------ C. crawl board
Lb, Wb, tb = P["board"]
bwt, bdt, _ = P["batten"]
Wt = (A["m_person"] * A["dyn"] + M["board"]) * g
area = (Wb / 1000) * 0.8
p_b = Wt / area
sink = p_b / A["k_debris"]
say("C1", f"Kneeling searcher {A['m_person']:.0f} kg x {A['dyn']} dynamic plus a {M['board']:.1f} kg board on 0.8 m of board: "
          f"{p_b / 1000:.1f} kPa; sinkage {sink * 1000:.0f} mm on very loose debris (subgrade modulus {A['k_debris'] / 1e6:.2f} MN/m3)")
Pv = A["m_person"] * A["dyn"] * g
Mv = Pv * A["void_span"] / 4
I_b = 2 * bwt * bdt ** 3 / 12
sig = Mv * 1000 * (bdt / 2) / I_b
defl = Pv * (A["void_span"] * 1000) ** 3 / (48 * A["E_timber"] / 1e6 * I_b)
say("C2", f"Bridging a {A['void_span']:.1f} m void with {Pv:.0f} N at mid-span: {Mv:.0f} N m; battens alone {sig:.1f} MPa "
          f"(C16 {A['f_timber'] / 1e6:.0f} MPa, factor {A['f_timber'] / 1e6 / sig:.1f}); deflection {defl:.1f} mm")
span = 2 * (Wb / 2 - P["batten"][2] - bwt)
Mk = 1000.0 * span / 1000 / 4
Zk = A["knee_w"] * 1000 * tb ** 2 / 6
say("C3", f"Deck between battens: {span:.0f} mm clear; a 1,000 N knee load on {A['knee_w'] * 1000:.0f} mm of deck gives "
          f"{Mk * 1000 / Zk:.1f} MPa in 15 mm plywood (about {A['f_ply'] / 1e6:.0f} MPa allowed)")
say("C4", f"Board {M['board']:.1f} kg; link plate {M['link']:.2f} kg; two 12 mm pins per side of a joint carry a sliding board easily")

# ------------------------------------------------------------------ D. stretcher
Wc = (A["m_casualty"] + M["stretcher"]) * g
s = math.radians(A["slope_deg"])
cases = {}
for nm, mu in (("debris", A["mu_debris"]), ("boards", A["mu_boards"])):
    for sl, ang in (("level", 0.0), ("15 deg up", s)):
        F = Wc * (mu * math.cos(ang) + math.sin(ang))
        cases[(nm, sl)] = F
        say(f"D-{nm}-{sl[:2]}", f"Stretcher on {nm}, {sl}: {F:.0f} N; {F / 2:.0f} N each for two haulers, {F / 4:.0f} N each for four")

# ------------------------------------------------------------------ E. sheet clamp
F_clamp = 4 * A["bolt_preload"] * A["mu_sheet"] * 2
say("E1", f"Sheet clamp: four M12 wing bolts at {A['bolt_preload'] / 1000:.1f} kN each, two faces at {A['mu_sheet']}: holds about "
          f"{F_clamp / 1000:.1f} kN before the sheet slips (below the pin's nominal release; a slipping sheet is safe)")

# ------------------------------------------------------------------ F. masses and carrying
bought = {"shovels": 4 * 2.3, "rope": P["rope_len"] * 0.135, "slings and shackles": 3.0, "mallet": 1.8,
          "lookout kit": 3.0, "lighting": 1.5, "PPE": 6.5, "bags and cards": 2.5}
cap_body = M["frame"] + M["roller"] + M["roller_pin"]
cap_drum = M["drum"] + M["bushes"] + M["drive_ratchet"] + M["shear_pin"] + M["head"] + M["drive_pawl"] + M["keeper"] + M["hold_pawls"]
items = {"Capstan frame with post and roller": cap_body, "Capstan drum, head and ratchet": cap_drum,
         "Capstan bars (2)": M["bars"] + M["bar_pins"], "Stakes and mallet": M["stakes"] + bought["mallet"],
         "Rope (30 m)": bought["rope"], "Slings, shackles and sheet clamp": bought["slings and shackles"] + M["clamp"],
         "Crawl board (each)": M["board"], "Board link plates (8)": 8 * M["link"], "Probes (6)": 6 * M["probe"],
         "Shovels (4)": bought["shovels"], "Sheet stretcher": M["stretcher"], "Lookout kit": bought["lookout kit"],
         "Lighting": bought["lighting"], "PPE": bought["PPE"], "Bags and cards": bought["bags and cards"]}
heaviest = max((v, k) for k, v in items.items())
wave1 = 4 * M["board"] + 8 * M["link"] + 6 * M["probe"] + bought["shovels"] + bought["lookout kit"] + bought["lighting"] + bought["PPE"] + M["stretcher"] + 1.0
wave2 = cap_body + cap_drum + M["bars"] + M["bar_pins"] + M["stakes"] + bought["mallet"] + bought["rope"] + bought["slings and shackles"] + M["clamp"] + 1.5
total = wave1 + wave2
for k, v in items.items():
    say("F-" + re.sub(r"[^a-z]", "", k.lower())[:12], f"{k}: {v:.1f} kg")
say("F1", f"Heaviest single carried item: {heaviest[1].lower()} at {heaviest[0]:.1f} kg; site box {M['box_body']:.0f} kg body and "
          f"{M['box_lid']:.0f} kg lid (stays at the shed)")
say("F2", f"Carried kit {total:.0f} kg: search wave (boards, probes, shovels, stretcher, lookout kit, lights, PPE) {wave1:.0f} kg, "
          f"capstan wave {wave2:.0f} kg; {total / 4:.1f} kg each if four carry it all at once, {wave1 / 4:.1f} kg each for the "
          f"search wave alone")
t_run = A["distance"] / A["run_mps"]
t_carry = A["distance"] / A["carry_mps"]
t_total = t_run + A["open_s"] + t_carry + max(A["boards_s"], A["probe_assemble_s"]) + A["lookout_s"]
say("F3", f"Deployment: run {A['distance']:.0f} m to the shed {t_run:.0f} s, open {A['open_s']:.0f} s, carry back {t_carry:.0f} s, "
          f"lookout posted {A['lookout_s']:.0f} s, first boards laid while probes are joined {A['boards_s']:.0f} s: "
          f"{t_total:.0f} s ({t_total / 60:.1f} min)")

# ------------------------------------------------------------------ G. cost
rows = list(csv.DictReader(open(ROOT / "bom" / "bom.csv")))
cost = sum(float(r_["qty"]) * float(r_["unit_cost_usd"]) for r_ in rows)
byline = {int(r_["item"].split()[0]): float(r_["qty"]) * float(r_["unit_cost_usd"]) for r_ in rows}
target = float(re.search(r"budget_usd:\s*([0-9.]+)", (ROOT / "project.yaml").read_text()).group(1))
cap_cost = sum(byline[k] for k in range(9, 23))
search_cost = sum(byline[k] for k in (4, 5, 6, 7, 8, 23, 24, 27))
say("G1", f"Parts for one site kit: USD {cost:,.2f}; capstan with its rope, slings and clamp USD {cap_cost:,.2f}; "
          f"box and hardware USD {byline[1] + byline[2] + byline[3]:,.2f}; PPE and lighting USD {byline[25] + byline[26]:,.2f}")
say("G2", f"Search core (boards, links, probes, pins, shovels, stretcher, lookout kit, cards): USD {search_cost:,.2f}")
say("G3", f"Value-engineering target: USD {target:,.0f}. Estimated cost of the constructable design: USD {cost:,.2f} "
          f"(USD {abs(target - cost):,.2f} {'under' if cost <= target else 'over'} the target)")

# ------------------------------------------------------------------ results table
res = [
    ("R1", "Deploy fast", f"{t_total / 60:.1f} min estimated from alarm to first probe line", "Met on paper; timed drills at TRL 4"),
    ("R2", "Probe depth", f"Central debris: one person {reach[('central', 'one')]:.1f} m, two {reach[('central', 'two')]:.1f} m; "
                          f"stiff debris: one {reach[('stiff', 'one')]:.1f} m, two {reach[('stiff', 'two')]:.1f} m", "At risk"),
    ("R3", "Crawl board support", f"Sinkage {sink * 1000:.0f} mm; bridges a 0.8 m void at {sig:.1f} MPa", "Met on paper"),
    ("R4", "Capstan pull", f"Pin releases at {T_rel:.0f} N ({T_lo:.0f} to {T_hi:.0f} N); {F_end / 2:.0f} N each for four people at 5,000 N", "Met on paper"),
    ("R5", "Casualty transport", f"Debris level {cases[('debris', 'level')]:.0f} N: {cases[('debris', 'level')] / 4:.0f} N each for four, "
                                 f"{cases[('debris', 'level')] / 2:.0f} N each for two; boards {cases[('boards', 'level')] / 2:.0f} N each for two",
     "Met with four haulers; at risk with two on debris"),
    ("R6", "Stop rule understood", "Stop rule printed on the lid and pocket cards", "Not verifiable at TRL 3"),
    ("R7", "Storage life", "Exterior plywood, painted or galvanised steel, UV-stabilised HDPE, alkaline cells stored out", "Met on paper by material choice; inspection at TRL 4"),
    ("R8", "Portable", f"Heaviest item {heaviest[0]:.1f} kg; whole carried kit {total:.0f} kg ({total / 4:.1f} kg each for four)", "At risk"),
    ("R9", "Cost", f"USD {cost:,.2f} per site kit", "Not met"),
    ("R10", "Overload limit", f"Pin releases at {T_rel:.0f} N nominal, {T_hi:.0f} N at most; rope factor {mbs_spliced / A['design_T']:.1f} at the design tension", "Met on paper"),
    ("R11", "Holds when let go", f"Two holding pawls; one takes {F_hold / 1000:.1f} kN at {F_hold / (hh * P['ring_t']):.0f} MPa tooth bearing", "Met on paper"),
]
with open(ROOT / "docs" / "04-calcs" / "results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "result", "status"])
    w.writerows(res)
print("wrote docs/04-calcs/results.csv")
