# Polymarket Python SDK Skill (CLOB + Gamma)

Use this skill when generating, reviewing, or debugging **Python** code that interacts with:

- Polymarket's official Python CLOB client: `py-clob-client`
- Polymarket's public **Gamma API** for market discovery

This skill is for **backend / scripting / agentic coding** work. It is intentionally scoped to **CLOB + Gamma** only.

## Scope

Included:
- public market discovery with Gamma (`/markets`, `/events`, `/tags`, `/sports`)
- read-only CLOB access (order books, prices, tick size, neg risk, market metadata)
- authenticated CLOB trading flows with `py-clob-client`
- balances, allowances, orders, cancellations, and trade history
- correct use of **condition IDs** vs **token IDs**

Excluded:
- Builder APIs
- Builder signing / relayer SDKs
- front-end browser code that would expose secrets
- unrelated Polymarket products

## Non-negotiable rules for coding agents

1. **Use the official Python SDK for CLOB work.**
   - Install with `pip install py-clob-client`
   - Default host: `https://clob.polymarket.com`
   - Default chain: `137` (Polygon mainnet)

2. **Use Gamma for market discovery, not the trading client.**
   - Gamma is public and unauthenticated.
   - Use it to find events, markets, slugs, tags, and `clobTokenIds`.

3. **Never confuse IDs.**
   - `condition_id` identifies a market.
   - `token_id` identifies a specific YES / NO (or outcome) token.
   - `client.get_market(condition_id)` takes a **condition ID**.
   - `client.get_order_book(token_id)`, `client.get_tick_size(token_id)`, `client.get_neg_risk(token_id)`, and order placement all use a **token ID**.

4. **Treat `clobTokenIds` as the source of orderable token IDs.**
   - For standard binary markets, the first ID is the **YES** token and the second ID is the **NO** token.
   - Do not guess token IDs from slugs or condition IDs.

5. **All authenticated CLOB actions require a properly initialized client.**
   - Create or derive API credentials with `create_or_derive_api_creds()`.
   - Then call `set_api_creds(...)` or initialize `ClobClient(..., creds=...)`.

6. **Choose the correct signature type and funder.**
   - `0` = EOA
   - `1` = `POLY_PROXY`
   - `2` = `GNOSIS_SAFE`
   - The **funder** is the address that actually holds the funds.

7. **Never expose secrets in generated code.**
   - Keep private keys and API secrets in environment variables.
   - Do not put authenticated CLOB code into browser/client-side code.

8. **Respect price / tick-size constraints.**
   - Order prices are between `0` and `1`.
   - Prices must conform to the market's tick size.
   - If the market is negative-risk, the order must be built with `neg_risk=True`.

9. **Prefer explicit market metadata when you already have it, but know the SDK can auto-resolve.**
   - The current `py-clob-client` source auto-resolves `tick_size`, `neg_risk`, and fee rate for `create_order(...)` and `create_market_order(...)` when options are omitted.
   - When you already fetched market metadata, passing it explicitly is still a good pattern for clarity.

10. **Do not use Builder / relayer flows here.**
    - Keep generated code limited to CLOB + Gamma.

## Important source-vs-docs note

Some Polymarket Python quickstart snippets show `options={"tick_size": ..., "neg_risk": ...}`.
The current `py-clob-client` source types `options` as `PartialCreateOrderOptions` and accesses `options.tick_size` / `options.neg_risk`.

In this skill:
- use `PartialCreateOrderOptions(...)`, or
- omit `options` and let the SDK auto-resolve them.

Do **not** pass a plain dict unless you have verified the installed SDK version accepts it.

## Recommended workflow

### 1) Discover a market with Gamma

Use `requests` against `https://gamma-api.polymarket.com`.

Common patterns:
- `GET /markets?slug=...`
- `GET /events?slug=...`
- `GET /markets?active=true&closed=false&limit=...`
- `GET /events?tag_id=...&active=true&closed=false`

Extract:
- `condition_id` or market ID context
- `clobTokenIds`
- question / slug / outcome labels

### 2) Use read-only CLOB methods to validate tradability

Typical checks:
- `get_order_book(token_id)`
- `get_midpoint(token_id)`
- `get_price(token_id, side="BUY")`
- `get_tick_size(token_id)`
- `get_neg_risk(token_id)`
- `get_market(condition_id)`

### 3) Initialize an authenticated trading client

Required inputs:
- private key
- chain ID `137`
- signature type
- funder address

Derive L2 creds:
- `client.create_or_derive_api_creds()`
- `client.set_api_creds(creds)`

### 4) Place the order

For limit orders:
- build `OrderArgs(...)`
- use `create_and_post_order(...)`, or `create_order(...)` + `post_order(...)`

For market orders:
- build `MarketOrderArgs(...)`
- use `create_market_order(...)` + `post_order(...)`

### 5) Query / cancel orders and inspect trades

Useful methods:
- `get_orders(...)`
- `get_trades(...)`
- `cancel(order_id)`
- `cancel_orders([...])`
- `cancel_all()`
- `cancel_market_orders(market=condition_id)` or `cancel_market_orders(asset_id=token_id)`

## Python SDK surface to prefer

### Core imports

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import (
    ApiCreds,
    AssetType,
    BalanceAllowanceParams,
    BookParams,
    MarketOrderArgs,
    OpenOrderParams,
    OrderArgs,
    OrderType,
    PartialCreateOrderOptions,
)
from py_clob_client.order_builder.constants import BUY, SELL
```

### Public / read-only methods

- `get_ok()`
- `get_server_time()`
- `get_midpoint(token_id)`
- `get_midpoints([...])`
- `get_price(token_id, side)`
- `get_prices([...])`
- `get_spread(token_id)`
- `get_spreads([...])`
- `get_tick_size(token_id)`
- `get_neg_risk(token_id)`
- `get_fee_rate_bps(token_id)`
- `get_order_book(token_id)`
- `get_order_books([...])`
- `get_last_trade_price(token_id)`
- `get_last_trades_prices([...])`
- `get_markets(next_cursor="MA==")`
- `get_simplified_markets(next_cursor="MA==")`
- `get_sampling_markets(next_cursor="MA==")`
- `get_sampling_simplified_markets(next_cursor="MA==")`
- `get_market(condition_id)`
- `get_market_trades_events(condition_id)`
- `calculate_market_price(token_id, side, amount, order_type)`

### Authenticated / trading methods

- `create_or_derive_api_creds()`
- `set_api_creds(creds)`
- `create_order(order_args, options=None)`
- `create_market_order(order_args, options=None)`
- `post_order(order, orderType=OrderType.GTC, post_only=False)`
- `post_orders([...])`
- `create_and_post_order(order_args, options=None)`
- `get_orders(params=None, next_cursor="MA==")`
- `get_order(order_id)`
- `get_trades(params=None, next_cursor="MA==")`
- `cancel(order_id)`
- `cancel_orders(order_ids)`
- `cancel_all()`
- `cancel_market_orders(market="", asset_id="")`
- `get_balance_allowance(params)`
- `update_balance_allowance(params)`
- `get_api_keys()`
- `delete_api_key()`

## Decision guide

- Need to **find markets / token IDs** -> use `requests` + Gamma.
- Need **order books or public price info** -> use read-only `ClobClient`.
- Need to **trade / cancel / query private orders** -> authenticated `ClobClient`.
- Need **balance / allowance checks** -> authenticated `ClobClient` + `BalanceAllowanceParams`.

## Common agent mistakes to avoid

- Using `condition_id` where a `token_id` is required.
- Hardcoding token IDs instead of fetching them from Gamma.
- Forgetting `create_or_derive_api_creds()` before L2 actions.
- Using the wrong signature type or funder address.
- Building order prices that break the market tick size.
- Treating market orders as a separate primitive instead of SDK-assisted marketable orders.
- Shipping secrets in source code.
- Adding Builder / relayer code even though the task only needs CLOB + Gamma.

## Files in this skill pack

- `tasks/market_discovery.md`
- `tasks/read_only_clob.md`
- `tasks/trading_setup.md`
- `tasks/order_workflows.md`
- `tasks/common_failures.md`
- `examples/gamma_find_markets.py`
- `examples/clob_read_only.py`
- `examples/trading_client_from_env.py`
- `examples/place_limit_order.py`
- `examples/place_market_order.py`
- `examples/manage_orders.py`
- `sources.md`

## Output expectations for coding agents

When using this skill, produce code that is:

- copy-pasteable
- backend-safe
- explicit about IDs and assumptions
- narrow in scope
- compatible with `py-clob-client`
- free of Builder / relayer dependencies unless the user explicitly asks for them
