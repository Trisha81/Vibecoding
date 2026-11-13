"""Turns raw query-string values into a validated FilterCriteria object."""
from dataclasses import dataclass, field
from typing import Optional

SORT_OPTIONS = {
    "featured": "Featured",
    "price_asc": "Price: Low to High",
    "price_desc": "Price: High to Low",
    "rating_desc": "Top Rated First",
    "name_asc": "Name: A to Z",
}


class ValidationError(ValueError):
    """Raised when a query parameter is malformed. Mapped to HTTP 400."""


@dataclass(frozen=True)
class FilterCriteria:
    categories: frozenset = field(default_factory=frozenset)  # empty = all categories
    min_price: Optional[float] = None                          # None = no lower bound
    max_price: Optional[float] = None                          # None = no upper bound
    min_rating: Optional[int] = None                           # None = any rating
    sort: str = "featured"
    query: str = ""                                            # "" = no text search


def _number(raw, name):
    if raw is None or str(raw).strip() == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        raise ValidationError(f"{name} must be a number") from None
    if value != value or value in (float("inf"), float("-inf")) or value < 0:
        raise ValidationError(f"{name} must be a non-negative number")
    return value


def parse_criteria(args, valid_categories) -> FilterCriteria:
    """`args` is any object with .getlist() / .get() (e.g. Flask's request.args)."""
    categories = set()
    for chunk in args.getlist("category"):
        categories.update(part.strip() for part in chunk.split(",") if part.strip())
    unknown = categories - set(valid_categories)
    if unknown:
        raise ValidationError(f"unknown category: {', '.join(sorted(unknown))}")

    min_price = _number(args.get("min_price"), "min_price")
    max_price = _number(args.get("max_price"), "max_price")
    if min_price is not None and max_price is not None and min_price > max_price:
        raise ValidationError("min_price cannot be greater than max_price")

    min_rating = None
    raw_rating = args.get("min_rating")
    if raw_rating not in (None, ""):
        try:
            min_rating = int(raw_rating)
        except ValueError:
            raise ValidationError("min_rating must be a whole number from 0 to 5") from None
        if not 0 <= min_rating <= 5:
            raise ValidationError("min_rating must be a whole number from 0 to 5")
        if min_rating == 0:
            min_rating = None  # 0 means "any rating"

    sort = args.get("sort") or "featured"
    if sort not in SORT_OPTIONS:
        raise ValidationError(f"sort must be one of: {', '.join(SORT_OPTIONS)}")

    query = (args.get("q") or "").strip()
    if len(query) > 80:
        raise ValidationError("q must be 80 characters or fewer")

    return FilterCriteria(frozenset(categories), min_price, max_price, min_rating, sort, query.lower())
