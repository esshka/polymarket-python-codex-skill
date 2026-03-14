# Trading Client Setup

Use an authenticated `ClobClient` for placing orders, cancelling, fetching private orders, balance/allowance checks, and trade history.

## Required environment variables

```text
POLYMARKET_PRIVATE_KEY=0x...
POLYMARKET_FUNDER=0x...
POLYMARKET_SIGNATURE_TYPE=0
POLYMARKET_HOST=https://clob.polymarket.com
POLYMARKET_CHAIN_ID=137
```

Optional, when reusing existing L2 credentials:

```text
POLYMARKET_API_KEY=...
POLYMARKET_API_SECRET=...
POLYMARKET_API_PASSPHRASE=...
```

## Signature types

- `0` -> EOA
- `1` -> `POLY_PROXY`
- `2` -> `GNOSIS_SAFE`

The **funder** must be the address that actually holds funds.

## Safe setup helper

```python
import os

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds


def build_authenticated_client() -> ClobClient:
    host = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com")
    chain_id = int(os.getenv("POLYMARKET_CHAIN_ID", "137"))
    private_key = os.environ["POLYMARKET_PRIVATE_KEY"]
    signature_type = int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "0"))
    funder = os.environ["POLYMARKET_FUNDER"]

    api_key = os.getenv("POLYMARKET_API_KEY")
    api_secret = os.getenv("POLYMARKET_API_SECRET")
    api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")

    creds = None
    if api_key and api_secret and api_passphrase:
        creds = ApiCreds(
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
        )

    client = ClobClient(
        host=host,
        chain_id=chain_id,
        key=private_key,
        creds=creds,
        signature_type=signature_type,
        funder=funder,
    )

    if creds is None:
        client.set_api_creds(client.create_or_derive_api_creds())

    return client
```

## Balance / allowance check

```python
from py_clob_client.clob_types import AssetType, BalanceAllowanceParams

client = build_authenticated_client()

collateral = client.get_balance_allowance(
    BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
)

conditional = client.get_balance_allowance(
    BalanceAllowanceParams(
        asset_type=AssetType.CONDITIONAL,
        token_id="YOUR_TOKEN_ID",
    )
)

print("collateral:", collateral)
print("conditional:", conditional)
```

## Security rules

- Never hardcode the private key.
- Never ship API secrets to front-end code.
- Treat authenticated CLOB code as backend-only.
