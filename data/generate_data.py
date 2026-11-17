import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np
import pandas as pd

fake = Faker("de_DE")
np.random.seed(42)
random.seed(42)


def generate_fmcg_dataset(n_rows=10000):
    channels = ["Supermarket", "Discounter", "E-Commerce", "Convenience"]
    regions = ["North", "South", "East", "West"]
    categories = {
        "Beverages": [
            "Craft Beer 0.33L",
            "Mineral Water 1.0L",
            "Organic Cola 0.5L",
            "Energy Drink 0.25L",
        ],
        "Snacks": [
            "Potato Chips 150g",
            "Salted Peanuts 200g",
            "Protein Bar 50g",
        ],
        "Dairy": ["Oat Milk 1.0L", "Greek Yogurt 500g", "Butter 250g"],
    }

    base_prices = {
        "Craft Beer 0.33L": 1.49,
        "Mineral Water 1.0L": 0.79,
        "Organic Cola 0.5L": 1.19,
        "Energy Drink 0.25L": 1.99,
        "Potato Chips 150g": 1.89,
        "Salted Peanuts 200g": 1.29,
        "Protein Bar 50g": 2.29,
        "Oat Milk 1.0L": 1.99,
        "Greek Yogurt 500g": 1.49,
        "Butter 250g": 2.19,
    }

    start_date = datetime(2025, 1, 1)
    records = []

    for i in range(1, n_rows + 1):
        order_date = start_date + timedelta(days=random.randint(0, 364))
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        channel = random.choices(channels, weights=[0.45, 0.30, 0.15, 0.10])[0]
        region = random.choice(regions)

        base_price = base_prices[product]
        is_promo = random.choices([0, 1], weights=[0.75, 0.25])[0]
        discount_rate = random.choice([0.10, 0.15, 0.20, 0.30]) if is_promo else 0.0

        units = random.randint(1, 12) if not is_promo else random.randint(3, 24)
        unit_price = round(base_price * (1 - discount_rate), 2)
        unit_cost = round(base_price * 0.55, 2)

        gross_revenue = round(units * base_price, 2)
        net_revenue = round(units * unit_price, 2)
        cogs = round(units * unit_cost, 2)
        gross_margin = round(net_revenue - cogs, 2)

        records.append({
            "TransactionID": f"TRX-{100000 + i}",
            "Date": order_date.strftime("%Y-%m-%d"),
            "Product": product,
            "Category": category,
            "Channel": channel,
            "Region": region,
            "UnitsSold": units,
            "BasePrice": base_price,
            "DiscountApplied": discount_rate,
            "IsPromo": is_promo,
            "NetRevenue": net_revenue,
            "GrossMargin": gross_margin,
        })

    df = pd.DataFrame(records)
    df.to_csv("data/raw_fmcg_data.csv", index=False)
    print(f"Generated {len(df)} transactions -> data/raw_fmcg_data.csv")


if __name__ == "__main__":
    generate_fmcg_dataset()
