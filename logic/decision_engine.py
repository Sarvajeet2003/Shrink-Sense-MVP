import pandas as pd
from .reallocation import check_reallocation_viability

def get_primary_strategy(risk_score, category, can_reallocate, can_donate, days_remaining):
    """
    Main decision logic for primary strategy INCLUDING DONATE option
    """
    risk_level = get_risk_level_from_score(risk_score)
    
    # CRITICAL Risk (81-100%)
    if risk_level == "CRITICAL":
        if category == "Fresh Food":
            if can_donate and days_remaining >= 1:  # At least 1 day for donation processing
                return "DONATE"
            else:
                return "LIQUIDATE"
        else:
            return "LIQUIDATE"
    
    # HIGH Risk (61-80%)
    elif risk_level == "HIGH":
        if category == "Fresh Food":
            if can_donate and days_remaining >= 2:  # Need 2 days for donation
                return "DONATE"
            elif can_reallocate and days_remaining >= 3:  # Combined strategy for Fresh Food
                return "REALLOCATE+MARKDOWN"
            else:
                return "MARKDOWN"
        else:
            if can_reallocate and days_remaining >= 4:  # Combined strategy for other categories
                return "REALLOCATE+MARKDOWN"
            elif can_reallocate:
                return "REALLOCATE"
            else:
                return "MARKDOWN"
    
    # MEDIUM Risk (41-60%)
    elif risk_level == "MEDIUM":
        if can_reallocate and days_remaining >= 5:  # Good candidate for combined approach
            return "REALLOCATE+MARKDOWN"
        elif can_reallocate:
            return "REALLOCATE"
        elif can_donate and category in ["Fresh Food", "Perishables"] and days_remaining >= 3:
            return "DONATE"
        else:
            return "MARKDOWN"
    
    # LOW Risk (0-40%)
    else:
        return "NO ACTION"

def get_secondary_options(risk_score, category, can_reallocate, can_donate, primary_strategy, days_remaining):
    """
    Generate secondary options based on primary strategy
    """
    options = []
    
    if primary_strategy != "REALLOCATE" and can_reallocate:
        options.append("REALLOCATE")
    
    if primary_strategy != "DONATE" and can_donate and category in ["Fresh Food", "Perishables"] and days_remaining >= 1:
        options.append("DONATE")
    
    if primary_strategy != "MARKDOWN":
        options.append("MARKDOWN")
    
    if primary_strategy != "LIQUIDATE":
        options.append("LIQUIDATE")
    
    return " | ".join(options) if options else "None"

def can_donate_item(category, days_remaining, cost_basis):
    """
    Determine if item can be donated
    """
    # Donation criteria:
    # 1. Must be Fresh Food or Perishables
    # 2. Must have at least 1 day remaining
    # 3. Must have reasonable value (cost >  $ 1)
    
    if category not in ["Fresh Food", "Perishables"]:
        return False
    
    if days_remaining < 1:
        return False
    
    if cost_basis < 1.0:  # Too low value items
        return False
    
    return True

def get_risk_level_from_score(risk_score):
    """Convert risk score to risk level"""
    if risk_score <= 40:
        return "LOW"
    elif risk_score <= 60:
        return "MEDIUM"
    elif risk_score <= 80:
        return "HIGH"
    else:
        return "CRITICAL"

def add_decision_logic(df):
    """
    Add all decision logic to dataframe
    """
    # Add donation eligibility
    df['can_donate'] = df.apply(
        lambda row: can_donate_item(row['category'], row['days_remaining'], row['cost_basis']), 
        axis=1
    )
    
    # Add reallocation viability (this will be updated by reallocation module)
    df['can_reallocate'] = False
    
    # Add primary strategy
    df['primary_recommendation'] = df.apply(
        lambda row: get_primary_strategy(
            row['risk_score'], 
            row['category'], 
            row['can_reallocate'], 
            row['can_donate'],
            row['days_remaining']
        ), 
        axis=1
    )
    
    # Add secondary options
    df['secondary_options'] = df.apply(
        lambda row: get_secondary_options(
            row['risk_score'], 
            row['category'], 
            row['can_reallocate'], 
            row['can_donate'],
            row['primary_recommendation'],
            row['days_remaining']
        ), 
        axis=1
    )
    
    return df
