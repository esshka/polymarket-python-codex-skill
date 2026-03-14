from py_clob_client.clob_types import OrderArgs, PartialCreateOrderOptions
from py_clob_client.order_builder.constants import BUY

from trading_client_from_env import build_authenticated_client

CONDITION_ID = "YOUR_CONDITION_ID"
TOKEN_ID = "YOUR_TOKEN_ID"

client = build_authenticated_client()
market = client.get_market(CONDITION_ID)

options = PartialCreateOrderOptions(
    tick_size=str(market["minimum_tick_size"]),
    neg_risk=bool(market["neg_risk"]),
)

response = client.create_and_post_order(
    OrderArgs(
        token_id=TOKEN_ID,
        price=0.50,
        size=10,
        side=BUY,
    ),
    options=options,
)

print(response)
