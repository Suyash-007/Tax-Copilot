# Tax questions

Every Indian-tax edge case the app touches, written down rather than buried in code. Each entry has
the scenario, my best reading, the source(s), and a status. Code that depends on an entry carries
`// TAX-VERIFY: TQ-nnn`, and the UI shows the flag next to the affected number.

**Status:** `open` (not yet checked against a primary source) · `verified` (checked; source cited) ·
`decided` (you made a call; reason recorded).

**Source quality:** links marked *(secondary)* are commentary, not the statute. A rule cannot be
marked `verified: true` on a secondary source.

**Reading "w.e.f." dates:** an amendment "w.e.f. 1-4-2026" under the 1961 Act usually means
**AY 2026-27, i.e. FY 2025-26**. Getting this wrong shifts a rule by a year, so every entry states
the FY explicitly.

---

### TQ-001 · 87A rebate against special-rate income (111A / 112A) — open

- **Years:** FY 2023-24 and 2024-25 (disputed); FY 2025-26 onward (statutory bar).
- **Scenario:** new regime; slab income under the rebate threshold, plus STCG u/s 111A.
- **Best reading:** from FY 2025-26 (AY 2026-27) the Finance Act 2025 bars the rebate against tax
  on special-rate income. The ₹12L eligibility test still looks at *total* income, which includes
  capital gains. For FY 2024-25 and earlier, ITAT benches split: Delhi (Renu Singla) and Agra
  (Pramod Kumar Dubey) allowed the rebate; Rajkot (Kotecha) disallowed it.
- **Engine:** a per-FY rule `rebate_87a.excludes_special_rate`. For FY ≤ 2024-25 the app shows the
  liability both ways and does not pick a side.
- **Sources:** [Greater Kashmir explainer](https://m.greaterkashmir.com/article/explainer-tax-free-limit-of-rs-12-lakh-excludes-special-income/424363) *(secondary)* ·
  [TaxGuru](https://taxguru.in/income-tax/rebate-u-s-87a-applicability-stcg-u-s-111a-filing-itr.html) *(secondary)* ·
  [BCAJ](https://bcajonline.org/journal/rebate-and-capital-gains/) *(secondary)*. Primary to cite:
  Finance Act 2025, amendment to s. 87A.

### TQ-002 · 112A exemption in FY 2024-25 across the 23-Jul-2024 change — open

- **Scenario:** LTCG on listed equity both before and after 23 Jul 2024 in the same year.
- **Best reading:** one ₹1.25L exemption for the whole year, in aggregate (not ₹1L + ₹1.25L).
  Gains are taxed at 10% before and 12.5% on/after the date. **Open point:** which portion the
  exemption is set against first. Setting it against the 12.5% portion first is better for you;
  I need to confirm that this is allowed and how the AY 2025-26 ITR utility handled it.
- **Sources:** primary to cite: Finance (No. 2) Act 2024; CBDT FAQs on capital gains (Jul 2024).

### TQ-003 · HRA: which cities are "metro" (50%) — open

- **FY ≤ 2025-26:** Delhi, Mumbai, Kolkata, Chennai (Rule 2A, 1962 Rules). Bengaluru is non-metro (40%).
- **Tax year 2026-27:** the Income-tax Rules 2026 reportedly add **Bengaluru, Hyderabad, Pune,
  Ahmedabad** (draft Rule 279; reportedly notified 20 Mar 2026, in force 1 Apr 2026). The HRA
  exemption only matters under the old regime.
- **Needs from you:** city of residence for each year.
- **Sources:** [ClearTax](https://cleartax.in/s/hra-house-rent-allowance) *(secondary)* ·
  [Angel One](https://www.angelone.in/news/taxation/draft-income-tax-rules-2026-bengaluru-pune-hyderabad-ahmedabad-set-to-get-50-hra-rebate-in-new-rules) *(secondary)* ·
  [Patron Accounting](https://www.patronaccounting.com/blog/hra-exemption-2026-pune-bengaluru-hyderabad-ahmedabad-50-percent) *(secondary)*.
  Primary to cite: the notified Income-tax Rules 2026.

### TQ-004 · Section numbers under the Income-tax Act, 2025 — open

- **Scenario:** from tax year 2026-27 the UI shows both old and new section references.
- **What sources say:** 115BAC → 202; 80C → 123 (read with Schedule XV); 87A → 156 (one source
  says 155: conflict); 111A / 112A → not confirmed.
- **Engine:** `section_new` stays null with `verified: false` until each is checked against the
  Act text.
- **Sources:** [incometaxindia.gov.in, s. 1 of the 2025 Act](https://www.incometaxindia.gov.in/w/section-1-1) (primary; commencement 1 Apr 2026) ·
  [TaxGuru on Chapter VIII](https://taxguru.in/income-tax/chapter-vi-a-deductions-reorganised-chapter-viii-income-tax-act-2025.html) *(secondary)* ·
  [TaxAJ mapping](https://www.taxaj.com/learn/?p=635) *(secondary)*.

### TQ-005 · Converting US-share gains to INR (Rule 115) — open

- **Options:** (a) compute the gain in USD and convert it once at the SBI TT buying rate (TTBR) on
  the last day of the month before the month of transfer (literal Rule 115 for capital gains);
  (b) convert the sale value and the cost separately, each at the TTBR on the last day of the month
  before its own transaction month (common practice; captures the FX movement);
  (c) use the actual remittance rates.
- **Best reading:** (b) by default, set in the rule file (`fx.conversion_convention`) so it can be
  switched. The app shows the difference between (a) and (b).
- **RSU cost basis:** the FMV at vest that was taxed as a perquisite (Rule 3(8)).
- **Sources:** primary to cite: Income-tax Rules 1962, Rule 115 and Rule 3(8).

### TQ-006 · Foreign shares: holding period and rate across 23-Jul-2024 — open

- **Best reading:** shares listed only abroad are not "listed" (that means a recognised Indian
  exchange), so they are long-term after **24 months** both before and after the change. Before
  23 Jul 2024: LTCG 20% with indexation (s. 112). On or after: 12.5% without indexation. STCG is
  taxed at slab.
- **Sources:** primary to cite: s. 2(42A) and s. 112 as amended by the Finance (No. 2) Act 2024.

### TQ-007 · Debt MF units bought before 1-Apr-2023 — open

- **Best reading:** sold before 23 Jul 2024: long-term after 36 months, 20% with indexation (needs
  the CII table). Sold on or after: long-term after 24 months, 12.5% without indexation. Units
  bought on or after 1 Apr 2023 are specified MFs (TQ-008): deemed STCG at slab whatever the
  holding period.
- **Sources:** primary to cite: s. 50AA, s. 112, s. 2(42A); CII notification.

### TQ-008 · "Specified mutual fund" (s. 50AA): the definition changed — open

- **Up to FY 2024-25:** a fund with ≤ 35% of proceeds in domestic equity.
- **From FY 2025-26 (AY 2026-27):** a fund with > 65% in debt and money-market instruments, or a
  fund-of-funds with ≥ 65% in such funds. International FoFs and gold/silver funds bought after
  1 Apr 2023 fall *out* of 50AA for sales in FY 2025-26 onward; if held > 24 months they become LTCG
  at 12.5%.
- **Engine:** MF tax class is derived per FY from scheme facts (category, equity %, FoF status),
  never stored as a fixed attribute.
- **Sources:** [ICICI Pru Tax Reckoner 2025-26](https://www.icicipruamc.com/blob/knowledgecentre/tax_reckoner/Tax_Reckoner_2025_26.pdf) *(secondary)* ·
  [TaxHeal](https://www.taxheal.com/?p=127927) *(secondary)* ·
  [Arthgyaan](https://arthgyaan.com/blog/budget-2024-how-will-international-debt-and-gold-silver-funds-get-taxed-going-forward.html) *(secondary)*.
  One TaxGuru piece dates the change differently, so the sources conflict. Primary to cite:
  Finance (No. 2) Act 2024.

### TQ-009 · Cumulative FD/RD interest: accrual or receipt basis — open

- **Scenario:** a cumulative FD pays all its interest at maturity, but the bank deducts TDS on the
  interest accrued each year, and AIS reports it on accrual.
- **Best reading:** an individual may follow either method under s. 145 but must be consistent.
  TDS credit is claimed in the year the matching income is offered (Rule 37BA). The app defaults
  to accrual, which matches TDS and AIS.
- **Needs from you:** the method used in past returns (question Q6).

### TQ-010 · Employer NPS (80CCD(2)) and the ₹7.5L employer-contribution cap — open

- **Best reading:** 80CCD(2) is capped at 14% of salary (basic + DA) under the new regime from
  FY 2024-25 (10% before), and 10% under the old regime. Separately, employer contributions to
  EPF + NPS + superannuation above ₹7.5L a year are a taxable perquisite (s. 17(2)(vii)), and so
  is the accretion on them (s. 17(2)(viia)).

### TQ-011 · Surcharge and marginal relief — open

- **Best reading:** 10% / 15% / 25% / 37% above ₹50L / 1Cr / 2Cr / 5Cr. The new regime caps it at
  25%. On 111A, 112A, 112 and dividend income it is capped at 15%. Marginal relief applies at
  each step. Implemented in full even if it doesn't bite for you.

### TQ-012 · Unused basic exemption against special-rate gains — open

- **Best reading:** a resident can set the unused part of the basic exemption (the 0% slab) against
  111A / 112A / 112 income before applying the special rate. I need to confirm this applies under
  115BAC with its ₹3L / ₹4L zero slab.

### TQ-013 · Rounding — open

- **Best reading:** total income is rounded to the nearest ₹10 (s. 288A) and tax to the nearest
  ₹10 (s. 288B). Need the 2025-Act equivalents. Rule ids `rounding.income` and `rounding.tax`.

### TQ-014 · Advance tax, 234B and 234C with capital gains and dividends — open

- **Best reading:** instalments are 15/45/75/100% by 15 Jun / 15 Sep / 15 Dec / 15 Mar. No advance
  tax is due if the net liability after TDS/TCS is under ₹10,000. A shortfall caused by capital
  gains or dividends is excused from 234C if the tax is paid in the instalments remaining after the
  income arises. Need the 2025-Act mapping (s. 211 / 234B / 234C equivalents).

### TQ-015 · TCS on LRS remittances: rates and thresholds by date — open

- **Best reading:** up to 30 Sep 2023, 5% above ₹7L. From 1 Oct 2023 to 31 Mar 2025, 20% above ₹7L
  for investment remittances. From 1 Apr 2025 the threshold is ₹10L (Finance Act 2025). Education
  and medical remittances have lower rates. TCS is a credit in the year it is collected (26AS /
  Form 27D).
- **Sources:** primary to cite: s. 206C(1G) as amended; Finance Act 2023 and 2025.

### TQ-016 · Schedule FA: period, values and FX — open

- **Best reading:** calendar-year basis. The FY 2025-26 return reports CY 2025 (1 Jan – 31 Dec
  2025): initial, peak and closing values, plus income. Convert at the SBI TTBR on the relevant
  date, per the ITR instructions. Separately, Budget 2024 relaxed the Black Money Act *penalty*
  for small non-property holdings (≤ ₹20L); disclosure is still required. Check each AY's ITR-2
  instructions.

### TQ-017 · Foreign tax credit and Form 67 — open

- **Best reading:** Form 67 is due by the end of the AY, provided the return is filed within s. 139(1)
  or 139(4) (Rule 128(9) as amended in 2022). The credit is the lower of the US tax withheld and the
  Indian tax on that income. US withholding on dividends for an Indian resident with a W-8BEN is
  25% (India–US DTAA, Art. 10, portfolio holding).

### TQ-018 · RSU / ESPP — open

- **Best reading:** the perquisite (FMV at vest or allotment, minus anything paid) is salary,
  already in Form 16. For capital gains the cost is that FMV and the holding period starts at vest
  or allotment. Sell-to-cover shares are a disposal on the vest date.

### TQ-019 · Buybacks from 1-Oct-2024 — open

- **Best reading:** the whole buyback consideration is a deemed dividend (s. 2(22)(f)) taxed at
  slab; the cost of the shares bought back becomes a capital loss (s. 46A), usable under the normal
  set-off rules.

### TQ-020 · ITR form eligibility by year — open

- **Best reading:** from AY 2025-26, ITR-1 allows 112A LTCG up to ₹1.25L with no losses carried
  forward. Any foreign asset or foreign income → ITR-2. Intraday or F&O (business income) → ITR-3.
  Check each AY's notification. Tax year 2026-27 forms are not yet notified.

### TQ-021 · Return deadlines, and what is still actionable — open

- **Reported (Budget 2026):** ITR-1/2 due 31 Jul; ITR-3/4 without audit moved to 31 Aug; revised
  returns allowed up to 12 months after the end of the tax year (31 Mar), with a fee; updated
  returns allowed even where losses are reduced. To verify: whether these apply to FY 2025-26
  returns, and the belated-return date (31 Dec 2026).
- **Sources:** [Moneylife](https://www.moneylife.in/article/budget-202627-no-change-in-incometax-slabs-fm-offers-compliance-relief-for-individuals/79540.html) *(secondary)* ·
  [TaxGuru](https://taxguru.in/income-tax/itr-filing-2026-important-due-dates-budget-2026-updates-strategies.html) *(secondary)*.
  Primary to cite: Finance Act 2026.

### TQ-022 · Intraday and F&O — open (only if you trade them)

- **Best reading:** intraday equity is speculative business income; its losses set off only against
  speculative income and carry forward 4 years. F&O is non-speculative business income; losses set
  off against any head except salary and carry forward 8 years. Turnover follows the ICAI Guidance
  Note (2022 revision: options turnover = absolute profit or loss). The 44AB audit thresholds
  apply. Either one means ITR-3.

### TQ-023 · EPF interest on contributions above ₹2.5L — open

- **Best reading:** from FY 2021-22, interest on the part of employee contributions above ₹2.5L a
  year (₹5L if the employer doesn't contribute) is taxable (s. 10(11)/(12) provisos, Rule 9D).
  Needs the EPF passbook.

### TQ-024 · Grandfathering: where the 31-Jan-2018 FMV comes from — open

- **Best reading:** for listed shares, the highest price quoted on a recognised exchange on
  31 Jan 2018; for MF units, the NAV that day (s. 55(2)(ac)). Cost for tax = max(actual cost,
  min(FMV, sale value)). The app needs a reference file of these values (question Q9).

### TQ-025 · Which date is the "transfer date" for the 23-Jul-2024 split? — open

- **Scenario:** a listed share sold on 22 Jul 2024 (trade date) and settled on 23 Jul (T+1).
- **Best reading:** the trade (contract-note) date. The engine uses `trade_date`, and the edge
  case is flagged when a trade and its settlement straddle a rule boundary.
