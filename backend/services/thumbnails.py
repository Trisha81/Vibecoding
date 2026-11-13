"""Generates simple SVG thumbnails so the project has no external image dependency."""
from html import escape

from .illustrations import HOME_KITCHEN

_GLYPH = {"Electronics": "🎧", "Apparel": "👕", "Footwear": "👟", "Home & Kitchen": "🏠"}

# Warm storefront palette (cream, apricot, sage, mint, clay) so cards match the site theme.
_PALETTE = [
    ("#fbe3b8", "#f6c378"), ("#d8efdf", "#9fd3b3"), ("#fdd9c4", "#f4a98b"),
    ("#e9efc9", "#c7d98a"), ("#f7e6d0", "#e7c49a"), ("#cfe8e1", "#8cc5b8"),
]


def make_thumbnail(product: dict) -> str:
    glyph = _GLYPH.get(product["category"], "📦")
    c1, c2 = _PALETTE[product["id"] % len(_PALETTE)]
    label = escape(product["name"])
    art = HOME_KITCHEN.get(product["name"]) if product["category"] == "Home & Kitchen" else None
    if art is None:
        art = f'<text x="160" y="140" font-size="84" text-anchor="middle">{glyph}</text>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" role="img" aria-label="{label}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
</linearGradient></defs>
<rect width="320" height="240" fill="url(#g)"/>
<circle cx="250" cy="50" r="70" fill="#fff" opacity=".25"/>
{art}
</svg>"""
