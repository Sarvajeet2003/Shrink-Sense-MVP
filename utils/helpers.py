import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def create_risk_distribution_chart(df):
    """
    Create risk level distribution chart
    """
    risk_counts = df['risk_level'].value_counts()
    
    colors = {'LOW': '#28a745', 'MEDIUM': '#ffc107', 'HIGH': '#fd7e14', 'CRITICAL': '#dc3545'}
    
    fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map=colors,
        title="Risk Level Distribution",
        labels={'x': 'Risk Level', 'y': 'Number of Items'}
    )
    
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_recommendation_chart(df):
    """
    Create recommendation distribution chart
    """
    rec_counts = df['primary_recommendation'].value_counts()
    
    colors = {
        'NO ACTION': '#28a745',
        'REALLOCATE': '#17a2b8',
        'MARKDOWN': '#ffc107',
        'DONATE': '#6f42c1',
        'LIQUIDATE': '#dc3545',
        'REALLOCATE+MARKDOWN': '#20c997'  # Teal color for the combined strategy
    }
    
    fig = px.pie(
        values=rec_counts.values,
        names=rec_counts.index,
        title="Recommendation Distribution",
        color=rec_counts.index,
        color_discrete_map=colors
    )
    
    fig.update_layout(height=400)
    return fig

def create_financial_impact_chart(df):
    """
    Create financial impact chart
    """
    # Group by recommendation and sum financial impact
    financial_summary = df.groupby('primary_recommendation').agg({
        'potential_loss': 'sum',
        'expected_recovery': 'sum',
        'margin_impact': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Potential Loss',
        x=financial_summary['primary_recommendation'],
        y=financial_summary['potential_loss'],
        marker_color='red',
        opacity=0.7
    ))
    
    fig.add_trace(go.Bar(
        name='Expected Recovery',
        x=financial_summary['primary_recommendation'],
        y=financial_summary['expected_recovery'],
        marker_color='green',
        opacity=0.7
    ))
    
    fig.update_layout(
        title='Financial Impact by Recommendation',
        xaxis_title='Recommendation',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400
    )
    
    return fig

def create_category_risk_heatmap(df):
    """
    Create category vs risk level heatmap
    """
    heatmap_data = df.groupby(['category', 'risk_level']).size().reset_index(name='count')
    pivot_data = heatmap_data.pivot(index='category', columns='risk_level', values='count').fillna(0)
    
    fig = px.imshow(
        pivot_data,
        title="Risk Distribution by Category",
        labels=dict(x="Risk Level", y="Category", color="Count"),
        aspect="auto"
    )
    
    fig.update_layout(height=300)
    return fig

def format_currency(amount):
    """
    Format currency for display
    """
    return f"${amount:,.2f}"

def format_percentage(value):
    """
    Format percentage for display
    """
    return f"{value:.1f}%"

def get_risk_color(risk_level):
    """
    Get color for risk level
    """
    colors = {
        'LOW': '#28a745',
        'MEDIUM': '#ffc107', 
        'HIGH': '#fd7e14',
        'CRITICAL': '#dc3545'
    }
    return colors.get(risk_level, '#6c757d')

def get_recommendation_color(recommendation):
    """
    Get color for recommendation
    """
    colors = {
        'NO ACTION': '#28a745',
        'REALLOCATE': '#17a2b8',
        'MARKDOWN': '#ffc107',
        'DONATE': '#6f42c1',
        'LIQUIDATE': '#dc3545',
        'REALLOCATE+MARKDOWN': '#20c997'  # Teal color for the combined strategy
    }
    return colors.get(recommendation, '#6c757d')

def create_summary_metrics(df):
    """
    Create summary metrics for dashboard
    """
    total_items = len(df)
    critical_items = len(df[df['risk_level'] == 'CRITICAL'])
    total_value = df['potential_loss'].sum()
    expected_recovery = df['expected_recovery'].sum()
    potential_savings = expected_recovery - (total_value - expected_recovery)
    
    return {
        'total_items': total_items,
        'critical_items': critical_items,
        'total_value': total_value,
        'expected_recovery': expected_recovery,
        'potential_savings': potential_savings,
        'recovery_rate': (expected_recovery / total_value * 100) if total_value > 0 else 0
    }
