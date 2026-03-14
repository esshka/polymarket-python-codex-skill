---
name: polymarket-python-codex-skill
description: Build, review, and debug Python integrations against Polymarket's official CLOB client (`py-clob-client`) and the public Gamma API. Use when Codex needs to discover markets, normalize `clobTokenIds`, inspect books and prices, configure authenticated trading clients, place or cancel orders, query balances or trades, or diagnose Polymarket Python SDK failures while keeping `condition_id` and `token_id` separate.
---

# Polymarket Python SDK Skill

Use this skill for backend Python work only. Keep scope to Polymarket CLOB plus Gamma. Do not switch to Builder, relayer, or browser-side flows unless the user explicitly asks.

## Follow these rules

- Use `py-clob-client` for all CLOB reads and trading actions.
- Use Gamma for public market discovery and `clobTokenIds`.
- Keep `condition_id` and `token_id` distinct in every code path.
- Treat `clobTokenIds` as the source of orderable token IDs.
- Initialize authenticated clients with the correct `signature_type`, `funder`, and L2 credentials.
- Keep private keys and API secrets in environment variables.
- Respect tick size, price bounds, and `neg_risk`.
- Use `PartialCreateOrderOptions(...)` or omit `options`; do not assume a plain dict is accepted.

## Pick the workflow

- Discover markets or token IDs: read `tasks/market_discovery.md`.
- Inspect public books, prices, spreads, or market metadata: read `tasks/read_only_clob.md`.
- Configure authenticated trading access from environment variables: read `tasks/trading_setup.md`.
- Place, query, or cancel orders: read `tasks/order_workflows.md`.
- Debug common failures: read `tasks/common_failures.md`.
- Need supported scope, preferred SDK methods, or the source-vs-docs warning for `options`: read `tasks/sdk_reference.md`.

## Use the bundled examples

- `examples/gamma_find_markets.py`: fetch a market and normalize `clobTokenIds`.
- `examples/clob_read_only.py`: inspect order books, prices, and market metadata.
- `examples/trading_client_from_env.py`: build an authenticated client from environment variables.
- `examples/place_limit_order.py`: submit a limit order with explicit metadata.
- `examples/place_market_order.py`: submit a market order.
- `examples/manage_orders.py`: check balances, query open orders, cancel orders, and inspect trades.

## Return code that matches the request

- Prefer Gamma plus read-only CLOB calls when the user only needs discovery or market data.
- Ask for or read secrets only when the task truly requires authenticated trading actions.
- Return both `condition_id` and normalized `clobTokenIds` when generating market-selection code.
- Keep examples small and executable; do not add extra abstractions.

## Verify facts against the bundled sources

Use `sources.md` when you need the official docs or SDK source links that informed this skill.
