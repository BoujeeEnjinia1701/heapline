---
doc_id: HPL-PLN-001
title: HeapLine project plan
project: HeapLine
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First plan, written for the kit 1.9.1 upgrade
---

# HeapLine project plan

The project is at stage P3 (TRL 3, paper proof of concept) with the pipeline documents and the D3 model of every concept option in place. The next gate is Amish's review of the concept options and of the decisions listed in `docs/REVIEW.md`; no TRL 4 work starts until he asks. Method: STANDARDS sections 19 and 23.

*Table 1. Workstreams.*

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Project lead | HPL-PRB-001 with users and stakeholders | Done (P3) |
| STEM check | Design lead | HPL-STM-001, `stem_check.py` | Done (P3) |
| Concept options | Design lead | HPL-OPT-001, `options_calc.py`, three D3 models | Done; choice awaiting Amish |
| Requirements | Design lead | HPL-URS-001, HPL-PRS-001, HPL-RTM-001 | Done (P3) |
| CAD and drawings | Design lead | `cad/src/model.py`, STEP, STL, HPL-DWG-001 and 002 | Done (P3, D3) |
| Calculations | Design lead | HPL-CAL-001 | Done (P3) |
| Build plan | Design lead | HPL-BLD-001, HPL-DWG-101 to 116 | Done (P3, plan only) |
| Regulatory, feasibility, risk, market | Project lead | HPL-REG-001, FEA, RSK, MKT | Done (P3) |
| Co-design partner | Project lead | Agreement with a cooperative and a Red Cross branch or fire service | Not started |
| Prototype build and tests | Fabricator | Build log, release and pull tests, probe trials, drills | Planned, TRL 4 (on hold while the stage cap is P3) |

*Table 2. Resources.*

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design partner | Site trials and drills | To assess | To assess |
| Fabricator with a small welder | First prototype of the capstan and the search kit | To assess | About 1,374 in parts for the host site (HPL-CAL-001 G3), indicative, not a quote |
| Test site (a waste heap) | Probe trials and board load tests | To assess | To assess |
| Reviewer for regulatory questions | HPL-REG-001 items marked "to assess" | To assess | To assess |

*Table 3. Stages (P4 to P6 on hold while the stage cap is P3).*

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P3 | Pipeline documents, D3 model of every option, constructable design, build plan, priced BOM | Reached |
| P4 | Co-design partner agreed; prototype built and tested | On hold (stage cap) |
| P5 | Pilot at one site with drills | On hold (stage cap) |
| P6 | Release and handover | On hold (stage cap) |

## Next steps and decision requested

1. Amish chooses among the concept options (HPL-DDR-005, "Proposed, awaiting Amish").
2. Amish decides whether to approach the co-design partner and start the TRL 4 plan; none of it begins before he asks.

## References

Every source cited in this repo's documents is listed in its own Sources section (HPL-PRB-001, HPL-STM-001, HPL-REG-001, HPL-MKT-001) and in the Chicago-style list in `docs/REVIEW.md`.
