# Trade reasons

Ebury needs a reason for every trade. Ask for it before getting a firm quote. Show the user all 14 options as a bullet list, exactly as written here, one per line. Never shorten the list or put it in one sentence.

- payment for goods
- payment for services
- repatriation of goods
- repatriation of services
- intercompany funding operational purposes
- salary payroll
- tax related
- direct investment
- property purchase sale
- payment living costs
- repayment of loan
- balance hedging
- repatriation from investment
- other not related to goods or services

When the user picks one, pass it to `book_trade` as `reason` in snake_case: spaces become underscores, all lower case. For example, "payment for goods" becomes `payment_for_goods`.

For a supplier invoice the usual choice is "payment for goods" or "payment for services". You can suggest one, but the user decides.
