# Exports

The script writes plain CSV files with one row per trade or payment, and amounts as exact decimals with a separate currency column. Most accounting tools can import them with a column mapping.

## Files

| File | One row per | Columns |
|---|---|---|
| `trades.csv` | trade | order_date, settlement_date, trade_id, type, status, sold_currency, sold_amount, bought_currency, bought_amount, dealt_rate, rate_symbol, fee_currency, fee_amount, reference |
| `payments.csv` | payment | payment_date, payment_id, payee, currency, amount, status, reference, funding_trade_id, fee_currency, fee_amount |
| `totals.csv` | currency | currency, bought, sold, paid, in_flight, trade_fees, payment_fees |
| `summary.md` | | The summary tables shown in chat. |

## Importing into an accounting system

Don't claim a file is in a specific system's import format. Instead:

1. Ask which system and which import they use (for example a bank statement import or a manual journal import).
2. Ask for their import template, or the column names it expects, if they have it.
3. Map the columns above to their template, keeping one currency per row and amounts unchanged.
4. Remind them to check the import on a few rows first.

Useful mappings:

- **Bank statement style imports** usually want date, description, reference and a signed amount, one file per currency account. Use `payments.csv` (amount as money out) for each currency separately.
- **Journal imports** usually want date, account, debit, credit, currency and a description. Each trade is two lines: the bought currency in and the sold currency out, with the dealt rate in the description.

Account codes, tax codes and the treatment of FX gains or losses are the client's accounting choices. Leave those columns for them to fill.
