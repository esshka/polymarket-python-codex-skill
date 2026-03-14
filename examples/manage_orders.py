from py_clob_client.clob_types import OpenOrderParams, AssetType, BalanceAllowanceParams

from trading_client_from_env import build_authenticated_client

TOKEN_ID = "YOUR_TOKEN_ID"
CONDITION_ID = "YOUR_CONDITION_ID"

client = build_authenticated_client()

collateral = client.get_balance_allowance(
    BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
)
conditional = client.get_balance_allowance(
    BalanceAllowanceParams(asset_type=AssetType.CONDITIONAL, token_id=TOKEN_ID)
)
print("collateral:", collateral)
print("conditional:", conditional)

open_orders = client.get_orders(OpenOrderParams(asset_id=TOKEN_ID))
print(f"open orders: {len(open_orders)}")

if open_orders:
    order_id = open_orders[0]["id"]
    print("cancel one:", client.cancel(order_id))

print("cancel market:", client.cancel_market_orders(market=CONDITION_ID))
print("trades:", client.get_trades())
