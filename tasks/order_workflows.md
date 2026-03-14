# Order Workflows

This skill supports two reliable patterns:

1. **Explicit metadata path**
   - fetch `condition_id` and `token_id`
   - fetch market metadata
   - pass `PartialCreateOrderOptions(...)`

2. **SDK auto-resolution path**
   - omit options
   - let `py-clob-client` fetch tick size / neg risk / fee rate internally

Prefer the explicit path when you already have market metadata or want easier debugging.

## Limit order

```python
from py_clob_client.clob_types import OrderArgs, OrderType, PartialCreateOrderOptions
from py_clob_client.order_builder.constants import BUY

from trading_client_from_env import build_authenticated_client

client = build_authenticated_client()

condition_id = "YOUR_CONDITION_ID"
token_id = "YOUR_TOKEN_ID"

market = client.get_market(condition_id)
options = PartialCreateOrderOptions(
    tick_size=str(market["minimum_tick_size"]),
    neg_risk=bool(market["neg_risk"]),
)

response = client.create_and_post_order(
    OrderArgs(
        token_id=token_id,
        price=0.50,
        size=10,
        side=BUY,
    ),
    options=options,
)

print(response)
```

## Limit order with SDK auto-resolution

```python
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY

from trading_client_from_env import build_authenticated_client

client = build_authenticated_client()

response = client.create_and_post_order(
    OrderArgs(
        token_id="YOUR_TOKEN_ID",
        price=0.50,
        size=10,
        side=BUY,
    )
)

print(response)
```

## Market order

```python
from py_clob_client.clob_types import MarketOrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

from trading_client_from_env import build_authenticated_client

client = build_authenticated_client()

signed = client.create_market_order(
    MarketOrderArgs(
        token_id="YOUR_TOKEN_ID",
        amount=25.0,
        side=BUY,
        order_type=OrderType.FOK,
    )
)

response = client.post_order(signed, OrderType.FOK)
print(response)
```

## Two-step sign then submit

Use this when you need to inspect / batch / customize submission.

```python
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import SELL

from trading_client_from_env import build_authenticated_client

client = build_authenticated_client()

signed_order = client.create_order(
    OrderArgs(
        token_id="YOUR_TOKEN_ID",
        price=0.62,
        size=5,
        side=SELL,
    )
)

response = client.post_order(signed_order, OrderType.GTC)
print(response)
```

## Query and cancel

```python
from py_clob_client.clob_types import OpenOrderParams

from trading_client_from_env import build_authenticated_client

client = build_authenticated_client()

open_orders = client.get_orders(OpenOrderParams(asset_id="YOUR_TOKEN_ID"))
print(f"open orders: {len(open_orders)}")

if open_orders:
    first_order_id = open_orders[0]["id"]
    print(client.cancel(first_order_id))

print(client.cancel_market_orders(market="YOUR_CONDITION_ID"))
# print(client.cancel_all())
```

## Important behavioral notes

- Limit orders use `OrderArgs(price=..., size=...)`.
- Market orders use `MarketOrderArgs(amount=...)`.
- Market orders typically use `FOK` or `FAK`.
- `post_only=True` is only valid with `GTC` or `GTD`.
- Keep price aligned to the market tick size.
