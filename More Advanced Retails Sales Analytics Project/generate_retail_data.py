"""
Generate synthetic Retail Sales Data
500K+ transactions across 100 stores, 200K customers, 5K products
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

print("Generating retail analytics data...")

# Stores (100 stores)
stores = pd.DataFrame({
    'store_id': range(1, 101),
    'store_name': [f'Store-{i}' for i in range(1, 101)],
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 100),
    'store_type': np.random.choice(['Flagship', 'Regional', 'Outlet'], 100),
    'store_size_sqft': np.random.randint(5000, 50000, 100),
    'revenue_target': np.random.uniform(50000000, 200000000, 100)
})
stores.to_csv('stores.csv', index=False)
print(f"✓ Generated {len(stores)} stores")

# Customers (200K customers)
base_date = datetime(2024, 1, 1)
customers = pd.DataFrame({
    'customer_id': range(1, 200001),
    'customer_name': [f'Customer-{i}' for i in range(1, 200001)],
    'membership_type': np.random.choice(['Gold', 'Silver', 'Bronze', 'Non-Member'], 200000, p=[0.1, 0.2, 0.3, 0.4]),
    'first_purchase_date': [base_date - timedelta(days=np.random.randint(0, 365)) for _ in range(200000)],
    'lifetime_value': np.random.lognormal(10, 1.5, 200000)
})
customers.to_csv('customers.csv', index=False)
print(f"✓ Generated {len(customers)} customers")

# Products (5K SKUs)
categories = ['Apparel', 'Electronics', 'Home', 'Beauty', 'Sports']
products = pd.DataFrame({
    'sku_id': range(1, 5001),
    'product_name': [f'Product-{i}' for i in range(1, 5001)],
    'category': np.random.choice(categories, 5000),
    'cost_price': np.random.uniform(500, 5000, 5000),
    'mrp': np.random.uniform(1000, 15000, 5000),
    'stock_level': np.random.randint(10, 1000, 5000)
})
products.to_csv('products.csv', index=False)
print(f"✓ Generated {len(products)} products")

# Transactions (500K transactions)
transactions = []
for i in range(500000):
    trans_date = base_date + timedelta(days=np.random.randint(0, 365))
    store_id = np.random.choice(stores['store_id'])
    customer_id = np.random.choice(customers['customer_id'])
    sku_id = np.random.choice(products['sku_id'])
    product = products[products['sku_id'] == sku_id].iloc[0]
    
    quantity = np.random.randint(1, 5)
    discount = np.random.choice([0, 0.1, 0.2, 0.3], p=[0.4, 0.3, 0.2, 0.1])
    price = product['mrp'] * (1 - discount)
    transaction_amount = quantity * price
    
    transactions.append({
        'transaction_id': f'TXN-{i+1:06d}',
        'transaction_date': trans_date,
        'store_id': store_id,
        'customer_id': customer_id,
        'sku_id': sku_id,
        'quantity': quantity,
        'price_per_unit': price,
        'discount': discount,
        'transaction_amount': transaction_amount,
        'payment_method': np.random.choice(['Card', 'Cash', 'Digital', 'Wallet'])
    })
    
    if (i + 1) % 100000 == 0:
        print(f"  Processed {i + 1} transactions...")

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv('transactions.csv', index=False)
print(f"✓ Generated {len(transactions_df)} transactions")

# Inventory (50K records)
inventory = []
for store_id in stores['store_id']:
    for month in range(1, 13):
        date = datetime(2024, month, 1)
        for sku_id in np.random.choice(products['sku_id'], 50):
            inventory.append({
                'date': date,
                'store_id': store_id,
                'sku_id': sku_id,
                'opening_stock': np.random.randint(10, 500),
                'closing_stock': np.random.randint(5, 450),
                'stock_out_flag': np.random.choice([0, 1], p=[0.98, 0.02])
            })

inventory_df = pd.DataFrame(inventory)
inventory_df.to_csv('inventory.csv', index=False)
print(f"✓ Generated {len(inventory_df)} inventory records")

# Promotions (500 campaigns)
promotions = pd.DataFrame({
    'promotion_id': range(1, 501),
    'promotion_type': np.random.choice(['Discount', 'Bundle', 'BOGO', 'Seasonal'], 500),
    'start_date': [base_date + timedelta(days=np.random.randint(0, 300)) for _ in range(500)],
    'end_date': [base_date + timedelta(days=np.random.randint(301, 365)) for _ in range(500)],
    'discount_percentage': np.random.uniform(5, 50, 500),
    'budget': np.random.uniform(100000, 5000000, 500),
    'category': np.random.choice(categories, 500)
})
promotions.to_csv('promotions.csv', index=False)
print(f"✓ Generated {len(promotions)} promotions")

# Customer Engagement (100K records)
engagement = pd.DataFrame({
    'engagement_id': range(1, 100001),
    'customer_id': np.random.choice(customers['customer_id'], 100000),
    'email_opens': np.random.randint(0, 20, 100000),
    'email_clicks': np.random.randint(0, 10, 100000),
    'website_visits': np.random.randint(0, 50, 100000),
    'loyalty_points_earned': np.random.randint(0, 5000, 100000),
    'last_engagement_date': [base_date + timedelta(days=np.random.randint(0, 365)) for _ in range(100000)]
})
engagement.to_csv('customer_engagement.csv', index=False)
print(f"✓ Generated {len(engagement)} engagement records")

print("\n✓ ALL DATA GENERATED SUCCESSFULLY")
print(f"  - Stores: 100")
print(f"  - Customers: 200,000")
print(f"  - Products: 5,000")
print(f"  - Transactions: 500,000")
print(f"  - Inventory Records: 50,000")
print(f"  - Promotions: 500")
print(f"  - Engagement Records: 100,000")
print(f"  Total Records: 855,600")
