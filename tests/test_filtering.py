import pytest

from backend.app import create_app
from backend.data.products import CATEGORIES, PRODUCTS
from backend.services.product_service import apply_filters, query_products
from backend.services.validation import FilterCriteria


@pytest.fixture
def client():
    return create_app().test_client()


def test_no_filters_returns_full_inventory():
    assert apply_filters(PRODUCTS, FilterCriteria()) == PRODUCTS


def test_filters_are_combined_with_and():
    c = FilterCriteria(frozenset({"Footwear"}), 1000, 4000, 3)
    result = apply_filters(PRODUCTS, c)
    assert result
    assert all(p["category"] == "Footwear" and 1000 <= p["price"] <= 4000 and p["rating"] >= 3 for p in result)


def test_rating_meets_or_exceeds():
    exact = next(p for p in PRODUCTS if p["rating"] == int(p["rating"]))
    assert exact in apply_filters(PRODUCTS, FilterCriteria(min_rating=int(exact["rating"])))


def test_impossible_filters_return_empty():
    assert apply_filters(PRODUCTS, FilterCriteria(min_price=10**9)) == []


def test_sort_runs_after_filter_and_does_not_mutate_master():
    snapshot = list(PRODUCTS)
    c = FilterCriteria(frozenset({"Apparel"}), sort="price_asc")
    result = query_products(PRODUCTS, c)
    assert {p["category"] for p in result} == {"Apparel"}
    prices = [p["price"] for p in result]
    assert prices == sorted(prices)
    assert PRODUCTS == snapshot


def test_top_rated_first():
    ratings = [p["rating"] for p in query_products(PRODUCTS, FilterCriteria(sort="rating_desc"))]
    assert ratings == sorted(ratings, reverse=True)


def test_api_roundtrip(client):
    data = client.get("/api/products?category=Electronics&min_rating=4&sort=price_desc").get_json()
    assert data["count"] == len(data["products"]) <= data["total"]
    assert all(p["category"] == "Electronics" and p["rating"] >= 4 for p in data["products"])


def test_api_no_params_returns_everything(client):
    assert client.get("/api/products").get_json()["count"] == len(PRODUCTS)


@pytest.mark.parametrize("qs", ["min_price=abc", "min_price=500&max_price=100", "min_rating=9", "category=Nope", "sort=bad"])
def test_api_rejects_bad_input(client, qs):
    assert client.get(f"/api/products?{qs}").status_code == 400


def test_meta_and_thumbnail(client):
    meta = client.get("/api/meta").get_json()
    assert [c["name"] for c in meta["categories"]] == CATEGORIES
    assert sum(meta["price"]["histogram"]) == len(PRODUCTS)
    assert client.get("/api/thumb/1.svg").mimetype == "image/svg+xml"
    assert client.get("/api/thumb/9999.svg").status_code == 404


def test_text_search_combines_with_other_filters():
    c = FilterCriteria(frozenset({"Electronics"}), query="speaker")
    result = apply_filters(PRODUCTS, c)
    assert result and all(p["category"] == "Electronics" and "speaker" in p["name"].lower() for p in result)


def test_api_search_and_validation(client):
    assert client.get("/api/products?q=sneakers").get_json()["count"] >= 1
    assert client.get("/api/products?q=" + "x" * 81).status_code == 400


def test_sale_fields_and_featured(client):
    assert all((p["mrp"] or 0) > p["price"] for p in PRODUCTS if p["discount"])
    featured = client.get("/api/meta").get_json()["featured"]
    assert featured["discount"] > 0 and featured["rating"] >= 4
