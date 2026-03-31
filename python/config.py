import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # python/
PROJECT_ROOT = os.path.dirname(BASE_DIR)               # pricing_analytics-excel/




# Shared Configuration for File Generators

NUM_REGIONS = 16
NUM_TRANSACTIONS = 50000
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 200
ERROR_RATE = 0.05

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
SEED = 23


# Corruption configuration per dataset

SALES_CORRUPTION = {
    "numeric_to_string": {
        "columns": ["units_sold", "list_price", "final_price", "revenue", "profit"],
        "rate": 0.05
    },
    "inject_text": {
        "columns": ["list_price", "final_price"],
        "rate": 0.03
    },
    "outliers": {
        "columns": ["units_sold"],
        "rate": 0.01
    },
    "negative": {
        "columns": ["final_price", "profit"],
        "rate": 0.02
    },
    "percentage": {
        "columns": ["discount_pct"],
        "rate": 0.02
    },
    "dates": {
        "columns": ["date"],
        "rate": 0.03
    },
    "fk": {
        "columns": ["product_id", "region_id"],
        "rate": 0.02
    }
}