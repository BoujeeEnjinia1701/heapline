---
doc_id: HPL-MKT-001
title: HeapLine market and viability
project: HeapLine
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-11-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-03'
  author: Amish Chadha
  change: First market note, written for the kit 1.9.1 upgrade; prices cited with the date they were checked
---

# HeapLine market and viability

The users are waste pickers' cooperatives and the site operators, municipal units and Red Cross branches that stand behind them; nothing was found that packages a probe, board, stretcher and capstan kit for a dumpsite, so the benchmarks below price single items only. An open design lets a local workshop build and mend the kit from stock steel, timber and rope for an estimated USD 827 a site plus USD 547 for each shared capstan set, and lets it spread through cooperatives, NGOs and workshops without a licence fee. Method: STANDARDS section 23.

*Table 1. Market segments.*

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Waste pickers' cooperatives and associations | Active dumpsites with homes at the toe, for example Kiteezi (Kampala) and Koshe (Addis Ababa) ([IDS, 2017](https://www.ids.ac.uk/opinions/recognise-informal-waste-pickers-to-avoid-future-disasters-like-koshe/)) | Avalanche probe, one 320 cm: Black Diamond Quickdraw Pro 320, USD 74.96, retailer page checked 2026-11-03 ([evo](https://www.evo.com/products/200661-black-diamond-quickdraw-pro-320-probe)); HeapLine has six probes in the kit | Search kit USD 827 a site (HPL-CAL-001 G1) | A site-kept kit with a plan, lookout and stop rule that people on site can use in the first minutes |
| Site operators and municipal staff | Sites awaiting closure or rehabilitation | Folding pole stretcher: USD 179.00 (350 lb rating), retailer page checked 2026-11-03 ([SOS Products](https://www.sosproducts.com/Folding-Pole-Stretcher-p/122795.htm)); HeapLine's HDPE sheet stretcher is BOM line 23, USD 82 | Host site USD 1,374 (search kit and the shared capstan set) | A low-cost emergency measure that can be stocked and inspected monthly |
| Red Cross branches, fire and police responders | Handover from community search to formal rescue | A 2 ton hand cable puller (come-along), USD 83.99, listed as discontinued, retailer page checked 2026-11-03 ([Paul B Hardware](https://paulbhardware.com/maasdam-144sb-6-cable-puller-2-ton-lifting-3-16-in-dia-rope-cable-12-ft-l-rope-cable-6)); for scale only: it is a different, wire-rope machine, not tested against the 5 kN pull here | Capstan set USD 547 shared by neighbouring sites (HPL-CAL-001 G1b) | Arrive to a search that is organised, with marks placed |
| Local fabricators | Workshops near dumpsites | No kit price found for a made, site-held slide-rescue kit: to assess | Parts only; labour and workshop margin to assess | A paid build and repair service from open drawings |

## Open route

Cooperatives and NGOs would borrow or buy a kit, local fabricators would build it from `bom/bom.csv` and the drawings, and universities and makerspaces could build a test unit. The hardware is under CERN-OHL-S-2.0 and the calculators under MIT (`REUSE.toml`), so any maker can share improvements back under the same terms. Whether a commercial supplier would ever sell kits is Amish's decision and is not assumed here.

## Viability

On paper the parts cost is USD 426 under the USD 1,800 value-engineering target (a hypothetical control target, not a limit). Demand is episodic and tied to rainy seasons and to cooperatives' ability to inspect the kit monthly. Unknown and all "to assess" with a co-design partner: willingness to pay, how many sites would share a capstan, local labour rates and who pays for the monthly inspection. No price in this note is a quote; unit costs come from `bom/bom.csv`, which is indicative.

## Sources

- IDS, Recognise informal waste pickers to avoid future disasters like Koshe, 2017, <https://www.ids.ac.uk/opinions/recognise-informal-waste-pickers-to-avoid-future-disasters-like-koshe/>.
- evo, Black Diamond Quickdraw Pro 320 Probe, USD 74.96, <https://www.evo.com/products/200661-black-diamond-quickdraw-pro-320-probe>, checked 2026-11-03.
- SOS Products, Folding Pole Stretcher 122795, USD 179.00, <https://www.sosproducts.com/Folding-Pole-Stretcher-p/122795.htm>, checked 2026-11-03.
- Paul B Hardware, Maasdam Powr-Pull 2 ton cable puller MP144SB6, USD 83.99, discontinued, checked 2026-11-03 (shared with SiltHaul).
