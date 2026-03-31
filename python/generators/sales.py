# sales.py

import random
import pandas as pd
from datetime import datetime, timedelta

from config import (
    NUM_TRANSACTIONS,
    SEED
)

random.seed(SEED)


def generate_sales(products_df, customers_df, num_transactions=NUM_TRANSACTIONS):
    """
    Generate sales transactions (fact table).

    Columns:
    - transaction_id
    - date
    - product_id
    - customer_id
    - region_id
    - units_sold
    - list_price
    - discount_pct
    - final_price
    - cost
    - revenue
    - profit

    Args:
        products_df (pd.DataFrame): Output from products.py
        customers_df (pd.DataFrame): Output from customers.py

    Returns:
        pd.DataFrame
    """

    rows = []

    # Date range (1 year for realistic time series)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    for i in range(1, num_transactions + 1):
        # --- Sample dimension keys ---
        product = products_df.sample(1).iloc[0]
        customer = customers_df.sample(1).iloc[0]

        product_id = product["product_id"]
        customer_id = customer["customer_id"]
        region_id = customer["region_id"]  # enforce consistency

        # --- Date ---
        random_days = random.randint(0, date_range_days)
        date = start_date + timedelta(days=random_days)

        # --- Sales mechanics ---
        units_sold = random.randint(1, 20)

        list_price = product["base_price"]
        cost = product["cost"]

        # Discount logic (bounded, realistic)
        discount_pct = round(random.uniform(0.0, 0.30), 2)

        final_price = round(list_price * (1 - discount_pct), 2)

        # --- Financials ---
        revenue = round(units_sold * final_price, 2)
        total_cost = round(units_sold * cost, 2)
        profit = round(revenue - total_cost, 2)

        rows.append({
            "transaction_id": i,
            "date": date.strftime("%Y-%m-%d"),
            "product_id": product_id,
            "customer_id": customer_id,
            "region_id": region_id,
            "units_sold": units_sold,
            "list_price": list_price,
            "discount_pct": discount_pct,
            "final_price": final_price,
            "cost": cost,
            "revenue": revenue,
            "profit": profit
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Minimal test (requires products/customers modules)
    from products import generate_products
    from customers import generate_customers

    products_df = generate_products()
    customers_df = generate_customers()

    sales_df = generate_sales(products_df, customers_df)
    print(sales_df.head())