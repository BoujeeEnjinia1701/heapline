---
doc_id: HPL-PRS-001
title: HeapLine product requirements and specifications
project: HeapLine
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold (as HPL-REQ-001)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2; concept status for each requirement; R10 (overload limit) and R11 (holds when let go) added under HPL-DDR-001
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 results from HPL-CAL-001 on the constructable design (HPL-DDR-002); R2, R5 and R8 at risk and R9 not met, with decisions for Amish in docs/REVIEW.md
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish's requirement decisions 20A, 21A, 22A and 23C (HPL-DDR-003): R2 met with the 18 mm tip; R5 met under the four-hauler rule; R8 met in two waves; R9 restated to USD 850 per site search kit with one capstan set shared by neighbouring sites"
- version: "0.5"
  date: '2026-10-04'
  author: Amish Chadha
  change: "Siting limit for a shared capstan set decided by Amish (round-3 decision 3A, HPL-DDR-004); targets and results unchanged"
- version: "0.6"
  date: '2026-11-03'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: migrated to the PRS format (PR-001 to PR-011 are R1 to R11, same targets; PR-012 to PR-015 added from the user requirements); document ID HPL-REQ-001 becomes HPL-PRS-001; every PR traces to a user requirement in HPL-URS-001"
---

# HeapLine product requirements and specifications

What the kit must do, each requirement traced to a user need in the URS (`03a-user-requirements.md`). PR-001 to PR-011 are the earlier requirements R1 to R11 with unchanged targets (column "Was"); PR-012 to PR-015 were added so that every user requirement has a product requirement. Results are paper estimates from HPL-CAL-001 on the constructable design, not test results.

On 2026-10-03 Amish decided the four requirement decisions put to him at TRL 3 as recommended: "i agree with all the 46 recommendations you provided. please proceed." For HeapLine these are 20A (PR-002), 21A (PR-005), 22A (PR-008) and 23C (PR-009), recorded in HPL-DDR-003. On 2026-10-04 Amish decided option 3A on how far apart sites may share a capstan: "For round 3, I agree with all your proposed recommendations". A shared capstan serves only sites within about 500 m walk of the host shed (HPL-DDR-004); farther sites keep their own capstan set or rely on the search kit alone.

> **Safety:** HeapLine is used on unstable ground where a second slide can bury the searchers. It is published as an open engineering reference, not certified rescue equipment. The capstan stores energy in its rope; the overload limit (PR-010) and the holding pawls (PR-011) are safety requirements.

*Table 1. Product requirements and specifications.*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Deploy fast | Kit carried 100 m (330 ft) and first probe line started within 5 minutes of the alarm | 5 | max | min after the alarm | Timed drills with the partner cooperative | Met on paper | R1 |
| PR-002 | UR-002 | Performance | Probe depth | Probes reach at least 2.5 m (8.2 ft) into loose waste | 2.5 | min | m | Probe trials on a waste test heap, including whether the sleeve friction rises with the 18 mm tip's smaller clearance | Met on paper | R2 |
| PR-003 | UR-003 | Performance | Crawl board support | Board carries a 100 kg (220 lb) searcher with sinkage under 50 mm on loose fill | 50 | max | mm sinkage | Load tests on representative fill | Met on paper | R3 |
| PR-004 | UR-004 | Performance | Capstan pull | At least 5 kN (1,124 lbf) pull from a hand capstan on a ground anchor | 5 | min | kN | Pull test on CalRig | Met on paper | R4 |
| PR-005 | UR-005 | Performance | Casualty transport | Sheet stretcher moves a 100 kg (220 lb) casualty 30 m (98 ft) over debris with two to four haulers | 30 | min | m, 100 kg casualty | Drill with manikin | Met on paper under the drill-card rule | R5 |
| PR-006 | UR-006, UR-012 | Usability | Stop rule understood | All drill participants state the stop signals correctly after training | 100 | min | % of participants | Post-drill check | To verify at TRL 4 | R6 |
| PR-007 | UR-007 | Materials | Storage life | All items usable after 12 months stored in the site box | 12 | min | months | Annual inspection log at the pilot site | Met by design | R7 |
| PR-008 | UR-008 | Packaging and transport | Portable | No single item over 25 kg (55 lb); whole kit carried by four people | 25 | max | kg per item | Weighing; timed carry in two waves | Met on paper in two waves | R8 |
| PR-009 | UR-009 | Performance | Cost | Restated 2026-10-03 (decision 23C): parts at most USD 850 per site search kit, with one capstan set shared by neighbouring sites and costed per group, a reused crate (or bought job box) and PPE from the cooperative's stock. Was: parts under USD 400 per site kit | 850 | max | USD per site search kit | Costed bill of materials | Met on paper as restated | R9 |
| PR-010 | UR-010 | Safety | Overload limit | Rope tension limited so the rope, capstan and anchor are never loaded past the 8 kN design tension | 8 | max | kN rope tension | Shear pin release tests on a batch (TRL 4) | Met on paper | R10 |
| PR-011 | UR-010 | Safety | Holds when let go | The drum cannot run back when the bars are released | 0 | max | turns of drum run-back | Release test at working pull (TRL 4) | Met on paper | R11 |
| PR-012 | UR-014 | Usability | Light without power | Searchers carry head lamps and hand lamps that take AA alkaline cells, with the cells stored out of the lamps | 8 | min | lamps (six head, two hand) | Inspection at the monthly check (BOM line 25) | Met by design | New |
| PR-013 | UR-011 | Materials | Repair with common stock | Every made part is steel tube or bar, timber, board, plastic sheet or rope that a local workshop holds | all | min | made parts | Review of the BOM and HPL-BLD-001 | Met by design | PRB constraint |
| PR-014 | UR-013 | Safety | Not certified equipment | The README, the drill card and every drawing state that HeapLine is an open engineering reference, not certified rescue equipment | all | min | documents | Document review | Met by design | New |
| PR-015 | UR-015 | Performance | Shared capstan arrival | A capstan set kept at a host shed reaches a site within about 500 m walk while the search is under way | 15 | max | min after the alarm | Timed capstan wave drill at TRL 4 | Met on paper | Decision 3A (HPL-DDR-004) |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4. Tolerance "min" means the target is the least acceptable value, "max" the greatest. Requirements met "on paper" are first-order estimates; verification is at TRL 4 or later.

PR-009 as restated (decision 23C): parts at most USD 850 per site search kit, with one capstan set shared by neighbouring sites and costed per group, a reused crate (or bought job box) and PPE from the cooperative's stock. It was: parts under USD 400 per site kit.

*Table 2. Results on paper (HPL-CAL-001).*

| Requirement | Result |
| --- | --- |
| PR-001 | 4.6 min estimated: run to the shed, open, carry the search wave back, post the lookout, lay boards while probes are joined |
| PR-002 | 18 mm tip on all six probes (decision 20A). Loosened debris: 2.6 m (full usable depth) by one person. Stiffer debris: 2.6 m by two people, 0.6 m by one |
| PR-003 | 44 mm on very loose debris with a 1.5 dynamic factor; bridges a 0.8 m void at 4.0 MPa in the battens |
| PR-004 | 5 kN with four people at 114 N each; the shear pin releases at about 6.4 kN (5.1 to 7.6 kN over a batch) |
| PR-005 | Drill-card rule (decision 21A): four haulers on debris, 127 N each on level debris; two haulers only along the boards, 153 N each |
| PR-006 | Six stop signals printed on the lid and on pocket cards |
| PR-007 | Exterior plywood, painted or galvanised steel, UV-stabilised HDPE, acetal, polyester; alkaline cells stored out of the lamps; no lithium cells |
| PR-008 | Heaviest carried item 20.9 kg (capstan frame). Carried in two waves (decision 22A): four people carry the search kit first, 21.5 kg each; a second group of three brings the capstan set, 21.4 kg each |
| PR-009 | USD 827 per site search kit; shared capstan set with its crate USD 547 per group (USD 274 a site if two share it) |
| PR-010 | 6 mm S275 shear pin releases at 6.4 kN nominal, 7.6 kN at the top of the batch spread; rope factor 4.5 at 8 kN |
| PR-011 | Two holding pawls on a 24-tooth ring; one pawl takes the design tension at 77 MPa tooth bearing |
| PR-012 | Six head lamps and two hand lamps on AA cells; no lithium cells in the box (BOM line 25) |
| PR-013 | Steel tube and bar, plywood, timber, HDPE sheet, acetal and polyester rope throughout (bom/bom.csv) |
| PR-014 | Safety notes in the PRB, README, drill card and drawing title blocks |
| PR-015 | 14.8 min from 500 m walk, 3.8 min from 100 m (HPL-CAL-001 [F4]) |

Requirements not met: none on paper. PR-006 (stop rule understood) cannot be verified before the drills at TRL 4. The value-engineering target of USD 1,800 (`budget_usd`) is met by the estimated USD 1,374 for the host site.

## Assumptions

- Pickers and neighbours will organise a search in the first minutes if they have tools and a plan.
- Burial depths in the first minutes of a slide are within reach of hand probes and shovels in at least some cases.
- Sites or cooperatives can keep a box secure and inspected.
- Formal responders will welcome an organised community search rather than stop it.
- A sound anchor (a tree, a parked vehicle or a structural column) can be found on firm ground near most dumpsites; where none exists the capstan is not used.
- Debris resistance to probing has no published data for dumpsite slides; HPL-CAL-001 brackets it with a loosened and a stiffer case.
- Neighbouring sites that share one capstan set are close enough for its second wave to arrive while the search is still under way; a shared capstan serves only sites within about 500 m walk of the host shed (Amish, 2026-10-04, decision 3A: "For round 3, I agree with all your proposed recommendations"; HPL-DDR-004), checked in the TRL 4 timed drills.
- The cooperative keeps PPE in stock for the kit and replaces what is used.
