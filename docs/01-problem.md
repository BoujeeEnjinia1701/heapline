---
doc_id: HPL-PRB-001
title: HeapLine problem statement
project: HeapLine
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-11-03'
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
- version: "0.3"
  date: '2026-11-03'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: users and needs and stakeholders tables added under Users and context (the user requirements in HPL-URS-001 come from them)"
---

# HeapLine problem statement

In the first minutes after a dumpsite slide, the only people who can reach buried victims are those already on site. Today they search without tools, a plan or any protection from a second slide.

## The problem

The death tolls at Koshe and Kiteezi came from slides onto homes and working areas where hundreds of people spend their days ([IDS, 2017](https://www.ids.ac.uk/opinions/recognise-informal-waste-pickers-to-avoid-future-disasters-like-koshe/); [Wikipedia](https://en.wikipedia.org/wiki/Kiteezi_Landfill)). Formal rescue has to travel to the site, and at Kiteezi coverage described the effort as rudimentary ([The Independent, Uganda, 2024](https://www.independent.co.ug/cover-story-lets-not-waste-kiteezi-garbage-tragedy/)). Evidence from snow avalanches, the closest well-studied analogue, shows why speed matters: in Swiss data on 422 buried skiers, 92 % survived if dug out within 15 minutes but only 30 % after 35 minutes ([Wikipedia, avalanche rescue](https://en.wikipedia.org/wiki/Avalanche_rescue)). Waste is not snow, but the lesson that the people on the spot must search at once carries over.

The long-term answer is to engineer or close dumpsites. At Koshe, rehabilitation after 2017 added compacted roads, gas venting pipes and graded slopes, and pickers report no fear of slides ([UN-Habitat, 2019](https://unhabitat.org/news/05-jul-2019/after-the-tragic-landslide-that-killed-116-koshe-landfill-in-addis-ababa-is-safer)). That work takes years and money that many sites do not have. Avalanche companion kits (probe, shovel and beacon) are designed for snow and for people who carry them on their bodies ([Wikipedia](https://en.wikipedia.org/wiki/Avalanche_rescue)). Nothing packages a site-kept kit and drill for waste pickers.

## Users and context

*Table 1. Users and needs.*

| User type | Goals and needs | Typical use scenario | Pain points and challenges |
| --- | --- | --- | --- |
| Waste pickers and their cooperatives | Search and dig for buried colleagues and neighbours in the first minutes without being buried themselves; know when to stop | A slide buries a work area in daylight; people fetch the kit from the shed, post a lookout, probe from boards, dig, and haul sheeting off a mark with the capstan | No tools, plan or protection from a second slide; sharp waste, gas and rain; no power or vehicle at the scene |
| Neighbours living beside the dump | Join an organised search with a clear point to stop | Called by the alarm to carry, probe or haul under the lookout's direction | Untrained; fear and urgency push people past the stop signals |
| Site operators and municipal staff | A low-cost emergency measure to stock, inspect and keep secure | Kit kept in a reused crate in a shed, inspected monthly, hosts one capstan set shared by nearby sites | Budget; heat and damp in storage; who keeps the key or the padlock code |
| Fire, police and Red Cross responders | Arrive to a search that is organised, with burial points marked | Take over the search from the community crew | A search that has no lookout or marks; crowd on unstable ground |

## Stakeholders

*Table 2. Stakeholders.*

| Stakeholder group | Role or interest | Engagement needed |
| --- | --- | --- |
| Waste pickers' cooperatives and associations | Users and owners of the kit; keep the monthly inspection log | Co-design partner; drills and trials at TRL 4 |
| Red Cross branch, fire and rescue service | Take over a search; agree the stop rule and handover | Co-design review of the stop rule and drill card |
| Site operators and municipal authorities | Host the shed and crate; permission for anchors and site access | Agree siting and the 500 m sharing limit |
| Neighbouring households | Join searches; live below the slide path | Briefing and drill cards |
| Local fabricators and steel stockholders | Build and mend the kit from open drawings | Review of the build plan for constructability |
| Regulators and standards bodies | Whether a kit like this is regulated as machinery or rescue equipment | Review of HPL-REG-001 items marked "to assess" |
| Open hardware community | Reuse, improve and share back under CERN-OHL-S-2.0 | Publish drawings early and keep the licence split |

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
