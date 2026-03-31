# customers.py

import random
import pandas as pd
from config import NUM_CUSTOMERS, NUM_REGIONS, SEED

random.seed(SEED)


def generate_customers(num_customers=NUM_CUSTOMERS):
    """
    Generate customer data.

    Columns:
    - customer_id
    - customer_name
    - segment (Retail, Corporate, SMB)
    - industry
    - region_id

    Returns:
        pd.DataFrame
    """

    segments = ["Retail", "Corporate", "SMB"]

    industries = [
        "Food & Beverage", "Retail", "Healthcare", "Education",
        "Hospitality", "Manufacturing", "Technology", "Construction",
        "Finance", "Logistics"
    ]

    # Simple name pools
    first_names = [
        "John", "Emma", "Liam", "Olivia", "Noah", "Ava",
        "William", "Sophia", "James", "Isabella"
    ]

    last_names = [
        "Smith", "Brown", "Wilson", "Taylor", "Anderson",
        "Thomas", "Jackson", "White", "Harris", "Martin"
    ]

    company_suffixes = ["Ltd", "Corp", "Group", "Solutions", "Enterprises"]

    rows = []

    for i in range(1, num_customers + 1):
        segment = random.choice(segments)
        industry = random.choice(industries)

        # Region IDs must match regions.py format
        region_id = f"R{random.randint(1, NUM_REGIONS):03d}"

        # Naming logic depends on segment
        if segment == "Retail":
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
        else:
            base = random.choice(last_names)
            suffix = random.choice(company_suffixes)
            name = f"{base} {suffix}"

        rows.append({
            "customer_id": i,
            "customer_name": name,
            "segment": segment,
            "industry": industry,
            "region_id": region_id
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_customers()
    print(df.head())