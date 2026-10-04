---
doc_id: HPL-DDR-003
title: HeapLine requirement decisions (R2, R5, R8, R9)
project: HeapLine
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's requirement decisions 20A, 21A, 22A and 23C carried out
---

# 0003: Requirement decisions on probe depth, casualty transport, carrying and cost

- **Date:** 2026-10-03
- **Status:** accepted
- **Decided by:** Amish Chadha, 2026-10-03, accepting every recommendation put to him in the second round of requirement decisions: "i agree with all the 46 recommendations you provided. please proceed." For HeapLine: 20A (R2), 21A (R5), 22A (R8) and 23C (R9).

> **Safety:** The 18 mm tip stays blunt, with a 3 mm rounded point, and probes are still never driven. The four-hauler rule keeps each hauler within a sustainable pull on loose debris, so a casualty is not dropped or dragged in jerks. Sharing the capstan changes only when it arrives; the capstan is never needed for the first probe line, and the rules on anchors, the shear pin and the rope line are unchanged.

## Context

At TRL 3 (HPL-CAL-001 v0.1) four requirements were at risk or not met on paper: R2, because two people reached only 1.8 m with the 22 mm tip in stiffer debris; R5, because two haulers on loose debris need 255 N each; R8, because the whole 151 kg kit is 37.8 kg each for four people in one trip; and R9, because the kit cost USD 1,599 against USD 400. Each was put to Amish as state, options and a recommendation in `docs/REVIEW.md`.

## Options considered

- **R2 (decision 20):** A (chosen): 18 mm tip on all six probes. B: three probes with each tip. C: keep 22 mm and measure first.
- **R5 (decision 21):** A (chosen): drill-card rule, four haulers on debris, two only along the boards. B: a haul line with shoulder loops. C: both.
- **R8 (decision 22):** A (chosen): two waves, the search kit first and the capstan set second. B: lighter boards. C: a handcart.
- **R9 (decision 23):** A: share one capstan set. B: reused crate or bought job box, and PPE from the cooperative. C (chosen): both, and restate the target.

## Decision

1. **20A.** Every probe tip is turned from 18 mm bar (35 mm cone to a 3 mm rounded point, 20 mm parallel, 30 mm spigot); BOM line 6, HPL-DWG-103, Figure 7.
2. **21A.** The drill card (BOM line 27) and the build plan say: four people haul the stretcher whenever it crosses debris; two may haul it only along the boards.
3. **22A.** The drill card and the build plan say: four people carry the search kit first; a second group of three brings the capstan set.
4. **23C.** Every site keeps its search kit in a reused timber crate (or a bought steel job box where none can be had), at least 1604 x 824 x 622 mm inside (BOM lines 1 to 3). One capstan set is shared by neighbouring sites and kept at the host site in its own reused crate, at least 904 x 864 x 1042 mm inside (BOM line 31). The PPE comes from the cooperative's own stock (BOM line 26, no cost to the kit). R9 is restated as "parts at most USD 850 per site search kit, with one capstan set shared by neighbouring sites and costed per group" (HPL-REQ-001 v0.4).

## Consequences

- R2: two people reach the full 2.6 m in stiffer debris and one person 0.6 m; one person still reaches 2.6 m in loosened debris (HPL-CAL-001 [B1c], [B1s]). Met on paper, provided the sleeve friction does not rise as the tip's clearance over the tube falls from 3 mm to 1 mm a side [B5]; the TRL 4 test heap confirms it. Each probe is 3.07 kg, about 0.03 kg lighter.
- R5: met under the rule: 127 N each for four haulers on level debris, 153 N each for two on the boards [D].
- R8: met in two waves: 21.5 kg each for four in the search wave, 21.7 kg each for three in the capstan wave; heaviest item 21.2 kg [F2b]. R1 unchanged at 4.6 min [F3].
- R9: USD 827 per site search kit against the restated USD 850 [G1, G2b]; the shared capstan set with its crate is USD 547 per group of sites, USD 274 a site if two share it [G1b]. A bought steel job box (about USD 300 to 600) in place of the reused crate would take a site over the restated target.
- Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 1,374 (USD 426 under the target), for the host site, which keeps a search kit and the shared capstan set [G3]. `budget_usd` unchanged.
- The capstan wave from the host site arrives 3.8 min after the alarm from 100 m and 14.8 min from 500 m [F4]. How far apart sharing sites may be is a new open decision for Amish in `docs/06-design-decisions.md`.
- Model: crates parametrised in `cad/src/model.py` (`box`, `cap_box`), `packed_capstan()` added; checks cover both crates (no overlaps between packed items or with the crate, every item inside its crate). STEP and STL regenerated, with `heapline-capbox.step` and `.stl` added. HPL-DWG-002 Rev P3.
