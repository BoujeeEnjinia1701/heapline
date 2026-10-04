---
doc_id: HPL-DDR-003
title: HeapLine requirement decisions, round 2
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
  change: Four requirement decisions (R2, R5, R8, R9) decided by Amish on 2026-10-03 as recommended, and carried into the design
---

# 0003: Requirement decisions, round 2

- **Date:** 2026-10-03
- **Status:** Decided
- **Decided by:** Amish Chadha, 2026-10-03

## Context

The TRL 3 review (`docs/REVIEW.md`, Session 2026-10-03, TRL 3, Decisions for Amish) posed four requirements that were at risk or not met on paper as decisions for Amish, each with its state, options and a recommendation: R2 probe depth, R5 casualty transport, R8 portable and R9 cost. On 2026-10-03 Amish wrote: "i approve all of the 47 recommendations provided by you. Execute them." Each of the four is therefore decided as its recommendation, exactly as worded, and carried into the design at TRL 3 scope only: model, calculations, bill of materials, drawings, build plan and documents. Nothing here is built or tested; the conditions below are checked at TRL 4.

> **Safety:** None of the four decisions touches the capstan's safety case (shear pin, holding pawls, anchors). Decision 1 keeps the probe tip blunt and hand pushed; decision 2 keeps each hauler within a sustained pull; decision 4 moves PPE to the cooperative's stock, which is safe only if a full set stays in every box.

## Options considered

The options for each decision are set out in full in `docs/REVIEW.md` (Session 2026-10-03, TRL 3, Decisions for Amish, items 1 to 4). Table 1 lists the option chosen.

## Decision

*Table 1. Decisions of 2026-10-03.*

| # | Requirement | Option chosen | Effect (HPL-CAL-001 v0.2, paper estimates) | Condition |
| --- | --- | --- | --- | --- |
| 1 | R2, probe depth | A: 18 mm tip on all six probes | In stiffer debris two people reach the full 2.6 m (1.8 m before) and one person 0.6 m (could not start before); loosened debris unchanged at 2.6 m for one person. Tip force to start in stiff debris 254 N (380 N before). Probe 3.07 kg (3.10 kg before). No cost change. R2 met on paper | Holds only if the sleeve friction does not rise as the tip's clearance over the tube falls from 3 mm to 1 mm a side; confirmed on a test heap of mixed waste at TRL 4 |
| 2 | R5, casualty transport | A: drill card rule: four haulers on debris, two only along the boards | 127 N each for four on level debris; 153 N each for two along the boards; both within the 200 N sustained pull. No cost or mass. R5 met on paper | The boards are laid back to firm ground before a casualty is moved; the rule is printed on the drill card and practised in drills |
| 3 | R8, portable | A: two waves: four carry the search kit first, a second group of three brings the capstan set | Search wave 21.5 kg each for four; capstan wave 21.7 kg each for three; both under the 25 kg carry limit. R1 unchanged at 4.6 min, since the capstan is not needed for the first probe line. No cost or mass. R8 met on paper for each wave | Seven people in all; the capstan arrives after the first probe line. The R8 target text still says "whole kit carried by four people" (new question, `docs/06-design-decisions.md`) |
| 4 | R9, cost | C: one capstan set shared by neighbouring sites, and a reused crate (or bought steel job box) for the site box with PPE from the cooperative's own stock | Parts bought for each site USD 830.00 (USD 1,599.00 before): capstan set USD 449.00 per group of sites; box with hardware USD 101.00 (USD 253.00 before); PPE (USD 168.00 if new) from stock. With the capstan share: USD 1,279.00 a site unshared, USD 1,054.50 shared by two, USD 979.67 by three. R9 still not met against USD 400 | A sound crate with the inside size of the plywood box is found for each site, otherwise the plywood box is made (USD 152 more); the cooperative keeps a full PPE set in every box; the group of sites sharing the capstan and its distance are still to be set (new question) |

## Consequences

- `cad/src/model.py`: probe tip 18 mm. STEP and STL regenerated; constructability checks still report no overlaps and no floating parts.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (HPL-CAL-001 v0.2), `results.csv`: R2, R5 and R8 met on paper; R9 not met; per-site cost basis added.
- `bom/bom.csv`: a `cost_basis` column (site, shared, stock); lines 1 and 2 as a reused crate refit (estimated allowances of USD 40 and USD 13); line 6 18 mm bar; line 26 from stock; line 27 carries the carry and haul rules.
- `HPL-DWG-002` Rev P3; `HPL-DWG-103`, `115` and `116` Rev P2; build plan pictures, concept media and `media/model.glb` regenerated.
- `docs/03-requirements.md` v0.4, `docs/02-concept.md` v0.4, `docs/05-build-plan.md` v0.2, `README.md` updated. R targets are not restated.
- `budget_usd` in `project.yaml` stays at 1,800, the value-engineering target set by Amish; the estimate falls to USD 830 a site plus the capstan share.
- New questions raised by these decisions are posed in `docs/REVIEW.md` and the design decisions register: the capstan sharing group, the R8 target wording, and the fallback where no reused crate is found.
