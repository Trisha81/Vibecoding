// Network layer. The frontend sends the filter state; the server does all filtering/sorting.

export async function fetchMeta() {
  const res = await fetch("/api/meta");
  if (!res.ok) throw new Error("Could not load catalogue info.");
  return res.json();
}

/** Builds the query string from the filter state. Only active filters are sent. */
export function buildQuery(state, bounds) {
  const params = new URLSearchParams();
  state.categories.forEach((c) => params.append("category", c));
  if (state.minPrice > bounds.min) params.set("min_price", state.minPrice);
  if (state.maxPrice < bounds.max) params.set("max_price", state.maxPrice);
  if (state.minRating > 0) params.set("min_rating", state.minRating);
  if (state.query) params.set("q", state.query);
  if (state.sort !== "featured") params.set("sort", state.sort);
  return params.toString();
}

export async function fetchProducts(query, signal) {
  const res = await fetch(`/api/products?${query}`, { signal });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Could not load products.");
  }
  return res.json();
}
