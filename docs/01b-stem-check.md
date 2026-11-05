---
doc_id: HPL-STM-001
title: HeapLine STEM check
project: HeapLine
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First STEM check, written for the kit 1.9.1 upgrade; two fixes made under the standing instruction of 2026-10-23 (HPL-DDR-006)
---

# HeapLine STEM check

Verdict: all 29 claims across the three concept options sit within known science, 9 of them outright and 20 as plausible and to be confirmed at TRL 4; none fails. Two first-draft details of options B and C failed their screen, and the independent review (below) found three more weaknesses in option A and the shared kit; all five were fixed in the same session under Amish's standing instruction of 2026-10-23 (HPL-DDR-006). Verdicts were also tightened where a row rests on an estimate: it is plausible, not within. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, `docs/04-calcs/options_calc.py` and the calculation note HPL-CAL-001.

## Claims checked

*Table 1. Claims, governing science and verdicts.*

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | A tailer holds the tail of the rope with 33 N while the capstan pulls 5 kN | Physics | Mechanics and statics | Capstan (Euler-Eytelwein) equation T_load / T_tail = exp(mu theta): four turns, mu 0.20 polyester on painted steel | 33 N <= 150 N | Within known science | HPL-CAL-001 A3 |
| S2 | Four people at the bars give the 5 kN pull with 114 N each | Physics | Mechanics and statics | Moment balance at the head: M = T (r + bush friction) shared over two bar ends 754 mm from the axis; sustained push per person for short bouts 150 N | 114 N <= 150 N | Within known science | HPL-CAL-001 A2 |
| S3 | Four people can keep up the 1.5 m/min stroke rate | Physics | Mechanics and statics | Power each = pull x rope speed / 4 = 5,000 N x 0.025 m/s / 4; sustained hand power 75 W per person | 31 W each <= 75 W each | Within known science | HPL-CAL-001 A10; options_calc.py A |
| S4 | A quarter-turn stroke takes in 101 mm of rope | Mathematics | Geometry | Arc length = r x angle, 64.2 mm centre radius, 90 degrees | claimed 101 mm, estimate 101 mm (ratio 1.00) | Within known science | HPL-CAL-001 A10 |
| S5 | The 6 mm S275 shear pin, from a bar certified at 410 to 480 MPa ultimate strength, releases below the 8 kN design tension | Physics | Strength of materials | Single shear of a mild steel pin, tau = 0.6 x Rm, torque to rope tension at the head. EN 10025-2 allows 410 to 560 MPa for S275 bar of 3 to 100 mm; at 560 MPa the release would be 8300 N, above 8 kN, so the bar is bought with a mill certificate at 480 MPa or less and three pins per batch are release-tested (HPL-DDR-006); 5 % test scatter | 7470 N <= 8000 N | Plausible, to confirm at TRL 3 | HPL-CAL-001 A4; release tests on each pin batch at TRL 4 |
| S6 | The same pin does not release below the 5 kN the capstan must pull, even at the bottom of its spread | Physics | Strength of materials | As S5 at the bottom of the certified range (410 MPa) and minus 5 % test scatter | 5773 N >= 5000 N | Plausible, to confirm at TRL 3 | HPL-CAL-001 A4; release tests on each pin batch at TRL 4 |
| S7 | The rope keeps its factor of 4.5 on break at the top of the pin's release range | Physics | Strength of materials | 14 mm polyester double braid, 40 kN minimum break, 90 % through an eye splice, over the upper release tension (HPL-DDR-001 item 5 sets 4.5) | 4.82 x >= 4.5 x | Plausible, to confirm at TRL 3 | HPL-CAL-001 A5 |
| S8 | A 14 mm polyester double braid with at least 40 kN minimum breaking load can be bought | Engineering and technology | Standards practice | Maker's data: Marlow D/Braid PES 14 mm, minimum break load 5,570 kg (about 54.6 kN) (shop.marlowropes.com, checked 2026-11-03); one other maker's article quotes about 4,700 kg (about 46 kN) for 14 mm polyester rope (iropes.com, checked 2026-11-03). Both exceed 40 kN | Minimum break 54.6 kN against 40 kN | Within known science | BOM line 20 |
| S9 | The 114.3 mm drum and the 60.3 mm hold-down roller do not cut the rope's strength | Engineering and technology | Standards practice | Fibre rope strength and life fall as the bend ratio D/d falls; usual guidance asks for about 8 or more where the rope wraps a sheave or drum. Drum 8.2, roller 4.3 (the rope wraps the roller by only about 15 degrees). The guidance was not checked against a source | Drum 8.2, roller 4.3: confirm the figure with the rope supplier | Plausible, to confirm at TRL 3 | Rope supplier's bend-ratio data at TRL 4 |
| S10 | The 60.3 x 5.0 post stays below 0.6 of S355 yield at the 8 kN design tension | Physics | Strength of materials | Bending of the post at the centre member from the rope pull; yield S355 355 MPa (EN 10025-2) | 63 MPa <= 213 MPa | Within known science | HPL-CAL-001 A6 |
| S11 | One holding pawl takes the full design tension without crushing its tooth | Physics | Strength of materials | Bearing stress on the 12 x 6 mm tooth face at 8 kN (one pawl taking it all); limit 0.6 x S275 yield 275 MPa | 77 MPa <= 165 MPa | Within known science | HPL-CAL-001 A7 |
| S12 | The probe reaches 2.5 m in stiffer debris with two people | Physics | Mechanics and statics | Push needed = cone resistance x tip area + sleeve friction x perimeter x depth (cone 1.0 MPa, sleeve 3 kPa, estimates; no published data for slide debris); two people push 650 N | 631 N <= 650 N | Plausible, to confirm at TRL 3 | HPL-CAL-001 B1s; test heap at TRL 4 |
| S13 | The 16 x 2.0 probe tube does not buckle under one person's push (half of two people's 650 N) at the full 3.07 m free length | Physics | Strength of materials | Euler buckling, pinned ends, E 210 GPa, free length 3.07 m (worst case, start of a push); one person pushes while more than 1.5 m is above the debris, two below that, where the critical load is 2026 N | 325 N <= 484 N | Within known science | HPL-CAL-001 B2; probe trials at TRL 4 |
| S14 | A kneeling searcher on a crawl board sinks less than 50 mm on very loose debris | Physics | Mechanics and statics | Bearing pressure over the board divided by a subgrade modulus of 0.10 MN/m3 (low side, estimate; no sourced value for slide debris); the load is shared over an assumed 0.8 m length of board | 44 mm against 50 mm, resting on an estimated modulus | Plausible, to confirm at TRL 3 | HPL-CAL-001 C1; load tests on representative fill at TRL 4 |
| S15 | The two battens alone bridge a 0.8 m void under a 100 kg searcher | Physics | Strength of materials | Bending of two 45 x 70 mm battens at mid-span against C16 timber bending strength 16 MPa (EN 338), a factor of 2 required | 4 MPa <= 8 MPa | Within known science | HPL-CAL-001 C2 |
| S16 | Four haulers pull the stretcher 15 degrees up debris with 189 N each | Physics | Mechanics and statics | Coulomb friction mu 0.5 on debris plus the slope term, 100 kg casualty and the 3.9 kg stretcher; sustained pull per hauler 200 N over a short distance | 189 N <= 200 N | Plausible, to confirm at TRL 3 | HPL-CAL-001 D; drill-card rule 21A |
| S17 | The first probe line starts 4.6 min after the alarm, inside the 300 s of PR-001 | Mathematics | Orders of magnitude | Sum of legs: run 100 m at 2.5 m/s, open 30 s, carry 100 m at 0.8 m/s, lookout 20 s, boards 60 s; the speeds and opening time are estimates | 275 s against 300 s (8.3 % under) | Plausible, to confirm at TRL 3 | Timed drills at TRL 4 |
| S18 | No flame or smoking near the debris, and stop on any gas smell, removes the ignition sources for landfill gas; with no detector it does not remove toxic or asphyxiant gas (see S29) | Chemistry | Reaction kinetics and thermodynamics | Methane is explosive in air only between 5 % and 15 % by volume; landfill gas is typically about 50 % methane and 40 to 60 % carbon dioxide, so gas that has migrated and diluted can be in the explosive range (ATSDR Landfill Gas Primer, chapter 3, 2001, checked 2026-11-03). The rule removes ignition sources; it does not detect gas, and carbon dioxide and hydrogen sulfide can harm without any smell or flame | Rule stands; a detector is not added (HPL-DDR-001 item 11); a partner who maintains one would allow it | Plausible, to confirm at TRL 3 | Co-design review at TRL 4; PRC safety section |
| S19 | AA alkaline cells stored out of the lamps stay usable for 12 months in a warm shed | Chemistry | Materials and polymer chemistry | Alkaline cells lose charge slowly and can leak when left flat inside equipment; the kit stores them in their packet. No shelf-life figure or temperature limit was checked against a maker's datasheet | Maker's shelf life at shed temperature to assess; monthly inspection log | Plausible, to confirm at TRL 3 | BOM line 25; monthly inspection |
| S20 | Cut-resistant gloves, boots and glasses make a search on sharp waste acceptable | Biology | Anatomy and physiology | Wounds contaminated with dirt or soil, and puncture wounds, are higher risk for tetanus; vaccination status decides the care needed (CDC, Clinical Guidance for Wound Management to Prevent Tetanus, checked 2026-11-03). PPE lowers the injury rate but does not remove it; the kit gives first-aid wording only, not medical treatment | PPE reduces, does not remove, wound and infection risk; vaccination advice goes with the drill card | Plausible, to confirm at TRL 3 | PRC safety section; RSK hazard H6 |
| S21 | A six-part tackle turns the pull of six people into 5 kN with under 200 N each | Physics | Mechanics and statics | Real advantage = sum of k^i for six parts, k = 0.93 per bushed sheave (estimate), 4.69 against the ideal 6; tail pull 1066 N shared by 6 rope handles. First draft with five handles needed 213 N each, above the 200 N sustained; fix (HPL-DDR-006, standing instruction): six handles | 178 N <= 200 N | Plausible, to confirm at TRL 3 | options_calc.py B |
| S22 | The rope grab can hold the tail while the hands let go | Physics | Mechanics and statics | A cam grab holds if the clamp load N satisfies mu N >= tail tension; mu 0.3 on rope is an estimate (no source checked) and the 6 kN clamp load is an assumed figure to be replaced by the grab maker's rated hold; the same mu is used in S26. Tail tension at 5 kN load | 1066 N <= 1800 N | Plausible, to confirm at TRL 3 | Rope grab hold test at TRL 4 |
| S23 | The 125 mm sheaves keep the rope's bend ratio at about 8 or more | Engineering and technology | Standards practice | D/d = 125 / 14 (same usual guidance as S9, not checked against a source) | 8.9  >= 8  | Plausible, to confirm at TRL 3 | Rope supplier's bend-ratio data at TRL 4 |
| S24 | Four people at the lever give the 5 kN pull with under 150 N each | Physics | Mechanics and statics | Pull = handle force x lever ratio x efficiency; ratio 12.2 (1.6 m lever over 131 mm to the drive pin; assumes all four hands at 1.6 m, so a cross handle at the end is to be assessed), efficiency 0.7 (estimate). First draft with a 1.1 m lever needed 213 N each; fix (HPL-DDR-006, standing instruction): lever 1.6 m | 146 N <= 150 N | Plausible, to confirm at TRL 3 | options_calc.py C |
| S25 | Four people sustain 15 strokes a minute of 120 mm | Physics | Mechanics and statics | Power each = pull x rope speed / efficiency / 4 = 5,000 N x 0.030 m/s / 0.7 / 4 | 54 W each <= 75 W each | Plausible, to confirm at TRL 3 | options_calc.py C |
| S26 | A grooved steel cam grips 14 mm polyester rope at 5 kN without cutting or glazing it | Chemistry | Materials and polymer chemistry | Holding 5 kN by friction alone at mu 0.3 (estimate) needs a clamp load of 16.7 kN, about 8.5 MPa over a 14 x 140 mm groove. No rope maker's limit on clamp pressure was checked; polyester fibre melts or glazes under frictional heating and crushes under high clamp load, and the capstan (option A) loads the rope far more gently over four turns | Clamp pressure high; rope supplier's limit to assess | Plausible, to confirm at TRL 3 | Grip test on the rope at TRL 4 |
| S27 | The capstan wave arrives 14.8 min after the alarm from 500 m, inside the 15 min of PR-015 | Mathematics | Orders of magnitude | Run to the host shed at 2.5 m/s, 60 s to open the crate, carry back at 0.8 m/s with 21.4 kg each; the 25 kg carry limit and the pace are the 100 m figures applied over 500 m, and the seven people are two waves (four, then three), not four | 885 s against 900 s (1.7 % under) | Plausible, to confirm at TRL 3 | Timed drills at TRL 4 over 500 m; HPL-DDR-004 limit |
| S28 | A 1,000 N knee load on the deck between the battens stays inside the 15 mm plywood's bending strength | Physics | Strength of materials | Bending of a 15 mm plywood strip on the clear span between the battens; the 20 MPa allowed is an unsourced value, a factor of 1.5 | 13.3 MPa <= 20 MPa | Plausible, to confirm at TRL 3 | HPL-CAL-001 C3; plywood maker's data at TRL 4 |
| S29 | Dug voids and holes can hold carbon dioxide or hydrogen sulfide that a flame or smell rule does not catch | Chemistry | Reaction kinetics and thermodynamics | Carbon dioxide is heavier than air and collects in holes and trenches; hydrogen sulfide dulls the sense of smell (ATSDR, Landfill Gas Primer, ch. 3, checked 2026-11-03). Searchers dig where casualties lie, so the no-flame rule (S18) only removes ignition sources | Digging guidance added for the drill card: no one goes head first into a hole, a watcher at every hole, back out on headache, dizziness or any smell; the six-signal stop rule is not changed (HPL-DDR-006) | Plausible, to confirm at TRL 3 | Co-design review at TRL 4; RSK hazard H8; Amish asked whether to add a seventh stop signal |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3** (the kit's label; every such row here closes at TRL 4 or on purchase), **Fails**. S1 to S20 and S27 to S29 check option A, the current design, and the kit shared by all options (probes, boards, stretcher, hazards, arrival time); S21 to S23 check option B; S24 to S26 check option C. Rows marked plausible are inside 10 % of their limit or rest on an estimate or a source not yet read; each names the test or check that would close it.

## Fixes made at this check

*Table 2. Fixes decided under the standing instruction of 2026-10-23.*

| Option | Failure at the first draft | Fix that keeps the working principle | Result |
| --- | --- | --- | --- |
| B | Five rope handles on the tail needed 213 N each, above the 200 N sustained pull per person (HPL-CAL-001 haul limit) | Six rope handles on the tail (`cad/src/opt_b.py`) | 178 N each (S21) |
| C | A 1.1 m lever needed 213 N each from four people, above the 150 N sustained push on a bar | Lever 1.6 m from the pivot to the grips (`cad/src/opt_c.py`) | 146 N each (S24), 2.7 % under the limit |
| A | Pin bar: the check used 430 MPa and a plus or minus 20 % spread, but EN 10025-2 allows 410 to 560 MPa for S275 bar, so a pin could release at 8.3 kN, above the 8 kN limit | Buy the pin bar with a mill certificate at 480 MPa or less and release-test three pins per batch (a purchase specification, no geometry change) | Release 5,773 to 7,470 N (S5, S6); rope factor 4.82 (S7) |
| A and shared | Probe buckling was checked only at 0.57 m of free tube | One person pushes while more than 1.5 m of tube is above the debris; two only below (drill-card wording) | 325 N against 484 N critical at the full free length (S13) |
| Shared | The gas rule was called sufficient, but it removes only ignition sources | Rule reworded; digging guidance for the drill card (no head first entry, a watcher at every hole); the six-signal stop rule is not changed | S18 and S29 plausible; Amish asked about a seventh stop signal (HPL-DDR-006) |

None of these fixes changes the working principle, the pitch or the scope. Option A had no failing row on its own first-draft numbers; the pin bar and probe rules are fixes to its purchase specification and drill card.

## Fields not relevant

- Heat transfer and thermodynamics: no heat source or sink; friction heating in the capstan and the cam grip is small at the speeds used (the cam grip is flagged in S26).
- Electricity and electronics: only AA lamps, bought; no mains voltage, no lithium cells.
- Biology beyond injury and infection: no living material in the design; S20 covers cuts and tetanus only.

## Concept options

- Option A, pumped friction capstan: within known science; its plausible rows (S5 to S7, S9, S12, S14, S16 to S20, S27 to S29) are closed by pin release tests, rope data, the test heap and timed drills at TRL 4.
- Option B, six-part rope tackle: within known science after the six-handle fix; S21 to S23 (tackle efficiency, grab hold and sheave bend ratio) are plausible.
- Option C, lever rope-grip puller: within known science after the 1.6 m lever fix; S24 to S26 (lever effort, power and cam clamp pressure on the rope) are plausible; the clamp pressure is the main risk of this option.

## Independent review

A second model run (`claude -p --model claude-opus-5-5`, 2026-11-03) was given only this document, `docs/04-calcs/01-sizing.md`, `docs/03-requirements.md` and `docs/04-calcs/sizing.py`. It recomputed the other figures (33 N, 114 N, 101 mm, 4.71, 63 MPa, 77 MPa, 631 N, 44 mm, 189 N, 275 s, 4.69, 1,066 N, 178 N, 12.2, 146 N, 54 W and more) and found them correct. It could not check `options_calc.py`, which it was not given. Its sixteen findings and what was done:

*Table 3. Independent review findings and disposition.*

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | S5 to S7: the pin band centres on the 430 MPa minimum; EN 10025-2 allows 410 to 560 MPa for bar of 3 to 100 mm, so release could reach 8.3 kN | High | Fixed (standing instruction): bar bought with a mill certificate at 480 MPa or less, three pins per batch release-tested; S5, S6 recomputed (the reviewer's low end double counted the 20 % spread over the whole range) |
| 2 | S18: "sufficient control" is not supported by the cited source (carbon dioxide and hydrogen sulfide) | High | Fixed: claim reworded, S29 added, digging guidance added; the six-signal stop rule is not changed; whether to add a seventh signal goes to Amish |
| 3 | S13: buckling checked at the least critical depth | High | Fixed: checked at the full 3.07 m free length with one person pushing; rule one person above 1.5 m of free tube |
| 4 | Missing claim for the 14.8 min arrival (PR-015) and for the seven people in two waves against "four" in PR-008 | Medium high | S27 added (plausible); the PR-008 wording is raised in REVIEW for Amish |
| 5 | S22: grab hold has no source for mu or clamp load | Medium | Verdict plausible; clamp load flagged as assumed; tied to S26 |
| 6 | S21, S25: rest on estimated efficiencies yet rated within | Medium | Both plausible |
| 7 | S17: repeats the claim and sits 8.3 % under the 300 s limit | Medium | Rewritten against 300 s; plausible |
| 8 | S14: rests on an estimated modulus | Medium low | Plausible; 0.8 m length noted as an assumption |
| 9 | S24: ratio 12.2 assumes all four hands at 1.6 m | Medium low | Noted in the claim; cross handle to assess; stays plausible |
| 10 | S11: tooth root shear and pawl impact not screened; run back of one tooth pitch against 0 turns in PR-011 | Medium low | Not fixed here: carried to TRL 4 and raised in REVIEW for Amish (PR-011 wording) |
| 11 | S3: power should use head torque (34 W each, not 31 W) | Low | Not changed; verdict holds either way |
| 12 | Crawl board deck stress has no row | Low | S28 added (plausible) |
| 13 | S7 ignores strength loss at the drum and roller bends | Low | Carried to the rope supplier's data at TRL 4 (S9) |
| 14 | S19 plausible but PR-007 says met by design | Low | PR-007 wording raised in REVIEW |
| 15 | The kit's verdict label says TRL 3 but rows close at TRL 4 | Low | Kit label, not edited (kit bug, reported) |
| 16 | Source check dates differ (2026-10-24 and 2026-11-03) | Low | Dates unified to 2026-11-03 |


## Sources

- Capstan (Euler-Eytelwein) equation, Euler buckling of columns, von Mises stress, Coulomb friction: standard textbook mechanics; first-order use only.
- EN 10025-2 (structural steel yield), EN 338 (C16 timber strength): as cited in HPL-CAL-001; values not re-read this session.
- Marlow Ropes, D/Braid PES 14 mm white, minimum break load 5,570 kg, <https://shop.marlowropes.com/d-3-braid-pes-14mm-white-100mr-kb2040>, checked 2026-11-03.
- iRopes, Exploring 14mm polyester rope for versatile applications, about 4,700 kg, <https://www.iropes.com/blog/insights-4/exploring-14mm-polyester-rope-for-versatile-applications-650>, checked 2026-11-03.
- ATSDR, Landfill Gas Primer, chapter 3 (2001), <https://www.atsdr.cdc.gov/HAC/landfill/html/ch3.html>, checked 2026-11-03.
- CDC, Clinical Guidance for Wound Management to Prevent Tetanus, <https://www.cdc.gov/tetanus/hcp/clinical-guidance/>, checked 2026-11-03.
