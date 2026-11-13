// Presentation only: turns data into DOM. No filtering or sorting happens here.

const $ = (id) => document.getElementById(id);
const money = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });
export const formatPrice = (n) => money.format(n);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const ARROW = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

export function renderCategories(categories, onToggle) {
  $("category-list").innerHTML = categories.map((c) => `
    <label class="check">
      <input type="checkbox" value="${esc(c.name)}">
      <span>${esc(c.name)}</span><span class="count">${c.count}</span>
    </label>`).join("");
  $("category-list").addEventListener("change", (e) => onToggle(e.target.value, e.target.checked));
}

export function renderRatings(ratings, onSelect) {
  const options = [0, ...ratings];
  $("rating-list").innerHTML = options.map((r) => `
    <label class="rate">
      <input type="radio" name="min-rating" value="${r}" ${r === 0 ? "checked" : ""}>
      ${r === 0
        ? `<span class="rate__text">Any rating</span>`
        : `<span class="stars__bar" aria-hidden="true"><span style="width:${(r / 5) * 100}%"></span></span>
           <span class="rate__text">${r === 5 ? "5 stars" : `${r} & up`}</span>`}
    </label>`).join("");
  $("rating-list").addEventListener("change", (e) => onSelect(Number(e.target.value)));
}

export function renderSort(options, current, onChange) {
  const select = $("sort");
  select.innerHTML = options.map((o) => `<option value="${o.value}">${o.label}</option>`).join("");
  select.value = current;
  select.addEventListener("change", () => onChange(select.value));
}

export function setupPriceSlider(price, state, onChange) {
  const minEl = $("price-min"), maxEl = $("price-max");
  for (const el of [minEl, maxEl]) {
    el.min = price.min; el.max = price.max; el.step = price.step;
  }
  minEl.value = state.minPrice; maxEl.value = state.maxPrice;

  $("price-hist").innerHTML = (() => {
    const peak = Math.max(...price.histogram) || 1;
    return price.histogram.map((n) => `<span style="height:${Math.max(6, (n / peak) * 100)}%"></span>`).join("");
  })();

  const handle = (changed) => {
    let lo = Number(minEl.value), hi = Number(maxEl.value);
    if (lo > hi) { // thumbs can't cross
      if (changed === "min") { lo = hi; minEl.value = lo; } else { hi = lo; maxEl.value = hi; }
    }
    paintPrice(price, lo, hi);
    onChange(lo, hi);
  };
  minEl.addEventListener("input", () => handle("min"));
  maxEl.addEventListener("input", () => handle("max"));
  paintPrice(price, state.minPrice, state.maxPrice);
}

export function syncPriceSlider(price, lo, hi) {
  $("price-min").value = lo; $("price-max").value = hi;
  paintPrice(price, lo, hi);
}

function paintPrice(price, lo, hi) {
  const span = price.max - price.min;
  $("price-fill").style.left = `${((lo - price.min) / span) * 100}%`;
  $("price-fill").style.right = `${100 - ((hi - price.min) / span) * 100}%`;
  $("price-min-out").textContent = formatPrice(lo);
  $("price-max-out").textContent = formatPrice(hi);
  const bars = $("price-hist").children, n = bars.length, width = span / n;
  for (let i = 0; i < n; i++) {
    const barLo = price.min + i * width, barHi = barLo + width;
    bars[i].classList.toggle("in", barHi > lo && barLo <= hi);
  }
  // Keep the thumb that is on top reachable when both sit at the far right.
  $("price-min").style.zIndex = lo > price.max - span * 0.1 ? 3 : 2;
}

export function resetControls(state, price) {
  document.querySelectorAll("#category-list input").forEach((i) => (i.checked = false));
  document.querySelector('#rating-list input[value="0"]').checked = true;
  syncPriceSlider(price, state.minPrice, state.maxPrice);
}

function starsHtml(rating) {
  return `<span class="stars__bar" role="img" aria-label="${rating} out of 5 stars"><span style="width:${(rating / 5) * 100}%"></span></span>`;
}

export function renderGrid(products, onAdd) {
  const grid = $("grid");
  grid.innerHTML = products.map((p) => `
    <article class="card">
      <div class="card__media">
        <img src="${p.image}" alt="${esc(p.name)}" loading="lazy" width="320" height="240">
        ${p.discount ? `<span class="tag tag--sale">${p.discount}% off</span>` : ""}
        ${p.is_new ? `<span class="tag tag--new">Newest</span>` : ""}
      </div>
      <h3 class="card__name">${esc(p.name)}</h3>
      <p class="card__category">${esc(p.category)}</p>
      <div class="stars">${starsHtml(p.rating)}<span>${p.rating.toFixed(1)} (${p.reviews.toLocaleString("en-IN")})</span></div>
      <div class="card__foot">
        <p class="card__price">${p.mrp ? `<s>${formatPrice(p.mrp)}</s>` : ""}${formatPrice(p.price)}</p>
        <button type="button" class="go" data-id="${p.id}" aria-label="Add ${esc(p.name)} to cart">${ARROW}</button>
      </div>
    </article>`).join("");
  grid.onclick = (e) => {
    const btn = e.target.closest(".go");
    if (btn) onAdd(Number(btn.dataset.id));
  };
}

export function renderDeal(p, onAdd) {
  const el = $("deal");
  if (!p) { el.hidden = true; return; }
  el.hidden = false;
  el.innerHTML = `
    <div class="deal__media">
      <img src="${p.image}" alt="${esc(p.name)}" width="320" height="240">
      <span class="deal__badge" aria-label="${p.discount}% off">Sale</span>
    </div>
    <div class="deal__panel">
      <h2 class="deal__title">${esc(p.name)}</h2>
      <p class="deal__text">${esc(p.category)} · rated ${p.rating.toFixed(1)} by ${p.reviews.toLocaleString("en-IN")} shoppers. Now ${p.discount}% off.</p>
      <div class="deal__row">
        <p class="deal__prices"><s>${formatPrice(p.mrp)}</s><strong>${formatPrice(p.price)}</strong></p>
        <button type="button" class="btn" id="deal-add">Shop now</button>
      </div>
    </div>`;
  $("deal-add").onclick = () => onAdd(p.id);
}

export function setCartCount(n) {
  const el = $("cart-count");
  el.textContent = n;
  el.classList.add("bump");
  setTimeout(() => el.classList.remove("bump"), 220);
}

export function showState({ count, total, error, busy }) {
  $("grid").setAttribute("aria-busy", busy ? "true" : "false");
  const hasError = Boolean(error);
  const empty = !hasError && count === 0;
  $("error").hidden = !hasError;
  $("empty").hidden = !empty;
  $("grid").hidden = hasError || empty; // grid disappears when nothing matches
  if (hasError) {
    $("error-text").textContent = error;
    $("result-count").textContent = "";
  } else if (count !== undefined) {
    $("result-count").textContent = `Showing ${count} of ${total} products`;
  }
}

export function showClearAll(visible) { $("clear-all").hidden = !visible; }
