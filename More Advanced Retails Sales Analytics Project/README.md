# Retail Sales Analytics: Customer Behavior, Product Performance & Revenue Optimization

## Project Overview

This project demonstrates comprehensive end-to-end retail analytics for a multi-channel retail company. The analysis covers 500,000+ transactions across 100+ stores, 5,000+ SKUs, 50+ product categories, and 200,000+ customers over 12 months. The system tracks sales performance, customer behavior, inventory management, promotional effectiveness, and revenue forecasting with advanced dashboards and interactive visualizations.

## Business Context

**Challenge**: Retail companies struggling with inventory optimization, customer churn, promotional ROI visibility, and accurate sales forecasting across multiple channels and locations.

**Solution**: Integrated retail analytics platform tracking transaction-level data, customer lifetime value, product performance, store efficiency, promotional impact, and demand forecasting with real-time dashboards and predictive models.

## Datasets

### 1. Store Master Data (100 stores)
- Store ID, store name, location, region
- Store type (flagship, regional, outlet)
- Store size (sq ft), opening date
- Manager, contact details
- Revenue target, profitability tier

### 2. Customer Master (200,000 customers)
- Customer ID, name, contact information
- Membership type (gold, silver, bronze, non-member)
- First purchase date, last purchase date
- Total lifetime value
- Preferred payment method
- Email preferences, location

### 3. Product Catalog (5,000 SKUs)
- SKU ID, product name, category
- Sub-category, brand, supplier
- Cost price, MRP, discount allowed
- Stock level, reorder point
- Product tier (economy, standard, premium)

### 4. Transaction Data (500,000 transactions)
- Transaction ID, date, time
- Store ID, customer ID
- SKU ID, quantity sold, price, discount
- Payment method, transaction amount
- Category, loyalty points earned
- Return status (if applicable)

### 5. Inventory Data (50,000 records)
- Date, store ID, SKU ID
- Opening stock, purchases, sales
- Closing stock, stock-outs
- Reorder status, lead time

### 6. Promotions & Campaigns (500+ promotions)
- Promotion ID, start date, end date
- Discount percentage, promotion type
- SKU covered, stores covered
- Budget, actual spend
- Sales lift %, ROI

### 7. Customer Engagement (100,000 records)
- Customer ID, email opens, email clicks
- Website visits, app downloads
- Social media follows, reviews
- Loyalty program points earned/redeemed
- Last engagement date

## Key Features

### Advanced SQL Queries Included

1. **Sales Performance Analysis**
   - Revenue by store, category, SKU with trends
   - Top and bottom performing products
   - Sales growth month-over-month
   - Store efficiency ranking

2. **Customer Analytics**
   - Customer lifetime value by segment
   - Purchase frequency and recency analysis
   - Churn prediction and retention analysis
   - RFM segmentation (Recency, Frequency, Monetary)

3. **Inventory Management**
   - Stock turnover ratio by category
   - Inventory aging analysis
   - Stock-out frequency and impact
   - Reorder optimization

4. **Promotional Effectiveness**
   - Campaign ROI analysis
   - Lift analysis (with vs without promotion)
   - Discount elasticity
   - Best and worst performing campaigns

5. **Revenue Forecasting**
   - Daily/weekly/monthly sales forecast
   - Seasonal decomposition
   - Trend analysis with confidence intervals
   - Store-level forecasting

### Advanced SQL Query Examples

```sql
-- Customer Lifetime Value with RFM Segmentation
SELECT 
    c.customer_id,
    c.customer_name,
    c.membership_type,
    MAX(t.transaction_date) as last_purchase_date,
    COUNT(DISTINCT t.transaction_id) as purchase_frequency,
    DATEDIFF(day, MAX(t.transaction_date), GETDATE()) as days_since_purchase,
    SUM(t.transaction_amount) as total_spend,
    ROUND(AVG(t.transaction_amount), 2) as avg_transaction_value,
    SUM(t.transaction_amount) - (SELECT SUM(p.cost_price * t.quantity) 
                                  FROM products p WHERE t.sku_id = p.sku_id) as gross_profit,
    NTILE(5) OVER (ORDER BY SUM(t.transaction_amount) DESC) as monetary_quintile,
    NTILE(5) OVER (ORDER BY COUNT(DISTINCT t.transaction_id) DESC) as frequency_quintile,
    NTILE(5) OVER (ORDER BY DATEDIFF(day, MAX(t.transaction_date), GETDATE())) as recency_quintile
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.customer_name, c.membership_type;

-- Store Performance with Rank and Running Total
SELECT 
    s.store_id,
    s.store_name,
    s.region,
    SUM(t.transaction_amount) as total_revenue,
    COUNT(DISTINCT t.transaction_id) as total_transactions,
    COUNT(DISTINCT t.customer_id) as unique_customers,
    ROUND(AVG(t.transaction_amount), 2) as avg_transaction_value,
    SUM(t.quantity) as total_units_sold,
    ROUND(SUM(t.transaction_amount) / s.revenue_target * 100, 2) as target_achievement_pct,
    RANK() OVER (ORDER BY SUM(t.transaction_amount) DESC) as revenue_rank,
    DENSE_RANK() OVER (PARTITION BY s.region ORDER BY SUM(t.transaction_amount) DESC) as region_rank,
    SUM(SUM(t.transaction_amount)) OVER (ORDER BY s.store_id) as cumulative_revenue,
    ROUND(100.0 * SUM(t.transaction_amount) / SUM(SUM(t.transaction_amount)) OVER (), 2) as revenue_contribution_pct
FROM stores s
LEFT JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.store_id, s.store_name, s.region, s.revenue_target
ORDER BY total_revenue DESC;

-- Product Performance with Category Benchmarking
SELECT 
    p.sku_id,
    p.product_name,
    p.category,
    SUM(t.quantity) as units_sold,
    SUM(t.transaction_amount) as revenue,
    ROUND(AVG(t.transaction_amount / NULLIF(t.quantity, 0)), 2) as avg_price_per_unit,
    COUNT(DISTINCT t.store_id) as stores_sold,
    COUNT(DISTINCT t.customer_id) as unique_customers,
    ROUND(SUM(t.transaction_amount) / (p.cost_price * SUM(t.quantity)) - 1, 2) as margin_percentage,
    AVG(SUM(t.transaction_amount)) OVER (PARTITION BY p.category) as category_avg_revenue,
    ROUND(SUM(t.transaction_amount) / AVG(SUM(t.transaction_amount)) 
          OVER (PARTITION BY p.category), 2) as category_performance_index,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(t.transaction_amount) DESC) as category_rank
FROM products p
LEFT JOIN transactions t ON p.sku_id = t.sku_id
GROUP BY p.sku_id, p.product_name, p.category, p.cost_price
ORDER BY revenue DESC;

-- Promotional Campaign ROI Analysis
SELECT 
    pm.promotion_id,
    pm.promotion_type,
    pm.start_date,
    pm.end_date,
    COUNT(DISTINCT t.transaction_id) as promotional_transactions,
    SUM(CASE WHEN t.discount > 0 THEN t.transaction_amount ELSE 0 END) as promotional_revenue,
    SUM(CASE WHEN t.discount > 0 THEN t.quantity ELSE 0 END) as promotional_units_sold,
    ROUND(AVG(CASE WHEN t.discount > 0 THEN t.discount ELSE 0 END), 2) as avg_discount_given,
    SUM(CASE WHEN t.discount > 0 THEN (t.transaction_amount - (p.cost_price * t.quantity)) ELSE 0 END) as promotional_profit,
    pm.budget as promotion_budget,
    ROUND((SUM(CASE WHEN t.discount > 0 THEN (t.transaction_amount - (p.cost_price * t.quantity)) ELSE 0 END) - pm.budget) / 
          pm.budget * 100, 2) as roi_percentage,
    ROUND(((SUM(CASE WHEN t.discount > 0 THEN t.transaction_amount ELSE 0 END) / 
            COUNT(DISTINCT t.transaction_id)) - 
           (SELECT AVG(t2.transaction_amount) FROM transactions t2 
            WHERE t2.transaction_date < pm.start_date AND 
                  t2.sku_id IN (SELECT sku_id FROM promotion_items WHERE promotion_id = pm.promotion_id))) / 
          (SELECT AVG(t2.transaction_amount) FROM transactions t2 
           WHERE t2.transaction_date < pm.start_date AND 
                 t2.sku_id IN (SELECT sku_id FROM promotion_items WHERE promotion_id = pm.promotion_id)) * 100, 2) 
    as sales_lift_percentage
FROM promotions pm
LEFT JOIN transactions t ON t.transaction_date BETWEEN pm.start_date AND pm.end_date
LEFT JOIN products p ON t.sku_id = p.sku_id
GROUP BY pm.promotion_id, pm.promotion_type, pm.start_date, pm.end_date, pm.budget
ORDER BY roi_percentage DESC;

-- Sales Forecast with Seasonal Decomposition
SELECT 
    CAST(transaction_date as DATE) as sales_date,
    SUM(transaction_amount) as daily_revenue,
    AVG(SUM(transaction_amount)) OVER (ORDER BY CAST(transaction_date as DATE) 
                                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day,
    AVG(SUM(transaction_amount)) OVER (ORDER BY CAST(transaction_date as DATE) 
                                        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as moving_avg_30day,
    STDDEV(SUM(transaction_amount)) OVER () as revenue_stddev,
    (AVG(SUM(transaction_amount)) OVER (ORDER BY CAST(transaction_date as DATE) 
                                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)) + 
    (STDDEV(SUM(transaction_amount)) OVER () * 1.96) as forecast_upper_bound,
    (AVG(SUM(transaction_amount)) OVER (ORDER BY CAST(transaction_date as DATE) 
                                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)) - 
    (STDDEV(SUM(transaction_amount)) OVER () * 1.96) as forecast_lower_bound,
    CASE WHEN DATEPART(quarter, transaction_date) = 4 THEN 'Q4 - Peak Season'
         WHEN DATEPART(quarter, transaction_date) = 3 THEN 'Q3 - Pre-Festive'
         ELSE 'Regular' END as seasonal_pattern
FROM transactions
GROUP BY CAST(transaction_date as DATE)
ORDER BY sales_date DESC;
```

### Advanced Visualizations Included

1. **Sales Performance Dashboard**
   - Revenue trend (line chart with forecast)
   - Store-wise revenue comparison (horizontal bar chart)
   - Category performance matrix (bubble chart)
   - Top 10 products (ranked bar chart)

2. **Customer Analytics Dashboard**
   - RFM segmentation (3D scatter plot)
   - Customer lifetime value distribution (histogram)
   - Purchase frequency vs average order value (scatter)
   - Churn rate by segment (gauge charts)

3. **Inventory Dashboard**
   - Stock turnover by category (heatmap)
   - Inventory aging (Pareto chart)
   - Stock-out impact analysis (waterfall chart)
   - Reorder optimization (recommendation engine)

4. **Promotional Analytics Dashboard**
   - Campaign ROI comparison (grouped bar chart)
   - Discount elasticity curve (regression plot)
   - Category lift analysis (funnel chart)
   - Best and worst campaigns (ranked table)

5. **Store Efficiency Dashboard**
   - Store performance scorecard (KPI gauges)
   - Revenue per sq ft (bench marking)
   - Customer acquisition cost by store (heat map)
   - Store profitability matrix (quadrant plot)

6. **Executive Summary Dashboard**
   - Key metrics (KPI tiles)
   - YoY growth comparison (dual-axis bar chart)
   - Region performance (geographic map)
   - Forecast accuracy (line chart with actual vs forecast)

### Advanced Excel Features

1. **Dynamic Dashboards**
   - Slicer-based filtering across all sheets
   - Real-time KPI updates
   - Conditional formatting for quick insights
   - Sparklines for trend visualization

2. **Complex Formulas**
   - SUMIFS, COUNTIFS for multi-dimensional analysis
   - INDEX/MATCH for dynamic lookups
   - FORECAST functions for trend projection
   - Array formulas for RFM segmentation

3. **Data Models**
   - Relationships between customers, transactions, products
   - Calculated fields for derived metrics
   - Aggregations at multiple hierarchy levels

## Files Included

### Data Files (Generated)
- `stores.csv` - 100 store master records
- `customers.csv` - 200,000 customer records
- `products.csv` - 5,000 SKU catalog
- `transactions.csv` - 500,000 transaction records (50+ MB)
- `inventory.csv` - 50,000 inventory records
- `promotions.csv` - 500+ promotion records
- `customer_engagement.csv` - 100,000 engagement records

### SQL Scripts
- `retail_analytics_queries.sql` - 10+ complex queries
  - Customer lifetime value analysis
  - Store performance ranking
  - Product performance with benchmarking
  - Promotional ROI analysis
  - Sales forecasting with confidence intervals

### Excel Workbooks
- `retail_analytics_dashboard.xlsx` - Interactive dashboard
  - Executive KPI summary
  - Sales performance analysis
  - Customer segmentation
  - Inventory management
  - Promotional effectiveness

### Python Analytics
- `generate_retail_data.py` - Data generation script
- `retail_analytics.py` - Analysis and computation
- `dashboard_generator.py` - Interactive dashboard creation

### HTML/Interactive Dashboards
- `sales_dashboard.html` - Interactive sales analytics
- `customer_dashboard.html` - Customer lifetime value analysis
- `store_dashboard.html` - Store performance tracking
- `inventory_dashboard.html` - Inventory optimization
- `promotional_dashboard.html` - Campaign ROI analysis
- `forecast_dashboard.html` - Sales forecasting
- `executive_summary.html` - KPI dashboard

## Key Metrics Tracked

### Sales Metrics
- Total annual revenue: INR 500+ crores
- Average transaction value: INR 2,500-3,500
- Same-store sales growth: 8-12% YoY
- Revenue per store per day: INR 5-8 lakhs
- Category mix: Apparel 40%, Electronics 35%, Home 25%

### Customer Metrics
- Total customers: 200,000
- Active customers (last 90 days): 120,000
- Customer retention rate: 65-70%
- Average customer lifetime value: INR 50,000-100,000
- Purchase frequency: 4-6 times per year

### Inventory Metrics
- Inventory turnover: 8-12x per year
- Stock-out frequency: <2%
- Days inventory outstanding: 30-45 days
- Carrying cost as % of inventory value: 15-20%
- Forecast accuracy: 80-85%

### Promotional Metrics
- Average promotional discount: 15-25%
- Promotion frequency: 4-6 per category per year
- Average campaign ROI: 200-300%
- Sales lift during promotions: 30-50%
- Customer acquisition cost: INR 500-1,500

### Store Performance Metrics
- Average store profitability margin: 12-18%
- Revenue per sq ft: INR 1,500-2,500
- Customer footfall per day: 200-500 customers
- Conversion rate: 8-12%
- Average items per transaction: 3-4 items

## Project Structure

```
retail_sales_analytics_project/
|-- README.md (this file)
|-- GITHUB_UPLOAD_GUIDE.md
|-- LICENSE
|-- requirements.txt
|-- .gitignore
|
|-- Data/
|   |-- stores.csv
|   |-- customers.csv
|   |-- products.csv
|   |-- transactions.csv (500K records)
|   |-- inventory.csv
|   |-- promotions.csv
|   |-- customer_engagement.csv
|
|-- SQL/
|   |-- retail_analytics_queries.sql (10+ queries)
|
|-- Excel/
|   |-- retail_analytics_dashboard.xlsx
|
|-- Python/
|   |-- generate_retail_data.py
|   |-- retail_analytics.py
|   |-- dashboard_generator.py
|
|-- Dashboards/
|   |-- sales_dashboard.html
|   |-- customer_dashboard.html
|   |-- store_dashboard.html
|   |-- inventory_dashboard.html
|   |-- promotional_dashboard.html
|   |-- forecast_dashboard.html
|   |-- executive_summary.html
```

## Installation and Setup

### Requirements

```bash
pip install pandas numpy scipy matplotlib seaborn plotly openpyxl xlsxwriter
```

### How to Run

#### Step 1: Generate Retail Data
```bash
python generate_retail_data.py
```
Generates all 7 CSV files with 500K+ transaction records.

#### Step 2: Load to SQL
```bash
# Import CSVs to your SQL database
# Run retail_analytics_queries.sql to execute all queries
```

#### Step 3: Open Excel Dashboard
```bash
# Open retail_analytics_dashboard.xlsx
# Refresh data and interact with slicers
```

#### Step 4: View HTML Dashboards
```bash
# Open any .html file in browser
# Explore interactive visualizations
```

## Key Insights (Example Output)

### Sales Insights
- Top performing store: Store-25 (INR 1.2 crore annual revenue)
- Highest performing category: Apparel (40% of total revenue)
- Top SKU: Premium Jeans (INR 5 crore annual revenue)
- Average store growth: 9.5% YoY
- Q4 revenue: 35% of annual revenue (seasonal peak)

### Customer Insights
- High-value segment: 5% of customers, 40% of revenue
- Customer acquisition cost declining: 12% YoY
- Repeat purchase rate: 68% (above industry average)
- Churn rate by segment: High-value 5%, Regular 15%
- Email engagement rate: 25% (opens), 8% (clicks)

### Inventory Insights
- Fastest moving category: Apparel (12x turnover)
- Slowest moving category: Home (6x turnover)
- Stock-out impact: INR 2-3 crore lost annual revenue
- Excess inventory: 15% of inventory value (overstocked items)
- Forecast accuracy: 83% MAPE

### Promotional Insights
- Best performing campaign: Summer Sale (450% ROI)
- Worst performing campaign: Clearance Sale (80% ROI)
- Optimal discount level: 20-25% (elasticity sweet spot)
- Category lift variance: Apparel 45%, Electronics 35%, Home 25%
- Campaign frequency impact: Diminishing returns after 5 per year

## Recommendations

1. **Optimize Store Portfolio**: Focus on top 20 stores; invest in underperforming stores
2. **Customer Retention**: Implement loyalty program targeting high-value repeat customers
3. **Inventory Optimization**: Reduce excess inventory by 10-15%; improve forecast accuracy
4. **Promotional Strategy**: Focus on 4-5 high-impact campaigns per category
5. **Omnichannel Integration**: Integrate online and offline sales data for unified view
6. **Dynamic Pricing**: Implement AI-based pricing based on demand and inventory levels
7. **Store Efficiency**: Improve revenue per sq ft by 15-20% through category optimization

## Technical Stack

- **Data Generation**: Python (Pandas, NumPy)
- **Database**: SQL (complex queries, window functions, CTEs)
- **Analytics**: Python (Scipy, Scikit-learn)
- **Excel**: Advanced formulas, pivot tables, power query
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Dashboards**: HTML/JavaScript interactive dashboards

## Skills Demonstrated

✓ **500,000+ transaction records** across retail network
✓ **200,000+ customer records** with lifecycle analysis
✓ **5,000 SKU catalog** with performance tracking
✓ **Advanced SQL queries** with window functions, CTEs, complex joins
✓ **Customer segmentation** and RFM analysis
✓ **Inventory optimization** and forecast accuracy
✓ **Promotional ROI** and elasticity analysis
✓ **Sales forecasting** with confidence intervals
✓ **Interactive dashboards** with Plotly
✓ **End-to-end retail analytics** from transaction to insight

## Contact

For questions about this retail analytics portfolio project, please reach out.

## License

MIT License - Portfolio demonstration project.

---

**Portfolio Note:** This analysis demonstrates comprehensive end-to-end retail analytics capabilities including sales performance, customer behavior, inventory management, promotional effectiveness, and revenue forecasting. All data is synthetically generated for portfolio purposes.
