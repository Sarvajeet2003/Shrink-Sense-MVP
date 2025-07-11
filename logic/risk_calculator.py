import pandas as pd
import numpy as np

def calculate_risk_score(row):
    """
    Calculate risk score based on time urgency and sales performance
    """
    # Time Factor: How much shelf life is left?
    days_remaining = max(0, row['days_remaining'])
    time_urgency = 1 - (days_remaining / row['shelf_life_days']) if row['shelf_life_days'] > 0 else 1
    
    # Sales Factor: How poorly is it selling?
    sales_problem = 1 - row['sale_through_rate']
    
    # Combined Risk (0-100%)
    risk_score = (time_urgency * 0.6) + (sales_problem * 0.4)
    
    return min(100, max(0, risk_score * 100))  # Ensure 0-100 range

def get_risk_level(risk_score):
    """
    Convert risk score to risk level
    """
    if risk_score <= 40:
        return "LOW"
    elif risk_score <= 60:
        return "MEDIUM"
    elif risk_score <= 80:
        return "HIGH"
    else:
        return "CRITICAL"

def calculate_time_to_action(risk_score):
    """
    Calculate recommended time to take action
    """
    if risk_score <= 40:
        return "7+ days"
    elif risk_score <= 60:
        return "3-7 days"
    elif risk_score <= 80:
        return "1-3 days"
    else:
        return "0-24 hours"

def add_risk_calculations(df):
    """
    Add all risk-related calculations to dataframe
    """
    df['risk_score'] = df.apply(calculate_risk_score, axis=1)
    df['risk_level'] = df['risk_score'].apply(get_risk_level)
    df['time_to_action'] = df['risk_score'].apply(calculate_time_to_action)
    
    return df
