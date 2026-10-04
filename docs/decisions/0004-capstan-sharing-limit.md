---
doc_id: HPL-DDR-004
title: HeapLine siting limit for a shared capstan set
project: HeapLine
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-04'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-04'
  author: Amish Chadha
  change: Amish's round-3 decision 3A recorded
---

# 0004: Siting limit for a shared capstan set

- **Date:** 2026-10-04
- **Status:** accepted. Decided by Amish on 2026-10-04: "For round 3, I agree with all your proposed recommendations". For HeapLine this accepts option (a) of open decision 1 in HPL-DEC-001 (portfolio item 3A).

## Context

Decisions 22A and 23C keep one capstan set at the host site, brought by a second wave of three people. Its arrival grows with the walk from the host shed: 3.8 min after the alarm from 100 m, 9.2 min from 300 m, 14.8 min from 500 m, 28.5 min from 1 km [F4].

## Options considered

(a) Share only between sites within about 500 m walk of the host shed. (b) Share within about 1 km. (c) No limit, agreed site by site. Recommendation was (a).

## Decision

A shared capstan serves only sites within about 500 m walk of the host shed, so it arrives within about 15 min. Farther sites keep their own capstan set (USD 547) or rely on the search kit alone. The limit is checked in the TRL 4 timed drills (capstan wave drill, build plan Table 2).

## Consequences

Requirements text, calculation note, build plan drill table and registers only. No geometry or cost change. Value-engineering target: USD 1,800. Estimated cost of the constructable design: USD 1,374.00 (USD 426.00 under the target).
