---
doc_id: HPL-DDR-006
title: HeapLine STEM check fixes
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
  change: Two STEM fixes (options B and C) decided under Amish's standing instruction of 2026-10-23
---

# 0006: STEM check fixes

- **Date:** 2026-11-03
- **Status:** Decided under Amish's standing instruction of 2026-10-23: when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session; a fix that changes the working principle, pitch or scope goes to Amish instead. Neither fix below changes the working principle, the pitch or the scope.

## Context

The STEM check (HPL-STM-001, `docs/04-calcs/stem_check.py`) of the pull-set options found two details that failed their first screen. Option A had no failing row on its first-draft numbers. A second model run then reviewed the check (HPL-STM-001, Independent review) and found three weaknesses in option A and the shared kit, which are fixed below. The check now has 29 claims: 9 within known science, 20 plausible, none failing.

## Options considered

Table 1. Fixes considered.

| # | Option | Failure on first screen | Fixes considered | Chosen |
| --- | --- | --- | --- | --- |
| 1 | B | Effort at the rope end with four handles was too high for the pull set to reach 5 kN | (a) six rope handles; (b) a longer tackle; (c) fewer people on a heavier pull | (a): six handles (`N_HANDLES = 6` in `opt_b.py`) keeps the principle; effort is 178 N each |
| 2 | C | A short lever needed more than a person can give for 5 kN | (a) lever 1.6 m (ratio 12.2); (b) a second lever; (c) gearing | (a): `LEVER = 1600.0` in `opt_c.py`; effort 146 N each; the cost is mass and swing room (S24) |
| 3 | A | The shear pin was sized on 430 MPa plus or minus 20 %, but EN 10025-2 allows 410 to 560 MPa for S275 bar, so release could reach 8.3 kN against the 8 kN limit | (a) a mill certificate at 480 MPa or less and a release test of three pins per batch; (b) a smaller pin; (c) a bought shear pin | (a): a purchase specification, no change of geometry; release 5.77 to 7.47 kN (S5, S6) |
| 4 | A and shared | Probe buckling was checked only at 0.57 m of free tube | (a) one person pushes while more than 1.5 m is above the debris; (b) a stiffer tube | (a): drill-card wording; 325 N against 484 N critical (S13) |
| 5 | Shared | The no-flame rule was called sufficient for landfill gas, but carbon dioxide and hydrogen sulfide collect in holes | (a) digging guidance on the drill card; (b) a detector (declined in HPL-DDR-001 item 11); (c) a seventh stop signal | (a): no head first entry into a hole, a watcher at every hole, back out on headache, dizziness or any smell. The six-signal stop rule is not changed |

## Decision

The fixes to options B and C are made in the models and the checks rerun. They are recorded as decided under the standing instruction. Option A is not touched.

Item 5(c), adding a seventh stop signal, and item 5(b), a detector, touch decisions Amish made (HPL-DDR-001 items 11 and 12), so they are Proposed, awaiting Amish and are not made here.

## Consequences

- The pin bar specification (mill certificate at 480 MPa or less, three-pin release test per batch) is now in BOM line 18; the probe push rule and the digging guidance are in the build plan drill card text (line 27).

- B needs six people at the rope, which is more than the capstan wave brings (three); this is why B scores 2 on the pull criterion (HPL-OPT-001).
- C's lever is long and swings when released; it has no overload device yet, which is why it scores 2 on overload.
- Plausible rows for B and C (S22 to S26) carry the estimate to TRL 4 tests if Amish asks for either option.
