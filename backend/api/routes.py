"""HTTP layer: thin handlers that validate input and delegate to the service layer."""
from flask import Blueprint, Response, abort, jsonify, request

from ..data.products import CATEGORIES, PRODUCTS
from ..services.product_service import build_meta, query_products
from ..services.thumbnails import make_thumbnail
from ..services.validation import ValidationError, parse_criteria

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/meta")
def meta():
    return jsonify(build_meta(PRODUCTS, CATEGORIES))


@api.get("/products")
def products():
    criteria = parse_criteria(request.args, CATEGORIES)
    items = query_products(PRODUCTS, criteria)
    return jsonify({"count": len(items), "total": len(PRODUCTS), "products": items})


@api.get("/thumb/<int:product_id>.svg")
def thumbnail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        abort(404)
    return Response(make_thumbnail(product), mimetype="image/svg+xml",
                    headers={"Cache-Control": "public, max-age=86400"})


@api.errorhandler(ValidationError)
def bad_request(err):
    return jsonify({"error": str(err)}), 400
