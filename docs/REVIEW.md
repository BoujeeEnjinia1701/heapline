# Review note: HeapLine

## Session 2026-10-03: TRL 3 (kit 1.7.0, /to-trl3 under Amish's pre-approvals, batch 2)

Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." For this batch: "Proceed with the remaining 15 scaffolds", under the same pre-approval. Every design choice and recommendation in this session is therefore recorded as decided, dated 2026-10-03, in `docs/06-design-decisions.md`. Requirements that are not met or at risk are not decided: each is posed below as a decision for Amish (Amish, 2026-10-03: "A simple statement doesn't add value - ensure you are identifying a state and posing it as a clear recommendation for me to decide on."). Kit 1.7.0 was installed from the kit source; `.kit/PHASE.yaml` kept as installed.

### TRL 2

**What was done.**

- `docs/01-problem.md` (HPL-PRB-001 v0.2): first co-design candidate, safety note, open questions answered or carried to the first trials.
- `docs/03-requirements.md` (HPL-REQ-001 v0.2): concept status for each requirement; R10 (overload limit) and R11 (holds when let go) added.
- `docs/02-concept.md` (HPL-PRC-001 v0.2): how it works, components, key design choices, stop rule, safety.
- `docs/decisions/0001-trl2-review-decisions.md` (HPL-DDR-001): sixteen TRL 2 review items decided.

**Results.** A hand capstan of the SiltHaul type gives only 2.5 kN and weighs about 48 kg, so HeapLine needs its own capstan; a pumped vertical friction capstan gives 5 kN with four people. Probing depth in waste depends on how compact the debris is and has no published data.

**Requirements not met.** R9 (cost) was already far above USD 400 with a capstan in every kit; R2 was uncertain. Both carried to TRL 3.

**Decisions made under the pre-approvals.** HPL-DDR-001, items 1 to 16: pumped friction capstan; shear pin (R10); holding pawls and tail cleat (R11); sound anchors only; 14 mm rope; the capstan never lifts or pulls on a person; blunt hand-pushed probes; linked plywood boards; made HDPE stretcher; no lithium cells; no gas detector; six-signal stop rule with a lookout; Uganda Red Cross Society in Kampala with the Kiteezi pickers as first co-design candidate (not agreed); CalRig as first proof-load rig; combination padlock; budget kept.

**Safety concerns.** A second slide burying searchers; rope whip from an overloaded rope or a failed anchor; drum run-back; landfill gas; sharp waste and infection.

### TRL 3

**What was done.**

- `docs/04-calcs/01-sizing.md` and `docs/04-calcs/sizing.py` (HPL-CAL-001 v0.1), `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model with constructability checks (no overlaps, no floating parts, every item packs in the closed site box); STEP and STL in `cad/step` and `cad/stl` (capstan, probe, board pair, box, stretcher, clamp; assembly STEP in the display layout).
- `cad/src/sheets.py`: HPL-DWG-001 (hand capstan GA) and HPL-DWG-002 (site box, packed arrangement), Rev P2.
- `bom/bom.csv`: 30 lines, all priced, with suppliers by type.
- `cad/src/concept_media.py`: `media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.png` and `.pdf` (HPL-DWG-010), `model.glb` (coarse tessellation) and `viewer.html`. No cutaway; the capstan's inside is shown in the build plan joints.
- `docs/decisions/0002-design-for-construction.md` (HPL-DDR-002); `design_state: constructable`.
- `cad/src/build_plan_media.py`: overview, sixteen making sketches (HPL-DWG-101 to 116), eleven joint close-ups and fifteen step pictures; `docs/05-build-plan.md` (HPL-BLD-001) and `docs/06-design-decisions.md` (HPL-DEC-001).
- `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded, detail); scenes exported to `/home/claude/renders/heapline`. Photoreal renders, captions and cards are made on Amish's Mac; the README already leads with `media/render-hero.png`.
- `docs/01-problem.md` v0.2, `docs/02-concept.md` v0.3, `docs/03-requirements.md` v0.3, `README.md`, `project.yaml` (trl 3, trl_target 3).

**Results (HPL-CAL-001).** First probe line 4.6 min after the alarm. Capstan: 5 kN with four people at 114 N each; shear pin releases at 6.4 kN (5.1 to 7.6 kN); every capstan part, the rope (factor 4.5), the slings and the anchor eye sized on 8 kN; post 63 MPa; one holding pawl takes the design tension. Probes 3.07 m, 3.1 kg. Boards 9.7 kg, 44 mm sinkage, bridge a 0.8 m void at 4.0 MPa. Stretcher 510 N on level debris. Heaviest carried item 21.2 kg; carried kit 151 kg; site box 104 kg (stays at the shed). Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 1,599.00 (USD 201.00 under the target).

**Requirements not met or at risk.** R2 and R8 at risk, R5 at risk with two haulers, R9 not met; each is set out under Decisions for Amish. R6 is not verifiable at TRL 3.

### Decisions for Amish

Each item below is proposed, awaiting Amish, and is listed as open in `docs/06-design-decisions.md`. Effects are paper estimates from HPL-CAL-001.

**1. R2, probe depth: at risk.**
State: in loosened debris one person reaches the full 2.6 m usable depth, but in stiffer debris one person cannot start a probe and two reach 1.8 m. Cause: the 22 mm tip needs 380 N to start in stiff debris, more than one person's push, and near the surface a two-person push is capped by the probe's buckling load (506 N with 3 m free).

| Option | Effect on R2 | Cost | Mass |
| --- | --- | --- | --- |
| A: 18 mm tip on all six probes | Stiff debris: two people reach 2.6 m, one 0.6 m; loosened debris unchanged, if sleeve friction does not rise with the smaller clearance | No change | About 0.03 kg less a probe |
| B: three probes with 22 mm tips, three with 18 mm | Half the line as A, half as now | No change | Negligible |
| C: keep the 22 mm tip; measure debris resistance on a test heap at TRL 4 before choosing | None now | Test heap time only | None |

**Recommendation: A**, the 18 mm tip on all six, confirmed on a test heap at TRL 4; it is the only option that reaches 2.5 m on paper in stiff debris at no cost.

**2. R5, casualty transport: met with four haulers, at risk with two.**
State: on level debris the stretcher needs 510 N: 127 N each for four haulers, but 255 N each for two. Cause: friction of about 0.5 between HDPE and loose waste.

| Option | Effect on R5 | Cost | Mass |
| --- | --- | --- | --- |
| A: drill card rule: four haulers on debris; two only along the boards (153 N each) | Met in both cases | None | None |
| B: add a 10 m haul line with two shoulder loops so two more people pull from firm ground | 127 N each for four | About USD 15 | About 0.8 kg |
| C: both | Met with margin | About USD 15 | About 0.8 kg |

**Recommendation: A**: it meets R5 with no new parts, because the boards are already laid back to firm ground.

**3. R8, portable: at risk.**
State: the heaviest carried item is 21.2 kg, but the carried kit is 151 kg, 37.8 kg each if four people carry it in one trip. Cause: the capstan set (65 kg with stakes, rope, slings and clamp) on top of an 86 kg search kit.

| Option | Effect on R8 | Cost | Mass |
| --- | --- | --- | --- |
| A: two waves: four carry the search kit first (21.5 kg each, the 4.6 min of R1); a second group of three brings the capstan set (about 22 kg each) | Met for each wave; the capstan arrives a few minutes later | None | None |
| B: lighter boards (12 mm plywood on 45 x 45 battens) | Carried kit about 141 kg, 35 kg each for four | About USD 8 less | About 10 kg less |
| C: a two-wheeled handcart for the box contents | Met on tracks; poor on rough waste | About USD 150 more | About 25 kg more |

**Recommendation: A**: the capstan is not needed for the first probe line, so a second wave costs nothing and keeps R1.

**4. R9, cost: not met.**
State: USD 1,599 per site kit, against the per-kit cost target in HPL-REQ-001. Cause: the capstan set (USD 449), the site box with hardware (USD 253) and PPE with lighting (USD 263) on top of a USD 526 search core.

| Option | Effect on R9 | Cost | Mass |
| --- | --- | --- | --- |
| A: one capstan set shared by neighbouring sites, kept at the largest shed | About USD 1,150 a site | USD 449 less a site | Capstan wave only where it is kept |
| B: a reused crate or bought steel job box for the site box, and PPE from the cooperative's own stock | About USD 1,280 a site | About USD 320 less | Box mass unchanged or less |
| C: both | About USD 830 a site | About USD 770 less | As A and B |

**Recommendation: C**: it more than halves the cost without removing any function at the slide; no option within the concept reaches the target, so R9 would remain not met at about USD 830.

### Decisions made under the pre-approvals

HPL-DDR-002, the fifteen design-for-construction changes (below); the appearance model additions (below). All in `docs/06-design-decisions.md`.

### Build plan findings (design changes made for construction, HPL-DDR-002)

1. Capstan base frame 700 x 440 in 40 x 40 x 3 tube with a 100 x 40 x 4 centre member.
2. Post passes through the centre member, welded at both faces.
3. Hold-down roller takes the rope down to 38 mm, level with a rear anchor eye: no tipping.
4. Drum and spindle turn on acetal bushes on the fixed post.
5. Lever head with two sockets and a drive pawl: pumped through a quarter turn, nobody walks round.
6. Shear pin placed between the drive ratchet and the drum's top flange.
7. Pawl noses and pivots placed so the pawls clear the teeth (checked).
8. Keeper collar and pin on the post top.
9. Stake tubes and headed stakes.
10. Tail cleat on the rear member.
11. Probe spigot joints with R-clips; blunt 22 mm tip.
12. Boards on battens with pinned link plates.
13. Site box enlarged to 1700 x 1020 x 1060 so everything packs, capstan upright (checked).
14. Sheet clamp added.
15. Stretcher slots and straps defined.

### Appearance model

`product_model.py` uses the `model.py` solids in the display layout (kit beside the open box). Additions not in `model.py`: four turns of rope on the drum with a lead to the coil, the drill card on the inside of the lid, and a 1.75 m mannequin (`mannequin()`, standing) beside the capstan, behind it as seen from the hero camera so it is never between the camera and the kit. Decided under the pre-approvals.

### Safety concerns

- A second slide can bury searchers; the lookout and the six-signal stop rule are the only protection, and R6 (understood under stress) can only be shown in drills.
- Rope whip: the shear pin bounds rope tension, but a pin replaced by a bolt removes the bound; stop 3 and stop 6 say so.
- The capstan's anchor depends on finding a sound tree, vehicle or column on firm ground; where there is none the capstan is not used.
- Pulling debris near a buried person can shift the debris onto them; the capstan pulls sideways away from the dig only.
- Probes must never be driven; the blunt tip and the no-hammer rule protect a buried person.
- Landfill gas, sharp waste and infection remain hazards the kit cannot remove.
- The kit must not be used to argue against closing or rehabilitating a dumpsite.

### Recommended next step

When the phase allows TRL 4: Amish's choices on the four decisions above; then build one kit, run the shear pin release and proof-load tests on CalRig, the board and probe trials on a test heap of mixed waste, and timed drills with the first co-design candidate.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (HPL-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (HPL-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (HPL-REQ-001 v0.1): 9 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
