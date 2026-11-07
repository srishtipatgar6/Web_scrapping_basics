
from bs4 import BeautifulSoup

# ==================================
# STEP 1: OPEN SAVED HTML FILE
# ==================================

with open("flipkart_page.html", "r", encoding="utf-8") as file:
    html_content = file.read()

print("HTML file loaded successfully!")
print("HTML length:", len(html_content))


# ==================================
# STEP 2: PARSE HTML USING BS4
# ==================================

soup = BeautifulSoup(html_content, "html.parser")

print("\nHTML parsed successfully!")


# ==================================
# STEP 3: EXTRACT PAGE TITLE
# ==================================

page_title = soup.title

if page_title:
    print("\nPage Title:", page_title.get_text(strip=True))
else:
    print("\nPage title not found")


# ==================================
# STEP 4: EXTRACT PRODUCT CONTAINERS
# ==================================

products = soup.select("div[data-id]")

print("\nTotal matching containers:", len(products))


# ==================================
# STEP 5: EXTRACT PRODUCT DETAILS
# ==================================

product_data = []

for product in products:

    # Product ID
    product_id = product.get("data-id")

    # Product name
    name = product.select_one("a[title]")

    # Product price
    price = product.select_one("div.Nx9bqj")

    # Product rating
    rating = product.select_one("div.XQDdHH")

    # Product link
    link = product.select_one("a[href]")

    product_info = {
        "Product ID": product_id,
        "Name": name.get("title") if name else "Not found",
        "Price": price.get_text(strip=True) if price else "Not found",
        "Rating": rating.get_text(strip=True) if rating else "Not found",
        "Link": (
            "https://www.flipkart.com" + link.get("href")
            if link and link.get("href", "").startswith("/")
            else link.get("href") if link else "Not found"
        )
    }

    product_data.append(product_info)


# ==================================
# STEP 6: DISPLAY RESULTS
# ==================================

for index, product in enumerate(product_data, start=1):

    print(f"\nProduct {index}")
    print("-" * 40)

    for key, value in product.items():
        print(f"{key}: {value}")


# ==================================
# STEP 7: SAVE RESULTS TO CSV
# ==================================

import pandas as pd

if product_data:

    df = pd.DataFrame(product_data)

    df.to_csv(
        "parsed_flipkart_products.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nProduct data saved successfully!")

else:

    print("\nNo matching product containers found.")
    print("Inspect the saved HTML to identify the correct selectors.")
