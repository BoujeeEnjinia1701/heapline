---
doc_id: HPL-DEC-001
title: HeapLine design decisions register
project: HeapLine
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
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
  change: The four requirement decisions decided by Amish as recommended (HPL-DDR-003) and moved to decisions made; three new questions proposed, awaiting Amish
---

# HeapLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set HeapLine's safety case (lookout and stop rule, capstan overload limit, holding, anchors, what the capstan may pull, blunt probes, no lithium cells). Each took the conservative option; the evidence that would relax it is in HPL-DDR-001, Table 1.

## Open decisions

The four requirement decisions of the TRL 3 review were decided by Amish on 2026-10-03 (HPL-DDR-003) and are listed under Decisions made. Carrying them into the design raised the three questions below; the state and the effect of each option are set out in `docs/REVIEW.md`, Session 2026-10-03: round 2 requirement decisions applied.

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 5 | How many neighbouring sites share one capstan set, and how far apart they may be | A: up to three sites within 300 m of the shed that keeps it. B: two sites within 300 m. C: up to four sites within 500 m | A. Proposed, awaiting Amish | Number of capstan sets built; drill card wording | HPL-DDR-003, item 4; REVIEW.md |
| 6 | R8 target wording, which still says "whole kit carried by four people" while two waves use seven | A: restate R8 as no item over 25 kg and no carrier over 25 kg, with the search kit carried by four people in the first wave. B: keep the wording and report R8 as met for each wave | A. Proposed, awaiting Amish | Requirements and drill card only | HPL-DDR-003, item 3; REVIEW.md |
| 7 | Site box where no sound reused crate is found | A: make the plywood box (HPL-DWG-115 and 116). B: buy a steel job box with the same inside size | A. Proposed, awaiting Amish | Site box (section 3.15 and 3.16 of the build plan) | HPL-DDR-003, item 4; REVIEW.md |

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
| 8 | Inside size, soundness and dryness of each reused crate | The packing of HPL-DWG-002 needs an inside of at least 1664 x 984 x 1042 mm; R7 assumes a sound, painted box | HPL-DDR-003, item 4 |
| 9 | PPE issued from the cooperative's stock meets line 26 of the bill of materials | Gloves, boots, masks and glasses are part of the safety case on sharp waste | HPL-DDR-003, item 4 |

## Value engineering

Value-engineering target: USD 1,800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 830.00 a site plus a share of one USD 449.00 capstan set per group of neighbouring sites (USD 970.00 under the target before the share; USD 979.67 a site if three sites share). R9's USD 400 a site is still not met. Main cost drivers and savings worth trying:

- The capstan set (frame, drum, ratchets, head, pawls, bars, bushes, roller, keeper, pins, stakes, rope, slings and clamp) is USD 449, now shared by neighbouring sites (HPL-DDR-003).
- The site box with its hardware is USD 101 as a reused crate refit (estimate), USD 253 where the plywood box is made.
- Lighting is USD 95; PPE (USD 168 new) comes from the cooperative's stock.
- Bought lifting gear (slings and shackles, USD 66) and the rope (USD 72) stay at rated grades because they carry the safety case.
- Savings worth trying: buying the search core in bulk across cooperatives; profile cutting the ratchets and pawls for several kits at once; a local turner for the probe tips.

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
| 2026-10-03 | R2: 18 mm tip on all six probes (option A), confirmed on a test heap at TRL 4 | Amish: "i approve all of the 47 recommendations provided by you. Execute them." | HPL-DDR-003, item 1 |
| 2026-10-03 | R5: drill card rule, four haulers on debris, two only along the boards (option A) | Amish, same approval | HPL-DDR-003, item 2 |
| 2026-10-03 | R8: two waves, four with the search kit, then three with the capstan set (option A) | Amish, same approval | HPL-DDR-003, item 3 |
| 2026-10-03 | R9: one capstan set shared by neighbouring sites, and a reused crate or bought job box with PPE from the cooperative's stock (option C); R9 still not met at about USD 830 a site | Amish, same approval | HPL-DDR-003, item 4 |

## Change log

- 2026-10-03 (v0.2): open decisions 1 to 4 decided by Amish as recommended (HPL-DDR-003) and moved to Decisions made; new open decisions 5 to 7 and items 8 and 9 to confirm added; value engineering updated.
