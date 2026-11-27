---
name: ebury-fx-report
description: Report what a client converted and paid through Ebury over a period, per currency, with dealt rates, fees and balances, and export it as CSV for accounting. Use when the user asks what they converted, paid or spent in FX for a month, quarter or date range, wants an FX or payments summary for finance, a month-end report, or an export for Xero, Sage, NetSuite or a spreadsheet. Read-only.
---

# Ebury FX report

Build an accurate, per-currency report of a client's FX trades and payments for a period, from Ebury's data only. This Skill only reads.

Follow the rules in `ebury-essentials` if it's installed. The two that matter most here:

- **Never add amounts in different currencies.** Every total is per currency. A single-currency total is allowed only from `calculate_cash_position`, labelled "indicative".
- **Show dealt rates exactly as Ebury returned them.** Don't compute or round rates, except the labelled average described below.

## 1. Agree the scope

Ask only for what's missing:

- **Period.** Default: last full calendar month. Use the client's dates exactly.
- **Client account.** From `list_clients`.
- **What to include.** Default: trades, payments, current balances. Fees only if asked or if the period is small (see step 2).
- **Output.** Default: a summary in chat plus CSV files. If they name an accounting system, see `references/export-formats.md`.

## 2. Collect the data

Make these calls for the period:

1. **Trades:** `search_trades` with `from_order_date` and `to_order_date`. For fees, margin or receipts on a trade, call `get_trade`.
2. **Payments:** `search_payments` with `from_payment_date`, `to_payment_date` and `status: all`, so rejected and cancelled ones are visible too.
3. **Money in and out (if asked):** `search_transactions` with full datetimes (`2026-10-01T00:00:00` to `2026-10-31T23:59:59`). Use `transaction_type` to narrow: `incoming` for money received, `margin`, `payment_returned`.
4. **Balances:** `list_balances`. These are **today's** balances, not balances at the end of the period. Label them "balances now".
5. **Fees on payments:** only `get_payment` shows them. Call it for each payment only if the user asks for fees and there are 25 payments or fewer. Otherwise, say payment fees aren't included and offer to fetch them for specific payments.

If a result says it is partial or asks you to narrow the filters, split the period (for example by week) and call again. Remove duplicates by `trade_id` and `payment_id`. Say if any part of the period couldn't be fetched.

## 3. Compute the totals

If you can run code, copy the `data` arrays from the trade and payment results into a JSON file and run:

```
python3 scripts/fx_report.py report-input.json --out ebury-report
```

The input format is in the script's header. It writes `trades.csv`, `payments.csv`, `totals.csv` and `summary.md`, using exact decimal arithmetic. Copy amounts exactly as returned.

Without code, add amounts carefully per currency and say the totals were added by hand.

How to count:

- **Trades:** cancelled trades are listed but not counted in totals.
- **Payments:** `Payment complete` counts as sent; rejected and cancelled count as not sent; anything else is in flight.
- **Average rate per pair:** only if the user asks. Compute it as total bought ÷ total sold for that pair, with code, and label it "calculated average, not a dealt rate". Show the inputs.

## 4. Present the report

Keep it to one screen. In order:

1. **Headline**, one line per currency, for example "Converted GBP 15,000.00 into USD 17,473.55 in 2 trades; paid USD 11,623.55 to 2 payees."
2. **Trades**: date, trade id, type, sold, bought, dealt rate with its symbol (for example `1.162345 GBPUSD`), status.
3. **Payments by currency and payee**: count and total per payee, per currency. List in-flight, rejected and cancelled separately.
4. **Balances now**, per currency. Add `calculate_cash_position` only if they ask for one total, and label it indicative.
5. **Notes**: anything not included (fees, partial results), and which figures were calculated.

Then offer the CSV files.

## What this report can't tell you

Say so if asked, and don't estimate:

- **Historical market rates or spreads.** `get_fx_rate` only gives today's indicative rate. The cost of a past trade compared with the market can't be computed from these tools. Suggest the client asks their Ebury dealer.
- **Balances on a past date.** Only current balances are available.
- **Accounting treatment** (realised gains or losses, VAT): that's for the client's accountant. The report gives the source figures.

## Example

"What did we convert and pay in October?" → `search_trades` (1–31 Oct), `search_payments` (1–31 Oct, `all`), `list_balances` → script → "In October you converted GBP 15,000.00 into USD 17,473.55 in 2 spot trades (dealt rates 1.162345 and 1.17 GBPUSD). You paid USD 11,623.55 to 2 payees; USD 0.20 is still in flight and one EUR 500.00 payment was rejected. Balances now: … Want the CSV files?"
