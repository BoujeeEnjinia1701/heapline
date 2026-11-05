---
doc_id: HPL-RSK-001
title: HeapLine risk register and hazard analysis
project: HeapLine
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First register, hazard analysis and design FMEA, written for the kit 1.9.1 upgrade
---

# HeapLine risk register and hazard analysis

The top risks are that a second slide buries searchers, that the capstan's rope or anchor fails under load, and that field facts (probe resistance, drill times, the reach of a shared capstan) turn out worse than the paper estimates. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); the scores are the author's first-pass judgement for review with a co-design partner.

> **Safety:** HeapLine is used on unstable ground and its capstan stores energy in a loaded rope. It is published as an open engineering reference, not certified rescue equipment. Every search has a lookout and a stop rule; formal responders are called at once.

## Project risk register

*Table 1. Project risks.*

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner agrees to trial the kit | The first candidate (Uganda Red Cross Society with the Kiteezi waste pickers) is not agreed (HPL-DDR-001 item 13) | The design stays on paper; stop rule and drills are never tested | 3 | 4 | Project lead | Approach the candidate; keep a second candidate (a municipal unit or NGO) |
| P2 | Probe reach in real slide debris is lower than estimated | No published resistance data for dumpsite slides; stiff case is within 3 % of the push two people can give | Searchers cannot probe to 2.5 m (PR-002) | 3 | 4 | Design lead | Test heap at TRL 4; the 18 mm tip is already the response to the earlier shortfall (decision 20A) |
| P3 | The shared capstan arrives too late from 500 m | Walking time from the host shed is 14.8 min (HPL-CAL-001 F4) | Heavy cover stays on a mark for longer | 3 | 3 | Cooperative | The 500 m limit (HPL-DDR-004); farther sites keep their own set or rely on the search kit |
| P4 | Shear pin batch releases outside 5.1 to 7.6 kN | Bar stock and heat treatment scatter | Pin releases below 5 kN (capstan cannot do PR-004) or near the 8 kN design tension | 3 | 3 | Design lead | Release tests on a batch at TRL 4; spare pins on a tag chain |
| P5 | Prices rise or no reused crate can be found | Indicative prices only; crates vary by site | Over USD 850 a site (PR-009) | 3 | 2 | Project lead | Bought steel job box would exceed the target: ask Amish before accepting |
| P6 | The kit is read as certified rescue equipment | Open design with no certification | Misplaced reliance; liability for the partner | 2 | 5 | Project lead | Safety wording in every document (PR-014); no marking or claim |
| P7 | Kit not inspected or sabotaged | Combination padlock known to every member; shed in heat and damp | Missing items on the day (PR-007) | 3 | 4 | Cooperative | Monthly inspection log; PPE and cells checked each month |
| P8 | Amish does not choose between the concept options | Options A and B/C are scored in HPL-OPT-001 and put to him | The design stays at A, the current design | 2 | 1 | Project lead | None needed: A stays the design (CLAUDE.md section 5c) |

## Preliminary hazard analysis

*Table 2. Hazards.*

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | A second slide buries the searchers | Unstable debris, rain, ground still moving | Death or crush injury | 5 | 3 | Lookout posted before anyone steps on the debris; six stop signals; safe zone to the side of the slide path; call emergency services at once | Medium: a second slide can still outrun a warning |
| H2 | Rope snaps or the anchor fails under load | Overload, worn rope, a weak anchor | Whip-back of rope, shackle or sling strikes a person | 5 | 2 | 6 mm shear pin releases at about 6.4 kN; rope factor 4.5 at 8 kN; sound anchors only (tree, vehicle, column; never waste, never stakes alone); nobody within 2 m of the loaded rope | Low to medium |
| H3 | Drum runs back or a bar flies when released | Hands let go under load | Blow to the head or hands | 4 | 3 | Two holding pawls on a 24-tooth ring; tail made fast on the cleat whenever hauling stops; bars off the head when idle | Low |
| H4 | Pinch or crush at the pawls, bar sockets and ratchets | Moving parts at the head | Hand injury | 3 | 3 | Hands only on the bars; drill card rule; no guard at the head (to assess under ISO 14120 at TRL 4) | Medium |
| H5 | The capstan pulls on a person | Misuse | Serious injury | 5 | 2 | Rule: only sheeting, timber and debris, sideways away from the dig; never lifting, never on a person (HPL-DDR-001 item 6) | Low |
| H6 | Cuts, punctures and infection from sharp waste | Search on debris | Wound, tetanus | 3 | 4 | Cut-resistant gloves, boots with steel midsole, glasses; wound care and vaccination advice on the card | Medium |
| H7 | Landfill gas or fire | Methane in or near the debris | Poisoning, explosion | 5 | 2 | No flames or smoking; stop on any gas smell, smoke or hissing; no detector in the base kit | Medium: gas can be present without smell or flame |
| H8 | Capstan tips or skates under pull | Rope or sling at the wrong height | Frame strikes a person | 4 | 2 | Rope leaves at the same height as the anchor eye; stakes only resist turning | Low |
| H9 | Manual handling injury | 21.5 kg per person over rough ground | Back or limb injury | 3 | 3 | Two waves; no item over 25 kg; carry bags with straps | Low to medium |
| H10 | Stretcher dropped or dragged in jerks | Too few haulers on debris | Further injury to a casualty | 4 | 3 | Four haulers on debris, two only along the boards (decision 21A) | Medium |
| H11 | Heat and exhaustion | Hard physical work in a hot site | Collapse of a searcher | 3 | 3 | Rotate people; water; lookout watches the crew | Medium |

## Design FMEA (first pass, P3)

*Table 3. Failure modes of option A, the current design. RPN = severity x occurrence x detection; detection 5 means hard to detect before use.*

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Shear pin, 6 mm S275 | Limits rope tension | Releases below 5 kN | Capstan cannot pull 5 kN | Weak bar stock | 2 | 3 | 3 | 18 | Batch release tests; spares on the tag chain |
| F2 | Shear pin | Limits rope tension | Does not release, or releases above 8 kN | Rope, sling or anchor overloaded | Over-strong pin (wrong bar, hardened) | 5 | 2 | 4 | 40 | Use unhardened S275 bar only; BOM line 18; check pin before each use |
| F3 | Rope, 14 mm polyester | Carries the pull | Cut or abraded; rotted by sun | Rope parts under load | Sharp waste, UV, storage | 5 | 2 | 3 | 30 | Inspect at each monthly check; replace on cuts or glazing; bend ratio at the roller (S9) |
| F4 | Anchor sling | Holds the capstan | Chokes or cuts on a sharp edge | Capstan loses its anchor | Sharp tree bark, vehicle edge | 5 | 2 | 3 | 30 | Tree protector strap; sound anchors only |
| F5 | Holding pawls (2) | Hold the drum when bars are released | One pawl bends or its spring fails | Drum runs back | Overload, fatigue | 4 | 2 | 3 | 24 | Two pawls; one takes the design tension at 77 MPa bearing; check springs monthly |
| F6 | Drive pawl and ratchet | Turn the drum on the up-stroke | Tooth wear | Slip, strokes lost | Dust, wear | 2 | 3 | 2 | 12 | Replace the pawl; keep clean |
| F7 | Post and frame welds | Carry the rope pull | Fatigue crack at a weld | Frame fails under load | Poor weld, 63 MPa post stress | 5 | 2 | 4 | 40 | Weld inspection in the first build; proof pull test at TRL 4 |
| F8 | Acetal bushes | Let the head and drum turn on the post | Seize or wear | Stiff bars, higher effort | Grit, dry running | 2 | 3 | 2 | 12 | Keep clean; replace bushes |
| F9 | Bars, 40 x 40 x 2.5 | Give the lever arm | Bend | Bars unusable | Misuse, bar pulled sideways | 3 | 2 | 2 | 12 | Stress 50 MPa at pin release; spare bar not carried; drill card |
| F10 | Probe tube, 16 x 2.0 | Carries the push | Buckles | Probe unusable | Side load, push over 650 N | 3 | 3 | 2 | 18 | Push straight down; three-section length limits free length (S13) |
| F11 | Crawl board battens | Carry a searcher over a void | Crack at a knot | Board fails at a void | Poor timber | 4 | 2 | 3 | 24 | Factor 4.0 on C16; reject knotted timber; inspect |
| F12 | Crate hasp and padlock | Keep the kit secure and openable | Lock seized or lost code | Kit not opened | Rust, forgotten code | 4 | 3 | 2 | 24 | Combination known to every trained member; monthly check |
| F13 | Stretcher straps | Haul a casualty | Strap or rivet fails | Casualty dropped | Overload, UV | 4 | 2 | 3 | 24 | Four haulers on debris; replace straps yearly (to assess) |

Highest RPN: F2 and F7 at 40. Both are covered by an action; neither is closed until the TRL 4 tests.
