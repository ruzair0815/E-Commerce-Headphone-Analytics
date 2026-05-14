import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from datetime import datetime, timedelta

products = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

known_brands = [
    "Sony",
    "Logitech",
    "Razer",
    "HyperX",
    "JBL",
    "Bose",
    "Corsair",
    "SteelSeries",
    "Apple",
    "Beats",
    "Skullcandy",
    "Anker",
    "Sennheiser",
    "Audio-Technica"
]

page = 1

while page <= 20:

    print(f"Scraping page {page}...")

    url = f"https://www.newegg.com/p/pl?d=headphones&page={page}"

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("div", class_="item-cell")

    for item in items:

        title_tag = item.find("a", class_="item-title")
        price_tag = item.find("li", class_="price-current")

        if title_tag and price_tag:

            title = title_tag.text.strip()

            raw_price = price_tag.text.strip()

            cleaned_price = re.findall(r"\d+\.\d+", raw_price)

            if cleaned_price:

                base_price = float(cleaned_price[0])

                brand = "Other"

                for known_brand in known_brands:

                    if known_brand.lower() in title.lower():
                        brand = known_brand
                        break

                # Generate 30 days of historical data
                for days_ago in range(30):

                    fake_date = datetime.now() - timedelta(days=days_ago)

                    fluctuation = random.uniform(-15, 15)

                    simulated_price = round(base_price + fluctuation, 2)

                    if simulated_price < 1:
                        simulated_price = base_price

                    products.append([
                        title,
                        brand,
                        simulated_price,
                        fake_date
                    ])

    page += 1

    time.sleep(1)

df = pd.DataFrame(
    products,
    columns=["Product", "Brand", "Price", "Timestamp"]
)

df.to_csv("headphones.csv", index=False)

print(f"\nSaved {len(products)} rows!")
