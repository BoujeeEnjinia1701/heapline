---
doc_id: HPL-DDR-002
title: HeapLine design for construction
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
  change: Constructability review and changes that make the design buildable, decided under Amish's pre-approvals of 2026-10-03
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted

## Context

STANDARDS section 18 asks for every part to be makeable by its stated process and to fit and fasten to its neighbours (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept (HPL-PRC-001 v0.2, HPL-DDR-001) was reviewed part by part in `cad/src/model.py`: how each part is made, how it joins each neighbour, and build123d checks for parts that overlap, parts that do not touch what holds them, and contents that do not fit the site box. The checks now report no overlaps and no floating parts. Amish pre-approved every recommendation on 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." and, for this batch, "Proceed with the remaining 15 scaffolds". No change alters what HeapLine does or its pitch; the safety-related changes all take the conservative side.

> **Safety:** Changes 3, 6, 7 and 8 carry the capstan's safety case (no tipping, overload limit, holding, nothing coming off the post). Change 11 keeps the probe tip blunt.

## Options considered

For each problem the simplest physically sound fix was chosen; the alternatives are noted in Table 1.

## Decision

*Table 1. Changes made for construction.*

| # | Part | Problem found | Change | Why |
| --- | --- | --- | --- | --- |
| 1 | Capstan base | The concept had a capstan "on a ground anchor" with no base | Frame 700 x 440 in 40 x 40 x 3 tube with a 100 x 40 x 4 centre member; 19.2 kg with the post | A base that carries the post, the roller, the eye and the stakes |
| 2 | Post | A post standing on a plate would have to carry 0.7 kN m at its foot through one weld | Post 60.3 x 5.0 passes through the centre member and is welded at the top and bottom faces | The two welds form a couple; 63 MPa in the tube |
| 3 | Rope lead | Rope leaving the drum 130 mm up while the sling pulls lower would tip the capstan; walkers or bar crews would step over a rope at knee height | A hold-down roller at the front takes the rope down to 38 mm above the ground, level with a rear anchor eye | No tipping moment; the rope lies along the ground |
| 4 | Drum | A drum turning on nothing | Barrel on two discs and a spindle up to bar height, turning on three acetal bushes on the fixed post, standing on an acetal thrust washer | Every turning part has a bearing surface |
| 5 | Head | Bars fixed to the drum mean walking round | A lever head turning on its own bush, with two radial sockets and a drive pawl on a 20-tooth drive ratchet | Pumping through a quarter turn; nobody moves their feet |
| 6 | Shear pin | Not placed | 6 mm pin through the drum's top flange and the drive ratchet on a 60 mm radius; the drive ratchet is otherwise free on the post | Only the pin passes the drive (R10) |
| 7 | Pawls | Pawl bodies first drawn clashed with the teeth behind their noses | Noses 0.12 of a tooth past the face; pivots along the tangent lifted 30 degrees; checked clear by intersection | Each pawl clears the teeth it rides over (R11) |
| 8 | Keeper | Nothing held the head and drum on the post when it is carried or tipped | Collar and 10 mm cross pin on the post top | Parts cannot slide off |
| 9 | Stakes | No way to stop the frame turning against the pawl reaction | Four stake tubes at the corners; 25 mm stakes with welded heads | Each stake rests on its tube |
| 10 | Tail | Nowhere to make the tail fast | Horn cleat on the rear member | Tail made fast whenever hauling stops |
| 11 | Probes | Joint and tip not defined | Three 1 m sections of 16 x 2.0 tube on 11.5 mm spigots with 5 mm R-clips; tube ends bear on each other; 22 mm tip with a 3 mm rounded point | Push goes through the tube, not the pin; tip 3 mm wider than the tube each side cuts friction |
| 12 | Crawl boards | No way to join boards; deck alone too flexible over a void | Two 45 x 70 battens 30 mm in from the edges; four 13 mm holes; link plates with two 12 mm pins drop across each joint | Boards stay in line; bridges a 0.8 m void at 4.0 MPa |
| 13 | Site box | The assembled capstan (995 mm tall) and the 1.5 m boards did not fit the concept box | Box enlarged to 1700 x 1020 x 1060 mm on skids, with corner battens and a lid skirt over a seal; a packing layout checked clear of every wall and item | Everything packs; nothing has to be assembled at the slide except the bars |
| 14 | Sheet clamp | The capstan had no way to grip plastic sheeting | A bolted two-bar clamp with a shackle lug | Holds about 6 kN, below the pin's release |
| 15 | Stretcher | Handles and straps not defined | Twelve hand slots, three riveted straps with cam buckles, a head haul strap | Fixings |

## Consequences

- `cad/src/model.py` holds the constructable design; STEP and STL, HPL-DWG-001 and 002 (Rev P2), the concept media and the build plan pictures are regenerated from it.
- HPL-CAL-001 is written on it; the parts cost is USD 1,599, USD 201 under the value-engineering target.
- The site box is heavier (104 kg) but never leaves the shed.
- `design_state: constructable` is set in `project.yaml`.
