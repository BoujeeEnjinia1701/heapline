---
doc_id: HPL-DDR-005
title: HeapLine concept options and modelling depth
project: HeapLine
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: Concept options B and C proposed and modelled at D3; recommendation proposed, awaiting Amish
---

# 0005: Concept options and modelling depth

- **Date:** 2026-11-03
- **Status:** Proposed, awaiting Amish. Nothing in this record is decided. Option A is the current design and does not change.

## Context

The kit 1.9.1 upgrade asks for at least one other option with a different working principle for the part of HeapLine that does the heavy pulling (UR-004), scored against the user requirements (HPL-OPT-001). Options already declined by Amish are not re-proposed: HPL-DDR-001 item 1 declined the SiltHaul winding drum with chain drive and the walk-round capstan, and items 6 and 7 fix what the capstan may pull and that probes are never driven. The options not chosen in HPL-DDR-003 (20B, 20C, 21B, 21C, 22B, 22C, 23A, 23B) are also left alone.

## Options considered

Table 1. Pull-set options.

| # | Option | Working principle | Result (HPL-OPT-001) |
| --- | --- | --- | --- |
| A | Pumped friction capstan (current design) | Rope turns round a vertical drum, quarter-turn bar strokes with a drive ratchet and holding pawls | 90 of 125 (72.0 %) |
| B | Six-part rope tackle | Two triple sheave blocks, mechanical advantage 6, a shear link in series and a rope grab at the tail | 87 of 125 (69.6 %) |
| C | Lever rope-grip puller | A 1.6 m lever walks a cam grip along the rope in 120 mm strokes | 64 of 125 (51.2 %) |

A geared drum winch was drafted first as option C and dropped before scoring, because a winding drum is the arrangement HPL-DDR-001 item 1 declined. The lever rope-grip puller replaced it.

## Decision

Proposed, awaiting Amish:

1. A and B are within 10 % (3.3 %), so both go to Amish with no pick. A stays the design (`concept_chosen: "open: A or B, no pick proposed"`).
2. B's rope grab could be grafted onto A as a second way to hold the load; that is a design change and is not made here.
3. Modelling depth: every option is modelled at D3 (real stock, weld beads, fasteners, clips) so that the comparison of mass and part count is like for like. This is a modelling choice, not a change to the design.

## Consequences

- `cad/src/opt_b.py` and `cad/src/opt_c.py` hold the two other options; `OPTIONS`, `PRINCIPLES` and `CHOSEN` are in `cad/src/model.py`.
- B and C estimates (cost, effort, reach) are scaled from BOM lines and are not measured; they are marked as estimates in `docs/04-calcs/options_calc.py`.
- No test of B or C is planned before Amish decides; any proof loading is TRL 4 work.
