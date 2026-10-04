---
doc_id: HPL-REQ-001
title: HeapLine requirements
project: HeapLine
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-04'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
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
---

# HeapLine requirements

Requirements for the site-kept slide-rescue kit. Targets are unchanged from the scaffold except R9, restated on 2026-10-03; R10 and R11 were added at TRL 2 (HPL-DDR-001). Results are paper estimates from HPL-CAL-001 v0.2 on the constructable design, not test results.

On 2026-10-03 Amish decided the four requirement decisions put to him at TRL 3 as recommended: "i agree with all the 46 recommendations you provided. please proceed." For HeapLine these are 20A (R2), 21A (R5), 22A (R8) and 23C (R9), recorded in HPL-DDR-003. On 2026-10-04 Amish decided option 3A on how far apart sites may share a capstan: "For round 3, I agree with all your proposed recommendations". A shared capstan serves only sites within about 500 m walk of the host shed (HPL-DDR-004); farther sites keep their own capstan set or rely on the search kit alone.

> **Safety:** HeapLine is used on unstable ground where a second slide can bury the searchers. It is published as an open engineering reference, not certified rescue equipment. The capstan stores energy in its rope; the overload limit (R10) and the holding pawls (R11) are safety requirements.

*Table 1. Requirements and their status at TRL 3.*

| ID | Requirement | Target | Verification (TRL 4 or later) | Result on paper (HPL-CAL-001) | Status |
| --- | --- | --- | --- | --- | --- |
| R1 | Deploy fast | Kit carried 100 m (330 ft) and first probe line started within 5 minutes of the alarm | Timed drills with the partner cooperative | 4.6 min estimated: run to the shed, open, carry the search wave back, post the lookout, lay boards while probes are joined | Met on paper |
| R2 | Probe depth | Probes reach at least 2.5 m (8.2 ft) into loose waste | Probe trials on a waste test heap, including whether the sleeve friction rises with the 18 mm tip's smaller clearance | 18 mm tip on all six probes (decision 20A). Loosened debris: 2.6 m (full usable depth) by one person. Stiffer debris: 2.6 m by two people, 0.6 m by one | Met on paper; confirm on a test heap at TRL 4 |
| R3 | Crawl board support | Board carries a 100 kg (220 lb) searcher with sinkage under 50 mm on loose fill | Load tests on representative fill | 44 mm on very loose debris with a 1.5 dynamic factor; bridges a 0.8 m void at 4.0 MPa in the battens | Met on paper |
| R4 | Capstan pull | At least 5 kN (1,124 lbf) pull from a hand capstan on a ground anchor | Pull test on CalRig | 5 kN with four people at 114 N each; the shear pin releases at about 6.4 kN (5.1 to 7.6 kN over a batch) | Met on paper |
| R5 | Casualty transport | Sheet stretcher moves a 100 kg (220 lb) casualty 30 m (98 ft) over debris with two to four haulers | Drill with manikin | Drill-card rule (decision 21A): four haulers on debris, 127 N each on level debris; two haulers only along the boards, 153 N each | Met on paper under the drill-card rule |
| R6 | Stop rule understood | All drill participants state the stop signals correctly after training | Post-drill check | Six stop signals printed on the lid and on pocket cards | Not verifiable at TRL 3 |
| R7 | Storage life | All items usable after 12 months stored in the site box | Annual inspection log at the pilot site | Exterior plywood, painted or galvanised steel, UV-stabilised HDPE, acetal, polyester; alkaline cells stored out of the lamps; no lithium cells | Met on paper by material choice |
| R8 | Portable | No single item over 25 kg (55 lb); whole kit carried by four people | Weighing; timed carry in two waves | Heaviest carried item 21.2 kg (capstan frame). Carried in two waves (decision 22A): four people carry the search kit first, 21.5 kg each; a second group of three brings the capstan set, 21.7 kg each | Met in two waves |
| R9 | Cost | Restated 2026-10-03 (decision 23C): parts at most USD 850 per site search kit, with one capstan set shared by neighbouring sites and costed per group, a reused crate (or bought job box) and PPE from the cooperative's stock. Was: parts under USD 400 per site kit | Costed bill of materials | USD 827 per site search kit; shared capstan set with its crate USD 547 per group (USD 274 a site if two share it) | Met as restated |
| R10 | Overload limit | Rope tension limited so the rope, capstan and anchor are never loaded past the 8 kN design tension | Shear pin release tests on a batch (TRL 4) | 6 mm S275 shear pin releases at 6.4 kN nominal, 7.6 kN at the top of the batch spread; rope factor 4.5 at 8 kN | Met on paper |
| R11 | Holds when let go | The drum cannot run back when the bars are released | Release test at working pull (TRL 4) | Two holding pawls on a 24-tooth ring; one pawl takes the design tension at 77 MPa tooth bearing | Met on paper |

## Assumptions

- Pickers and neighbours will organise a search in the first minutes if they have tools and a plan.
- Burial depths in the first minutes of a slide are within reach of hand probes and shovels in at least some cases.
- Sites or cooperatives can keep a box secure and inspected.
- Formal responders will welcome an organised community search rather than stop it.
- A sound anchor (a tree, a parked vehicle or a structural column) can be found on firm ground near most dumpsites; where none exists the capstan is not used.
- Debris resistance to probing has no published data for dumpsite slides; HPL-CAL-001 brackets it with a loosened and a stiffer case.
- Neighbouring sites that share one capstan set are close enough for its second wave to arrive while the search is still under way; a shared capstan serves only sites within about 500 m walk of the host shed (Amish, 2026-10-04, decision 3A: "For round 3, I agree with all your proposed recommendations"; HPL-DDR-004), checked in the TRL 4 timed drills.
- The cooperative keeps PPE in stock for the kit and replaces what is used.
