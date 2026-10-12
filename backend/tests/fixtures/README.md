# Parser fixtures

One directory per parser id, e.g. `tests/fixtures/hdfc.bank.pdf/`:

```
sample_01.pdf          # anonymised file in the bank's exact layout
sample_01.expected.yaml
```

`expected.yaml` asserts what every parser test must check:

```yaml
row_count: 42             # transaction rows
opening_balance: "12345.67"
closing_balance: "23456.78"
total_debits: "9876.54"
total_credits: "21987.65"
first: { date: 2025-04-01, amount: "-500.00" }
last:  { date: 2025-04-30, amount: "75000.00" }
```

Rules:
- **Never commit a real statement.** Fixtures are synthesised to mirror a real layout, using a
  redacted sample only as a template. Names, account numbers, UPI ids, UTRs and merchants are fake.
- Balances must still tie out (`opening + credits - debits = closing`), because the tie-out is
  what the tests check.
