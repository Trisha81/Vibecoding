import { fetchMeta, fetchProducts, buildQuery } from "./api.js";
import * as ui from "./ui.js";

const state = { categories: new Set(), minPrice: 0, maxPrice: 0, minRating: 0, sort: "featured", query: "" };
let cart = 0;
let price;            // {min, max, step, histogram} from the server
let controller;       // lets us cancel a stale request when a newer one starts
let timer;

function isDefault() {
  return state.categories.size === 0 && state.minPrice === price.min &&
         state.maxPrice === price.max && state.minRating === 0 && state.query === "";
}

async function refresh() {
  controller?.abort();
  controller = new AbortController();
  ui.showClearAll(!isDefault());
  ui.showState({ busy: true });
  try {
    const data = await fetchProducts(buildQuery(state, price), controller.signal);
    ui.renderGrid(data.products, addToCart);
    ui.showState({ count: data.count, total: data.total, busy: false });
  } catch (err) {
    if (err.name === "AbortError") return; // a newer request replaced this one
    ui.showState({ error: err.message, busy: false });
  }
}

function addToCart() { ui.setCartCount(++cart); }

const refreshSoon = () => { clearTimeout(timer); timer = setTimeout(refresh, 120); }; // for slider drags

function resetFilters() {
  state.categories.clear();
  state.minPrice = price.min; state.maxPrice = price.max; state.minRating = 0; state.query = "";
  document.getElementById("search").value = "";
  ui.resetControls(state, price);
  refresh();
}

async function init() {
  try {
    const meta = await fetchMeta();
    price = meta.price;
    state.minPrice = price.min; state.maxPrice = price.max;

    ui.renderDeal(meta.featured, addToCart);
    ui.renderCategories(meta.categories, (name, on) => {
      on ? state.categories.add(name) : state.categories.delete(name);
      refresh();
    });
    ui.setupPriceSlider(price, state, (lo, hi) => { state.minPrice = lo; state.maxPrice = hi; refreshSoon(); });
    ui.renderRatings(meta.ratings, (r) => { state.minRating = r; refresh(); });
    ui.renderSort(meta.sort_options, state.sort, (s) => { state.sort = s; refresh(); });

    const search = document.getElementById("search");
    search.addEventListener("input", () => { state.query = search.value.trim(); refreshSoon(); });
    document.getElementById("search-form").addEventListener("submit", (e) => { e.preventDefault(); refresh(); });

    document.getElementById("clear-all").addEventListener("click", resetFilters);
    document.getElementById("reset-filters").addEventListener("click", resetFilters);
    document.getElementById("retry").addEventListener("click", () => location.reload());
    await refresh();
  } catch (err) {
    ui.showState({ error: err.message, busy: false });
  }
}

init();
