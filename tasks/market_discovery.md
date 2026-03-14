# Market Discovery with Gamma

Use Gamma for market discovery. Gamma is public and does not require authentication.

Base URL:

```text
https://gamma-api.polymarket.com
```

## What Gamma is for

Use Gamma to find:
- active markets
- event / market slugs
- tag metadata
- `clobTokenIds`
- question text and outcome labels

## What to fetch

### Find by slug

```python
import requests

BASE = "https://gamma-api.polymarket.com"

def get_market_by_slug(slug: str) -> dict:
    resp = requests.get(f"{BASE}/markets", params={"slug": slug}, timeout=20)
    resp.raise_for_status()
    markets = resp.json()
    if not markets:
        raise ValueError(f"No market found for slug={slug!r}")
    return markets[0]
```

### List active markets

```python
import requests

BASE = "https://gamma-api.polymarket.com"

def list_active_markets(limit: int = 10) -> list[dict]:
    resp = requests.get(
        f"{BASE}/markets",
        params={"active": "true", "closed": "false", "limit": limit},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()
```

### List active events with embedded markets

```python
import requests

BASE = "https://gamma-api.polymarket.com"

def list_active_events(limit: int = 10) -> list[dict]:
    resp = requests.get(
        f"{BASE}/events",
        params={"active": "true", "closed": "false", "limit": limit},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()
```

## Extracting token IDs safely

`clobTokenIds` is the important field for CLOB trading.

Use a normalizer because some integrations may hand you a JSON string instead of a list:

```python
import json

def normalize_clob_token_ids(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return [value]
        if isinstance(parsed, list):
            return [str(v) for v in parsed]
        return [str(parsed)]
    return [str(value)]
```

For standard binary markets, the first token is **YES** and the second token is **NO**.

```python
market = get_market_by_slug("fed-decision-in-october")
token_ids = normalize_clob_token_ids(market.get("clobTokenIds"))
yes_token_id = token_ids[0]
no_token_id = token_ids[1]
```

## ID hygiene

Keep these separate in generated code:

- `slug` -> human-friendly lookup key
- `condition_id` -> CLOB market identifier
- `token_id` -> orderable asset identifier

## Recommended agent behavior

- Prefer fetching by `slug` when the user references a specific URL or market slug.
- Prefer `/events` when the user wants broader discovery.
- Return both `condition_id` and normalized `clobTokenIds` to downstream trading code.
- Never derive token IDs yourself.
