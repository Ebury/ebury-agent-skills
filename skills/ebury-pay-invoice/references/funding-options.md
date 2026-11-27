# Funding options when the balance is short

Explain the options in plain words and let the user choose. Show amounts per currency only.

## A. Convert the full invoice amount, linked to this payment

- One spot trade buys exactly the invoice amount. The payment is drafted with that `trade_id` as its funding source.
- `book_trade` with `convert: false`: the trade is tied to the payment.
- The payment date must be on or after the trade's `maturity_date`.
- Best when the client holds little or none of the invoice currency. It leaves a clean record: one invoice, one trade, one payment.

## B. Convert only the shortfall

- One spot trade buys the missing amount into the client's balance in the invoice currency (`book_trade` with `convert: true`). The payment is then paid from the balance.
- Set the payment date on or after the trade's `maturity_date`, so the funds are there.
- Best when the client already holds most of the amount.

## C. Top up by bank transfer

1. `get_accounts` with the invoice currency, then `get_account_details` for that account.
2. Give the client the account details to send money to.
3. If the account holder (`account_name`) is an Ebury entity rather than the client, it's a pooled account: the transfer reference **must be the client id**, so Ebury can credit the right client. Always say this.
4. Then draft the payment. It can be approved now and goes once the funds arrive.

## D. Prepare the payment now, fund it later

- Draft the payment as it is. Ebury warns that funds are insufficient. The payment can be approved; it's held until funds arrive from a trade or a top-up.
- Tell the user the payment won't go until then.

## Not covered here

Forwards, payments on a later date at today's rate, and target rates. Suggest the client speaks to their Ebury dealer.
