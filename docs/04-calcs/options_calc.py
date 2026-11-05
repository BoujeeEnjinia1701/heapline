"""HeapLine first-order numbers for the concept options (HPL-OPT-001, HPL-STM-001).

Run from the repo root:  python docs/04-calcs/options_calc.py
Option A (pumped friction capstan) is the existing design; its numbers come from sizing.py (HPL-CAL-001) and
bom/bom.csv. Options B (six-part rope tackle) and C (lever rope-grip puller) are first-order screens with the
assumptions listed below; they are estimates to be measured at TRL 4, not calculation notes. Part counts and
masses come from the D3 models in cad/src/model.py (cad/src/opt_b.py, opt_c.py). Importing this file builds the
models (about two minutes).
"""
import contextlib
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "docs" / "04-calcs"), str(ROOT / "cad" / "src"), str(ROOT / ".kit")]
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  HPL-CAL-001, builds option A
import model as M  # noqa: E402
import cad_parts as cp  # noqa: E402

A = CAL.A
P = M.PARAMS
OUT = []


def say(tag, text):
    OUT.append(f"[{tag}] {text}")


# ------------------------------------------------------------------ assumptions (estimates, to measure at TRL 4)
T_REQ = 5000.0            # N, the capstan pull of PR-004
PUSH_BAR = A["push_sustained"]       # N, sustained push per person on a bar or lever, short bouts (HPL-CAL-001)
PULL_ROPE = A["haul_sustained"]      # N, sustained pull per person on a rope, short distance (HPL-CAL-001)
STROKES = A["strokes_per_min"]       # strokes a minute, as for the capstan
K_SHEAVE = 0.93           # efficiency of one bushed sheave with 14 mm rope on a 125 mm sheave (D/d 8.9); estimate
ETA_CAM = 0.70            # lever, pins and cam grip together; estimate
MU_CAM = 0.30             # rope on a grooved steel cam; estimate
STROKE_C = P["C"]["stroke"] / 1000.0
USD_PER_KG_MADE = 62.0 / 19.2       # BOM line 9 (welded frame, USD 62 for 19.2 kg): used for made steel parts
ROPE_USD, SLING_USD, CRATE_USD, HANDLE_USD = 72.0, 66.0, 98.0, 2.0       # BOM lines 20, 21, 31; handle estimate


def pull_set(option):
    """Parts, mass (kg) and the made-steel mass of the pull set (group shell) of one option, from the D3 model."""
    ps = [p for p in M.components(option) if p["kind"] != "context" and p["group"] == "shell"]
    mass = sum(cp.mass_kg(p) for p in ps)
    made = sum(cp.mass_kg(p) for p in ps if p["kind"] == "made")
    return len(ps), mass, made


# ------------------------------------------------------------------ option A (HPL-CAL-001)
n_a, m_a, made_a = pull_set("A")
F_a_each = CAL.F_end / 2            # N each, four people, two per bar end
cost_a = 547.0                      # USD, shared capstan set with its crate (BOM, HPL-CAL-001 [G1b])
v_a = 1.5 / 60                      # m/s, HPL-CAL-001 [A10]
P_a_each = T_REQ * v_a / 4.0

# ------------------------------------------------------------------ option B: six-part tackle
N_PARTS = P["B"]["n_parts"]
ma_ideal = N_PARTS
ma_real = sum(K_SHEAVE ** i for i in range(1, N_PARTS + 1))
pull_b = T_REQ / ma_real
N_HANDLES = 6                       # after the fix recorded in HPL-DDR-006 (five handles gave more than 200 N each)
pull_b_each = pull_b / N_HANDLES
pull_b_each_old = pull_b / 5
travel_b = 1.1                      # m of load travel before the blocks are two-blocked and the grab resets (blocks 1.5 m apart at the start)
tail_b = travel_b * N_PARTS         # m of tail rope hauled per reset
n_b, m_b, made_b = pull_set("B")
cost_b = made_b * USD_PER_KG_MADE + ROPE_USD + SLING_USD + CRATE_USD + N_HANDLES * HANDLE_USD

# ------------------------------------------------------------------ option C: lever rope-grip puller
LEVER = 1600.0                      # mm from the pivot to the grips after the fix (1100 mm gave 212 N each)
OFFSET = 130.9                      # mm, pivot to drive pin (cad/src/opt_c.py)
ratio_c = LEVER / OFFSET
ratio_c_old = 1100.0 / OFFSET
handle_c = T_REQ / (ratio_c * ETA_CAM)
handle_c_each = handle_c / 4.0
handle_c_each_old = T_REQ / (ratio_c_old * ETA_CAM) / 4.0
v_c = STROKE_C * STROKES / 60.0     # m/s
P_c_each = T_REQ * v_c / ETA_CAM / 4.0
N_cam = T_REQ / MU_CAM              # N, clamp load that two grooved faces must give by friction alone (one face; the fixed cam adds the second)
p_cam = N_cam / (14.0 * 140.0) / 1.0    # MPa on a 14 mm rope over a 140 mm long groove (flat projected area)
n_c, m_c, made_c = pull_set("C")
cost_c = made_c * USD_PER_KG_MADE + ROPE_USD + SLING_USD + CRATE_USD

if __name__ == "__main__":
    say("A", f"pull set {n_a} parts, {m_a:.1f} kg, USD {cost_a:.0f} with crate; {F_a_each:.0f} N each for four; {P_a_each:.0f} W each")
    say("B", f"MA ideal {ma_ideal}, real {ma_real:.2f}; pull {pull_b:.0f} N: {pull_b_each:.0f} N each for {N_HANDLES} (was {pull_b_each_old:.0f} N for 5); pull set {n_b} parts, {m_b:.1f} kg, USD {cost_b:.0f} (estimate)")
    say("C", f"ratio {ratio_c:.1f} (was {ratio_c_old:.1f}); handle {handle_c:.0f} N, {handle_c_each:.0f} N each for four (was {handle_c_each_old:.0f}); {P_c_each:.0f} W each; cam clamp {N_cam:.0f} N, {p_cam:.1f} MPa on the rope; pull set {n_c} parts, {m_c:.1f} kg, USD {cost_c:.0f} (estimate)")
    print("\n".join(OUT))
