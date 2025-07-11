import pandas as pd
import numpy as np

def check_reallocation_viability(row):
    """
    Check if item can be reallocated based on business rules
    """
    # Basic viability criteria
    if row['days_remaining'] < 3:  # Need minimum 3 days for transport
        return False, None, 0, 0
    
    if row['quantity'] < 5:  # Need minimum quantity for cost-effectiveness
        return False, None, 0, 0
    
    # Fresh food needs more time
    if row['category'] == "Fresh Food" and row['days_remaining'] < 2:
        return False, None, 0, 0
    
    # Find best store for reallocation
    best_store = find_best_reallocation_store(row)
    
    if best_store is None:
        return False, None, 0, 0
    
    # Calculate reallocation cost
    reallocation_cost = calculate_reallocation_cost(row, best_store)
    
    # Calculate expected store sell-through rate
    store_sell_through = get_store_sell_through_rate(row['category'], best_store)
    
    return True, best_store, reallocation_cost, store_sell_through

def find_best_reallocation_store(row):
    """
    Find the best store for reallocation based on category and store capabilities
    """
    current_store = row['store_location']
    category = row['category']
    
    # Store compatibility matrix
    store_capabilities = {
        'Store_A': ['Fresh Food', 'Perishables', 'General Goods'],  # Urban - accepts all
        'Store_B': ['Perishables', 'General Goods'],                # Suburban - no fresh food
        'Store_C': ['General Goods']                                # Rural - only general goods
    }
    
    # Available stores (excluding current store)
    available_stores = [store for store in store_capabilities.keys() if store != current_store]
    
    # Find stores that can accept this category
    compatible_stores = []
    for store in available_stores:
        if category in store_capabilities[store]:
            compatible_stores.append(store)
    
    if not compatible_stores:
        return None
    
    # Priority order: Store_A (Urban) > Store_B (Suburban) > Store_C (Rural)
    priority_order = ['Store_A', 'Store_B', 'Store_C']
    
    for store in priority_order:
        if store in compatible_stores:
            return store
    
    return compatible_stores[0] if compatible_stores else None

def calculate_reallocation_cost(row, target_store):
    """
    Calculate the cost of reallocating to target store
    """
    base_cost_per_unit = 0.50
    
    # Distance factor based on store combinations
    distance_factors = {
        ('Store_A', 'Store_B'): 1.2,
        ('Store_A', 'Store_C'): 1.5,
        ('Store_B', 'Store_A'): 1.2,
        ('Store_B', 'Store_C'): 1.3,
        ('Store_C', 'Store_A'): 1.5,
        ('Store_C', 'Store_B'): 1.3,
    }
    
    current_store = row['store_location']
    distance_factor = distance_factors.get((current_store, target_store), 1.0)
    
    # Category factor (fresh food costs more to transport)
    category_factors = {
        'Fresh Food': 1.5,
        'Perishables': 1.2,
        'General Goods': 1.0
    }
    
    category_factor = category_factors.get(row['category'], 1.0)
    
    # Total cost calculation
    cost_per_unit = base_cost_per_unit * distance_factor * category_factor
    total_cost = cost_per_unit * row['quantity']
    
    return total_cost

def get_store_sell_through_rate(category, store):
    """
    Get expected sell-through rate for category at target store
    """
    # Store performance matrix (different stores have different performance by category)
    store_performance = {
        'Store_A': {  # Urban store - high performance
            'Fresh Food': 0.85,
            'Perishables': 0.80,
            'General Goods': 0.75
        },
        'Store_B': {  # Suburban store - medium performance
            'Fresh Food': 0.70,
            'Perishables': 0.75,
            'General Goods': 0.80
        },
        'Store_C': {  # Rural store - lower performance but good for general goods
            'Fresh Food': 0.60,
            'Perishables': 0.65,
            'General Goods': 0.85
        }
    }
    
    return store_performance.get(store, {}).get(category, 0.70)

def add_reallocation_details(df):
    """
    Add detailed reallocation information to dataframe
    """
    reallocation_data = df.apply(check_reallocation_viability, axis=1, result_type='expand')
    
    df['can_reallocate'] = reallocation_data[0]
    df['reallocation_store'] = reallocation_data[1]
    df['reallocation_cost'] = reallocation_data[2]
    df['target_store_sell_through'] = reallocation_data[3]
    
    # Update primary recommendation now that we have reallocation info
    df['primary_recommendation'] = df.apply(
        lambda row: get_updated_primary_strategy(row), 
        axis=1
    )
    
    return df

def get_updated_primary_strategy(row):
    """
    Update primary strategy with reallocation information
    """
    from .decision_engine import get_primary_strategy
    
    return get_primary_strategy(
        row['risk_score'], 
        row['category'], 
        row['can_reallocate'], 
        row['can_donate'],
        row['days_remaining']
    )
