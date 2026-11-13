# The Second Hand Store – Product Multi-Filter Sidebar

E-commerce browsing page with a sticky sidebar (category checklist, dual-thumb price slider,
minimum-star radios) and a product grid that updates instantly. A **Sort by** dropdown reorders
the already-filtered results.

All business logic (validation, filtering, sorting, price bounds, histogram) lives on the **server**.
The frontend only renders data and sends the current filter state.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py                    # open http://127.0.0.1:5000
python -m pytest                 # run tests
```

## Structure

```
backend/
  app.py                    app factory, serves frontend
  api/routes.py             /api/meta, /api/products, /api/thumb/<id>.svg
  services/validation.py    query-string -> FilterCriteria (400 on bad input)
  services/product_service.py   apply_filters -> apply_sort -> query_products, build_meta
  services/thumbnails.py    generated SVG thumbnails
  data/products.py          master inventory (48 products, 4 categories)
frontend/
  index.html, css/styles.css
  js/api.js   fetch + query building
  js/ui.js    DOM rendering (no business logic)
  js/main.js  state, debounce, request cancellation
tests/test_filtering.py
```

## API

`GET /api/products?category=Footwear&category=Apparel&min_price=500&max_price=5000&min_rating=4&sort=price_asc`

| param | meaning |
|---|---|
| `category` (repeatable) | any of the selected categories; omitted = all |
| `min_price`, `max_price` | inclusive price bounds; omitted = no bound |
| `min_rating` | 1–5, product rating must be >= value; omitted/0 = any |
| `q` | optional text search on name/category (max 80 chars) |
| `sort` | `featured` (default), `price_asc`, `price_desc`, `rating_desc`, `name_asc` |

A product is returned only if it passes **all** active filters. With no filters, the full inventory is returned.

## Requirements checklist

| Requirement | Where |
|---|---|
| Sticky sidebar: category checklist, dual-thumb price slider, 1-5 star radios | `frontend/index.html`, `ui.js` |
| Product cards: thumbnail, price, star rating, name | `ui.renderGrid` |
| Instant updates, no submit button (slider debounced, stale requests cancelled) | `main.js` |
| Zero matches: grid hidden, "No items match your criteria. Reset filters" | `ui.showState` |
| Combinatorial AND filtering on the server | `product_service.apply_filters` |
| Null handling: nothing selected returns the full inventory | `apply_filters` skips inactive filters |
| Sort By (Price: Low to High, Top Rated First, ...) applied after filtering | `apply_sort`, `query_products` |

Extras: sale/newest tags and a deal spotlight (computed on the server), text search, cart counter.
