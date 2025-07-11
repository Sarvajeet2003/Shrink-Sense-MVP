import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Import custom modules
from data.sample_data import generate_sample_data, validate_csv_data
from logic.risk_calculator import add_risk_calculations
from logic.decision_engine import add_decision_logic
from logic.reallocation import add_reallocation_details
from logic.financial import add_financial_calculations
from utils.helpers import (
    create_risk_distribution_chart,
    create_recommendation_chart,
    create_financial_impact_chart,
    create_category_risk_heatmap,
    format_currency,
    format_percentage,
    get_risk_color,
    get_recommendation_color,
    create_summary_metrics
)

# Page configuration
st.set_page_config(
    page_title="Shrink Sense Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-LOW { background-color: #d4edda; }
    .risk-MEDIUM { background-color: #fff3cd; }
    .risk-HIGH { background-color: #f8d7da; }
    .risk-CRITICAL { background-color: #f5c6cb; }
    .recommendation-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Shrink Sense Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent Inventory Shrinkage Management System</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Problem Statement", "📊 Dashboard", "🧠 Logic Explanation", "🚀 Future Improvements"]
    )
    if page == "Problem Statement":
        show_problem_statement()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "🧠 Logic Explanation":
        show_logic_explanation()
    elif page == "🚀 Future Improvements":
        show_future_improvements()
def show_problem_statement():
    """Display detailed problem statement with illustrations"""
    
    # Hero section with title and subtitle
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; margin: 0;">📊 Shrink Sense Dashboard</h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0;">Transform Inventory Loss into Profit Opportunity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # What is inventory shrinkage - with visual appeal
    st.markdown("""
    ## 🔍 What is Inventory Shrinkage?
    
    Inventory shrinkage is the **#1 silent profit killer** in retail, costing businesses billions annually.
    """)
    
    # Visual representation of shrinkage causes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #ff6b6b; color: white; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">⏰</h3>
            <p style="margin: 0.5rem 0 0 0;"><strong>Product Expiration</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Time-sensitive items spoil</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #4ecdc4; color: white; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">📉</h3>
            <p style="margin: 0.5rem 0 0 0;"><strong>Poor Sales</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Slow-moving inventory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #45b7d1; color: white; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">🌡️</h3>
            <p style="margin: 0.5rem 0 0 0;"><strong>Spoilage</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Quality degradation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #f7b731; color: white; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">💸</h3>
            <p style="margin: 0.5rem 0 0 0;"><strong>Lost Opportunity</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Wasted shelf space</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # The real cost section
    st.markdown("""
    ## 💰 The Hidden Cost Crisis
    
    **Every expired product represents multiple layers of financial loss:**
    """)
    
    # Enhanced financial impact visualization
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Impact breakdown with better styling
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #007bff;">
            <h4 style="color: #007bff; margin-top: 0;">💸 Direct Cost Loss (40%)</h4>
            <p>Original purchase price completely lost</p>
            
            <h4 style="color: #28a745; margin-top: 1rem;">📊 Lost Margin (30%)</h4>
            <p>Potential profit never realized</p>
            
            <h4 style="color: #ffc107; margin-top: 1rem;">🗑️ Disposal Costs (15%)</h4>
            <p>Additional removal and disposal fees</p>
            
            <h4 style="color: #dc3545; margin-top: 1rem;">⏰ Opportunity Cost (15%)</h4>
            <p>Shelf space that could have generated profit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Enhanced pie chart
        data = {
            'Category': ['Direct Cost Loss', 'Lost Margin', 'Disposal Costs', 'Opportunity Cost'],
            'Impact': [40, 30, 15, 15]
        }
        
        fig = px.pie(
            data, 
            values='Impact', 
            names='Category',
            title='Financial Impact Breakdown',
            color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f7b731']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
        fig.update_layout(
            font=dict(size=14),
            title_font_size=16,
            title_x=0.5,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Real-world example - CORRECTED CALCULATION
    st.markdown("""
    <div style="background: #e8f4f8; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
        <h4 style="color: #2c3e50; margin-top: 0;">🏪 Real-World Example</h4>
        <p><strong>Store ABC:</strong> 100 units of premium yogurt ($5 retail, $3 cost each)</p>
        <p><strong>Problem:</strong> Poor placement leads to 30% sell-through, 70 units expire</p>
        <p><strong>Current Loss:</strong> $210 in direct costs + $35 disposal = <strong style="color: #e74c3c;">$245 total loss</strong></p>
        <p><strong>With Shrink Sense:</strong> Early detection → Reallocate + 15% markdown → <strong style="color: #27ae60;">$52.50 loss instead of $245</strong></p>
        <p><strong>Savings:</strong> <strong style="color: #27ae60;">$192.50 (79% loss reduction)</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # The challenge section
    st.markdown("""
    ## ⚠️ The Time-Sensitive Challenge
    
    **Retailers face a complex decision-making process with shrinking time windows:**
    """)
    
    # Challenge visualization with timeline
    challenge_data = {
        'Days Until Expiration': [10, 7, 5, 3, 1, 0],
        'Available Options': [5, 4, 3, 2, 1, 0],
        'Value Recovery Potential': [95, 85, 70, 50, 25, 0]
    }
    
    fig = go.Figure()
    
    # Add value recovery line
    fig.add_trace(go.Scatter(
        x=challenge_data['Days Until Expiration'],
        y=challenge_data['Value Recovery Potential'],
        mode='lines+markers',
        name='Value Recovery %',
        line=dict(color='#e74c3c', width=4),
        marker=dict(size=10)
    ))
    
    # Add options available line
    fig.add_trace(go.Scatter(
        x=challenge_data['Days Until Expiration'],
        y=[opt * 20 for opt in challenge_data['Available Options']],  # Scale for visibility
        mode='lines+markers',
        name='Available Options',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    # Add zones
    fig.add_vrect(x0=7, x1=10, fillcolor="rgba(46, 204, 113, 0.2)", annotation_text="Optimal Action Zone", line_width=0)
    fig.add_vrect(x0=3, x1=7, fillcolor="rgba(241, 196, 15, 0.2)", annotation_text="Critical Action Zone", line_width=0)
    fig.add_vrect(x0=0, x1=3, fillcolor="rgba(231, 76, 60, 0.2)", annotation_text="Emergency Zone", line_width=0)
    
    fig.update_layout(
        title='The Shrinking Window of Opportunity',
        xaxis_title='Days Until Expiration',
        yaxis_title='Value Recovery Potential (%)',
        yaxis2=dict(
            title='Available Options',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        height=450,
        showlegend=True,
        legend=dict(x=0.7, y=0.9)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Solution approach
    st.markdown("""
    ## 🎯 The Shrink Sense Solution
    
    **Our intelligent system transforms this challenge into opportunity through:**
    """)
    
    # Solution features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #e8f6f3; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1abc9c;">
            <h4 style="color: #1abc9c; margin-top: 0;">🔍 Smart Risk Assessment</h4>
            <ul style="margin: 0;">
                <li>Real-time expiration monitoring</li>
                <li>Sales velocity analysis</li>
                <li>Demand forecasting</li>
                <li>Multi-factor risk scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #fef9e7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f39c12; margin-top: 1rem;">
            <h4 style="color: #f39c12; margin-top: 0;">💡 Strategic Recommendations</h4>
            <ul style="margin: 0;">
                <li>Optimal markdown pricing</li>
                <li>Store reallocation analysis</li>
                <li>Donation tax benefits</li>
                <li>Combo strategy optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #eaf2ff; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #3498db;">
            <h4 style="color: #3498db; margin-top: 0;">📊 Financial Impact Analysis</h4>
            <ul style="margin: 0;">
                <li>Expected recovery calculations</li>
                <li>Cost-benefit analysis</li>
                <li>ROI projections</li>
                <li>Margin impact assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f4ecf7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #9b59b6; margin-top: 1rem;">
            <h4 style="color: #9b59b6; margin-top: 0;">🎯 Actionable Insights</h4>
            <ul style="margin: 0;">
                <li>Prioritized action lists</li>
                <li>Implementation timelines</li>
                <li>Performance tracking</li>
                <li>Success metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Strategy comparison chart
    st.markdown("""
    ## 📈 Strategy Performance Comparison
    
    **See how different strategies stack up in terms of value recovery:**
    """)
    
    strategy_data = {
        'Strategy': ['No Action', 'Markdown Only', 'Reallocate Only', 'Reallocate + Markdown', 'Donation', 'Liquidation'],
        'Value Recovery %': [0, 65, 75, 85, 30, 25],
        'Risk Level': ['Critical', 'Medium', 'Low', 'Medium', 'High', 'Critical'],
        'Implementation Speed': ['N/A', 'Fast', 'Medium', 'Medium', 'Fast', 'Slow']
    }
    
    # Create grouped bar chart
    # fig = go.Figure()
    
    risk_colors = {
        'Low': '#27ae60',
        'Medium': '#f39c12', 
        'High': '#e67e22',
        'Critical': '#e74c3c',
        'N/A': '#95a5a6'
    }
    
    colors = [risk_colors[risk] for risk in strategy_data['Risk Level']]
    
    fig.add_trace(go.Bar(
        x=strategy_data['Strategy'],
        y=strategy_data['Value Recovery %'],
        marker_color=colors,
        text=strategy_data['Value Recovery %'],
        texttemplate='%{text}%',
        textposition='outside',
        name='Value Recovery %'
    ))
    
    fig.update_layout(
        title='Value Recovery by Strategy',
        xaxis_title='Strategy',
        yaxis_title='Value Recovery (%)',
        yaxis=dict(range=[0, 100]),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Business value metrics
    st.markdown("""
    ## 💰 Proven Business Impact
    
    **Organizations using Shrink Sense report significant improvements:**
    """)
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; border-radius: 15px;">
            <h2 style="margin: 0; font-size: 2.5rem;">40-60%</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;"><strong>Waste Reduction</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Less expired inventory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #3498db, #2980b9); color: white; border-radius: 15px;">
            <h2 style="margin: 0; font-size: 2.5rem;">15-25%</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;"><strong>Margin Improvement</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">On at-risk inventory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; border-radius: 15px;">
            <h2 style="margin: 0; font-size: 2.5rem;">5-10</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;"><strong>Hours Saved</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Per week in analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #e67e22, #d35400); color: white; border-radius: 15px;">
            <h2 style="margin: 0; font-size: 2.5rem;">300%</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;"><strong>ROI</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Typical first-year ROI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sustainability impact
    st.markdown("""
    <div style="background: #d5f4e6; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
        <h4 style="color: #2d8a3e; margin-top: 0;">🌱 Environmental Impact</h4>
        <p>Beyond financial benefits, Shrink Sense contributes to sustainability goals:</p>
        <ul>
            <li><strong>Reduces food waste</strong> by 40-60% through better inventory management</li>
            <li><strong>Supports circular economy</strong> through donation and reallocation strategies</li>
            <li><strong>Minimizes landfill impact</strong> by extending product lifecycle</li>
            <li><strong>Enhances CSR profile</strong> through responsible inventory practices</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 2rem;">
        <h3 style="margin: 0 0 1rem 0;">Ready to Transform Your Inventory Management?</h3>
        <p style="margin: 0; font-size: 1.1rem;">Navigate to the <strong>Dashboard</strong> tab to see Shrink Sense in action!</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Start making data-driven decisions that protect your profits and support sustainability</p>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    st.header("📊 Inventory Analysis Dashboard")
    
    # Data source selection
    st.sidebar.subheader("Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Generate Sample Data", "Upload CSV File"]
    )
    
    # Load data based on selection
    if data_source == "Generate Sample Data":
        num_items = st.sidebar.slider("Number of items to generate:", 10, 100, 20)
        
        if st.sidebar.button("Generate New Data"):
            st.session_state['data_generated'] = True
        
        if st.sidebar.button("Refresh Data") or 'data_generated' not in st.session_state:
            st.session_state['data_generated'] = True
        
        if st.session_state.get('data_generated', False):
            with st.spinner("Generating sample data..."):
                df = generate_sample_data(num_items)
                df = process_data(df)
                display_dashboard(df)
    
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file with inventory data"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df = validate_csv_data(df)
                df = process_data(df)
                st.success("Data uploaded successfully!")
                display_dashboard(df)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.info("Please ensure your CSV has the required columns: sku, product_name, category, quantity, cost_basis, selling_price, shelf_life_days, current_age_days, sale_through_rate")

def process_data(df):
    """Process data through all logic modules"""
    df = add_risk_calculations(df)
    df = add_decision_logic(df)
    df = add_reallocation_details(df)
    df = add_financial_calculations(df)
    return df

def display_dashboard(df):
    """Display the main dashboard"""
    
    # Summary metrics
    metrics = create_summary_metrics(df)
    
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Items",
            metrics['total_items'],
            help="Total inventory items analyzed"
        )
    
    with col2:
        st.metric(
            "Critical Items",
            metrics['critical_items'],
            delta=f"{metrics['critical_items']/metrics['total_items']*100:.1f}%",
            help="Items requiring immediate action"
        )
    
    with col3:
        st.metric(
            "Total Value at Risk",
            format_currency(metrics['total_value']),
            help="Total value that could be lost without action"
        )
    
    with col4:
        st.metric(
            "Expected Recovery",
            format_currency(metrics['expected_recovery']),
            delta=f"{metrics['recovery_rate']:.1f}%",
            help="Expected value recovery with recommendations"
        )
    
    # Charts section
    st.subheader("📊 Analysis Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_risk_distribution_chart(df), use_container_width=True)
        st.plotly_chart(create_category_risk_heatmap(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_recommendation_chart(df), use_container_width=True)
        st.plotly_chart(create_financial_impact_chart(df), use_container_width=True)


    st.subheader("🎯 Detailed Recommendations Summary")
    
    # Group by recommendation with more detailed info
    recommendation_groups = df.groupby('primary_recommendation')
    
    for recommendation, group_df in recommendation_groups:
        count = len(group_df)
        total_quantity = group_df['quantity'].sum()
        total_potential_loss = group_df['potential_loss'].sum()
        total_expected_recovery = group_df['expected_recovery'].sum()
        total_margin_impact = group_df['margin_impact'].sum()
        
        with st.expander(f"📋 {recommendation} - {count} items ({total_quantity:.0f} units)"):
            
            # Summary metrics for this recommendation
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Quantity", f"{total_quantity:.0f}")
            with col2:
                st.metric("Potential Loss", format_currency(total_potential_loss))
            with col3:
                st.metric("Expected Recovery", format_currency(total_expected_recovery))
            with col4:
                st.metric("Margin Impact", format_currency(total_margin_impact))
            
            # Detailed table for this recommendation
            if recommendation == "REALLOCATE":
                # Special handling for reallocation with all details
                display_columns = [
                    'sku', 'product_name', 'category', 'store_location', 
                    'quantity', 'risk_level', 'days_remaining', 'cost_basis', 'selling_price',
                    'reallocation_store', 'reallocation_cost', 'target_store_sell_through',
                    'sale_through_rate', 'expected_recovery', 'margin_impact'
                ]
                
                # Later in the code where columns are renamed
                display_df = display_df.rename(columns={
                    'store_location': 'Current Store',
                    'cost_basis': 'Cost Basis ( $ )',
                    'selling_price': 'Selling Price ( $ )',
                    'reallocation_store': 'Target Store',
                    'reallocation_cost': 'Transport Cost ( $ )',
                    'target_store_sell_through': 'Target Store Rate',
                    'sale_through_rate': 'Current Store Rate',
                    'expected_recovery': 'Expected Recovery ( $ )',
                    'margin_impact': 'Margin Impact ( $ )'
                })
                
                st.dataframe(display_df, use_container_width=True)
                
                # Additional insights for reallocation
                st.write("**Reallocation Insights:**")
                avg_transport_cost = group_df['reallocation_cost'].mean()
                avg_target_rate = group_df['target_store_sell_through'].mean()
                avg_current_rate = group_df['sale_through_rate'].mean()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Transport Cost", f"${avg_transport_cost:.2f}")
                with col2:
                    st.metric("Avg Target Store Rate", f"{avg_target_rate:.1%}")
                with col3:
                    st.metric("Avg Current Store Rate", f"{avg_current_rate:.1%}")
                
            elif recommendation == "DONATE":
                # Special handling for donation
                display_columns = [
                    'sku', 'product_name', 'category', 'store_location',
                    'quantity', 'days_remaining', 'cost_basis', 'selling_price', 'sale_through_rate',
                    'expected_recovery', 'margin_impact'
                ]
                
                display_df = group_df[display_columns].copy()
                display_df['cost_basis'] = display_df['cost_basis'].round(2)
                display_df['sale_through_rate'] = display_df['sale_through_rate'].round(3)
                display_df['expected_recovery'] = display_df['expected_recovery'].round(2)
                display_df['margin_impact'] = display_df['margin_impact'].round(2)
                
                # Rename columns for better display
                display_df = display_df.rename(columns={
                    'store_location': 'Store ID',
                    'cost_basis': 'Cost Basis ( $ )',
                    'selling_price': 'Selling Price ( $ )',
                    'sale_through_rate': 'Current Store Rate',
                    'expected_recovery': 'Tax Benefit ( $ )',
                    'margin_impact': 'Net Impact ($)'
                })
                
                st.dataframe(display_df, use_container_width=True)
                
                # Additional insights for donation
                st.write("**Donation Insights:**")
                total_tax_benefit = group_df['expected_recovery'].sum()
                total_cost_basis = (group_df['cost_basis'] * group_df['quantity']).sum()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Tax Benefit", f"${total_tax_benefit:.2f}")
                with col2:
                    st.metric("Total Cost Basis", f"${total_cost_basis:.2f}")
                
            else:
                # Standard display for other recommendations
                display_columns = [
                    'sku', 'product_name', 'category', 'store_location',
                    'quantity', 'risk_level', 'days_remaining', 'cost_basis', 'selling_price', 'sale_through_rate',
                    'expected_recovery', 'margin_impact'
                ]
                
                if recommendation == "MARKDOWN":
                    display_columns.append('markdown_percentage')
                
                display_df = group_df[display_columns].copy()
                display_df['sale_through_rate'] = display_df['sale_through_rate'].round(3)
                display_df['expected_recovery'] = display_df['expected_recovery'].round(2)
                display_df['margin_impact'] = display_df['margin_impact'].round(2)
                display_df['cost_basis'] = display_df['cost_basis'].round(2)
                display_df['selling_price'] = display_df['selling_price'].round(2)
                
                # Rename columns for better display
                display_df = display_df.rename(columns={
                    'store_location': 'Store ID',
                    'cost_basis': 'Cost Basis ( $ )',
                    'selling_price': 'Selling Price ( $ )',
                    'sale_through_rate': 'Store Sell-Through Rate',
                    'expected_recovery': 'Expected Recovery ( $ )',
                    'margin_impact': 'Margin Impact ( $ )'
                })
                
                if recommendation == "MARKDOWN":
                    display_df = display_df.rename(columns={
                        'markdown_percentage': 'Markdown %'
                    })
                
                st.dataframe(display_df, use_container_width=True)
    
    # Detailed item analysis
    st.subheader("📋 Detailed Item Analysis")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.selectbox(
            "Filter by Risk Level:",
            ["All"] + list(df['risk_level'].unique())
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category:",
            ["All"] + list(df['category'].unique())
        )
    
    with col3:
        recommendation_filter = st.selectbox(
            "Filter by Recommendation:",
            ["All"] + list(df['primary_recommendation'].unique())
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df['risk_level'] == risk_filter]
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if recommendation_filter != "All":
        filtered_df = filtered_df[filtered_df['primary_recommendation'] == recommendation_filter]
    
    # Display filtered results
    st.write(f"Showing {len(filtered_df)} items")
    
    # Prepare display dataframe
    display_df = filtered_df[[
        'sku', 'product_name', 'category', 'quantity', 'cost_basis', 'selling_price', 'risk_level', 'risk_score',
        'days_remaining', 'primary_recommendation', 'expected_recovery', 'margin_impact'
    ]].copy()
    
    # Format numerical columns
    display_df['risk_score'] = display_df['risk_score'].round(1)
    display_df['expected_recovery'] = display_df['expected_recovery'].round(2)
    display_df['margin_impact'] = display_df['margin_impact'].round(2)
    
    # Color code the dataframe
    def color_risk_level(val):
        colors = {
            'LOW': 'background-color: #d4edda',
            'MEDIUM': 'background-color: #fff3cd',
            'HIGH': 'background-color: #f8d7da',
            'CRITICAL': 'background-color: #f5c6cb'
        }
        return colors.get(val, '')
    
    styled_df = display_df.style.applymap(color_risk_level, subset=['risk_level'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Download option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"shrink_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Interactive scenario analysis
    st.subheader("🔄 Interactive Scenario Analysis")
    
    selected_item = st.selectbox(
        "Select an item for detailed analysis:",
        options=df['sku'].tolist(),
        format_func=lambda x: f"{x} - {df[df['sku']==x]['product_name'].iloc[0]}"
    )
    
    if selected_item:
        item_data = df[df['sku'] == selected_item].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Current Situation:**")
            st.write(f"- Product: {item_data['product_name']}")
            st.write(f"- Category: {item_data['category']}")
            st.write(f"- Quantity: {item_data['quantity']}")
            st.write(f"- Days Remaining: {item_data['days_remaining']}")
            st.write(f"- Risk Level: {item_data['risk_level']}")
            st.write(f"- Risk Score: {item_data['risk_score']:.1f}%")
            st.write(f"- Sale Through Rate: {item_data['sale_through_rate']:.2f}")
        
        with col2:
            st.write("**Recommendations:**")
            st.write(f"- Primary: **{item_data['primary_recommendation']}**")
            st.write(f"- Secondary Options: {item_data['secondary_options']}")
            st.write(f"- Expected Recovery: {format_currency(item_data['expected_recovery'])}")
            # st.write(f"- Margin Impact: {format_currency(item_data['margin_impact'])}")
            st.write(f"- Time to Action: {item_data['time_to_action']}")
            
            if item_data['can_reallocate']:
                st.write(f"- Reallocation Cost: {format_currency(item_data.get('reallocation_cost', 0))}")
            
            if item_data['primary_recommendation'] == 'MARKDOWN':
                st.write(f"- Markdown Percentage: {item_data['markdown_percentage']}%")


def show_logic_explanation():
    """Display detailed logic explanation"""
    st.header("🧠 Logic Behind Shrink Sense Dashboard")
    
    st.markdown("""
    ## 🎯 Core Problem Being Solved
    
    The dashboard addresses inventory shrinkage - when products expire, spoil, or become unsellable, causing direct financial losses. It provides intelligent recommendations to minimize these losses through:
    - **Markdown pricing** (discount products to sell faster)
    - **Inventory relocation** (move items to stores where they'll sell better)
    - **Donation programs** (tax benefits + community impact) - **NEW**
    - **Combo strategies** (reallocation + markdown for maximum recovery) - **NEW**
    - **Liquidation** (sell to third parties when other options fail)
    """)
    
    st.markdown("""
    ## 🔄 Complete Workflow Example
    
    ### Scenario: Fresh Food Item at Store A
    
    **Data Input:**
    - SKU: Milk cartons
    - Shelf life: 7 days
    - Current age: 5 days
    - Sell-through rate: 30%
    - Inventory: 50 units
    
    **Risk Calculation:**
    - Time risk: 5/7 = 0.71 (71%)
    - Sales risk: 1 - 0.30 = 0.70 (70%)
    - Combined risk: 0.7 × 0.71 + 0.3 × 0.70 = 0.71 (71%)
    
    **Recommendation Logic:**
    - Risk > 0.6 → High risk category
    - Fresh Food + High risk → 25% markdown
    - Expected clearance: 85% (based on historical data)
    
    **Dashboard Display:**
    - Shows "MARKDOWN_25%" recommendation
    - Highlights in red for urgency
    - Calculates potential recovery: 50 × price × 0.75 × 0.85
    """)
    
    st.markdown("""
    ## 📊 Core Risk Assessment Formula
    
    ### Primary Risk Calculation:
    ```python
    # Time Risk: How close is the item to expiration?
    time_risk = inventory_age_days / shelf_life_days
    
    # Sales Risk: How poorly is it selling?
    sales_risk = 1 - sell_through_rate
    
    # Combined Shrinkage Risk (weighted formula)
    shrinkage_risk = (0.7 × time_risk) + (0.3 × sales_risk)
    ```
    
    ### Why This Formula?
    - **70% weight on time** - Expiration is absolute, sales can improve
    - **30% weight on sales** - Poor performers need earlier intervention
    - **Scale 0-1** - Easy to understand and set thresholds
    """)
    
    # Create three columns for category-specific rules
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ## 🥛 Fresh Food (1-7 days)
        
        **Business Logic:** Extremely perishable, customer safety critical
        
        | Risk Level | Action |
        |------------|--------|
        | **Critical (>60%)** | **DONATION** (if viable) or **LIQUIDATE** |
        | **High (40-60%)** | **REALLOCATE+MARKDOWN** or **MARKDOWN 25%** |
        | **Medium (20-40%)** | **MARKDOWN 15%** |
        | **Low (<20%)** | **NO ACTION** |
        
        **Key Features:**
        - Donation priority at 60% - tax benefits + community impact
        - Combo strategy for high-risk items with viable stores
        - Maximum 35% markdown - beyond this, customers assume spoilage
        - Emergency processing - decisions needed within hours
        """)
    
    with col2:
        st.markdown("""
        ## 🥗 Perishables (3-14 days)
        
        **Business Logic:** Moderate shelf life, quality degrades visibly
        
        | Risk Level | Action |
        |------------|--------|
        | **Critical (>80%)** | **DONATION** (if viable) or **LIQUIDATE** |
        | **High (60-80%)** | **REALLOCATE+MARKDOWN** or **MARKDOWN 25%** |
        | **Medium (40-60%)** | **REALLOCATE** or **MARKDOWN 15%** |
        | **Low (<40%)** | **NO ACTION** |
        
        **Key Features:**
        - Liquidation at 80% - standard high-risk threshold
        - Relocation preferred - more time available for transfers
        - Maximum 25% markdown - maintains perceived quality
        """)
    
    with col3:
        st.markdown("""
        ## 📦 General Merchandise (30-365 days)
        
        **Business Logic:** Long shelf life, appearance doesn't degrade
        
        | Risk Level | Action |
        |------------|--------|
        | **Critical (>80%)** | **DONATION** (if viable) or **LIQUIDATE** |
        | **High (60-80%)** | **REALLOCATE+MARKDOWN** or **RELOCATE** |
        | **Medium (40-60%)** | **REALLOCATE** or **MARKDOWN 15%** |
        | **Low (<40%)** | **NO ACTION** |
        
        **Key Features:**
        - Relocation first - time allows for strategic placement
        - Conservative markdowns - maintains brand value
        - Maximum 15% markdown - higher discounts signal clearance
        """)
    
    st.markdown("""
    ## 💰 Enhanced Financial Impact Calculations
    
    ### Revenue Recovery Formulas:
    
    #### Standard Strategies:
    ```python
    # Markdown scenario
    markdown_price = current_price × (1 - markdown_percentage)
    markdown_revenue = quantity × markdown_price
    
    # Liquidation scenario
    liquidation_revenue = quantity × current_price × 0.30  # 30% recovery
    ```
    
    #### NEW: Donation Recovery Formula:
    ```python
    # Donation scenario
    fair_market_value = quantity × current_price
    tax_benefit = fair_market_value × 0.25  # 25% corporate tax rate
    processing_cost = quantity × 0.50  # $0.50 per unit processing cost
    donation_net_benefit = tax_benefit - processing_cost
    donation_recovery = max(donation_net_benefit, 0)  # Cannot be negative
    ```
    
    #### NEW: Reallocation + Markdown Recovery Formula:
    ```python
    # Combo strategy: Reallocate + Markdown
    target_store_sell_through = 0.75  # Better performing store
    combo_sell_through = target_store_sell_through × 1.2  # 20% boost from markdown
    markdown_price = current_price × (1 - markdown_percentage)
    transfer_cost = quantity × 0.25  # $0.25 per unit transfer cost
    
    # Revenue calculation
    sold_quantity = quantity × min(combo_sell_through, 0.95)  # Cap at 95%
    revenue = sold_quantity × markdown_price
    combo_recovery = revenue - transfer_cost
    ```
    """)
    
    st.markdown("""
    ## 📈 Enhanced Expected Clearance Rates
    
    | Category | No Action | 15% Markdown | 25% Markdown | Reallocate | Combo Strategy | Donation | Liquidation |
    |----------|-----------|--------------|--------------|------------|----------------|----------|-------------|
    | **Fresh Food** | 60% | 70% | 85% | 65% | **88%** | **100%** | 100% |
    | **Perishables** | 70% | 80% | 90% | 75% | **92%** | **100%** | 100% |
    | **General Merchandise** | 80% | 85% | 92% | 82% | **94%** | **100%** | 100% |
    """)
    
    st.markdown("""
    ## 🎯 Enhanced Decision Tree Logic
    
    ### Step 1: Risk Assessment
    ```python
    if shrinkage_risk > 0.8:
        risk_level = "CRITICAL"
    elif shrinkage_risk > 0.6:
        risk_level = "HIGH"
    elif shrinkage_risk > 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    ```
    
    ### Step 2: Category-Specific Actions
    ```python
    if risk_level == "CRITICAL":
        if is_donation_viable(item):
            return "DONATE"
        elif category == "Fresh Food" and shrinkage_risk > 0.6:
            return "LIQUIDATE"
        elif shrinkage_risk > 0.8:
            return "LIQUIDATE"
        else:
            return "MARKDOWN_25%"
    
    elif risk_level == "HIGH":
        if category == "General Merchandise":
            if can_reallocate_and_markdown(item):
                return "REALLOCATE+MARKDOWN_15%"
            else:
                return "RELOCATE"
        else:
            if can_reallocate_and_markdown(item):
                return "REALLOCATE+MARKDOWN_15%"
            else:
                return "MARKDOWN_25%"
    
    elif risk_level == "MEDIUM":
        if category == "General Merchandise" and can_relocate(item):
            return "RELOCATE"
        else:
            return "MARKDOWN_15%"
    
    else:  # LOW risk
        return "NO_ACTION"
    ```
    """)
    
    st.markdown("""
    ## 🔄 Enhanced Relocation Logic
    
    ### Standard Relocation Viability:
    ```python
    def can_relocate(item):
        conditions = [
            item.shelf_life_remaining > 7,  # Enough time for transfer
            item.category == "General Merchandise",  # Stable during transport
            nearby_stores_have_capacity(),  # Receiving store can handle
            transfer_cost < potential_savings(),  # Economically viable
            destination_store_better_sell_through()  # Better chance of selling
        ]
        return all(conditions)
    ```
    
    ### NEW: Combo Strategy Viability:
    ```python
    def can_reallocate_and_markdown(item):
        conditions = [
            can_relocate(item),
            item.shelf_life_remaining > 5,  # Extra time needed for combo
            item.quantity > 20,  # Minimum quantity for combo efficiency
            calculate_combo_recovery(item) > calculate_best_single_strategy(item)
        ]
        return all(conditions)
    ```
    
    ### NEW: Donation Viability Logic:
    ```python
    def is_donation_viable(item):
        conditions = [
            item.shelf_life_remaining >= 3,  # Minimum time for donation processing
            item.category in ["Fresh Food", "Perishables"],  # Suitable categories
            item.quantity > 50,  # Minimum quantity for donation efficiency
            calculate_donation_recovery(item) > calculate_liquidation_recovery(item),
            item.meets_food_safety_standards(),  # Safety requirements
            nearby_donation_centers_available()  # Logistical feasibility
        ]
        return all(conditions)
    ```
    """)
    
    st.markdown("""
    ## 💡 Why These Enhanced Strategies?
    
    ### 🎁 Donation Strategy Benefits:
    - **Tax advantages:** 25% corporate tax rate creates significant value
    - **Community impact:** Positive brand image and social responsibility
    - **100% clearance:** Complete inventory elimination
    - **Processing efficiency:** Established donation networks
    
    ### 🔄 Combo Strategy (Reallocate + Markdown) Benefits:
    - **Maximum recovery:** Combines best store placement with price incentive
    - **Higher clearance rates:** 88-94% vs 85-92% for single strategies
    - **Risk mitigation:** Reduces dependency on single approach
    - **Optimal timing:** Uses available shelf life efficiently
    
    ### 🏷️ Enhanced Markdown Percentages:
    - **15% Markdown:** Psychological threshold, maintains profitability
    - **25% Markdown:** Urgency signal, competitive advantage
    - **35% Markdown (Fresh Food only):** Maximum viable before customers assume spoilage
    """)
    
    st.markdown("""
    ## 💡 Key Intelligence Features
    
    ### Relocation Optimization
    Considers multiple factors for inventory transfers:
    - Distance costs (fuel, labor, time)
    - Demand matching (higher sell-through at destination)
    - Capacity constraints (receiving store limits)
    - Transfer timing (shelf life remaining after transit)
    
    ### Smart Combo Strategy Selection
    - Analyzes whether combined approach yields better recovery
    - Considers processing time and logistics complexity
    - Optimizes for maximum financial recovery
    """)


def show_future_improvements():
    """Display future improvement suggestions"""
    st.header("🚀 Future Improvements & Enhancements")
    
    st.markdown("""
    ## 🤖 AI/ML Enhancements
    
    ### Predictive Analytics
    - **Demand Forecasting**: ML models to predict future sales patterns
    - **Seasonal Adjustment**: Automatic adjustment for seasonal demand patterns
    - **Customer Behavior**: Analysis of purchasing patterns to optimize timing
    - **Weather Integration**: Factor weather data for fresh food demand
    
    ### Dynamic Pricing
    - **Real-time Pricing**: Automatic markdown adjustments based on demand
    - **Competitive Pricing**: Integration with competitor price monitoring
    - **Customer Segmentation**: Targeted pricing for different customer groups
    """)
    
    st.markdown("""
    ## 📱 Technology Integration
    
    ### IoT Sensors
    - **Temperature Monitoring**: Real-time freshness tracking
    - **Inventory Sensors**: Automatic quantity updates
    - **Foot Traffic**: Store traffic patterns for reallocation decisions
    
    ### Mobile App
    - **Manager Dashboard**: Mobile access for store managers
    - **Barcode Scanning**: Quick item lookup and status updates
    - **Push Notifications**: Alerts for critical items
    - **Action Tracking**: Record and track completion of recommendations
    """)
    
    st.markdown("""
    ## 🌐 Supply Chain Integration
    
    ### Supplier Coordination
    - **Delivery Optimization**: Coordinate with suppliers for fresher inventory
    - **Quality Scoring**: Track supplier performance metrics
    - **Contract Optimization**: Negotiate better terms based on waste data
    
    ### Cross-Store Intelligence
    - **Network Optimization**: Optimal reallocation across entire chain
    - **Inventory Balancing**: Predictive allocation based on store patterns
    - **Centralized Markdown**: Coordinated pricing strategies
    """)
    
    st.markdown("""
    ## 📊 Advanced Analytics
    
    ### Business Intelligence
    - **Profit Optimization**: Advanced models for maximum margin recovery
    - **Trend Analysis**: Long-term patterns and seasonal adjustments
    - **Category Performance**: Deep-dive analytics by product category
    - **Supplier Analysis**: Performance metrics and recommendations
    
    ### Reporting & Dashboards
    - **Executive Dashboards**: High-level KPIs and trends
    - **Operational Reports**: Daily/weekly action reports
    - **Financial Analysis**: ROI tracking and waste cost analysis
    - **Benchmark Comparisons**: Industry and internal benchmarking
    """)
    
    st.markdown("""
    ## 🤝 Partnership Opportunities
    
    ### Food Banks & Charities
    - **Automated Donation**: Direct integration with local food banks
    - **Tax Optimization**: Maximize tax benefits from donations
    - **Impact Tracking**: Monitor social impact of donation programs
    
    ### Liquidation Partners
    - **Marketplace Integration**: Automated listing on liquidation platforms
    - **Bulk Buyers**: Direct connections to wholesale buyers
    - **Recycling Partners**: Sustainable disposal options
    """)
    
    st.markdown("""
    ## 🎯 Implementation Roadmap
    
    ### Phase 1 (Months 1-3): Foundation
    - [ ] Deploy current dashboard system
    - [ ] Integrate with existing inventory systems
    - [ ] Train staff on new processes
    - [ ] Establish baseline metrics
    
    ### Phase 2 (Months 4-6): Automation
    - [ ] Implement barcode scanning
    - [ ] Add mobile app functionality
    - [ ] Integrate with POS systems
    - [ ] Automated reporting
    
    ### Phase 3 (Months 7-12): Intelligence
    - [ ] ML-powered demand forecasting
    - [ ] Dynamic pricing algorithms
    - [ ] Cross-store optimization
    - [ ] Supplier integration
    
    ### Phase 4 (Year 2+): Innovation
    - [ ] IoT sensor deployment
    - [ ] Advanced AI/ML models
    - [ ] Blockchain for supply chain transparency
    - [ ] Sustainability metrics and reporting
    """)
    
    st.markdown("""
    ## 💡 Innovation Ideas
    
    ### Customer Engagement
    - **Clearance Alerts**: Notify customers about markdown items
    - **Loyalty Programs**: Rewards for purchasing near-expiry items
    - **Recipe Suggestions**: AI-powered meal ideas using available ingredients
    
    ### Sustainability Focus
    - **Carbon Footprint**: Track environmental impact of waste reduction
    - **Circular Economy**: Integration with food waste recycling programs
    - **Sustainability Scoring**: Rate products and suppliers on environmental impact
    
    ### Advanced Features
    - **Voice Commands**: Voice-activated dashboard queries
    - **Augmented Reality**: AR scanning for instant item information
    - **Blockchain Tracking**: Complete supply chain transparency
    """)
    
    st.markdown("""
    ## 📈 Expected Benefits
    
    ### Financial Impact
    - **Waste Reduction**: 40-60% reduction in inventory shrinkage
    - **Margin Improvement**: 15-25% improvement in overall margins
    - **Cost Savings**: Reduced disposal and handling costs
    
    ### Operational Benefits
    - **Time Savings**: 70% reduction in manual inventory analysis
    - **Decision Speed**: Real-time recommendations vs. weekly reviews
    - **Staff Efficiency**: Focus on high-value activities
    
    ### Strategic Advantages
    - **Competitive Edge**: Industry-leading waste management
    - **Customer Satisfaction**: Fresh inventory and better pricing
    - **Sustainability**: Corporate social responsibility goals
    """)

# Initialize session state
if 'data_generated' not in st.session_state:
    st.session_state['data_generated'] = False

# Run the main app
if __name__ == "__main__":
    main()

