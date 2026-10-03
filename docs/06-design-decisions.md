---
doc_id: HPL-DEC-001
title: HeapLine design decisions register
project: HeapLine
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; four requirement decisions proposed, awaiting Amish
---

# HeapLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set HeapLine's safety case (lookout and stop rule, capstan overload limit, holding, anchors, what the capstan may pull, blunt probes, no lithium cells). Each took the conservative option; the evidence that would relax it is in HPL-DDR-001, Table 1.

## Open decisions

The four requirements that are at risk or not met on paper are Amish's to decide (Amish, 2026-10-03: "A simple statement doesn't add value - ensure you are identifying a state and posing it as a clear recommendation for me to decide on."). The state and the effect of each option are set out in `docs/REVIEW.md`, TRL 3, Decisions for Amish.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | R2 probe depth, at risk in stiffer debris | A: 18 mm tip on all six probes. B: three probes with 22 mm tips and three with 18 mm tips. C: keep the 22 mm tip and measure debris resistance on a test heap first | A, confirmed on a test heap at TRL 4. Proposed, awaiting Amish | Probe tip turning (section 3.3) | HPL-CAL-001, B; REVIEW.md |
| 2 | R5 casualty transport, at risk with two haulers on debris | A: drill card rule of four haulers on debris, two only along the boards. B: add a 10 m haul line with shoulder loops. C: both | A. Proposed, awaiting Amish | Drill card wording; line 24 if B | HPL-CAL-001, D; REVIEW.md |
| 3 | R8 portable, at risk for four people in one trip | A: two waves, the search kit first and the capstan set by a second group. B: lighter boards. C: a two-wheeled handcart | A. Proposed, awaiting Amish | Drill card and carry bags; board battens if B | HPL-CAL-001, F; REVIEW.md |
| 4 | R9 cost, not met | A: one capstan set shared by neighbouring sites. B: a reused crate or bought job box and PPE from the cooperative's stock. C: both | C. Proposed, awaiting Amish | Box and capstan sets per site | HPL-CAL-001, G; REVIEW.md |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Release load of the shear pins from the bar actually bought | The 6 mm pin is sized on 258 MPa shear; the lower end of its band must stay above 5 kN (R4) and the upper end below 8 kN (R10) | HPL-CAL-001, A4 |
| 2 | Breaking strength of the rope and its splice | Factor 4.5 at 8 kN assumes 40 kN and 90 % at the splice | HPL-CAL-001, A5 |
| 3 | Working load limits and pin sizes of the slings and shackles bought | The anchor eye's 22 mm hole is drilled for a 19 mm shackle pin | HPL-DWG-104 |
| 4 | Outside sizes of the tubes bought (60.3, 76.1, 88.9, 114.3) | The acetal bushes are turned to the bores | HPL-DWG-110 |
| 5 | Plywood thickness and the C16 grade of the battens | Board sinkage and void bridging assume 15 mm plywood on 45 x 70 C16 | HPL-CAL-001, C |
| 6 | Friction of the HDPE sheet bought on boards and mixed waste | The haul forces of R5 assume 0.3 and 0.5 | HPL-CAL-001, D |
| 7 | Sizes of the carry bags | The packing layout in HPL-DWG-002 uses their outer sizes | HPL-DWG-002 |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,599.00 (USD 201.00 under the target). Main cost drivers and savings worth trying:

- The capstan set (frame, drum, ratchets, head, pawls, bars, bushes, roller, keeper, pins, stakes, rope, slings and clamp) is USD 449, the largest block.
- The site box with its hardware is USD 253; it only has to keep the kit dry and locked.
- PPE and lighting together are USD 263.
- Bought lifting gear (slings and shackles, USD 66) and the rope (USD 72) stay at rated grades because they carry the safety case.
- Savings worth trying: a reused crate or steel job box for the site box; buying PPE in bulk across cooperatives; profile cutting the ratchets and pawls for several kits at once; a local turner for the probe tips.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Vertical friction capstan pumped through a quarter turn with a drive ratchet, in place of the SiltHaul block or a walk-round capstan | Amish: "I pre-approve the batch runs along with any recommendations you come up with." and "Proceed with the remaining 15 scaffolds" | HPL-DDR-001, items 1, 14 |
| 2026-10-03 | 6 mm S275 shear pin limits the rope to about 6.4 kN; every part sized on 8 kN; R10 added | Amish, same pre-approvals | HPL-DDR-001, item 2 |
| 2026-10-03 | Two holding pawls on a ring at the drum's foot; tail made fast on a cleat when hauling stops; R11 added | Amish, same pre-approvals | HPL-DDR-001, item 3 |
| 2026-10-03 | Capstan anchored only by a sling to a sound tree, vehicle or column; stakes only against turning | Amish, same pre-approvals | HPL-DDR-001, item 4 |
| 2026-10-03 | 14 mm polyester double braid, 40 kN | Amish, same pre-approvals | HPL-DDR-001, item 5 |
| 2026-10-03 | The capstan pulls only sheeting, timber and debris sideways; never lifts, never pulls on a person | Amish, same pre-approvals | HPL-DDR-001, item 6 |
| 2026-10-03 | Sectional steel probes pushed by hand with a blunt tip; never driven | Amish, same pre-approvals | HPL-DDR-001, item 7 |
| 2026-10-03 | Plywood crawl boards on battens, linked end to end | Amish, same pre-approvals | HPL-DDR-001, item 8 |
| 2026-10-03 | Made HDPE sheet stretcher | Amish, same pre-approvals | HPL-DDR-001, item 9 |
| 2026-10-03 | AA alkaline lamps; no lithium cells in the box | Amish, same pre-approvals | HPL-DDR-001, item 10 |
| 2026-10-03 | No gas detector in the base kit; no flames; stop on any sign of gas | Amish, same pre-approvals | HPL-DDR-001, item 11 |
| 2026-10-03 | Six-signal stop rule; lookout posted before anyone steps onto debris; safe zone to the side | Amish, same pre-approvals | HPL-DDR-001, item 12 |
| 2026-10-03 | First co-design candidate to approach: Uganda Red Cross Society in Kampala with the Kiteezi waste pickers (not agreed) | Amish, same pre-approvals | HPL-DDR-001, item 13 |
| 2026-10-03 | CalRig as the first candidate rig for capstan proof loads and pin release tests | Amish, same pre-approvals | HPL-DDR-001, item 14 |
| 2026-10-03 | Combination padlock on the site box; monthly inspection log | Amish, same pre-approvals | HPL-DDR-001, item 15 |
| 2026-10-03 | `budget_usd` kept at 1,800 as a value-engineering target | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | HPL-DDR-001, item 16 |
| 2026-10-03 | Design for construction: the fifteen changes of HPL-DDR-002 | Amish: "I pre-approve the batch runs along with any recommendations you come up with." and "Proceed with the remaining 15 scaffolds" | HPL-DDR-002 |
| 2026-10-03 | Appearance model additions for renders: rope turns on the drum, drill card on the lid, a mannequin beside the capstan | Amish, same pre-approvals | docs/REVIEW.md, TRL 3 |
