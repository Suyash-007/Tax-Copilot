# Rule files

Statutory tax rules live here as data. The engine reads them and **never hardcodes** a slab, limit,
rate, holding period or date. Changing a value and recomputing changes the result with no code change.

The format is fixed in Phase 0. The files themselves are written in Phase 4, every rule starting
at `verified: false`.

## Files

| File | Contents |
|------|----------|
| `FY2022-23.yaml` … `FY2025-26.yaml` | One file per financial year (Income-tax Act, 1961; previous year / assessment year) |
| `FY2026-27.yaml` | Tax year 2026-27 (Income-tax Act, 2025). Same shape; `section_new` populated |
| `taxonomy.yaml` | Life categories and tax-bucket leaf codes (Phase 3) |
| `manual_inputs.yaml` | Keys you can supply by hand (rent paid, city, landlord PAN…) and their shapes (Phase 4) |

## Shape

```yaml
meta:
  fy: "2025-26"
  assessment_year: "2026-27"   # null from tax year 2026-27 onward
  tax_year: null               # "2026-27" from 2026-27 onward
  act: "Income-tax Act, 1961"
  file_version: 1              # bump on every edit; recorded on each computation with the file's sha256
  reviewed_on: null

rules:
  regime.new.slabs:
    - value:                   # amounts in rupees; rates as decimal strings, never floats
        - { upto: 400000,  rate: "0" }
        - { upto: 800000,  rate: "0.05" }
        - { upto: 1200000, rate: "0.10" }
        - { upto: 1600000, rate: "0.15" }
        - { upto: 2000000, rate: "0.20" }
        - { upto: 2400000, rate: "0.25" }
        - { upto: null,    rate: "0.30" }
      section_old: "115BAC(1A)"
      section_new: null        # filled for FY 2026-27 onward, once verified against the Act text
      source_url: "https://…"
      effective_from: 2025-04-01
      effective_to: 2026-03-31
      verified: false
      notes: ""

  cg.equity_112a.rate:         # one id, several dated entries inside one FY
    - value: "0.10"
      effective_from: 2024-04-01
      effective_to: 2024-07-22
      section_old: "112A"
      source_url: "https://…"
      verified: false
    - value: "0.125"
      effective_from: 2024-07-23
      effective_to: 2025-03-31
      section_old: "112A"
      source_url: "https://…"
      verified: false
```

## Rules for rule files

1. Every entry has `source_url`, `effective_from`, `effective_to` and `verified`. A primary source
   (the Act, a Finance Act, CBDT notification or circular, the ITR instructions) is preferred.
   A secondary source is allowed only with `verified: false` and a note saying so.
2. Entries for one id must not overlap, and must cover the whole FY if the id is required that year.
3. The engine looks rules up by id and date: `rules.get("cg.equity_112a.rate", on=transfer_date)`.
   A missing id is a hard error. There are no defaults in code.
4. A computation records the file name, sha256 and `file_version`, plus every `verified: false`
   rule it used. The UI shows those flags next to the numbers they affect.
5. Anything ambiguous gets a `TAX_QUESTIONS.md` entry, referenced from `notes` (e.g. `TQ-001`).

## Planned rule ids (Phase 4–6)

`regime.{old,new}.slabs` · `regime.{old,new}.standard_deduction` · `rebate_87a.{max,income_limit,marginal_relief,excludes_special_rate}` ·
`surcharge.{slabs,cap_new_regime,cap_special_rate}` · `cess.rate` · `rounding.{income,tax}` ·
`ded.80c.cap` · `ded.80ccd_1b.cap` · `ded.80ccd_2.pct_of_salary` · `ded.80d.*` · `ded.80tta.cap` · `ded.80ttb.cap` ·
`hp.24b.self_occupied_cap` · `hra.metro_cities` · `hra.pct_{metro,non_metro}` ·
`cg.holding_months.{listed_equity,foreign_shares,other}` · `cg.equity_111a.rate` · `cg.equity_112a.{rate,exemption}` ·
`cg.foreign_112.rate` · `cg.debt_mf.*` · `cg.specified_mf_50aa.*` · `cg.grandfathering.cutoff_date` · `cg.cii` ·
`cg.setoff.*` · `cg.carry_forward_years` · `fx.conversion_convention` · `tcs.lrs.*` · `advance_tax.schedule` ·
`interest.234b` · `interest.234c` · `itr.eligibility.*` · `schedule_fa.period`
