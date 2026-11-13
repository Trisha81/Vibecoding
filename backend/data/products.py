"""Master product inventory (in-memory).

Names and prices are hand-written; ratings and review counts come from a seeded
RNG so the dataset is identical on every run (important for tests and demos).
"""
import random

CATEGORIES = ["Electronics", "Apparel", "Footwear", "Home & Kitchen"]

_RAW = {
    "Electronics": [
        ("Wireless Earbuds", 2499), ("Bluetooth Speaker", 1799), ("Smartwatch Active", 3999),
        ("Power Bank 20000mAh", 1599), ("Mechanical Keyboard", 3499), ("Gaming Mouse", 1299),
        ("4K Action Camera", 6999), ("Noise-Cancelling Headphones", 8999), ("USB-C Hub 7-in-1", 1899),
        ('27" IPS Monitor', 15999), ("Full HD Webcam", 2199), ("Portable SSD 1TB", 7499),
    ],
    "Apparel": [
        ("Cotton Crew Tee", 499), ("Slim Fit Jeans", 1499), ("Hooded Sweatshirt", 1799),
        ("Linen Shirt", 1299), ("Packable Rain Jacket", 2999), ("Chino Shorts", 899),
        ("Wool Blend Sweater", 2499), ("Jersey Track Pants", 999), ("Denim Jacket", 3299),
        ("Tailored Blazer", 5499), ("Printed Cotton Kurta", 1199), ("Thermal Innerwear Set", 799),
    ],
    "Footwear": [
        ("Cushioned Running Shoes", 3499), ("Leather Loafers", 2799), ("Canvas Sneakers", 1299),
        ("Trail Boots", 4999), ("Everyday Flip Flops", 399), ("Formal Oxfords", 3999),
        ("Slip-on Sandals", 899), ("High-top Sneakers", 2999), ("Recovery Sliders", 599),
        ("Hiking Sandals", 2199), ("Court Basketball Shoes", 5499), ("Suede Ankle Boots", 3799),
    ],
    "Home & Kitchen": [
        ("Steel Water Bottle", 699), ("Non-stick Cookware Set", 2999), ("Digital Air Fryer", 5999),
        ("Memory Foam Pillow", 1199), ("LED Desk Lamp", 1099), ("Cotton Bedsheet Set", 1599),
        ("Electric Kettle 1.5L", 1299), ("Chef Knife Set", 2199), ("Stackable Storage Bins", 799),
        ("Aroma Diffuser", 1499), ("Mixer Grinder 750W", 3499), ("Robot Vacuum Cleaner", 18999),
    ],
}


def _build():
    rng = random.Random(2024)
    deals = random.Random(77)  # separate RNG so ratings/reviews above never change
    products, pid = [], 1
    for category in CATEGORIES:
        for name, price in _RAW[category]:
            discount = deals.choice([10, 15, 20, 25, 30, 40]) if deals.random() < 0.35 else 0
            is_new = deals.random() < 0.2
            products.append({
                "id": pid,
                "name": name,
                "category": category,
                "price": price,
                "rating": round(rng.uniform(2.2, 4.9), 1),
                "reviews": rng.randint(12, 4800),
                "image": f"/api/thumb/{pid}.svg",
                "discount": discount,  # percent off, 0 = not on sale
                "mrp": round(price / (1 - discount / 100) / 10) * 10 if discount else None,
                "is_new": is_new,
            })
            pid += 1
    return products


PRODUCTS = _build()
