#!/usr/bin/env python3
"""Build per-currency FX and payment totals and CSV exports from Ebury MCP results.

Input: a JSON file with the `data` arrays copied from Ebury tool results:

    {
      "period": {"from": "2026-10-01", "to": "2026-10-31"},   # optional
      "trades":   [ ...items from search_trades / get_trade... ],
      "payments": [ ...items from search_payments / get_payment... ]
    }

Output (in --out, default ./ebury-report):
    trades.csv, payments.csv, totals.csv, summary.md

All money is handled with Decimal and kept per currency. Nothing is converted
between currencies, and no rate is computed except the optional average dealt
rate per pair, which is labelled as calculated.

Usage: python3 fx_report.py input.json [--out DIR]
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

DONE_PAYMENT = {"payment complete"}
DEAD_PAYMENT = {"payment rejected", "payment cancelled"}
DEAD_TRADE = {"cancelled"}


def dec(value, field, item_id):
    """Exact Decimal from a string or number; numbers go through str() to avoid float noise."""
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        sys.exit(f"Not a number in {field} of {item_id}: {value!r}")


def fmt(d):
    """Thousands separators, at least 2 decimals, never rounds away decimals that are there."""
    if d is None:
        return ""
    d = d.normalize() if d == d.to_integral_value() else d
    places = max(2, -d.as_tuple().exponent) if d.as_tuple().exponent < 0 else 2
    return f"{d:,.{places}f}"


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        sys.exit("Input must be a JSON object with 'trades' and/or 'payments' lists.")
    return data


def build(data):
    trades, payments = data.get("trades") or [], data.get("payments") or []
    seen_t, seen_p = set(), set()
    trade_rows, payment_rows = [], []
    totals = defaultdict(lambda: defaultdict(Decimal))  # currency -> metric -> amount
    counts = defaultdict(int)
    pairs = defaultdict(lambda: [Decimal(0), Decimal(0), 0, None])  # symbol -> [sold, bought, n, (sell_ccy, buy_ccy)]

    for t in trades:
        tid = t.get("trade_id")
        if tid in seen_t:
            continue
        seen_t.add(tid)
        status = (t.get("status") or "").strip()
        buy = dec(t.get("buy_amount"), "buy_amount", tid)
        sell = dec(t.get("sell_amount"), "sell_amount", tid)
        fee = dec(t.get("fee_amount"), "fee_amount", tid)
        bccy, sccy = t.get("buy_currency"), t.get("sell_currency")
        trade_rows.append({
            "order_date": t.get("order_date", ""),
            "settlement_date": (t.get("maturity_date") or "")[:10],
            "trade_id": tid,
            "type": t.get("trade_type", ""),
            "status": status,
            "sold_currency": sccy, "sold_amount": sell,
            "bought_currency": bccy, "bought_amount": buy,
            "dealt_rate": t.get("rate", ""), "rate_symbol": t.get("rate_symbol", ""),
            "fee_currency": t.get("fee_currency", "") if fee else "", "fee_amount": fee if fee else None,
            "reference": t.get("reference") or t.get("external_reference_id") or "",
        })
        if status.lower() in DEAD_TRADE:
            counts["trades_cancelled"] += 1
            continue
        counts["trades"] += 1
        if buy is not None and bccy:
            totals[bccy]["bought"] += buy
        if sell is not None and sccy:
            totals[sccy]["sold"] += sell
        if fee and t.get("fee_currency"):
            totals[t["fee_currency"]]["trade_fees"] += fee
        if buy is not None and sell is not None and sccy and bccy:
            p = pairs[f"{sccy}->{bccy}"]
            p[0] += sell; p[1] += buy; p[2] += 1; p[3] = (sccy, bccy)

    for p in payments:
        pid = p.get("payment_id")
        if pid in seen_p:
            continue
        seen_p.add(pid)
        status = (p.get("status") or "").strip()
        amt = dec(p.get("amount"), "amount", pid)
        ccy = p.get("currency") or p.get("payment_currency")
        fee = dec(p.get("fee_amount"), "fee_amount", pid)
        payment_rows.append({
            "payment_date": p.get("payment_date", ""),
            "payment_id": pid,
            "payee": p.get("beneficiary_name", ""),
            "currency": ccy, "amount": amt,
            "status": status,
            "reference": p.get("reference", ""),
            "funding_trade_id": p.get("trade_id") or "",
            "fee_currency": p.get("fee_currency", "") if fee else "", "fee_amount": fee if fee else None,
        })
        s = status.lower()
        if s in DEAD_PAYMENT:
            counts["payments_not_sent"] += 1
            continue
        key = "paid" if s in DONE_PAYMENT else "in_flight"
        counts["payments_" + key] += 1
        if amt is not None and ccy:
            totals[ccy][key] += amt
        if fee and p.get("fee_currency"):
            totals[p["fee_currency"]]["payment_fees"] += fee

    return trade_rows, payment_rows, totals, counts, pairs


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--out", default="ebury-report")
    args = ap.parse_args()

    data = load(args.input)
    trade_rows, payment_rows, totals, counts, pairs = build(data)
    os.makedirs(args.out, exist_ok=True)

    tf = ["order_date", "settlement_date", "trade_id", "type", "status", "sold_currency", "sold_amount",
          "bought_currency", "bought_amount", "dealt_rate", "rate_symbol", "fee_currency", "fee_amount", "reference"]
    pf = ["payment_date", "payment_id", "payee", "currency", "amount", "status", "reference",
          "funding_trade_id", "fee_currency", "fee_amount"]
    write_csv(os.path.join(args.out, "trades.csv"), sorted(trade_rows, key=lambda r: r["order_date"]), tf)
    write_csv(os.path.join(args.out, "payments.csv"), sorted(payment_rows, key=lambda r: r["payment_date"]), pf)

    metrics = ["bought", "sold", "paid", "in_flight", "trade_fees", "payment_fees"]
    total_rows = [{"currency": c, **{m: totals[c].get(m) for m in metrics}} for c in sorted(totals)]
    write_csv(os.path.join(args.out, "totals.csv"), total_rows, ["currency"] + metrics)

    period = data.get("period") or {}
    title = "# Ebury FX and payments summary"
    if period.get("from") and period.get("to"):
        title += f", {period['from']} to {period['to']}"
    lines = [title, ""]
    lines.append(f"Trades: {counts['trades']} (plus {counts['trades_cancelled']} cancelled). "
                 f"Payments: {counts['payments_paid']} sent, {counts['payments_in_flight']} in flight, "
                 f"{counts['payments_not_sent']} rejected or cancelled.")
    lines += ["", "## Totals per currency (never added across currencies)", "",
              "| Currency | Bought | Sold | Paid (sent) | In flight | Trade fees | Payment fees |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for r in total_rows:
        lines.append("| " + " | ".join([r["currency"]] + [fmt(r[m]) for m in metrics]) + " |")
    if pairs:
        lines += ["", "## Conversions by currency pair", "",
                  "| Sold → bought | Trades | Total sold | Total bought | Calculated average (bought per 1 sold) |",
                  "|---|---:|---:|---:|---:|"]
        for sym, (sold, bought, n, (sccy, bccy)) in sorted(pairs.items()):
            avg = (bought / sold).quantize(Decimal("0.000001")) if sold else None
            lines.append(f"| {sccy} → {bccy} | {n} | {fmt(sold)} {sccy} | {fmt(bought)} {bccy} | {avg if avg is not None else ''} |")
        lines += ["", "The average is calculated from the trades above for reporting only. It is not a dealt rate. "
                  "Each trade's dealt rate is in trades.csv as Ebury returned it."]
    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nFiles written to {os.path.abspath(args.out)}: trades.csv, payments.csv, totals.csv, summary.md")


if __name__ == "__main__":
    main()
