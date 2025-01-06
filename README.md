# E-Commerce Dashboard

A data-driven project to analyze and visualize key metrics of an e-commerce business. This project leverages data wrangling, business analytics, and visualization techniques to provide actionable insights into customer behavior and product performance.

---

## 📊 Features
- **Interactive Dashboard**: Built using Streamlit to explore data through time filters and product categories.
- **Key Metrics**:
  - Total orders and revenue.
  - Top performing product categories and products.
  - Customer segmentation based on states.
  - RFM (Recency, Frequency, Monetary) analysis for customer profiling.
- **Dynamic Filters**:
  - Date range selection.
  - Product category filtering.

---

## 🛠️ Tools and Technologies
- **Python**: Pandas, Matplotlib, Seaborn, and Streamlit.
- **Data Analysis**: Cleaning, transforming, and analyzing raw e-commerce data.
- **Visualization**: Interactive graphs and charts for decision-making.

---

## 📂 Project Structure
```
📁 dataset                   # Contains raw and processed datasets
olist_data_wrangling.ipynb   # Jupyter Notebook for data wrangling and cleaning steps
olist_dashboard              # Main Python script for the Streamlit dashboard application
final_table.csv              # Cleaned and aggregated data for dashboard visualizations
rfm_table.csv                # RFM analysis results for customer segmentation
README.md                    # Project documentation and usage instructions

```

---

## 📦 Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run olist_dashboard.py
   ```

---

## 📈 Insights Delivered
- Identify trends in customer orders and revenue over time.
- Highlight top-performing product categories and products.
- Provide data for customer profiling and segmentation using RFM analysis.
- Offer actionable insights to improve marketing strategies and product offerings.

---

## 🖥️ Example Visualizations
1. **Daily Orders Trend**: Line chart showing the number of daily orders.
2. **Top Product Categories**: Bar chart for top categories by revenue.
3. **Customer Segmentation**: Breakdown of customer distribution by state.
