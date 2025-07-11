import pandas as pd
import numpy as np

def calculate_expected_recovery(row):
    """
    Calculate expected recovery based on recommendation
    """
    strategy = row['primary_recommendation']
    selling_price = row['selling_price']
    cost_basis = row['cost_basis']
    quantity = row['quantity']
    
    if strategy == "NO ACTION":
        # Expected revenue = selling_price * quantity * sell_through_rate
        # Plus salvage value for unsold items
        sold_quantity = quantity * row['sale_through_rate']
        unsold_quantity = quantity * (1 - row['sale_through_rate'])
        
        # Revenue from sold items at full price
        revenue_from_sales = sold_quantity * selling_price
        
        # Salvage value for unsold items (10% of selling price)
        salvage_value = unsold_quantity * selling_price * 0.10
        
        return revenue_from_sales + salvage_value
    
    elif strategy == "REALLOCATE":
        # 95% of selling price minus transport costs
        base_recovery = selling_price * 0.95 * quantity
        transport_cost = row.get('reallocation_cost', 0)
        # Factor in target store sell-through rate
        target_sell_through = row.get('target_store_sell_through', 0.8)
        return (base_recovery * target_sell_through) - transport_cost
    
    elif strategy == "MARKDOWN":
        # Selling price minus markdown percentage
        markdown_pct = get_markdown_percentage(row['risk_score'])
        discounted_price = selling_price * (1 - markdown_pct/100)
        return discounted_price * quantity
    
    elif strategy == "REALLOCATE+MARKDOWN":
        # Combined strategy: Reallocate 70% of inventory, markdown the rest
        reallocation_portion = 0.7
        markdown_portion = 0.3
        
        # Reallocate calculation for 70% of inventory
        realloc_quantity = quantity * reallocation_portion
        base_recovery = selling_price * 0.95 * realloc_quantity
        transport_cost = row.get('reallocation_cost', 0) * reallocation_portion
        target_sell_through = row.get('target_store_sell_through', 0.8)
        realloc_recovery = (base_recovery * target_sell_through) - transport_cost
        
        # Markdown calculation for 30% of inventory
        markdown_quantity = quantity * markdown_portion
        markdown_pct = get_markdown_percentage(row['risk_score'])
        discounted_price = selling_price * (1 - markdown_pct/100)
        markdown_recovery = discounted_price * markdown_quantity
        
        # Total recovery from both strategies
        return realloc_recovery + markdown_recovery
    
    elif strategy == "DONATE":
        # Tax deduction benefit (30% of cost basis)
        return cost_basis * 0.30 * quantity
    
    elif strategy == "LIQUIDATE":
        # 30% of selling price
        return selling_price * 0.30 * quantity
    
    else:
        return 0

def get_markdown_percentage(risk_score):
    """
    Get markdown percentage based on risk score
    """
    if risk_score >= 80:
        return 30
    elif risk_score >= 60:
        return 25
    elif risk_score >= 40:
        return 15
    else:
        return 0

def calculate_potential_loss(row):
    """
    Calculate potential loss if no action is taken
    """
    # Potential loss = cost basis of items that won't sell
    unsold_probability = 1 - row['sale_through_rate']
    return row['cost_basis'] * row['quantity'] * unsold_probability

def calculate_margin_impact(row):
    """
    Calculate margin impact (Revenue - Cost)
    This should be positive for profitable scenarios
    """
    expected_revenue = row['expected_recovery']
    total_cost = row['cost_basis'] * row['quantity']
    
    # For reallocation, add transport cost to total cost
    if row['primary_recommendation'] == "REALLOCATE" or row['primary_recommendation'] == "REALLOCATE+MARKDOWN":
        transport_cost = row.get('reallocation_cost', 0)
        # For combined strategy, only apply transport cost to the reallocated portion
        if row['primary_recommendation'] == "REALLOCATE+MARKDOWN":
            transport_cost = transport_cost * 0.7  # 70% of inventory is reallocated
        total_cost += transport_cost
    
    return expected_revenue - total_cost

def calculate_profit_margin_percentage(row):
    """
    Calculate profit margin percentage
    """
    if row['expected_recovery'] == 0:
        return 0
    
    total_cost = row['cost_basis'] * row['quantity']
    
    # Add transport costs for both REALLOCATE and REALLOCATE+MARKDOWN strategies
    if row['primary_recommendation'] == "REALLOCATE" or row['primary_recommendation'] == "REALLOCATE+MARKDOWN":
        transport_cost = row.get('reallocation_cost', 0)
        # For combined strategy, only apply transport cost to the reallocated portion
        if row['primary_recommendation'] == "REALLOCATE+MARKDOWN":
            transport_cost = transport_cost * 0.7  # 70% of inventory is reallocated
        total_cost += transport_cost
    
    return ((row['expected_recovery'] - total_cost) / row['expected_recovery']) * 100

def add_financial_calculations(df):
    """
    Add all financial calculations to dataframe
    """
    df['expected_recovery'] = df.apply(calculate_expected_recovery, axis=1)
    df['potential_loss'] = df.apply(calculate_potential_loss, axis=1)
    df['margin_impact'] = df.apply(calculate_margin_impact, axis=1)
    df['profit_margin_pct'] = df.apply(calculate_profit_margin_percentage, axis=1)
    df['markdown_percentage'] = df['risk_score'].apply(get_markdown_percentage)
    
    return df
