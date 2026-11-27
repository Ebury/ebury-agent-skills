# Explaining a payment status

Use the status exactly as returned, then the plain explanation and next step below.

| Status | Say | Next step |
|---|---|---|
| `Need more beneficiary information` | Ebury needs more details about the payee before it can send the payment. | Check Ebury Online for the request, or contact the account manager. |
| `Validating beneficiary information` | Ebury is checking the payee's details. This is a normal step. | Nothing for now. If it lasts more than 2 business days, contact Ebury. |
| `Payment pending of authorization` | It's waiting for approval from an authoriser on your account. | The authoriser approves it in Ebury Online. Say how many approvals remain (`minimum_remaining_authorisations`). |
| `Waiting for payment date` | It's approved and will be sent on its payment date. | Nothing, unless `fully_funded` is `false`: then the funds must arrive first. |
| `Executing Payment` | Ebury is sending it now. | Nothing. |
| `Payment complete` | Ebury has sent it. How long it takes to arrive depends on the currency, the route and the receiving bank. | If the payee hasn't received it after a few business days: Payment Tracker in Ebury Online (SWIFT payments), share the tracking id, then contact Ebury. |
| `Payment rejected` | It was rejected and no money was sent. | Say who rejected it and when, if the result shows it. Ask if they want to pay again. |
| `Payment cancelled` | It was cancelled and no money was sent. | Ask if they still need to pay. |

## Funding

| What you see | Say |
|---|---|
| `fully_funded: false`, linked trade `Created` | "It's waiting for the funds for the currency conversion. They're due by {maturity_date}." |
| `fully_funded: false`, linked trade `Funds In Partially` | "Part of the funds for the conversion has arrived; the rest is due by {maturity_date}." |
| `fully_funded: false`, no trade | "There isn't enough {currency} in the account yet. It will go once the account is topped up." |

## Flags

| What you see | Say |
|---|---|
| `hold` set, `AML_overdue: true` or `beneficiary_blocked: true` | "Ebury needs to look at this payment. Please contact your account manager." Don't guess the reason. |
| `returned: true` | "The receiving bank returned this payment." Show the `payment_returned` transaction if you found it. |
