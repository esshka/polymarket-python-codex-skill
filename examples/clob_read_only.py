from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BookParams

HOST = "https://clob.polymarket.com"
TOKEN_ID = "YOUR_TOKEN_ID"
CONDITION_ID = "YOUR_CONDITION_ID"

client = ClobClient(HOST)

print("ok:", client.get_ok())
print("server_time:", client.get_server_time())
print("midpoint:", client.get_midpoint(TOKEN_ID))
print("buy_price:", client.get_price(TOKEN_ID, side="BUY"))
print("sell_price:", client.get_price(TOKEN_ID, side="SELL"))
print("spread:", client.get_spread(TOKEN_ID))
print("tick_size:", client.get_tick_size(TOKEN_ID))
print("neg_risk:", client.get_neg_risk(TOKEN_ID))
print("fee_rate_bps:", client.get_fee_rate_bps(TOKEN_ID))
print("market:", client.get_market(CONDITION_ID))
print("last_trade:", client.get_last_trade_price(TOKEN_ID))
print("books:", client.get_order_books([BookParams(token_id=TOKEN_ID)]))
