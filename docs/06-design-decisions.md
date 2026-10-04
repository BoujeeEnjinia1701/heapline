---
doc_id: HPL-DEC-001
title: HeapLine design decisions register
project: HeapLine
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-04'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; design decisions made under Amish's pre-approvals of 2026-10-03; four requirement decisions proposed, awaiting Amish
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Requirement decisions 20A, 21A, 22A and 23C made by Amish (HPL-DDR-003); one new open decision on how far apart sites sharing a capstan may be"
- version: "0.3"
  date: '2026-10-04'
  author: Amish Chadha
  change: "Open decision 1 decided by Amish (round-3 decision 3A, HPL-DDR-004) and moved to Decisions made; no open decisions"
---

# HeapLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set HeapLine's safety case (lookout and stop rule, capstan overload limit, holding, anchors, what the capstan may pull, blunt probes, no lithium cells). Each took the conservative option; the evidence that would relax it is in HPL-DDR-001, Table 1.

## Open decisions

None. The four requirement decisions of 2026-10-03 and the siting limit for a shared capstan (decided 2026-10-04) are all under Decisions made.

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
| 8 | Inside sizes and soundness of the reused crates found | The search crate must be at least 1604 x 824 x 622 mm inside and the capstan crate 904 x 864 x 1042 mm; a bought job box costs more | HPL-DWG-002; BOM lines 1 and 31 |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,374.00 (USD 426.00 under the target), for the host site, which keeps a search kit and the shared capstan set. Each other site's search kit costs USD 827.00, against the restated R9 target of USD 850 (HPL-DDR-003). Main cost drivers and savings worth trying:

- The shared capstan set (frame, drum, ratchets, head, pawls, bars, bushes, roller, keeper, pins, stakes, rope, slings, clamp and its crate) is USD 547, once per group of neighbouring sites.
- The search core (boards, links, probes, pins, shovels, stretcher, lookout kit and cards) is USD 526 a site.
- The reused search crate with its hardware is USD 98 a site; a bought steel job box would add about USD 200 to 500.
- Lighting is USD 95 a site; PPE comes from the cooperative's stock (about USD 168 if bought).
- Bought lifting gear (slings and shackles, USD 66) and the rope (USD 72) stay at rated grades because they carry the safety case.
- Savings worth trying: buying lamps in bulk across cooperatives; profile cutting the ratchets and pawls for several capstan sets at once; a local turner for the probe tips.

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
| 2026-10-03 | R2: 18 mm probe tips on all six probes, confirmed on a test heap at TRL 4 (decision 20A) | Amish: "i agree with all the 46 recommendations you provided. please proceed." | [HPL-DDR-003](decisions/0003-requirement-decisions.md) |
| 2026-10-03 | R5: drill-card rule of four haulers on debris, two only along the boards (decision 21A) | Amish, same words | HPL-DDR-003 |
| 2026-10-03 | R8: the kit carried in two waves, the search kit first and the capstan set second (decision 22A) | Amish, same words | HPL-DDR-003 |
| 2026-10-03 | R9: one capstan set shared by neighbouring sites, a reused crate or bought job box, PPE from the cooperative's stock; R9 restated to USD 850 per site search kit (decision 23C) | Amish, same words | HPL-DDR-003 |
| 2026-10-04 | Open decision 1, R8 and R9 (3A): a shared capstan serves only sites within about 500 m walk of the host shed (capstan within about 15 min); farther sites keep their own capstan set or rely on the search kit alone; checked in the TRL 4 timed drills | Amish: "For round 3, I agree with all your proposed recommendations" | HPL-DDR-004 |
