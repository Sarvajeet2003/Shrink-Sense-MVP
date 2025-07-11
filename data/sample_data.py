import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_items=20):
    """
    Generate sample inventory data with equal distribution across all cases
    """
    np.random.seed(42)  # For reproducible results
    random.seed(42)
    
    # Product categories and their typical characteristics
    categories = {
        'Fresh Food': {
            'shelf_life_range': (1, 7),
            'cost_range': (2, 12),  # Changed from price_range to cost_range
            'margin_multiplier': (1.4, 2.2),  # Selling price = cost * this multiplier
            'products': ['Organic Milk 1L', 'Fresh Bread', 'Bananas 1kg', 'Lettuce Head', 'Chicken Breast 1kg']
        },
        'Perishables': {
            'shelf_life_range': (5, 30),
            'cost_range': (2, 18),  # Changed from price_range to cost_range
            'margin_multiplier': (1.5, 2.5),
            'products': ['Yogurt 500g', 'Cheese Block', 'Deli Ham 500g', 'Muffins 6pk', 'Fresh Pasta']
        },
        'General Goods': {
            'shelf_life_range': (30, 365),
            'cost_range': (3, 50),  # Changed from price_range to cost_range
            'margin_multiplier': (1.3, 2.0),
            'products': ['Canned Beans', 'Pasta Sauce', 'Breakfast Cereal', 'Shampoo 400ml', 'Laundry Detergent']
        }
    }
    
    stores = ['Store_A', 'Store_B', 'Store_C']
    
    data = []
    
    # Calculate items per category for equal distribution
    items_per_category = num_items // 3
    remaining_items = num_items % 3
    
    category_counts = {
        'Fresh Food': items_per_category + (1 if remaining_items > 0 else 0),
        'Perishables': items_per_category + (1 if remaining_items > 1 else 0),
        'General Goods': items_per_category
    }
    
    # Risk level distribution for each category
    risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    item_id = 1
    
    for category, count in category_counts.items():
        cat_info = categories[category]
        
        # Distribute risk levels evenly within each category
        risk_per_level = count // 4
        risk_distribution = [risk_per_level] * 4
        # Add remaining items to different risk levels
        for i in range(count % 4):
            risk_distribution[i] += 1
        
        risk_items = []
        for i, risk_level in enumerate(risk_levels):
            risk_items.extend([risk_level] * risk_distribution[i])
        
        random.shuffle(risk_items)
        
        for i in range(count):
            target_risk = risk_items[i]
            
            # Generate basic product info
            product_name = random.choice(cat_info['products'])
            sku = f"{category[:4].upper()}_{item_id:03d}"
            
            # Generate shelf life
            shelf_life = random.randint(*cat_info['shelf_life_range'])
            
            # Generate current age based on target risk level
            if target_risk == 'LOW':
                current_age = random.randint(0, int(shelf_life * 0.3))
            elif target_risk == 'MEDIUM':
                current_age = random.randint(int(shelf_life * 0.3), int(shelf_life * 0.6))
            elif target_risk == 'HIGH':
                current_age = random.randint(int(shelf_life * 0.6), int(shelf_life * 0.8))
            else:  # CRITICAL
                current_age = random.randint(int(shelf_life * 0.8), shelf_life - 1)
            
            days_remaining = max(0, shelf_life - current_age)
            
            # Generate sale_through_rate based on target risk and ensure it's realistic
            if target_risk == 'LOW':
                sale_through_rate = random.uniform(0.65, 0.95)  # Good performance
            elif target_risk == 'MEDIUM':
                sale_through_rate = random.uniform(0.45, 0.65)  # Moderate performance
            elif target_risk == 'HIGH':
                sale_through_rate = random.uniform(0.25, 0.45)  # Poor performance
            else:  # CRITICAL
                sale_through_rate = random.uniform(0.05, 0.25)  # Very poor performance
            
            # Generate realistic pricing (cost first, then selling price)
            cost_basis = round(random.uniform(*cat_info['cost_range']), 2)
            
            # Ensure selling price is always higher than cost
            margin_multiplier = random.uniform(*cat_info['margin_multiplier'])
            selling_price = round(cost_basis * margin_multiplier, 2)
            
            # Generate quantities
            quantity = random.randint(5, 100)
            
            # Calculate dates
            today = datetime.now()
            expiry_date = today + timedelta(days=days_remaining)
            
            # Generate sales data
            avg_daily_sales = round(quantity * sale_through_rate / 7, 1)
            last_week_sales = int(avg_daily_sales * 7 * random.uniform(0.8, 1.2))
            
            data.append({
                'sku': sku,
                'product_name': product_name,
                'category': category,
                'quantity': quantity,
                'cost_basis': cost_basis,
                'selling_price': selling_price,
                'shelf_life_days': shelf_life,
                'current_age_days': current_age,
                'days_remaining': days_remaining,
                'expiry_date': expiry_date.strftime('%d/%m/%Y'),
                'sale_through_rate': round(sale_through_rate, 2),
                'avg_daily_sales': avg_daily_sales,
                'last_week_sales': last_week_sales,
                'store_location': random.choice(stores),
                'store_type': random.choice(['Urban', 'Suburban', 'Rural']),
                'store_size': random.choice(['Large', 'Medium', 'Small']),
                'supplier': f"Supplier_{random.randint(1, 5)}"
            })
            
            item_id += 1
    
    return pd.DataFrame(data)

def ensure_realistic_financials(df):
    """
    Ensure that cost basis and selling price relationships are realistic
    This is a safety check for any data issues
    """
    # Fix any cases where selling price might be lower than cost basis
    mask = df['selling_price'] <= df['cost_basis']
    if mask.any():
        df.loc[mask, 'selling_price'] = df.loc[mask, 'cost_basis'] * np.random.uniform(1.3, 2.0, mask.sum())
        df['selling_price'] = df['selling_price'].round(2)
    
    # Ensure reasonable profit margins
    df['gross_margin'] = (df['selling_price'] - df['cost_basis']) / df['selling_price']
    
    # Fix any unrealistic margins (too high or too low)
    mask_high = df['gross_margin'] > 0.7  # More than 70% margin
    mask_low = df['gross_margin'] < 0.1   # Less than 10% margin
    
    if mask_high.any():
        df.loc[mask_high, 'selling_price'] = df.loc[mask_high, 'cost_basis'] * np.random.uniform(1.3, 1.7, mask_high.sum())
    
    if mask_low.any():
        df.loc[mask_low, 'selling_price'] = df.loc[mask_low, 'cost_basis'] * np.random.uniform(1.4, 2.0, mask_low.sum())
    
    df['selling_price'] = df['selling_price'].round(2)
    df = df.drop('gross_margin', axis=1)  # Remove temporary column
    
    return df

def validate_csv_data(df):
    """
    Validate and clean uploaded CSV data
    """
    required_columns = [
        'sku', 'product_name', 'category', 'quantity', 'cost_basis', 
        'selling_price', 'shelf_life_days', 'current_age_days', 'sale_through_rate'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Calculate derived fields
    df['days_remaining'] = df['shelf_life_days'] - df['current_age_days']
    df['expiry_date'] = pd.to_datetime('today') + pd.to_timedelta(df['days_remaining'], unit='D')
    df['expiry_date'] = df['expiry_date'].dt.strftime('%d/%m/%Y')
    
    # Fill missing optional fields
    if 'store_location' not in df.columns:
        df['store_location'] = 'Store_A'
    if 'avg_daily_sales' not in df.columns:
        df['avg_daily_sales'] = df['quantity'] * df['sale_through_rate'] / 7
    if 'last_week_sales' not in df.columns:
        df['last_week_sales'] = df['avg_daily_sales'] * 7
    
    # Ensure realistic financial relationships
    df = ensure_realistic_financials(df)
    
    return df

def generate_sample_data_with_validation(num_items=20):
    """
    Generate sample data and validate financial relationships
    """
    df = generate_sample_data(num_items)
    df = ensure_realistic_financials(df)
    return df
