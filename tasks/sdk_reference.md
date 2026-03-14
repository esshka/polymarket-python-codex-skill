# SDK Reference and Scope

Use this file when you need a quick reference for what this skill covers, which SDK surface to prefer, or which Polymarket path to choose for a task.

## Scope

Included:
- public market discovery with Gamma (`/markets`, `/events`, `/tags`, `/sports`)
- read-only CLOB access for order books, prices, tick size, neg risk, and market metadata
- authenticated CLOB trading flows with `py-clob-client`
- balances, allowances, orders, cancellations, and trade history
- correct use of `condition_id` versus `token_id`

Excluded:
- Builder APIs
- Builder signing or relayer SDKs
- front-end browser code that would expose secrets
- unrelated Polymarket products

## Source-vs-docs note

Some Polymarket Python quickstart snippets show:

```python
options = {"tick_size": "...", "neg_risk": True}
```

The current `py-clob-client` source types `options` as `PartialCreateOrderOptions` and accesses `options.tick_size` and `options.neg_risk`.

In this skill:
- use `PartialCreateOrderOptions(...)`, or
- omit `options` and let the SDK auto-resolve metadata

Do not pass a plain dict unless you have verified the installed SDK version accepts it.

## Core imports

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

## Public and read-only methods

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

## Authenticated and trading methods

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

- Need to find markets or token IDs: use `requests` plus Gamma.
- Need order books or public price info: use read-only `ClobClient`.
- Need to trade, cancel, or query private orders: use authenticated `ClobClient`.
- Need balance or allowance checks: use authenticated `ClobClient` plus `BalanceAllowanceParams`.

## Output expectations

Return code that is:
- copy-pasteable
- backend-safe
- explicit about IDs and assumptions
- narrow in scope
- compatible with `py-clob-client`
- free of Builder or relayer dependencies unless the user explicitly asks for them
