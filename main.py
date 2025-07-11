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
    st.header("📝 Understanding Inventory Shrinkage")
    
    # Introduction section
    st.markdown("""
    ## 🔍 What is Inventory Shrinkage?
    
    **Inventory shrinkage** refers to the loss of inventory that can be attributed to factors such as:
    - Product expiration
    - Spoilage
    - Poor sales performance
    - Theft or damage
    
    This dashboard focuses specifically on **time-sensitive inventory** that risks expiration or markdown due to poor sales performance.
    """)
    
    # Problem visualization
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## 💸 The Financial Impact
        
        When products expire or must be heavily discounted, retailers face significant financial losses:
        
        - **Direct Cost Loss**: The original cost of acquiring the product is lost
        - **Lost Margin**: The potential profit from selling at full price is never realized
        - **Disposal Costs**: Additional costs to remove and dispose of expired products
        - **Opportunity Cost**: Shelf space that could have been used for better-selling items
        
        According to industry research, retailers lose billions annually to preventable inventory shrinkage.
        """)
    
    with col2:
        # Financial impact visualization
        data = {
            'Category': ['Direct Cost', 'Lost Margin', 'Disposal', 'Opportunity'],
            'Impact': [40, 30, 15, 15]
        }
        fig = px.pie(data, values='Impact', names='Category', title='Financial Impact Breakdown',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # The challenge
    st.markdown("""
    ## ⚠️ The Challenge
    
    Retailers face a complex decision-making process when dealing with at-risk inventory:
    """)
    
    # Challenge visualization with timeline
    challenge_data = {
        'Stage': ['Early Warning', 'Decision Point', 'Action Window', 'Expiration'],
        'Days': [10, 7, 3, 0],
        'Options': [4, 3, 2, 1],
        'Recovery': [95, 70, 40, 10]
    }
    
    fig = go.Figure()
    
    # Add lines
    fig.add_trace(go.Scatter(
        x=challenge_data['Days'],
        y=challenge_data['Recovery'],
        mode='lines+markers',
        name='Value Recovery %',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    
    # Add annotations
    for i, stage in enumerate(challenge_data['Stage']):
        fig.add_annotation(
            x=challenge_data['Days'][i],
            y=challenge_data['Recovery'][i] + 5,
            text=stage,
            showarrow=False,
            font=dict(size=12)
        )
    
    fig.update_layout(
        title='Value Recovery Timeline',
        xaxis_title='Days Until Expiration',
        yaxis_title='Potential Value Recovery (%)',
        height=400,
        xaxis=dict(zeroline=False),
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Solution approach
    st.markdown("""
    ## 🎯 The Solution Approach
    
    The **Shrink Sense Dashboard** addresses this challenge through a systematic approach:
    
    1. **Risk Assessment**: Evaluate each item's risk level based on time and sales factors
    2. **Strategic Recommendations**: Generate optimal strategies based on risk level and product attributes
    3. **Financial Impact Analysis**: Calculate expected recovery and margin impact for each recommendation
    4. **Actionable Insights**: Provide clear, prioritized actions for inventory managers
    """)
    
    # Solution visualization
    solution_data = {
        'Strategy': ['No Action', 'Markdown', 'Reallocate', 'Reallocate+Markdown', 'Donate', 'Liquidate'],
        'Recovery': [60, 75, 85, 80, 30, 30],
        'Risk': ['Low', 'Medium', 'Medium', 'High', 'High', 'Critical']
    }
    
    risk_colors = {
        'Low': '#d4edda',
        'Medium': '#fff3cd',
        'High': '#f8d7da',
        'Critical': '#f5c6cb'
    }
    
    fig = px.bar(
        solution_data, 
        x='Strategy', 
        y='Recovery',
        color='Risk',
        title='Value Recovery by Strategy',
        color_discrete_map=risk_colors,
        text='Recovery'
    )
    
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Business value
    st.markdown("""
    ## 💰 Business Value
    
    Implementing an intelligent inventory management system like Shrink Sense can deliver significant business value:
    
    - **Reduce Waste**: 40-60% reduction in expired/wasted inventory
    - **Improve Margins**: 15-25% improvement in overall margins on at-risk items
    - **Optimize Operations**: Save 5-10 hours per week in manual inventory analysis
    - **Enhance Sustainability**: Reduce environmental impact through better inventory management
    
    By taking a data-driven approach to inventory shrinkage, retailers can transform a significant cost center into an opportunity for optimization and improved profitability.
    """)
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
    ## 📋 Problem Statement
    
    **Challenge**: Products expire before selling → Direct profit loss
    **Solution**: Smart recommendations to recover maximum value before expiration
    **Options**: Liquidate, Reallocate, Markdown, Donate (can combine strategies)
    """)
    
    st.markdown("""
    ## 🔢 Risk Calculation Logic
    
    ### Risk Score Formula:
    ```
    Risk Score = (Time Urgency × 0.6) + (Sales Problem × 0.4)
    
    Where:
    - Time Urgency = 1 - (Days Remaining / Total Shelf Life)
    - Sales Problem = 1 - Sale Through Rate
    ```
    
    ### Risk Levels:
    - **LOW (0-40%)**: 7+ days to act
    - **MEDIUM (41-60%)**: 3-7 days to act  
    - **HIGH (61-80%)**: 1-3 days to act
    - **CRITICAL (81-100%)**: 0-24 hours to act
    """)
    
    st.markdown("""
    ## 🎯 Decision Logic
    
    ### Primary Strategy Selection:
    
    **CRITICAL Risk (81-100%)**
    - Fresh Food → DONATE (if possible) or LIQUIDATE
    - Other categories → LIQUIDATE
    
    **HIGH Risk (61-80%)**
    - Fresh Food → DONATE (if possible) or REALLOCATE+MARKDOWN or MARKDOWN
    - Other categories → REALLOCATE+MARKDOWN or REALLOCATE or MARKDOWN
    
    **MEDIUM Risk (41-60%)**
    - All categories → REALLOCATE+MARKDOWN or REALLOCATE or MARKDOWN
    
    **LOW Risk (0-40%)**
    - All categories → NO ACTION (monitor)
    """)
    
    st.markdown("""
    ## 🔄 Reallocation Logic
    
    ### Viability Criteria:
    - Minimum 3 days remaining (transport time)
    - Minimum 5 units quantity (cost-effective)
    - Fresh Food needs minimum 2 days
    
    ### Store Compatibility:
    - **Store_A (Urban)**: Accepts all categories
    - **Store_B (Suburban)**: General Goods + Perishables
    - **Store_C (Rural)**: General Goods only
    
    ### Cost Calculation:
    - Base cost: $0.50 per unit
    - Distance factor: 1.2x multiplier
    - Total cost deducted from expected recovery
    """)
    
    st.markdown("""
    ## 💰 Financial Calculations
    
    ### Expected Recovery by Strategy:
    - **NO ACTION**: Full selling price (if sold)
    - **REALLOCATE**: 95% of selling price - transport costs
    - **MARKDOWN**: Selling price × (1 - markdown percentage)
    - **REALLOCATE+MARKDOWN**: Combined approach (70% reallocated, 30% markdown)
    - **DONATE**: 30% of cost basis (tax deduction)
    - **LIQUIDATE**: 30% of selling price
    
    ### Markdown Percentages:
    - CRITICAL risk: 30% markdown
    - HIGH risk: 25% markdown
    - MEDIUM risk: 15% markdown
    - LOW risk: 0% markdown
    """)
    
    st.markdown("""
    ## 🔍 Key Decision Factors
    
    ### Time Factor (60% weight):
    - Days remaining vs. total shelf life
    - Transport time requirements
    - Processing time for different actions
    
    ### Sales Performance (40% weight):
    - Current sale through rate
    - Historical sales patterns
    - Category-specific performance
    
    ### Category Considerations:
    - **Fresh Food**: Shortest timeline, donation eligible
    - **Perishables**: Medium timeline, some donation eligible
    - **General Goods**: Longest timeline, best reallocation candidates
    """)
    
    st.markdown("""
    ## ⚡ Action Prioritization
    
    1. **CRITICAL + Fresh Food**: Immediate donation/liquidation
    2. **CRITICAL + Others**: Immediate liquidation
    3. **HIGH risk items**: 1-3 day action window
    4. **MEDIUM risk items**: 3-7 day action window
    5. **LOW risk items**: Monitor and reassess
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

