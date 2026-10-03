---
doc_id: HPL-CAL-001
title: HeapLine sizing calculations
project: HeapLine
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First sizing note on the constructable design (HPL-DDR-002); capstan, probe, crawl board, stretcher, clamp, masses, deployment time and cost
---

# HeapLine sizing calculations

The constructable design meets R1, R3, R4, R10 and R11 on paper. R2 (probe depth) is at risk in stiffer debris, R5 (casualty transport) is at risk with only two haulers on loose debris, R8 (portable) is at risk because the whole kit is too heavy for four people in one trip, and R9 (cost) is not met. Every figure below is printed by `docs/04-calcs/sizing.py` with the tag shown in brackets, from the geometry in `cad/src/model.py` and the prices in `bom/bom.csv`. These are first-principles estimates for a paper proof of concept, not test results.

> **Safety:** The capstan stores energy in a loaded rope. Every capstan part is sized on an 8 kN design tension, above the top of the shear pin's release band, and the rope, slings and anchor are chosen so the shear pin is always the weakest link. Searches take place on unstable ground; nothing here makes a dumpsite safe.

## Assumptions

*Table 1. Assumptions.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Bush friction, acetal on painted steel | 0.15 | Dry or dusty; low-friction acetal would be about 0.1 |
| Rope friction on the drum | 0.20 | Polyester on painted steel, low side, so the tail force is not underestimated |
| Rope turns on the drum while hauling | 4 | Ship and rescue capstan practice |
| Shear pin material | S275 bar, ultimate shear 258 MPa (0.6 x 430 MPa) | Release spread taken as plus or minus 20 % over a batch |
| Design tension for every capstan part | 8,000 N | Above the top of the pin's release band (7,648 N) |
| Sustained push per person on a bar | 150 N | Short bouts; heaving can reach 300 to 400 N |
| Probe resistance, loosened debris | Cone 0.4 MPa, sleeve friction 1 kPa | No published data for dumpsite slides; a central case |
| Probe resistance, stiffer debris | Cone 1.0 MPa, sleeve friction 3 kPa | A compacted or wet case |
| Downward push on a probe | 350 N one person, 650 N two | Sustained, leaning on the T handle |
| Subgrade modulus of slide debris | 0.10 MN/m³ | Very loose, low side |
| Searcher on a board | 100 kg with a 1.5 dynamic factor | Kneeling and shifting weight |
| Timber battens | C16: 16 MPa bending, 8 GPa modulus | Treated softwood |
| Stretcher friction | 0.5 on debris, 0.3 on boards | HDPE on mixed waste and on plywood |
| Sustained pull per hauler | 200 N | Strap over the shoulder, 30 m |
| Carry limit per person | 25 kg | 100 m over rough ground |
| Walking speeds | 2.5 m/s running empty, 0.8 m/s carrying | Rough ground |

## A. Hand capstan

The capstan meets R4 with four people, and its shear pin bounds the rope tension (R10).

- The rope runs at a 64.2 mm radius on the drum; friction in the foot bush adds the equivalent of 4.5 mm of lever per newton of rope tension [A1].
- A 5,000 N pull needs 343 N m at the head: 228 N at each bar end, so 114 N each for four people (two on each bar) or 228 N each for two, with hands 754 mm from the axis [A2].
- With four turns the tailer holds about 33 N on the tail [A3].
- The 6 mm S275 shear pin on a 60 mm radius releases at 7.29 kN, 438 N m, which is a rope tension of about 6,374 N, between 5,099 and 7,648 N over a batch [A4]. The lower bound stays above the 5 kN of R4.
- The 14 mm polyester rope (40 kN, 36 kN through the splice) has a factor of 7.2 at 5,000 N and 4.5 at the 8,000 N design tension [A5].
- The rope leaves the drum 15 degrees down to the hold-down roller. The post carries 0.70 kN m at 8,000 N: 63 MPa in the 60.3 x 5.0 tube against a 355 MPa yield [A6].
- One holding pawl alone takes 5.5 kN at the design tension: 77 MPa bearing on a 12 x 6 mm tooth face and 49 MPa shear in its 12 mm pin [A7]. The drive pawl takes 5.9 kN at pin release: 62 MPa on the 12 x 8 mm tooth face [A8].
- Each 40 x 40 x 2.5 bar carries 219 N m at its socket when the pin releases: 50 MPa [A9].
- Each quarter-turn stroke takes in about 101 mm of rope, about 1.5 m a minute at 15 strokes [A10].
- The rope leaves under the roller 38 mm above the ground and the anchor sling pulls from the eye at the same height, so there is no tipping moment; the stakes only stop the frame turning and skating [A11].
- The 10 mm anchor eye sees 42 MPa bearing from the 19 mm shackle pin at 8,000 N; the 2,000 kg round sling has a factor of 2.5 on its working load limit at the design tension [A12].

## B. Probes

R2 is met in loosened debris and at risk in stiffer debris.

- Loosened debris: tip 152 N, friction 50 N per metre, 278 N to push to 2.5 m; one person reaches the full 2.6 m usable depth [B1c].
- Stiffer debris: tip 380 N, friction 151 N per metre, 757 N to push to 2.5 m. One person cannot start the probe; two reach 1.8 m, because the push is capped by the tip resistance and, near the surface, by the probe's buckling load [B1s].
- The 16 x 2.0 tube buckles at 4,558 N with 1 m free, 1,139 N with 2 m free and 506 N with 3 m free (pinned ends) [B2-1, B2-2, B2-3].
- The probe is 3,068 mm long assembled and weighs 3.10 kg; the 22 mm tip has a 3 mm rounded point; usable depth is about 2.6 m with the handle at chest height above the surface [B3].
- An 18 mm tip, one option for Amish's decision on R2, would let two people reach 2.6 m in the stiffer case and one person 0.6 m, if the sleeve friction does not rise as the tip's clearance over the tube falls from 3 mm to 1 mm a side [B4].

## C. Crawl boards

R3 is met on paper.

- A kneeling 100 kg searcher with a 1.5 dynamic factor, plus the 9.7 kg board, spread over 0.8 m of board gives 4.4 kPa and 44 mm of sinkage on very loose debris [C1].
- Bridging a 0.8 m void with 1,472 N at mid-span gives 294 N m; the battens alone see 4.0 MPa (factor 4.0 on C16) and deflect 0.8 mm [C2].
- The deck spans 300 mm clear between the battens; a 1,000 N knee on 150 mm of deck gives 13.3 MPa in 15 mm plywood [C3].
- Each board weighs 9.7 kg and each link plate 0.43 kg [C4].

## D. Sheet stretcher

R5 is met with four haulers and at risk with two on loose debris.

*Table 2. Haul force for a 100 kg casualty on the 3.9 kg stretcher [D].*

| Surface | Total | Each of two haulers | Each of four haulers |
| --- | --- | --- | --- |
| Debris, level | 510 N | 255 N | 127 N |
| Debris, 15 degrees up | 756 N | 378 N | 189 N |
| Boards, level | 306 N | 153 N | 76 N |
| Boards, 15 degrees up | 559 N | 280 N | 140 N |

## E. Sheet clamp

Four M12 wing bolts at 2.5 kN each, with two faces at a friction coefficient of 0.3, hold about 6.0 kN before the sheet slips [E1]. That is below the shear pin's nominal release; a sheet that slips out of the clamp is safe.

## F. Masses, carrying and deployment

*Table 3. Carried items [F].*

| Item | Mass |
| --- | --- |
| Capstan frame with post and roller | 21.2 kg |
| Capstan drum, head and ratchet | 15.3 kg |
| Capstan bars (2) | 5.4 kg |
| Stakes and mallet | 10.0 kg |
| Rope (30 m) | 4.1 kg |
| Slings, shackles and sheet clamp | 7.6 kg |
| Crawl board (each of 4) | 9.7 kg |
| Board link plates (8) | 3.5 kg |
| Probes (6) | 18.6 kg |
| Shovels (4) | 9.2 kg |
| Sheet stretcher | 3.9 kg |
| Lookout kit, lighting, PPE, bags and cards | 13.5 kg |

- The heaviest carried item is the capstan frame with its post and roller, 21.2 kg; the site box (83 kg body, 21 kg lid) stays at the shed [F1].
- The carried kit is 151 kg: 86 kg for the search wave and 65 kg for the capstan wave. Four people carrying everything at once would take 37.8 kg each; the search wave alone is 21.5 kg each [F2].
- Deployment from the alarm to the first probe line: 40 s to run 100 m to the shed, 30 s to open, 125 s to carry back, 20 s to post the lookout and 60 s to lay the first boards while the probes are joined: 275 s, 4.6 min [F3].

## G. Cost

- Parts for one site kit cost USD 1,599.00. The capstan with its rope, slings and clamp is USD 449.00, the box and its hardware USD 253.00, and PPE and lighting USD 263.00 [G1].
- The search core (boards, links, probes, pins, shovels, stretcher, lookout kit and cards) is USD 526.00 [G2].
- Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 1,599.00 (USD 201.00 under the target) [G3].

## Results against the requirements

*Table 4. Results (also written to `docs/04-calcs/results.csv`).*

| ID | Result | Status |
| --- | --- | --- |
| R1 | 4.6 min estimated from alarm to first probe line | Met on paper |
| R2 | Loosened debris 2.6 m by one person; stiffer debris 0 m for one, 1.8 m for two | At risk |
| R3 | 44 mm sinkage; bridges a 0.8 m void at 4.0 MPa | Met on paper |
| R4 | 5 kN at 114 N each for four people; pin releases at 5.1 to 7.6 kN | Met on paper |
| R5 | 127 N each for four on level debris; 255 N each for two | Met with four haulers; at risk with two on debris |
| R6 | Stop rule printed on the lid and pocket cards | Not verifiable at TRL 3 |
| R7 | Weather-resistant materials; no lithium cells | Met on paper by material choice |
| R8 | Heaviest item 21.2 kg; whole kit 37.8 kg each for four in one trip | At risk |
| R9 | USD 1,599 per site kit | Not met |
| R10 | Pin releases at 6.4 kN nominal, 7.6 kN at most; rope factor 4.5 at 8 kN | Met on paper |
| R11 | Two holding pawls; one takes the design tension | Met on paper |
