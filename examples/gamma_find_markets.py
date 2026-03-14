import json
import requests

BASE = "https://gamma-api.polymarket.com"


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


def get_market_by_slug(slug: str) -> dict:
    resp = requests.get(f"{BASE}/markets", params={"slug": slug}, timeout=20)
    resp.raise_for_status()
    markets = resp.json()
    if not markets:
        raise ValueError(f"No market found for slug={slug!r}")
    return markets[0]


if __name__ == "__main__":
    market = get_market_by_slug("fed-decision-in-october")
    token_ids = normalize_clob_token_ids(market.get("clobTokenIds"))

    print("question:", market.get("question"))
    print("condition_id:", market.get("conditionId") or market.get("condition_id"))
    print("token_ids:", token_ids)
    if len(token_ids) >= 2:
        print("yes_token_id:", token_ids[0])
        print("no_token_id:", token_ids[1])
