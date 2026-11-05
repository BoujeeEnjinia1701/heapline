---
doc_id: HPL-REG-001
title: HeapLine regulatory and standards register
project: HeapLine
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First register, written for the kit 1.9.1 upgrade; standards and guidance checked on their pages on 2026-11-03
---

# HeapLine regulatory and standards register

HeapLine is a community-held kit of probes, boards, a stretcher and a hand capstan for the first minutes after a dumpsite slide; no regulation was found that certifies it as a whole, and it is published as an open engineering reference, not certified rescue equipment. The design leans on lifting-accessory, machinery-safety and protective-equipment standards for its rope, sling, shackle and glove choices. This is not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

*Table 1. Regulatory and standards register.*

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | ISO 12100:2010 Safety of machinery, general principles for design, risk assessment and risk reduction | International | Method for hazard identification, risk estimation and risk reduction | The hazard analysis and design FMEA in HPL-RSK-001 follow its order: remove by design, guard, then inform | Design lead | Applies; used as method (HPL-RSK-001) |
| G2 | ISO 11228-2:2007 Ergonomics, manual handling, Part 2: pushing and pulling | International | Recommended limits for whole-body pushing and pulling | Bar push of 114 N each (PR-004), stretcher haul of 127 to 189 N each (PR-005) and, for options B and C, the rope and lever forces in HPL-STM-001 | Design lead | To assess: tables not read; check at TRL 4 |
| G3 | EN 1492-2:2000+A1:2008 Textile slings, safety, roundslings made of man-made fibres | EU, widely used elsewhere | Rating and testing of polyester roundslings; excludes lifting people | The 2 t round slings (BOM line 21) anchor the capstan to a tree, vehicle or column and choke debris: a pulling anchor, never a lift, never a person | Design lead | Applies to the bought sling; use as a pulling anchor to assess |
| G4 | EN 13889:2003+A1:2008 Forged steel shackles for general lifting purposes, dee and bow shackles, grade 6 | EU, widely used elsewhere | Dimensions and working load limits of grade 6 shackles with threaded pins | Bow shackles WLL 2 t with 19 mm pins on the sling and the capstan eye (BOM line 21); the model shows them with a plain pin | Design lead | To assess: buy rated shackles with threaded pins at TRL 4 |
| G5 | EN 388:2016+A1:2018 Protective gloves against mechanical risks | EU, widely used elsewhere | Abrasion, cut, tear and puncture classes for gloves | PPE line 26 asks for cut-resistant gloves at level C or better; the cooperative supplies them from its own stock | Cooperative (PPE) | Applies to the bought gloves; levels to assess against the waste on site |
| G6 | ISO 4017, ISO 4032 and ISO 7089 hex bolts, nuts and washers, as named by the CAD parts library | International | Dimensions of the bolts, nuts and washers in the model | The 51 fasteners in the 347-part model of option A (`cad/fidelity.json`); numbers as named in `.kit/cad_parts.py`, not checked against the standards this session | Design lead | Applies; to check at TRL 4 |
| G7 | Landfill gas safety guidance, for example ATSDR Landfill Gas Primer, chapter 3 | United States (guidance), used worldwide | Methane explosive range 5 to 15 % in air; carbon dioxide and other components of landfill gas | The no-flame, no-smoking rule and the stop signal for a gas smell, smoke or hissing (HPL-PRC-001); no detector in the base kit | Co-design partner | Applies as guidance; local site rules govern |
| G8 | Wound care and tetanus guidance, for example CDC Clinical Guidance for Wound Management to Prevent Tetanus | United States (guidance), used worldwide | Higher-risk wounds (puncture, soil-contaminated) and vaccination status | Sharp waste and soil on a search; the briefing wording and PPE (HPL-STM-001 S20); not medical treatment | Cooperative | Applies as guidance; local health advice governs |
| G9 | Machinery or equipment safety regulation of the country of use | To assess | Whether a hand-powered kit held by a cooperative is "machinery" in law | None identified; no CE-style marking is claimed | Regulatory consultant | To assess |
| G10 | Rescue equipment, stretcher and casualty-handling rules of the country of use | To assess | Whether a made sheet stretcher may be used to move a casualty | None identified; HeapLine is not certified rescue equipment and says so (PR-014) | Co-design partner, with the Red Cross branch or fire service | To assess |
| G11 | Fibre rope and polyester double braid specifications | To assess | Minimum breaking load and testing of the rope | The 14 mm rope is bought on the maker's minimum break load (HPL-STM-001 S8); no rope standard number was checked | Design lead | To assess |
| G12 | Permission to use a tree, vehicle or column as an anchor; rules for working at an active or closed dumpsite | Local | Owner's consent, site access, occupational and public rules for informal waste sites | The sling anchor rule (HPL-DDR-001 item 4); the shed and crate hosted at the cooperative's site | Co-design partner | To assess locally |
| G13 | CERN-OHL-S-2.0 and MIT licences; REUSE | International | Licensing of the hardware and calculators | `REUSE.toml`, `LICENSES/` | Project lead | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- ISO, ISO 12100:2010, <https://www.iso.org/standard/51528.html>, checked 2026-11-03.
- ISO, ISO 11228-2:2007, <https://www.iso.org/standard/26521.html>, checked 2026-11-03.
- Genorma, EN 1492-2:2000+A1:2008, <https://genorma.com/en/standards/en-1492-2-2000-a1-2008/amp>, checked 2026-11-03.
- SIS (Swedish Standards Institute), SS-EN 13889+A1:2008, <https://online.sis.se/en/produkter/maskinsakerhet-357f77b1/chains-ropes-webbing-slings-and-accessories/ssen13889a12008>, checked 2026-11-03.
- Singer, EN 388:2016+A1:2018, <https://www.singer.fr/en/norm/en388>, checked 2026-11-03.
- ATSDR, Landfill Gas Primer, chapter 3 (2001), <https://www.atsdr.cdc.gov/HAC/landfill/html/ch3.html>, checked 2026-11-03.
- CDC, Clinical Guidance for Wound Management to Prevent Tetanus, <https://www.cdc.gov/tetanus/hcp/clinical-guidance/>, checked 2026-11-03.
