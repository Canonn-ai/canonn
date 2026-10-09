# Payables agent: invoices checked against their contracts

An accounts-payable agent on Canonn R1. Each invoice is read against the contract it belongs to; the agent pays the ones that match and holds the ones that do not, quoting the contract sentence and the invoice sentence that disagree.

```bash
python make_pairs.py                    # 50 fictional pairs, 5 planted mismatches
CANONN_API_KEY=... python agent.py      # key: https://canonn.ai/dashboard/
```

Our run on 3 October 2026 (production, eight invoices at a time): 50 invoices in 28.8 s, all 5 planted mismatches held with verbatim quotes, no correct invoice held, USD 0.0057 for the run. The company, vendors and amounts are fictional; the mismatches are deliberately clear, so treat this as a working example, not a benchmark.
