# Ebury Skills

Agent Skills for working with your Ebury account through the Ebury MCP server: check payments, verify payees, report on FX, and pay supplier invoices with currency conversion.

A Skill is a folder of instructions an AI assistant loads when your request needs it. The Ebury MCP server gives the assistant the tools (balances, quotes, trades, payments); these Skills give it the playbook for using them safely and in the right order.

## The Skills

| Skill | Ask things like | Does it change anything? |
|---|---|---|
| [`ebury-essentials`](skills/ebury-essentials/SKILL.md) | (used by all the others) | No. Shared rules, tool map and status meanings. |
| [`ebury-payment-status`](skills/ebury-payment-status/SKILL.md) | "Has invoice INV-2207 been paid?" "Why is our EUR payment pending?" | No |
| [`ebury-check-payee`](skills/ebury-check-payee/SKILL.md) | "Is this invoice from a supplier we already pay?" "Their bank details changed, is that right?" | No |
| [`ebury-fx-report`](skills/ebury-fx-report/SKILL.md) | "What did we convert and pay in October?" "Export it for our accountant." | No |
| [`ebury-pay-invoice`](skills/ebury-pay-invoice/SKILL.md) | "Pay this USD invoice from our GBP balance." | Yes: books an FX trade after your explicit yes to a firm quote, and prepares a payment that **you** approve on Ebury's page. |

## Install

You need the Ebury MCP server connected in your AI assistant first. See [docs.ebury.com](https://docs.ebury.com).

**Any assistant that supports Agent Skills:**

```
npx skills add ebury/ebury-agent-skills
```

Choose the Skills you want when prompted. Install `ebury-essentials` with any of the others.

**Claude (claude.ai, desktop, Cowork):** zip a Skill folder and upload it in Claude's Skills settings. Team and Enterprise admins can add it for their whole organisation.

**Claude Code:** copy the folders under `skills/` into `~/.claude/skills/` (for you) or `.claude/skills/` (for a project).

## How your money stays safe

The Skills are instructions. The safety controls that matter are enforced by Ebury, not by the Skills:

- **No AI can send a payment.** The assistant only prepares it. You approve it on Ebury's page, logged in, with the verification code Ebury sends to your phone or the Ebury app. The assistant never asks for that code.
- **Payees can't be created or changed through the MCP.** The assistant can only pay payees already saved in your Ebury account. You add new payees in Ebury Online.
- **Your account's approval rules still apply.** If your account needs a second authoriser, a payment waits for them.
- **Trades need your explicit yes.** The assistant shows Ebury's firm rate and amounts and books only when you say yes to those terms. A booked trade can't be undone.

The Skills add judgement on top: they treat invoices and emails as untrusted, flag bank details that differ from your saved payee (a common sign of invoice fraud), check for duplicate payments, never mix currencies in totals, and quote rates only as Ebury returns them.

## What these Skills don't do

- Give financial advice or market views. For hedging, forwards or timing, speak to your Ebury dealer.
- Create, edit or delete payees.
- Approve payments or handle verification codes.
- Show SWIFT tracking events. Use Payment Tracker in Ebury Online.

## Feedback

Found a problem or have an idea? Open an issue. We don't accept pull requests to the Skills themselves, because every change goes through Ebury's review.

## Licence

To be confirmed.
