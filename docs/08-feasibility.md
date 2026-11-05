---
doc_id: HPL-FEA-001
title: HeapLine feasibility assessment
project: HeapLine
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First assessment, written for the kit 1.9.1 upgrade
---

# HeapLine feasibility assessment

On paper HeapLine is feasible as a kit a local workshop can build from stock steel, plywood and rope for an estimated USD 827 a site plus USD 547 for each shared capstan set; the open questions are field facts that only trials can settle: how hard slide debris resists a probe, and how far a shared capstan can safely reach. Method: STANDARDS section 23.

*Table 1. Feasibility by aspect.*

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A pumped friction capstan, sectional probes, linked crawl boards and a sheet stretcher, all sized on paper; every concept option modelled to D3 (A 347 parts, B 236, C 217) with no interference | High | Probe reach in stiff debris is within 3 % of the push two people can give (HPL-STM-001 S12); the shear pin spread leaves 2 % margin to the 5 kN pull (S6) | HPL-STM-001, HPL-CAL-001 |
| Materials | Steel tube and bar, exterior plywood, treated timber, UV-stabilised HDPE, acetal, polyester rope and webbing; no exotic material | High | Coating life in a hot, damp shed to assess; rope bend ratio on the roller is 4.3 (S9) | BOM, HPL-STM-001 S9 |
| Manufacturing and assembly | Cut, drill and weld from stock; the making sketches and 15 steps are in the build plan; a village fabricator with a small welder can make the capstan | Medium | Weld quality and fit-up to prove in the first build; profile-cut ratchets and pawls need a laser or plasma cutter, or hand cutting | HPL-BLD-001, `cad/fidelity.json` |
| Power and controls | None: people supply the power; no electrics beyond AA lamps | High | Lamps use alkaline cells stored out of the lamps | BOM line 25 |
| Supply of parts | Common stock sizes; bought parts are rope, slings, shackles, shovels, padlocks, hinges and lamps | Medium | Rated slings and shackles with threaded pins to source (HPL-REG-001 G3, G4); a reused crate must be found at each site | BOM, HPL-REG-001 |
| Cost | USD 827 a site against USD 850 (PR-009); USD 1,374 for the host site against the USD 1,800 value-engineering target | High | All prices indicative, not quotes; a bought steel job box would take a site over USD 850 | HPL-CAL-001 G1 to G3 |
| Safety and regulatory | No whole-product regulation found; a safety case rests on the overload pin, holding pawls, sound anchors, stop rule and lookout | Medium | Whether a made stretcher or a shared capstan may be used in law is to assess (HPL-REG-001 G9, G10); never certified rescue equipment | HPL-RSK-001, HPL-REG-001 |
| Field performance | Unknown until trials: debris resistance, drill times, how long a shared capstan takes to arrive from 500 m | Low | No published data on probe resistance in dumpsite slide debris; paper estimates bracket it with a loosened and a stiffer case | HPL-CAL-001 B1, F4 |

Ratings: High, Medium, Low.

Overall: feasible on paper at TRL 3. Trials with a co-design partner (TRL 4, not started) would settle the Low-rated field aspect.
