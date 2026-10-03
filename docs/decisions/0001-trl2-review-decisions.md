---
doc_id: HPL-DDR-001
title: HeapLine TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's pre-approvals of 2026-10-03
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted

## Context

The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) raised the items below. On 2026-10-03 Amish wrote: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." For this second batch he added: "Proceed with the remaining 15 scaffolds", under the same pre-approval. Every design recommendation below is therefore decided as recommended. Choices that touch safety take the conservative option, with the evidence that would relax them stated. Partners are first candidates to approach, not agreements. Requirements that are not met or at risk are not decided here; they are posed to Amish in `docs/REVIEW.md` and the design decisions register.

> **Safety:** HeapLine is used on unstable ground where a second slide can bury the searchers, and its capstan stores energy in a loaded rope. Items 2, 3, 4, 6, 7, 10, 11 and 12 set its safety case.

## Options considered

Table 1 lists the options for each item and the one chosen.

## Decision

*Table 1. Items decided on 2026-10-03 under Amish's pre-approvals.*

| # | Item | Options | Decision | What would relax a safety choice |
| --- | --- | --- | --- | --- |
| 1 | Capstan type | (a) the SiltHaul split winding drum with chain drive; (b) a walk-round vertical capstan with bars; (c) a vertical friction capstan worked by pumping two bars through a quarter turn, with a drive ratchet in the head | (c). SiltHaul's block is limited to 2.5 kN and weighs about 48 kg; with (b) the walkers step over the rope at every turn. With (c) four people stand still on firm ground and give 5 kN at 114 N each | Not a safety choice |
| 2 | Overload | (a) size everything on what four people can heave; (b) a shear pin between the drive ratchet and the drum | (b), conservative: R10 added. The 6 mm S275 pin releases at about 6.4 kN; every part, the rope, the slings and the anchor are sized on 8 kN | Release tests on a batch of pins with a tighter spread could raise the working pull, never the design tension |
| 3 | Holding | (a) the tailer holds the load; (b) two pawls on a ratchet ring at the drum's foot, and the tail made fast on a cleat whenever hauling stops | (b), conservative: R11 added | None proposed |
| 4 | Capstan anchor | (a) ground stakes or a picket holdfast; (b) a round sling to a sound tree, a parked vehicle's recovery point or a structural column, with stakes only against turning | (b), conservative. Never waste, never stakes alone. Where there is no sound anchor the capstan is not used | Pull tests of a picket holdfast in the local natural ground to twice the 8 kN design tension would allow it as an anchor |
| 5 | Rope | 12 mm or 14 mm polyester double braid | 14 mm, at least 40 kN: factor 4.5 at the design tension through the splice | Not relaxed |
| 6 | What the capstan may pull | (a) anything, including lifting; (b) only sheeting, timber and debris, sideways away from the dig, never lifting and never on a person | (b), conservative. Nobody stands in the line of the rope or within 2 m of it while it is loaded | None proposed; lifting or hauling people needs a different, certified system |
| 7 | Probes | (a) avalanche probes; (b) sectional steel probes pushed by hand; (c) probes driven with a hammer | (b): three 1 m sections of 16 x 2.0 tube with a 22 mm tip rounded to 3 mm. (c) rejected, conservative: a driven probe could injure a buried person | None proposed |
| 8 | Crawl boards | (a) bare plywood sheets; (b) plywood decks on two timber battens, linked end to end | (b): 1500 x 450 mm, 9.7 kg, link plates with pins | Not a safety choice |
| 9 | Stretcher | (a) a bought roll-up rescue stretcher; (b) a made HDPE sheet stretcher with straps | (b): about a fifth of the bought price; the same principle | Not a safety choice |
| 10 | Lighting cells | (a) rechargeable lithium lamps; (b) AA alkaline lamps with the cells stored out | (b), conservative: no lithium cells in a hot shed | Shed temperature records below 45 degrees C and a partner who charges and checks lamps monthly would allow lithium-iron-phosphate lamps |
| 11 | Gas detector | (a) a four-gas detector in the box; (b) no detector; no flames or smoking; stop on any gas smell, smoke or hissing | (b), conservative: an unmaintained detector gives false comfort | A partner who bump-tests and calibrates a detector monthly would allow one to be added |
| 12 | Stop rule | Signals that send everyone to the safe zone | Six signals: the lookout's long whistle; new cracks, bulging or movement above; water or mud flowing from the debris; rain getting heavier; gas smell, smoke or hissing; a formal responder's order. A lookout is posted before anyone steps onto the debris; the safe zone is to the side of the slide path, never below it | None proposed |
| 13 | Co-design partner | Cooperative, municipal unit, NGO or Red Cross branch | First candidate to approach: the Uganda Red Cross Society in Kampala with the waste pickers who work at Kiteezi (not agreed) | |
| 14 | Shared blocks | SiltHaul hand capstan; CalRig proof-load rig | SiltHaul's capstan is not used (item 1). CalRig is the first candidate rig for capstan proof loads and shear pin release tests | |
| 15 | Site box access | (a) key held by one person; (b) combination padlock known to every trained member | (b): no waiting for a key holder (R1). The owner keeps a monthly inspection log | |
| 16 | Budget | Keep `budget_usd` at 1,800 | Kept; it is a value-engineering target, not a limit | |

## Consequences

- R10 (overload limit) and R11 (holds when let go) are added to HPL-REQ-001.
- The design for construction (HPL-DDR-002) works from these choices.
- R2, R5, R8 and R9 are not met or at risk on paper. They are not decided here: each is posed to Amish with options and a recommendation in `docs/REVIEW.md` and listed as open in `docs/06-design-decisions.md`.
