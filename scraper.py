
import re
import json
import csv

# Read the saved HTML file
with open("flipkart_page.html", "r", encoding="utf-8") as file:
    html = file.read()

decoder = json.JSONDecoder()
products = {}

# Find embedded product JSON arrays
matches = re.finditer(r'"products"\s*:\s*\[', html)

for match in matches:
    start = html.find("[", match.start(), match.end())

    try:
        product_list, _ = decoder.raw_decode(html[start:])
    except json.JSONDecodeError:
        continue

    for item in product_list:
        product = (
            item.get("productInfo", {})
                .get("value", {})
        )

        if not product:
            continue

        product_id = product.get("id")
        name = product.get("titles", {}).get("title", "Not found")

        pricing = product.get("pricing", {})
        price = pricing.get("finalPrice", {}).get("value")

        # Fallback if finalPrice is unavailable
        if price is None:
            prices = pricing.get("prices", [])
            if prices:
                price = prices[0].get("value")

        rating = product.get("rating", {}).get("average", "Not found")
        url = product.get("smartUrl", "Not found")

        if product_id:
            products[product_id] = {
                "Product ID": product_id,
                "Name": name,
                "Price": price if price is not None else "Not found",
                "Rating": rating,
                "URL": url
            }

# Export to CSV
with open("flipkart_products.csv", "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["Product ID", "Name", "Price", "Rating", "URL"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products.values())

print("Total products extracted:", len(products))
print("Data saved to flipkart_products.csv")

# Display first 5 products
for product in list(products.values())[:5]:
    print(product)
