---
doc_id: HPL-CAL-001
title: HeapLine sizing calculations
project: HeapLine
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First sizing note on the constructable design (HPL-DDR-002); capstan, probe, crawl board, stretcher, clamp, masses, deployment time and cost
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Round 2 requirement decisions (HPL-DDR-003); 18 mm probe tip, drill card haul rule, two carrying waves, shared capstan set with a reused crate box and PPE from stock; R2, R5 and R8 met on paper, R9 still not met
---

# HeapLine sizing calculations

The constructable design, with Amish's round 2 decisions of 2026-10-03 (HPL-DDR-003), meets R1, R2, R3, R4, R5, R8, R10 and R11 on paper. R2 is met with the 18 mm probe tip when two people push in stiffer debris, to be confirmed on a test heap at TRL 4; R5 is met under the drill card rule of four haulers on debris and two only along the boards; R8 is met for each of two carrying waves. R9 (cost) is still not met at USD 830 a site with a shared capstan set. Every figure below is printed by `docs/04-calcs/sizing.py` with the tag shown in brackets, from the geometry in `cad/src/model.py` and the prices in `bom/bom.csv`. These are first-principles estimates for a paper proof of concept, not test results.

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
| Sleeve friction with the 18 mm tip | Unchanged from the 22 mm tip | The tip is now 1 mm wider than the tube each side, not 3 mm; to be confirmed on a test heap at TRL 4 |
| Subgrade modulus of slide debris | 0.10 MN/m³ | Very loose, low side |
| Searcher on a board | 100 kg with a 1.5 dynamic factor | Kneeling and shifting weight |
| Timber battens | C16: 16 MPa bending, 8 GPa modulus | Treated softwood |
| Stretcher friction | 0.5 on debris, 0.3 on boards | HDPE on mixed waste and on plywood |
| Sustained pull per hauler | 200 N | Strap over the shoulder, 30 m |
| Carry limit per person | 25 kg | 100 m over rough ground |
| Carrying | Two waves: four people with the search kit, then three with the capstan set | Drill card rule, HPL-DDR-003 |
| Per-site cost | Lines bought for every site only; the capstan set is shared by neighbouring sites and PPE comes from the cooperative's stock | HPL-DDR-003; the cost basis of each line is in `bom/bom.csv` |
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

R2 is met on paper with the 18 mm tip (HPL-DDR-003): one person in loosened debris and two people in stiffer debris reach the full 2.6 m usable depth.

- Loosened debris: tip 102 N, friction 50 N per metre, 227 N to push to 2.5 m; one person reaches the full 2.6 m usable depth [B1c].
- Stiffer debris: tip 254 N, friction 151 N per metre, 631 N to push to 2.5 m. Two people reach the full 2.6 m; one person reaches 0.6 m, held back by the friction along the probe [B1s].
- The 16 x 2.0 tube buckles at 4,558 N with 1 m free, 1,139 N with 2 m free and 506 N with 3 m free (pinned ends) [B2-1, B2-2, B2-3].
- The probe is 3,068 mm long assembled and weighs 3.07 kg; the 18 mm tip has a 3 mm rounded point and is 1 mm wider than the tube each side; usable depth is about 2.6 m with the handle at chest height above the surface [B3].
- For comparison, the 22 mm tip used before HPL-DDR-003 needed 380 N to start in stiffer debris: one person could not start the probe and two reached 1.8 m [B4]. The 18 mm result holds only if the sleeve friction does not rise as the tip's clearance over the tube falls from 3 mm to 1 mm a side; that is the condition of the decision, checked on a test heap at TRL 4.

## C. Crawl boards

R3 is met on paper.

- A kneeling 100 kg searcher with a 1.5 dynamic factor, plus the 9.7 kg board, spread over 0.8 m of board gives 4.4 kPa and 44 mm of sinkage on very loose debris [C1].
- Bridging a 0.8 m void with 1,472 N at mid-span gives 294 N m; the battens alone see 4.0 MPa (factor 4.0 on C16) and deflect 0.8 mm [C2].
- The deck spans 300 mm clear between the battens; a 1,000 N knee on 150 mm of deck gives 13.3 MPa in 15 mm plywood [C3].
- Each board weighs 9.7 kg and each link plate 0.43 kg [C4].

## D. Sheet stretcher

R5 is met on paper under the drill card rule (HPL-DDR-003): four haulers whenever the stretcher crosses debris, two only along the boards, where each pulls 153 N, within the 200 N sustained pull.

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
| Probes (6) | 18.4 kg |
| Shovels (4) | 9.2 kg |
| Sheet stretcher | 3.9 kg |
| Lookout kit, lighting, PPE, bags and cards | 13.5 kg |

- The heaviest carried item is the capstan frame with its post and roller, 21.2 kg; the site box (83 kg body, 21 kg lid) stays at the shed [F1].
- The carried kit is 151 kg: 86 kg for the search wave and 65 kg for the capstan wave. Four people carrying everything at once would take 37.7 kg each [F2].
- R8 is met on paper in two waves (HPL-DDR-003): four people carry the search wave at 21.5 kg each, and a second group of three brings the capstan wave at 21.7 kg each, both under the 25 kg carry limit [F2a]. The capstan is not needed for the first probe line, so R1 is unchanged. Where the shared capstan set is kept at a neighbouring site, its wave comes from that site's shed and arrives later; the distance is an open decision.
- Deployment from the alarm to the first probe line: 40 s to run 100 m to the shed, 30 s to open, 125 s to carry back, 20 s to post the lookout and 60 s to lay the first boards while the probes are joined: 275 s, 4.6 min [F3].

## G. Cost

R9 is not met. Under HPL-DDR-003 one capstan set is shared by neighbouring sites, the site box is a reused crate refitted, and PPE is issued from the cooperative's own stock; each BOM line carries its cost basis.

- Parts bought for each site: USD 830.00. The reused crate box with its hardware is USD 101.00 (USD 253.00 for the made plywood box before), lighting USD 95.00, and PPE from stock would be USD 168.00 if bought new [G1].
- The shared capstan set with its rope, slings and clamp is USD 449.00 for each group of sites. With its share the cost is USD 1,279.00 a site if not shared, USD 1,054.50 shared by two, USD 979.67 by three and USD 942.25 by four [G1-1 to G1-4].
- Every line at its listed price, as for one prototype kit with its own capstan set and new PPE, is USD 1,447.00 [G1b].
- The search core (boards, links, probes, pins, shovels, stretcher, lookout kit and cards) is USD 526.00 [G2].
- Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 830.00 a site plus a share of the USD 449.00 capstan set (USD 970.00 under the target before the share) [G3]. Against R9's USD 400 a site it is still not met.

## Results against the requirements

*Table 4. Results (also written to `docs/04-calcs/results.csv`).*

| ID | Result | Status |
| --- | --- | --- |
| R1 | 4.6 min estimated from alarm to first probe line | Met on paper |
| R2 | 18 mm tip: loosened debris 2.6 m by one person; stiffer debris 0.6 m for one, 2.6 m for two | Met on paper; confirm on a test heap at TRL 4 |
| R3 | 44 mm sinkage; bridges a 0.8 m void at 4.0 MPa | Met on paper |
| R4 | 5 kN at 114 N each for four people; pin releases at 5.1 to 7.6 kN | Met on paper |
| R5 | 127 N each for four on level debris; 153 N each for two along the boards | Met on paper under the drill card rule |
| R6 | Stop rule printed on the lid and pocket cards | Not verifiable at TRL 3 |
| R7 | Weather-resistant materials if the reused crate is sound and painted; no lithium cells | Met on paper by material choice |
| R8 | Heaviest item 21.2 kg; two waves: 21.5 kg each for four, then 21.7 kg each for three | Met on paper for each wave |
| R9 | USD 830 a site plus a share of the USD 449 capstan set | Not met |
| R10 | Pin releases at 6.4 kN nominal, 7.6 kN at most; rope factor 4.5 at 8 kN | Met on paper |
| R11 | Two holding pawls; one takes the design tension | Met on paper |
