# 🚀 **Shrink Sense Dashboard - Enhanced Logic with Donation & Combo Strategies**

## **🎯 Core Problem Being Solved** 
The dashboard addresses inventory shrinkage - when products expire, spoil, or become unsellable, causing direct financial losses. It provides intelligent recommendations to minimize these losses through: 
- **Markdown pricing** (discount products to sell faster) 
- **Inventory relocation** (move items to stores where they'll sell better) 
- **Donation programs** (tax benefits + community impact) - **NEW**
- **Combo strategies** (reallocation + markdown for maximum recovery) - **NEW**
- **Liquidation** (sell to third parties when other options fail) 

## **🔄 Complete Workflow Example** 
### **Scenario: Fresh Food Item at Store A** 
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

**Action Execution:** 
- Manager clicks "Apply Markdown" 
- System generates markdown instructions 
- Tracks implementation and results 

## **💡 Key Intelligence Features**  
### **Relocation Optimization** 
Considers multiple factors for inventory transfers: 
- Distance costs (fuel, labor, time) 
- Demand matching (higher sell-through at destination) 
- Capacity constraints (receiving store limits) 
- Transfer timing (shelf life remaining after transit) 

---

## **📊 Core Risk Assessment Formula** 
### **Primary Risk Calculation** 
```python
# Time Risk: How close is the item to expiration? 
time_risk = inventory_age_days / shelf_life_days 

# Sales Risk: How poorly is it selling? 
sales_risk = 1 - sell_through_rate 

# Combined Shrinkage Risk (weighted formula) 
shrinkage_risk = (0.7 × time_risk) + (0.3 × sales_risk) 
```

### **Why This Formula?** 
- **70% weight on time** - Expiration is absolute, sales can improve 
- **30% weight on sales** - Poor performers need earlier intervention 
- **Scale 0-1** - Easy to understand and set thresholds

---

## **🏷️ Enhanced Category-Specific Rules** 

### **Fresh Food (1-7 days shelf life)** 
**Business Logic:** Extremely perishable, customer safety critical 

| Risk Level | Shrinkage Risk | Action | Reasoning |
|------------|----------------|--------|-----------|
| **Critical** | >60% | **DONATION** (if viable) or **LIQUIDATE** | Tax benefit better than total loss |
| **High** | 40-60% | **REALLOCATE+MARKDOWN** or **MARKDOWN 25%** | Combo strategy for maximum recovery |
| **Medium** | 20-40% | **MARKDOWN 15%** | Light discount for acceleration |
| **Low** | <20% | **NO ACTION** | Natural turnover sufficient |

**Key Thresholds:** 
- **Donation priority** at 60% - tax benefits + community impact
- **Combo strategy** for high-risk items with viable stores
- **Maximum 35% markdown** - beyond this, customers assume spoilage 
- **Emergency processing** - decisions needed within hours 

### **Perishables (3-14 days shelf life)** 
**Business Logic:** Moderate shelf life, quality degrades visibly 

| Risk Level | Shrinkage Risk | Action | Reasoning |
|------------|----------------|--------|-----------|
| **Critical** | >80% | **DONATION** (if viable) or **LIQUIDATE** | Recovery better than total loss |
| **High** | 60-80% | **REALLOCATE+MARKDOWN** or **MARKDOWN 25%** | Significant discount drives urgency |
| **Medium** | 40-60% | **REALLOCATE** or **MARKDOWN 15%** | Modest discount clears inventory |
| **Low** | <40% | **NO ACTION** | Time for natural sales or relocation |

**Key Thresholds:** 
- **Liquidation at 80%** - standard high-risk threshold 
- **Relocation preferred** - more time available for transfers 
- **Maximum 25% markdown** - maintains perceived quality 

### **General Merchandise (30-365 days shelf life)** 
**Business Logic:** Long shelf life, appearance doesn't degrade 

| Risk Level | Shrinkage Risk | Action | Reasoning |
|------------|----------------|--------|-----------|
| **Critical** | >80% | **DONATION** (if viable) or **LIQUIDATE** | Last resort for slow movers |
| **High** | 60-80% | **REALLOCATE+MARKDOWN** or **RELOCATE** | Time available for better placement |
| **Medium** | 40-60% | **REALLOCATE** or **MARKDOWN 15%** | Conservative discount maintains margin |
| **Low** | <40% | **NO ACTION** | Plenty of time for natural sales |

**Key Thresholds:** 
- **Relocation first** - time allows for strategic placement 
- **Conservative markdowns** - maintains brand value 
- **Maximum 15% markdown** - higher discounts signal clearance 

---

## **💰 Enhanced Financial Impact Calculations** 
### **Revenue Recovery Formulas** 
```python
# Current inventory value 
current_value = quantity × current_price 

# Markdown scenario 
markdown_price = current_price × (1 - markdown_percentage) 
markdown_revenue = quantity × markdown_price  
markdown_shrinkage = quantity × current_price – markdown_revenue 

# Liquidation scenario 
liquidation_revenue = quantity × current_price × 0.30  # 30% recovery 
liquidation_shrinkage = quantity × current_price × 0.70  # 70% loss 

# No action scenario (if high risk) 
no_action_shrinkage = quantity × current_price × shrinkage_risk 
```

### **NEW: Donation Recovery Formula**
```python
# Donation scenario
fair_market_value = quantity × current_price
tax_benefit = fair_market_value × 0.25  # 25% corporate tax rate
processing_cost = quantity × 0.50  # $0.50 per unit processing cost
donation_net_benefit = tax_benefit - processing_cost
donation_recovery = max(donation_net_benefit, 0)  # Cannot be negative
```

### **NEW: Reallocation + Markdown Recovery Formula**
```python
# Combo strategy: Reallocate + Markdown
target_store_sell_through = 0.75  # Better performing store
combo_sell_through = target_store_sell_through × 1.2  # 20% boost from markdown
markdown_price = current_price × (1 - markdown_percentage)
transfer_cost = quantity × 0.25  # $0.25 per unit transfer cost

# Revenue calculation
sold_quantity = quantity × min(combo_sell_through, 0.95)  # Cap at 95%
revenue = sold_quantity × markdown_price
unsold_quantity = quantity - sold_quantity
salvage_value = unsold_quantity × markdown_price × 0.10

combo_recovery = revenue + salvage_value - transfer_cost
```

### **Enhanced Expected Clearance Rates** 

| Category | No Action | 15% Markdown | 25% Markdown | Reallocate | Combo Strategy | Donation | Liquidation |
|----------|-----------|--------------|--------------|------------|----------------|----------|-------------|
| **Fresh Food** | 60% | 70% | 85% | 65% | **88%** | **100%** | 100% |
| **Perishables** | 70% | 80% | 90% | 75% | **92%** | **100%** | 100% |
| **General Merchandise** | 80% | 85% | 92% | 82% | **94%** | **100%** | 100% |

---

## **🎯 Enhanced Decision Tree Logic** 

### **Step 1: Risk Assessment** 
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

### **Step 2: Enhanced Category-Specific Actions** 
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
            return "RELOCATE"  # Time available for better placement 
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

### **Step 3: Enhanced Relocation Logic** 
```python
def can_relocate(item): 
    # Check if relocation is viable 
    conditions = [ 
        item.shelf_life_remaining > 7,  # Enough time for transfer 
        item.category == "General Merchandise",  # Stable during transport 
        nearby_stores_have_capacity(),  # Receiving store can handle 
        transfer_cost < potential_savings(),  # Economically viable 
        destination_store_better_sell_through()  # Better chance of selling 
    ] 
    return all(conditions) 

def can_reallocate_and_markdown(item):
    # Check if combo strategy is viable
    conditions = [
        can_relocate(item),
        item.shelf_life_remaining > 5,  # Extra time needed for combo
        item.quantity > 20,  # Minimum quantity for combo efficiency
        calculate_combo_recovery(item) > calculate_best_single_strategy(item)
    ]
    return all(conditions)
```

### **NEW: Step 4: Donation Viability Logic**
```python
def is_donation_viable(item):
    # Check if donation is viable and beneficial
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

---

## **📊 Why These Enhanced Strategies?** 

### **Donation Strategy Benefits:**
- **Tax advantages:** 25% corporate tax rate creates significant value
- **Community impact:** Positive brand image and social responsibility
- **100% clearance:** Complete inventory elimination
- **Processing efficiency:** Established donation networks

### **Combo Strategy (Reallocate + Markdown) Benefits:**
- **Maximum recovery:** Combines best store placement with price incentive
- **Higher clearance rates:** 88-94% vs 85-92% for single strategies
- **Risk mitigation:** Reduces dependency on single approach
- **Optimal timing:** Uses available shelf life efficiently

### **Enhanced Markdown Percentages:**
- **15% Markdown:** 
  - Psychological threshold: Customers notice but don't assume problems 
  - Margin protection: Maintains reasonable profitability 
  - Clearing power: Sufficient to accelerate sales 20-30% 

- **25% Markdown:** 
  - Urgency signal: Customers understand time-sensitive nature 
  - Competitive advantage: Undercuts competitor pricing 
  - Fast clearance: Moves 85-90% of inventory quickly 

- **35% Markdown (Fresh Food only):** 
  - Maximum viable: Beyond this, customers assume spoilage 
  - Emergency clearance: Last attempt before liquidation 
  - Cost recovery: Better than 100% loss 
