# Read-Only CLOB Workflows

Use read-only `ClobClient` methods when you need market prices, order books, or metadata and do not need authentication.

## Basic client

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.polymarket.com"
client = ClobClient(HOST)
```

## Common reads

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BookParams

HOST = "https://clob.polymarket.com"
client = ClobClient(HOST)

token_id = "YOUR_TOKEN_ID"
condition_id = "YOUR_CONDITION_ID"

ok = client.get_ok()
server_time = client.get_server_time()
midpoint = client.get_midpoint(token_id)
buy_price = client.get_price(token_id, side="BUY")
sell_price = client.get_price(token_id, side="SELL")
spread = client.get_spread(token_id)
book = client.get_order_book(token_id)
books = client.get_order_books([BookParams(token_id=token_id)])
tick_size = client.get_tick_size(token_id)
neg_risk = client.get_neg_risk(token_id)
fee_rate_bps = client.get_fee_rate_bps(token_id)
market = client.get_market(condition_id)
last_trade = client.get_last_trade_price(token_id)
```

## When to use each identifier

- `token_id`: order book, spread, price, midpoint, tick size, neg risk, fees
- `condition_id`: market metadata, market trade events, market-scoped order filters

## Preferred agent behavior

- Use Gamma to discover the market, then use CLOB to inspect tradability.
- Fetch `tick_size` and `neg_risk` before constructing orders when you want explicit validation.
- If the user only wants market data, do not ask for secrets or initialize auth.
