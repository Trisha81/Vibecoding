"""Core business logic: filtering, sorting and catalogue metadata.

Pipeline order matters: FILTER the master list first, THEN SORT what is left.
The master list is never mutated.
"""
import math
from typing import Iterable

from .validation import FilterCriteria, SORT_OPTIONS


# ---------- Step 1: combinatorial (AND) filtering ----------
def apply_filters(products: Iterable[dict], c: FilterCriteria) -> list:
    """A product passes only if it satisfies ALL active filters.

    An inactive filter (empty set / None) is skipped, so with nothing selected
    the full inventory comes back unchanged.
    """
    result = []
    for p in products:
        if c.categories and p["category"] not in c.categories:
            continue
        if c.min_price is not None and p["price"] < c.min_price:
            continue
        if c.max_price is not None and p["price"] > c.max_price:
            continue
        if c.min_rating is not None and p["rating"] < c.min_rating:  # "meets or exceeds"
            continue
        if c.query and c.query not in p["name"].lower() and c.query not in p["category"].lower():
            continue
        result.append(p)
    return result


# ---------- Step 2: sorting (runs on the already-filtered list) ----------
_SORT_KEYS = {
    "price_asc": lambda p: (p["price"], p["id"]),
    "price_desc": lambda p: (-p["price"], p["id"]),
    "rating_desc": lambda p: (-p["rating"], -p["reviews"], p["id"]),
    "name_asc": lambda p: (p["name"].lower(), p["id"]),
}


def apply_sort(products: list, sort: str) -> list:
    key = _SORT_KEYS.get(sort)
    return list(products) if key is None else sorted(products, key=key)  # "featured" keeps original order


def query_products(master: list, c: FilterCriteria) -> list:
    return apply_sort(apply_filters(master, c), c.sort)


def pick_featured(master: list):
    """Spotlight product: biggest discount among well-rated (4+) deals, ties broken by rating."""
    deals = [p for p in master if p.get("discount") and p["rating"] >= 4] or [p for p in master if p.get("discount")]
    return max(deals, key=lambda p: (p["discount"], p["rating"])) if deals else None


# ---------- Catalogue metadata for building the sidebar ----------
def build_meta(master: list, categories: list, buckets: int = 24) -> dict:
    prices = [p["price"] for p in master]
    lo = int(math.floor(min(prices) / 100) * 100)
    hi = int(math.ceil(max(prices) / 100) * 100)
    width = (hi - lo) / buckets
    histogram = [0] * buckets
    for price in prices:
        histogram[min(int((price - lo) / width), buckets - 1)] += 1

    return {
        "categories": [
            {"name": name, "count": sum(1 for p in master if p["category"] == name)}
            for name in categories
        ],
        "price": {"min": lo, "max": hi, "step": 100, "histogram": histogram},
        "ratings": [1, 2, 3, 4, 5],
        "sort_options": [{"value": k, "label": v} for k, v in SORT_OPTIONS.items()],
        "total": len(master),
        "featured": pick_featured(master),
    }
