# Shrink Sense Dashboard - Technical Documentation

This document provides a comprehensive explanation of the logic and algorithms behind the Shrink Sense Dashboard, an intelligent inventory shrinkage management system designed to optimize inventory decisions and maximize value recovery.

## 📋 Project Overview

The Shrink Sense Dashboard is a data-driven tool that helps retailers manage inventory at risk of expiration or poor sales performance. It analyzes inventory data to provide strategic recommendations for maximizing value recovery and minimizing losses.

### Core Problem

- **Challenge**: Products expire before selling → Direct profit loss
- **Solution**: Smart recommendations to recover maximum value before expiration
- **Available Strategies**: Liquidate, Reallocate, Markdown, Donate, or combinations of these strategies

### Key Price Components

- **Cost Basis**: The original cost of acquiring the product (what the retailer paid)
- **Selling Price**: The retail price at which the product is sold to customers
- **Margin**: The difference between selling price and cost basis

## 🔢 Risk Assessment Logic

### Risk Score Calculation

The system calculates a risk score (0-100%) for each inventory item based on two key factors:

```
Risk Score = (Time Urgency × 0.6) + (Sales Problem × 0.4)

Where:
- Time Urgency = 1 - (Days Remaining / Total Shelf Life)
- Sales Problem = 1 - Sale Through Rate
```

This formula gives more weight (60%) to the time factor (how close an item is to expiration) while still considering sales performance (40%).

### Risk Level Classification

Based on the calculated risk score, items are classified into risk levels:

- **LOW (0-40%)**: 7+ days to act
- **MEDIUM (41-60%)**: 3-7 days to act
- **HIGH (61-80%)**: 1-3 days to act
- **CRITICAL (81-100%)**: 0-24 hours to act

## 🎯 Decision Engine Logic

The decision engine determines the primary recommendation strategy based on risk level, product category, and other factors.

### Primary Strategy Selection

#### CRITICAL Risk (81-100%)

- **Fresh Food**: DONATE (if possible) or LIQUIDATE
- **Other categories**: LIQUIDATE

#### HIGH Risk (61-80%)

- **Fresh Food**: DONATE (if possible) or REALLOCATE+MARKDOWN or MARKDOWN
- **Other categories**: REALLOCATE+MARKDOWN or REALLOCATE or MARKDOWN

#### MEDIUM Risk (41-60%)

- **All categories**: REALLOCATE+MARKDOWN or REALLOCATE or MARKDOWN

#### LOW Risk (0-40%)

- **All categories**: NO ACTION (monitor)

### Secondary Options

The system also provides secondary recommendation options based on the primary strategy, giving users alternatives to consider.

### Donation Eligibility

Items are eligible for donation if they meet these criteria:

1. Must be Fresh Food or Perishables category
2. Must have at least 1 day remaining before expiration
3. Must have reasonable value (cost basis > $1)

## 🔄 Reallocation Logic

Reallocation involves moving inventory to stores with better sales potential for those items.

### Reallocation Viability Criteria

- Minimum 3 days remaining (to allow for transport time)
- Minimum 5 units quantity (for cost-effectiveness)
- Fresh Food items need minimum 2 days remaining

### Store Compatibility Matrix

- **Store_A (Urban)**: Accepts all categories (Fresh Food, Perishables, General Goods)
- **Store_B (Suburban)**: Accepts Perishables and General Goods only
- **Store_C (Rural)**: Accepts General Goods only

### Store Selection Priority

When multiple stores are compatible, the system prioritizes in this order:

1. Store_A (Urban)
2. Store_B (Suburban)
3. Store_C (Rural)

### Transport Cost Calculation

```
Base cost per unit: $0.50
```

Modified by:

- **Distance factors** between stores (1.2x - 1.5x multiplier)
- **Category factors** (Fresh Food: 1.5x, Perishables: 1.2x, General Goods: 1.0x)

```
Total cost = Base cost × Distance factor × Category factor × Quantity
```

### Expected Sell-Through Rates by Store

Each store has different expected sell-through rates by category:

- **Store_A (Urban)**:

  - Fresh Food: 85%
  - Perishables: 80%
  - General Goods: 75%
- **Store_B (Suburban)**:

  - Fresh Food: 70%
  - Perishables: 75%
  - General Goods: 80%
- **Store_C (Rural)**:

  - Fresh Food: 60%
  - Perishables: 65%
  - General Goods: 85%

## 💰 Financial Calculations

### Expected Recovery by Strategy

- **NO ACTION**:

  - Revenue from sold items at full price (Quantity × Sell-through rate × Selling price)
  - Plus salvage value for unsold items (10% of selling price)
- **REALLOCATE**:

  - 95% of selling price × Target store sell-through rate
  - Minus transport costs
- **MARKDOWN**:

  - Selling price × (1 - markdown percentage) × Quantity
- **REALLOCATE+MARKDOWN**:

  - Combined approach:
    - 70% of inventory: Reallocate (95% of selling price × Target store sell-through - transport costs)
    - 30% of inventory: Markdown (Selling price × (1 - markdown percentage))
- **DONATE**:

  - 30% of cost basis (tax deduction benefit)
- **LIQUIDATE**:

  - 30% of selling price

### Markdown Percentages

Markdown percentages are determined by risk score:

- CRITICAL risk (81-100%): 30% markdown
- HIGH risk (61-80%): 25% markdown
- MEDIUM risk (41-60%): 15% markdown
- LOW risk (0-40%): 0% markdown

### Potential Loss Calculation

Potential loss represents the cost basis of items that won't sell if no action is taken:

```
Potential Loss = Cost basis × Quantity × (1 - Sale through rate)
```

### Margin Impact Calculation

Margin impact shows the profitability of the recommended strategy:

```
Margin Impact = Expected Recovery - Total Cost
```

Where Total Cost includes:

- Cost basis × Quantity
- Plus transport costs for REALLOCATE and REALLOCATE+MARKDOWN strategies
  - For REALLOCATE+MARKDOWN, transport costs are applied to only 70% of inventory

### Profit Margin Percentage

```
Profit Margin % = ((Expected Recovery - Total Cost) / Expected Recovery) × 100
```

## 📊 Visualization Components

The dashboard includes several visualization components to help users understand the data:

1. **Risk Distribution Chart**: Bar chart showing count of items by risk level
2. **Recommendation Distribution Chart**: Pie chart showing distribution of primary recommendations
3. **Financial Impact Chart**: Bar chart comparing potential loss vs. expected recovery by recommendation
4. **Category Risk Heatmap**: Heatmap showing risk distribution across product categories

## 🔍 Key Decision Factors Summary

### Time Factor (60% weight)

- Days remaining vs. total shelf life
- Transport time requirements
- Processing time for different actions

### Sales Performance (40% weight)

- Current sale through rate
- Historical sales patterns
- Category-specific performance

### Category Considerations

- **Fresh Food**: Shortest timeline, donation eligible
- **Perishables**: Medium timeline, some donation eligible
- **General Goods**: Longest timeline, best reallocation candidates

## ⚡ Action Prioritization

1. **CRITICAL + Fresh Food**: Immediate donation/liquidation
2. **CRITICAL + Others**: Immediate liquidation
3. **HIGH risk items**: 1-3 day action window
4. **MEDIUM risk items**: 3-7 day action window
5. **LOW risk items**: Monitor and reassess

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Required packages: streamlit, pandas, numpy, plotly

### Installation

```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run main.py
```

## 📁 Project Structure

- **main.py**: Main application file with Streamlit dashboard
- **logic/**: Core business logic modules
  - **risk_calculator.py**: Risk score calculation
  - **decision_engine.py**: Recommendation strategy logic
  - **reallocation.py**: Store reallocation logic
  - **financial.py**: Financial calculations
- **data/**: Data handling modules
  - **sample_data.py**: Sample data generation
- **utils/**: Utility functions
  - **helpers.py**: Visualization and formatting helpers

## 🔮 Future Enhancements

- AI/ML-powered demand forecasting
- Dynamic pricing algorithms
- Mobile app for store managers
- Integration with IoT sensors for real-time monitoring
- Automated donation coordination with food banks
- Cross-store optimization for chain-wide inventory management
