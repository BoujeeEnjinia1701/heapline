---
doc_id: HPL-PRB-001
title: HeapLine problem statement
project: HeapLine
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-10-03'
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
  change: TRL 2 and 3 update; first co-design candidate named (HPL-DDR-001); open questions answered or carried to the first trials; safety note
---

# HeapLine problem statement

In the first minutes after a dumpsite slide, the only people who can reach buried victims are those already on site. Today they search without tools, a plan or any protection from a second slide.

## The problem

The death tolls at Koshe and Kiteezi came from slides onto homes and working areas where hundreds of people spend their days ([IDS, 2017](https://www.ids.ac.uk/opinions/recognise-informal-waste-pickers-to-avoid-future-disasters-like-koshe/); [Wikipedia](https://en.wikipedia.org/wiki/Kiteezi_Landfill)). Formal rescue has to travel to the site, and at Kiteezi coverage described the effort as rudimentary ([The Independent, Uganda, 2024](https://www.independent.co.ug/cover-story-lets-not-waste-kiteezi-garbage-tragedy/)). Evidence from snow avalanches, the closest well-studied analogue, shows why speed matters: in Swiss data on 422 buried skiers, 92 % survived if dug out within 15 minutes but only 30 % after 35 minutes ([Wikipedia, avalanche rescue](https://en.wikipedia.org/wiki/Avalanche_rescue)). Waste is not snow, but the lesson that the people on the spot must search at once carries over.

The long-term answer is to engineer or close dumpsites. At Koshe, rehabilitation after 2017 added compacted roads, gas venting pipes and graded slopes, and pickers report no fear of slides ([UN-Habitat, 2019](https://unhabitat.org/news/05-jul-2019/after-the-tragic-landslide-that-killed-116-koshe-landfill-in-addis-ababa-is-safer)). That work takes years and money that many sites do not have. Avalanche companion kits (probe, shovel and beacon) are designed for snow and for people who carry them on their bodies ([Wikipedia](https://en.wikipedia.org/wiki/Avalanche_rescue)). Nothing packages a site-kept kit and drill for waste pickers.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Waste pickers and their cooperatives | Search and dig for buried colleagues and neighbours in the first minutes, without being buried themselves | Open dumps and uncontrolled landfills, often with homes at the toe |
| Neighbours living beside the dump | Join a search that has a lookout, a plan and a clear point to stop | Informal housing downslope of the waste |
| Site operators and municipal staff | A low-cost emergency measure they can stock and inspect | Sites awaiting closure or rehabilitation |
| Fire, police and Red Cross responders | Arrive to a search that is organised, with burial points marked | Handover from community search to formal rescue |

## Operating environment

- Loose, wet, mixed waste with voids, plastic sheeting, sharp objects and debris flows; ground can keep moving after the first slide.
- Landfill gas at some sites, which is why rehabilitated sites add gas venting ([UN-Habitat, 2019](https://unhabitat.org/news/05-jul-2019/after-the-tragic-landslide-that-killed-116-koshe-landfill-in-addis-ababa-is-safer)).
- Heavy rain preceded the Kiteezi failure ([Eos Landslide Blog, 2024](https://eos.org/thelandslideblog/kiteezi-1)), so searches may happen in rain and mud.
- Kit stored for months in a shed in heat, damp and dust; must still work on the day.
- No power at the scene; lighting may be needed at night.

## Constraints

- Value-engineering target of USD 1,800 for the prototype (a hypothetical control target, not a spending limit).
- Parts cost target under USD 400 per site kit (target).
- Carried to the slide by four people or fewer; no single item over 25 kg (55 lb) (target).
- Made from common steel tube, timber or plastic board, rope and tarpaulin; repairable locally.
- Kit and drill must include a lookout and a written stop rule.
- Open hardware under CERN-OHL-S-2.0; drawings published with dates early (IP screen).

## Out of scope

- Slope stability monitoring or early warning (a separate problem).
- Engineering, rehabilitation or closure of the dumpsite.
- Heavy plant such as excavators.
- Medical treatment beyond moving casualties to a pickup point.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Avalanche companion rescue (probe, shovel, beacon) | Survivors search at once with probes and shovels instead of waiting for help | Carried on the body and designed for snow, not a site-kept kit for mixed waste | [link](https://en.wikipedia.org/wiki/Avalanche_rescue) |
| Koshe rehabilitation using the Fukuoka method (UN-Habitat) | Compacted roads, gas venting and graded slopes that reduce slide risk | Prevention that takes years and funding; no first-minute rescue capability | [link](https://unhabitat.org/news/05-jul-2019/after-the-tragic-landslide-that-killed-116-koshe-landfill-in-addis-ababa-is-safer) |
| Formal response at Kiteezi, 2024 | Government and agency search and recovery after the collapse | Described as rudimentary; arrives after the first minutes | [link](https://www.independent.co.ug/cover-story-lets-not-waste-kiteezi-garbage-tragedy/) |

## Co-design

A waste pickers' cooperative or association at an active dumpsite, working with the local fire and rescue service or Red Cross branch, so the kit contents and the stop rule are shaped by the people who will use them and agreed with those who take over the search.

The first candidate to approach is the Uganda Red Cross Society in Kampala, together with the waste pickers who work at Kiteezi (HPL-DDR-001, item 11). This is a candidate to approach, not an agreement.

> **Safety:** A second slide can bury the searchers. HeapLine is published as an open engineering reference, not certified rescue equipment. Every search has a lookout and a stop rule, the fire service and emergency services are called at once, and nobody smokes or uses a naked flame near the debris.

## Open questions

Answered for the design at TRL 3 (HPL-DDR-001):

- **Stop rule.** Six signals, any one of which sends everyone to the marked safe zone at once: the lookout's long whistle; new cracks, bulging or movement on the slope above; water or mud flowing from the debris; rain getting heavier; a gas smell, smoke or hissing; or a formal responder's order. It is printed on the lid and on pocket cards.
- **Gas detector.** Not in the base kit: a detector that is not bump-tested and calibrated can give false comfort. The rule is no flames or smoking and stop on any sign of gas. A partner who will maintain a detector monthly would allow one to be added.
- **Ownership.** The cooperative or, where there is none, the site operator owns the kit and keeps a monthly inspection log.

Carried to the first trials with the co-design partner (TRL 4):

- How deep are people typically buried in dumpsite slides, and how far can probes be pushed in real slide debris? HPL-CAL-001 shows the answer depends strongly on how compact the debris is.
- How should the kit be introduced so it is not read as accepting unsafe dumps?
