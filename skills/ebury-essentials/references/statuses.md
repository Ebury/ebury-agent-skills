# Ebury statuses and what they mean

Use the status string exactly as the tool returns it, then explain it in plain words. Don't invent statuses that aren't listed here. If you see one that isn't listed, show it as returned and say you don't have an explanation for it.

## Payment status (in `search_payments` and `get_payment` results)

| Status shown | Plain meaning | Who acts next |
|---|---|---|
| `Need more beneficiary information` | Ebury needs more details about the payee before the payment can go. | The client: check Ebury Online or contact their account manager. |
| `Validating beneficiary information` | Ebury is checking the payee's details. | Usually nobody. If it lasts more than 2 business days, contact Ebury. |
| `Payment pending of authorization` | The payment is waiting for an authoriser on the client's account. | The client's authoriser(s). `approvals_workflow.minimum_remaining_authorisations` says how many approvals are still needed. |
| `Waiting for payment date` | Approved and scheduled for its payment date. | Nobody, unless funds are missing (check `fully_funded`). |
| `Executing Payment` | Ebury is sending the payment. | Nobody. |
| `Payment complete` | Ebury has sent the payment. Arrival depends on the route and the receiving bank. | Nobody. If the payee hasn't received it, see "Sent but not received" below. |
| `Payment rejected` | The payment was rejected and not sent. `rejected_by` and `rejected_date` say by whom and when. | The client, if they still need to pay. |
| `Payment cancelled` | The payment was cancelled and not sent. | The client, if they still need to pay. |

### Search filter tokens (for `search_payments` `status`)

These are different from the strings above:

- `pending`: not yet processed
- `pending_to_authorise`, `pending_your_approval`, `pending_others_approval`: waiting for approval
- `authorised`: approved, not yet complete
- `complete`, `cancelled`, `rejected`
- `all`

There is no `processing` filter. There is no "stuck" or age filter: to find old in-flight payments, search with `pending`, `pending_to_authorise` and `authorised` (one call each), merge by `payment_id`, and compare `created_date` with today.

### Flags in `get_payment` worth checking

| Field | If… | Tell the user |
|---|---|---|
| `fully_funded` | `false` | The payment is waiting for funds: a linked trade still settling, or a top-up of the account. |
| `trade_id` | set | The payment is funded by that trade. Check it with `get_trade` (status and `maturity_date`). |
| `approvals_workflow.minimum_remaining_authorisations` | above 0 | That many approvals are still needed. |
| `beneficiary_verified` / `beneficiary_authorised` | `false` | The payee isn't cleared yet. Ebury is checking it. |
| `beneficiary_blocked` | `true` | The payee is blocked. The client must contact Ebury. |
| `hold` | not empty | The payment is on hold. The client must contact their account manager. Don't guess the reason. |
| `AML_overdue` | `true` | A compliance check is outstanding. The client must contact their account manager. Don't speculate. |
| `returned` | `true` | The receiving bank sent the money back. Look for a `payment_returned` transaction with `search_transactions`. |
| `executed` | `true` | Ebury has sent it. |
| `uuid` with `is_uuid_used_for_tracking: true` | | The payment's end-to-end tracking id. The client can give it to the payee's bank to trace the payment. |

### Sent but not received

When a payment shows `Payment complete` but the payee says the money hasn't arrived:

1. Confirm the amount, currency, payment date and the payee's bank details (masked) from `get_payment`.
2. International payments can take a few business days and pass through intermediary banks, depending on the currency and route. Don't promise a time.
3. For SWIFT payments, the client can follow the payment in Ebury Online with Payment Tracker. You can't see tracking data through these tools; never invent it.
4. Give the client the tracking id (`uuid`) and the payment reference to pass to the payee, who can ask their bank.
5. If it's still missing after that, the client should contact their Ebury account manager.

## Trade status (in `search_trades` and `get_trade` results)

| Status | Plain meaning |
|---|---|
| `Created` | Booked. Ebury hasn't received the funds for it yet (awaiting funding). |
| `Funds In Partially` | Part of the funds has arrived. |
| `Funds In Full` | Fully funded. |
| `Funds Out Partially Allocated` | Some of the bought currency has been used, for example by payments. |
| `Funds Out Full Allocated` | All of the bought currency has been used. |
| `Closed` | Settled and finished. |
| `Cancelled` | Cancelled. |

There is no "Awaiting funding" status: that is `Created` or `Funds In Partially`. Funding is due by the trade's `maturity_date`.

Trade types you may see: `spot`, `forward`, `flexi_forward`, `window_forward`, `drawdown`, `ndf`.

## Payment approval (from `check_payment_approval`)

| Status | Meaning | What to do |
|---|---|---|
| `pending` | Not approved yet. | Give the link again if it's still valid (15 minutes from drafting). |
| `processing` | Ebury is creating the payment. | Tell the user; check once more only if they ask. |
| `submitted` | The payment was created. It has a `payment_id` and a status. | Report the payment status as returned. It may still need another authoriser or funds. Never say "sent" or "executed" unless the status says so. |
| `failed` | It wasn't created. | Show the reason. Don't retry without the user. |
| `unknown` | The outcome isn't known. | Don't draft again. Check `search_payments` first. |
| `rejected` / `refused` | The user rejected it. No payment was made. | Ask what they want to do. |
| `expired` | The link expired. | Check `search_payments` first, then offer to draft again. |
