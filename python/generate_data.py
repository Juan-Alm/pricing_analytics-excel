# generate_data.py

import os
import pandas as pd

from config import OUTPUT_DIR, SEED
from utils.helpers import set_seed
from utils.corruption import apply_corruption_pipeline

# Generators
from generators.products import generate_products
from generators.customers import generate_customers
from generators.regions import generate_regions
from generators.sales import generate_sales
from generators.competitors import generate_competitor_prices


def main():
    # ---------------------------
    # Setup
    # ---------------------------
    set_seed(SEED)

    clean_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "clean")
    raw_dir = OUTPUT_DIR

    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)

    # ---------------------------
    # Generate clean data
    # ---------------------------
    print("Generating clean datasets...")

    regions = pd.DataFrame(generate_regions())
    products = generate_products()
    customers = generate_customers()
    sales = generate_sales(products, customers)
    competitors = generate_competitor_prices(products)

    # ---------------------------
    # Save clean data
    # ---------------------------
    print("Saving clean data...")

    regions.to_csv(os.path.join(clean_dir, "regions.csv"), index=False)
    products.to_csv(os.path.join(clean_dir, "products.csv"), index=False)
    customers.to_csv(os.path.join(clean_dir, "customers.csv"), index=False)
    sales.to_csv(os.path.join(clean_dir, "sales_transactions.csv"), index=False)
    competitors.to_csv(os.path.join(clean_dir, "competitor_prices.csv"), index=False)

    # ---------------------------
    # Define corruption configs
    # ---------------------------
    print("Applying corruption...")

    sales_corruption = {
        "numeric_to_string": {"columns": ["units_sold", "revenue"], "rate": 0.05},
        "inject_text": {"columns": ["final_price"], "rate": 0.03},
        "outliers": {"columns": ["units_sold"], "rate": 0.02},
        "negative": {"columns": ["profit"], "rate": 0.02},
        "percentage": {"columns": ["discount_pct"], "rate": 0.02},
        "dates": {"columns": ["date"], "rate": 0.02},
        "fk": {"columns": ["product_id", "customer_id"], "rate": 0.02},
    }

    customers_corruption = {
        "fk": {"columns": ["region_id"], "rate": 0.03},
    }

    products_corruption = {
        "numeric_to_string": {"columns": ["base_price"], "rate": 0.03},
        "inject_text": {"columns": ["cost"], "rate": 0.02},
    }

    competitors_corruption = {
        "numeric_to_string": {"columns": ["competitor_price"], "rate": 0.05},
        "dates": {"columns": ["date"], "rate": 0.02},
    }

    # ---------------------------
    # Apply corruption
    # ---------------------------
    sales_raw = apply_corruption_pipeline(sales.copy(), sales_corruption)
    customers_raw = apply_corruption_pipeline(customers.copy(), customers_corruption)
    products_raw = apply_corruption_pipeline(products.copy(), products_corruption)
    competitors_raw = apply_corruption_pipeline(competitors.copy(), competitors_corruption)

    # Regions usually remain clean (reference table)
    regions_raw = regions.copy()

    # ---------------------------
    # Save corrupted data
    # ---------------------------
    print("Saving corrupted data...")

    regions_raw.to_csv(os.path.join(raw_dir, "regions.csv"), index=False)
    products_raw.to_csv(os.path.join(raw_dir, "products.csv"), index=False)
    customers_raw.to_csv(os.path.join(raw_dir, "customers.csv"), index=False)
    sales_raw.to_csv(os.path.join(raw_dir, "sales_transactions.csv"), index=False)
    competitors_raw.to_csv(os.path.join(raw_dir, "competitor_prices.csv"), index=False)

    print("Data generation complete.")


if __name__ == "__main__":
    main()