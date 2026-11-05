"""HeapLine STEM check calculations (HPL-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. First-order screens of every claim of the three concept options
(A pumped friction capstan, the existing design; B six-part rope tackle; C lever rope-grip puller). The sizing of
option A is the calculation note (HPL-CAL-001, sizing.py); the first-order numbers for B and C are in
options_calc.py. Both are imported here (about two minutes: the models are built once).
"""
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, limits, WITHIN, PLAUSIBLE  # noqa: E402
sys.path.insert(0, "docs/04-calcs")
import options_calc as OC  # noqa: E402
CAL = OC.CAL
P = CAL.P
A = CAL.A
D = CAL.D
E_STEEL = 210e3          # MPa
c = Check()

# ---------------------------------------------------------------- Option A: pumped friction capstan (HPL-CAL-001)
c.claim("S1", "A tailer holds the tail of the rope with 33 N while the capstan pulls 5 kN", "Physics", "Mechanics and statics",
        "Capstan (Euler-Eytelwein) equation T_load / T_tail = exp(mu theta): four turns, mu 0.20 polyester on painted steel",
        round(CAL.tail, 0), A["push_sustained"], "N", closed_by="HPL-CAL-001 A3")
c.claim("S2", "Four people at the bars give the 5 kN pull with 114 N each", "Physics", "Mechanics and statics",
        "Moment balance at the head: M = T (r + bush friction) shared over two bar ends 754 mm from the axis; sustained push per person for short bouts 150 N",
        round(CAL.F_end / 2, 0), A["push_sustained"], "N", margin=0.1, closed_by="HPL-CAL-001 A2")
c.claim("S3", "Four people can keep up the 1.5 m/min stroke rate", "Physics", "Mechanics and statics",
        f"Power each = pull x rope speed / 4 = 5,000 N x {OC.v_a:.3f} m/s / 4; sustained hand power {limits.HUMAN_SUSTAINED_W:.0f} W per person",
        round(OC.P_a_each, 0), limits.HUMAN_SUSTAINED_W, "W each", closed_by="HPL-CAL-001 A10; options_calc.py A")
c.order_of_magnitude("S4", "A quarter-turn stroke takes in 101 mm of rope", "Mathematics", "Geometry",
                     claimed=101.0, estimate=D["r_rope"] * math.pi / 2, unit="mm",
                     law="Arc length = r x angle, 64.2 mm centre radius, 90 degrees", closed_by="HPL-CAL-001 A10")
# Independent review (finding 1): 430 MPa is the EN 10025-2 minimum for S275 under 3 mm; for bar of 3 to 100 mm the
# range is 410 to 560 MPa, which the 6 mm pin's rope tension would follow (up to 8,301 N, above the 8 kN limit).
# Fix under the standing instruction: buy the pin bar with a mill certificate showing Rm 410 to 480 MPa and release-test
# three pins from each batch (HPL-DDR-006); the band below is that certified range plus 5 % test scatter.
RM_NOM, RM_LO, RM_HI = 430.0, 410.0, 480.0
T_pin_hi = CAL.T_rel * RM_HI / RM_NOM * 1.05
T_pin_lo = CAL.T_rel * RM_LO / RM_NOM * 0.95
c.claim("S5", "The 6 mm S275 shear pin, from a bar certified at 410 to 480 MPa ultimate strength, releases below the 8 kN design tension", "Physics", "Strength of materials",
        f"Single shear of a mild steel pin, tau = 0.6 x Rm, torque to rope tension at the head. EN 10025-2 allows 410 to 560 MPa for S275 bar of 3 to 100 mm; at 560 MPa the release would be {CAL.T_rel * 560 / RM_NOM:.0f} N, above 8 kN, so the bar is bought with a mill certificate at 480 MPa or less and three pins per batch are release-tested (HPL-DDR-006); 5 % test scatter",
        round(T_pin_hi, 0), A["design_T"], "N", margin=0.1, closed_by="HPL-CAL-001 A4; release tests on each pin batch at TRL 4")
c.claim("S6", "The same pin does not release below the 5 kN the capstan must pull, even at the bottom of its spread", "Physics", "Strength of materials",
        "As S5 at the bottom of the certified range (410 MPa) and minus 5 % test scatter",
        round(T_pin_lo, 0), 5000.0, "N", rule="above", margin=0.2, closed_by="HPL-CAL-001 A4; release tests on each pin batch at TRL 4")
c.claim("S7", "The rope keeps its factor of 4.5 on break at the top of the pin's release range", "Physics", "Strength of materials",
        "14 mm polyester double braid, 40 kN minimum break, 90 % through an eye splice, over the upper release tension (HPL-DDR-001 item 5 sets 4.5)",
        round(CAL.mbs_spliced / T_pin_hi, 2), 4.5, "x", rule="above", margin=0.1, closed_by="HPL-CAL-001 A5")
c.cited("S8", "A 14 mm polyester double braid with at least 40 kN minimum breaking load can be bought", "Engineering and technology", "Standards practice",
        "Maker's data: Marlow D/Braid PES 14 mm, minimum break load 5,570 kg (about 54.6 kN) (shop.marlowropes.com, checked 2026-11-03); one other maker's article quotes about 4,700 kg (about 46 kN) for 14 mm polyester rope (iropes.com, checked 2026-11-03). Both exceed 40 kN",
        "Minimum break 54.6 kN against 40 kN", WITHIN, closed_by="BOM line 20")
c.cited("S9", "The 114.3 mm drum and the 60.3 mm hold-down roller do not cut the rope's strength", "Engineering and technology", "Standards practice",
        f"Fibre rope strength and life fall as the bend ratio D/d falls; usual guidance asks for about 8 or more where the rope wraps a sheave or drum. Drum {114.3 / 14:.1f}, roller {60.3 / 14:.1f} (the rope wraps the roller by only about 15 degrees). The guidance was not checked against a source",
        "Drum 8.2, roller 4.3: confirm the figure with the rope supplier", PLAUSIBLE, closed_by="Rope supplier's bend-ratio data at TRL 4")
c.claim("S10", "The 60.3 x 5.0 post stays below 0.6 of S355 yield at the 8 kN design tension", "Physics", "Strength of materials",
        "Bending of the post at the centre member from the rope pull; yield S355 355 MPa (EN 10025-2)",
        round(CAL.Mpost * 1000 / CAL.Z_post, 0), 0.6 * 355.0, "MPa", closed_by="HPL-CAL-001 A6")
c.claim("S11", "One holding pawl takes the full design tension without crushing its tooth", "Physics", "Strength of materials",
        "Bearing stress on the 12 x 6 mm tooth face at 8 kN (one pawl taking it all); limit 0.6 x S275 yield 275 MPa",
        round(CAL.F_hold / (CAL.hh * CAL.P["ring_t"]), 0), 0.6 * 275.0, "MPa", closed_by="HPL-CAL-001 A7")
c.claim("S12", "The probe reaches 2.5 m in stiffer debris with two people", "Physics", "Mechanics and statics",
        "Push needed = cone resistance x tip area + sleeve friction x perimeter x depth (cone 1.0 MPa, sleeve 3 kPa, estimates; no published data for slide debris); two people push 650 N",
        round(A["qc_stiff"] * CAL.A_tip + A["fs_stiff"] * CAL.per_m * 2.5, 0),
        A["push_two"], "N", margin=0.1, closed_by="HPL-CAL-001 B1s; test heap at TRL 4")
# Independent review (finding 3): the governing case is the full 3.07 m free length at the start of a push, not 0.57 m.
# Fix under the standing instruction: one person pushes while more than 1.5 m of tube is above the debris, two only
# below that (drill-card wording, HPL-DDR-006).
c.claim("S13", "The 16 x 2.0 probe tube does not buckle under one person's push (half of two people's 650 N) at the full 3.07 m free length", "Physics", "Strength of materials",
        f"Euler buckling, pinned ends, E 210 GPa, free length 3.07 m (worst case, start of a push); one person pushes while more than 1.5 m is above the debris, two below that, where the critical load is {CAL.pcr(1.5):.0f} N",
        round(A["push_two"] / 2, 0), round(CAL.pcr(3.07), 0), "N", margin=0.1, closed_by="HPL-CAL-001 B2; probe trials at TRL 4")
c.cited("S14", "A kneeling searcher on a crawl board sinks less than 50 mm on very loose debris", "Physics", "Mechanics and statics",
        "Bearing pressure over the board divided by a subgrade modulus of 0.10 MN/m3 (low side, estimate; no sourced value for slide debris); the load is shared over an assumed 0.8 m length of board",
        f"{CAL.sink * 1000:.0f} mm against 50 mm, resting on an estimated modulus", PLAUSIBLE, closed_by="HPL-CAL-001 C1; load tests on representative fill at TRL 4")
c.claim("S15", "The two battens alone bridge a 0.8 m void under a 100 kg searcher", "Physics", "Strength of materials",
        "Bending of two 45 x 70 mm battens at mid-span against C16 timber bending strength 16 MPa (EN 338), a factor of 2 required",
        round(CAL.sig, 1), 16.0 / 2.0, "MPa", closed_by="HPL-CAL-001 C2")
c.claim("S16", "Four haulers pull the stretcher 15 degrees up debris with 189 N each", "Physics", "Mechanics and statics",
        "Coulomb friction mu 0.5 on debris plus the slope term, 100 kg casualty and the 3.9 kg stretcher; sustained pull per hauler 200 N over a short distance",
        189.0, A["haul_sustained"], "N", margin=0.1, closed_by="HPL-CAL-001 D; drill-card rule 21A")
leg_s = 100 / A["run_mps"] + A["open_s"] + 100 / A["carry_mps"] + A["lookout_s"] + A["boards_s"]
c.cited("S17", "The first probe line starts 4.6 min after the alarm, inside the 300 s of PR-001", "Mathematics", "Orders of magnitude",
        "Sum of legs: run 100 m at 2.5 m/s, open 30 s, carry 100 m at 0.8 m/s, lookout 20 s, boards 60 s; the speeds and opening time are estimates",
        f"{leg_s:.0f} s against 300 s ({(300 - leg_s) / 3:.1f} % under)", PLAUSIBLE, closed_by="Timed drills at TRL 4")
c.cited("S18", "No flame or smoking near the debris, and stop on any gas smell, removes the ignition sources for landfill gas; with no detector it does not remove toxic or asphyxiant gas (see S29)", "Chemistry", "Reaction kinetics and thermodynamics",
        "Methane is explosive in air only between 5 % and 15 % by volume; landfill gas is typically about 50 % methane and 40 to 60 % carbon dioxide, so gas that has migrated and diluted can be in the explosive range (ATSDR Landfill Gas Primer, chapter 3, 2001, checked 2026-11-03). The rule removes ignition sources; it does not detect gas, and carbon dioxide and hydrogen sulfide can harm without any smell or flame",
        "Rule stands; a detector is not added (HPL-DDR-001 item 11); a partner who maintains one would allow it", PLAUSIBLE,
        closed_by="Co-design review at TRL 4; PRC safety section")
c.cited("S19", "AA alkaline cells stored out of the lamps stay usable for 12 months in a warm shed", "Chemistry", "Materials and polymer chemistry",
        "Alkaline cells lose charge slowly and can leak when left flat inside equipment; the kit stores them in their packet. No shelf-life figure or temperature limit was checked against a maker's datasheet",
        "Maker's shelf life at shed temperature to assess; monthly inspection log", PLAUSIBLE, closed_by="BOM line 25; monthly inspection")
c.cited("S20", "Cut-resistant gloves, boots and glasses make a search on sharp waste acceptable", "Biology", "Anatomy and physiology",
        "Wounds contaminated with dirt or soil, and puncture wounds, are higher risk for tetanus; vaccination status decides the care needed (CDC, Clinical Guidance for Wound Management to Prevent Tetanus, checked 2026-11-03). PPE lowers the injury rate but does not remove it; the kit gives first-aid wording only, not medical treatment",
        "PPE reduces, does not remove, wound and infection risk; vaccination advice goes with the drill card", PLAUSIBLE, closed_by="PRC safety section; RSK hazard H6")

# ---------------------------------------------------------------- Option B: six-part rope tackle
c.claim("S21", "A six-part tackle turns the pull of six people into 5 kN with under 200 N each", "Physics", "Mechanics and statics",
        f"Real advantage = sum of k^i for six parts, k = {OC.K_SHEAVE} per bushed sheave (estimate), {OC.ma_real:.2f} against the ideal 6; tail pull {OC.pull_b:.0f} N shared by {OC.N_HANDLES} rope handles. First draft with five handles needed {OC.pull_b_each_old:.0f} N each, above the 200 N sustained; fix (HPL-DDR-006, standing instruction): six handles",
        round(OC.pull_b_each, 0), A["haul_sustained"], "N", margin=0.15, closed_by="options_calc.py B")
c.claim("S22", "The rope grab can hold the tail while the hands let go", "Physics", "Mechanics and statics",
        "A cam grab holds if the clamp load N satisfies mu N >= tail tension; mu 0.3 on rope is an estimate (no source checked) and the 6 kN clamp load is an assumed figure to be replaced by the grab maker's rated hold; the same mu is used in S26. Tail tension at 5 kN load",
        round(OC.pull_b, 0), round(0.3 * 6000.0, 0), "N", margin=0.5, closed_by="Rope grab hold test at TRL 4")
c.claim("S23", "The 125 mm sheaves keep the rope's bend ratio at about 8 or more", "Engineering and technology", "Standards practice",
        "D/d = 125 / 14 (same usual guidance as S9, not checked against a source)", round(125.0 / 14.0, 1), 8.0, "", rule="above", margin=0.15,
        closed_by="Rope supplier's bend-ratio data at TRL 4")

# ---------------------------------------------------------------- Option C: lever rope-grip puller
c.claim("S24", "Four people at the lever give the 5 kN pull with under 150 N each", "Physics", "Mechanics and statics",
        f"Pull = handle force x lever ratio x efficiency; ratio {OC.ratio_c:.1f} (1.6 m lever over 131 mm to the drive pin; assumes all four hands at 1.6 m, so a cross handle at the end is to be assessed), efficiency {OC.ETA_CAM} (estimate). First draft with a 1.1 m lever needed {OC.handle_c_each_old:.0f} N each; fix (HPL-DDR-006, standing instruction): lever 1.6 m",
        round(OC.handle_c_each, 0), A["push_sustained"], "N", margin=0.05, closed_by="options_calc.py C")
c.claim("S25", "Four people sustain 15 strokes a minute of 120 mm", "Physics", "Mechanics and statics",
        f"Power each = pull x rope speed / efficiency / 4 = 5,000 N x {OC.v_c:.3f} m/s / {OC.ETA_CAM} / 4", round(OC.P_c_each, 0), limits.HUMAN_SUSTAINED_W, "W each", margin=0.3,
        closed_by="options_calc.py C")
c.cited("S26", "A grooved steel cam grips 14 mm polyester rope at 5 kN without cutting or glazing it", "Chemistry", "Materials and polymer chemistry",
        f"Holding 5 kN by friction alone at mu 0.3 (estimate) needs a clamp load of {OC.N_cam / 1000:.1f} kN, about {OC.p_cam:.1f} MPa over a 14 x 140 mm groove. No rope maker's limit on clamp pressure was checked; polyester fibre melts or glazes under frictional heating and crushes under high clamp load, and the capstan (option A) loads the rope far more gently over four turns",
        "Clamp pressure high; rope supplier's limit to assess", PLAUSIBLE, closed_by="Grip test on the rope at TRL 4")

# ---------------------------------------------------------------- Added after the independent review
c.cited("S27", "The capstan wave arrives 14.8 min after the alarm from 500 m, inside the 15 min of PR-015", "Mathematics", "Orders of magnitude",
        "Run to the host shed at 2.5 m/s, 60 s to open the crate, carry back at 0.8 m/s with 21.4 kg each; the 25 kg carry limit and the pace are the 100 m figures applied over 500 m, and the seven people are two waves (four, then three), not four",
        f"{CAL.arrive[500.0]:.0f} s against 900 s ({(900 - CAL.arrive[500.0]) / 9:.1f} % under)", PLAUSIBLE, closed_by="Timed drills at TRL 4 over 500 m; HPL-DDR-004 limit")
c.claim("S28", "A 1,000 N knee load on the deck between the battens stays inside the 15 mm plywood's bending strength", "Physics", "Strength of materials",
        "Bending of a 15 mm plywood strip on the clear span between the battens; the 20 MPa allowed is an unsourced value, a factor of 1.5",
        round(CAL.Mk * 1000 / CAL.Zk, 1), CAL.A["f_ply"] / 1e6, "MPa", margin=0.4, closed_by="HPL-CAL-001 C3; plywood maker's data at TRL 4")
c.cited("S29", "Dug voids and holes can hold carbon dioxide or hydrogen sulfide that a flame or smell rule does not catch", "Chemistry", "Reaction kinetics and thermodynamics",
        "Carbon dioxide is heavier than air and collects in holes and trenches; hydrogen sulfide dulls the sense of smell (ATSDR, Landfill Gas Primer, ch. 3, checked 2026-11-03). Searchers dig where casualties lie, so the no-flame rule (S18) only removes ignition sources",
        "Digging guidance added for the drill card: no one goes head first into a hole, a watcher at every hole, back out on headache, dizziness or any smell; the six-signal stop rule is not changed (HPL-DDR-006)", PLAUSIBLE,
        closed_by="Co-design review at TRL 4; RSK hazard H8; Amish asked whether to add a seventh stop signal")

if __name__ == "__main__":
    print("Record of the fixes made at this check (HPL-DDR-006):")
    print(f"  B: five handles needed {OC.pull_b_each_old:.0f} N each against 200 N: six rope handles in cad/src/opt_b.py")
    print(f"  C: a 1.1 m lever needed {OC.handle_c_each_old:.0f} N each against 150 N: lever 1.6 m in cad/src/opt_c.py")
    c.write()
