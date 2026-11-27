# Previews

Keep them short and exact. Amounts always with their currency. Account numbers masked to the last 4 characters.

## Payment plan (first yes)

> **Payment to confirm**
>
> - Pay: {holder_name}, {bank name}, account ending {last 4}
> - Amount: {amount} {currency}
> - Reference: {reference}
> - Payment date: {date, "today", or "the day the conversion settles"} (Ebury confirms the value date when it's submitted)
> - Purpose code: {code} *(only if used)*
> - Funding: {"from your {currency} balance" | "convert {sell currency} into {amount} {currency} at a firm Ebury rate, linked to this payment" | "convert {sell currency} into the {shortfall} {currency} shortfall" | "you'll top up by bank transfer" | "funded later"}
> - Trade reason: {reason} *(only if converting)*
>
> Is this right? Reply yes to continue.

## Firm quote (second yes)

Show it the moment `get_quote` returns:

> **Firm rate, valid for about 15 seconds**
>
> - You sell: {sell_amount} {sell_currency}
> - You buy: {buy_amount} {buy_currency}
> - Rate: {rate} {rate_symbol}
> - Value date: {value_date}
>
> Book this? (yes / no)

## After drafting

> Your payment is ready for approval:
>
> {summary from draft_payment}
>
> **Approve it here: {approval link}**
> Log in, check the details and approve it with the verification code Ebury sends you. The link expires in 15 minutes. Tell me when you're done.

Never add a field to the approval message asking for the code.
