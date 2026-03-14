# Common Failures and Fixes

## Wrong ID type

Symptom:
- `market not found`
- empty order book
- invalid token ID / condition ID errors

Fix:
- Use `condition_id` with `get_market(...)` and market-scoped filters.
- Use `token_id` with `get_order_book(...)`, `get_tick_size(...)`, `get_neg_risk(...)`, and order placement.

## Price breaks tick-size rules

Symptom:
- order rejected for invalid price increment

Fix:
- fetch `tick_size = client.get_tick_size(token_id)`
- align price to the tick size
- or pass `PartialCreateOrderOptions(...)` with the market tick size

## Missing / wrong auth state

Symptom:
- L2-only methods fail
- order posting / cancel requests fail

Fix:
- initialize with private key + chain ID
- create or derive API creds
- set creds on the client before posting / cancelling / reading private data

## Wrong signature type or wrong funder

Symptom:
- signature problems
- account has funds but orders still fail

Fix:
- verify `POLYMARKET_SIGNATURE_TYPE`
- verify `POLYMARKET_FUNDER` is the address that actually holds funds
- for proxy / safe flows, do not assume the signer address is the funded address

## Not enough balance / allowance

Symptom:
- `not enough balance / allowance`

Fix:
- check `get_balance_allowance(...)`
- verify the funder has the needed collateral / outcome balance
- for EOA / MetaMask-style flows, verify allowances are set before trading

## Reused nonce / invalid expiration

Symptom:
- invalid nonce
- invalid expiration

Fix:
- avoid manually setting nonce unless needed
- if using GTD, ensure expiration is a valid future timestamp

## Plain dict passed as `options`

Symptom:
- attribute errors or unexpected order-builder failures

Fix:
- use `PartialCreateOrderOptions(...)`
- or omit `options` entirely and let the SDK auto-resolve

## Agent checklist before returning code

- Did you fetch token IDs from Gamma?
- Did you keep `condition_id` and `token_id` separate?
- Did you avoid hardcoded secrets?
- Did you choose the right signature type and funder?
- Did you keep the implementation limited to CLOB + Gamma?
