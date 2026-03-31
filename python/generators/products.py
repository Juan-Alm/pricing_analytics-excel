# products.py

import random
import pandas as pd
from config import NUM_PRODUCTS, SEED

random.seed(SEED)


def generate_products(num_products=NUM_PRODUCTS):
    # High-level grocery categories and subcategories
    category_map = {
        "Produce": ["Fruits", "Vegetables"],
        "Dairy": ["Milk", "Cheese", "Yogurt"],
        "Meat": ["Beef", "Chicken", "Pork"],
        "Bakery": ["Bread", "Pastries"],
        "Beverages": ["Juice", "Soft Drinks", "Tea", "Coffee"],
        "Pantry": ["Pasta", "Rice", "Canned Goods", "Spices"],
        "Frozen": ["Frozen Meals", "Ice Cream"],
        "Snacks": ["Chips", "Biscuits", "Nuts"]
    }

    brands = [
        "FreshFarm", "GreenValley", "DailyChoice", "PureFoods",
        "GoldenHarvest", "UrbanEats", "NatureBest", "ValueMart"
    ]

    # Base product names by subcategory
    product_names = {
        "Fruits": ["Apple", "Banana", "Orange", "Kiwi", "Grapes"],
        "Vegetables": ["Carrot", "Broccoli", "Spinach", "Potato", "Tomato"],
        "Milk": ["Whole Milk", "Skim Milk", "Almond Milk"],
        "Cheese": ["Cheddar", "Mozzarella", "Parmesan"],
        "Yogurt": ["Greek Yogurt", "Fruit Yogurt"],
        "Beef": ["Beef Steak", "Ground Beef"],
        "Chicken": ["Chicken Breast", "Chicken Thighs"],
        "Pork": ["Pork Chops", "Bacon"],
        "Bread": ["White Bread", "Wholegrain Bread"],
        "Pastries": ["Croissant", "Muffin"],
        "Juice": ["Orange Juice", "Apple Juice"],
        "Soft Drinks": ["Cola", "Lemon Soda"],
        "Tea": ["Black Tea", "Green Tea"],
        "Coffee": ["Ground Coffee", "Instant Coffee"],
        "Pasta": ["Spaghetti", "Penne"],
        "Rice": ["White Rice", "Brown Rice"],
        "Canned Goods": ["Canned Beans", "Canned Corn"],
        "Spices": ["Salt", "Pepper"],
        "Frozen Meals": ["Frozen Pizza", "Frozen Lasagna"],
        "Ice Cream": ["Vanilla Ice Cream", "Chocolate Ice Cream"],
        "Chips": ["Potato Chips", "Tortilla Chips"],
        "Biscuits": ["Chocolate Biscuits", "Crackers"],
        "Nuts": ["Almonds", "Peanuts"]
    }

    rows = []

    for i in range(1, num_products + 1):
        # Select category and subcategory
        category = random.choice(list(category_map.keys()))
        subcategory = random.choice(category_map[category])

        # Select product name and brand
        name = random.choice(product_names[subcategory])
        brand = random.choice(brands)

        product_name = f"{brand} {name}"

        # Generate pricing (cost < base_price)
        base_price = round(random.uniform(1.5, 20.0), 2)
        cost = round(base_price * random.uniform(0.5, 0.8), 2)

        rows.append({
            "product_id": i,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "base_price": base_price,
            "cost": cost
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_products()
    print(df.head())