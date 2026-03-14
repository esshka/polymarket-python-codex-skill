from py_clob_client.clob_types import MarketOrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

from trading_client_from_env import build_authenticated_client

TOKEN_ID = "YOUR_TOKEN_ID"

client = build_authenticated_client()

signed = client.create_market_order(
    MarketOrderArgs(
        token_id=TOKEN_ID,
        amount=25.0,
        side=BUY,
        order_type=OrderType.FOK,
    )
)

response = client.post_order(signed, OrderType.FOK)
print(response)
