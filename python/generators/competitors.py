# competitors.py

import random
import pandas as pd
from datetime import datetime, timedelta

from config import SEED

random.seed(SEED)


def generate_competitor_prices(products_df, start_date="2024-01-01", end_date="2025-12-31"):
    """
    Generate competitor price data.

    Columns:
    - date
    - product_id
    - competitor_name
    - competitor_price

    Args:
        products_df (pd.DataFrame): Output from products.py
        start_date (str): Start date (YYYY-MM-DD)
        end_date (str): End date (YYYY-MM-DD)

    Returns:
        pd.DataFrame
    """

    competitors = [
        "Countdown", "New World", "Pak'nSave", "FreshChoice", "SuperValue"
    ]

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end - start).days

    rows = []

    for _, product in products_df.iterrows():
        product_id = product["product_id"]
        base_price = product["base_price"]

        # For each product, generate periodic competitor prices
        for comp in competitors:
            # Not every day → simulate weekly/irregular scraping
            num_observations = random.randint(20, 60)

            for _ in range(num_observations):
                random_days = random.randint(0, num_days)
                date = start + timedelta(days=random_days)

                # Competitor pricing logic:
                # around our base price ±15%
                variation = random.uniform(-0.15, 0.15)
                competitor_price = round(base_price * (1 + variation), 2)

                # Ensure no unrealistic negative/zero prices
                competitor_price = max(0.5, competitor_price)

                rows.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "product_id": product_id,
                    "competitor_name": comp,
                    "competitor_price": competitor_price
                })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    from products import generate_products

    products_df = generate_products()
    df = generate_competitor_prices(products_df)
    print(df.head())