import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Konfigurasi gaya visual
sns.set_style("whitegrid")
plt.rcParams.update({
    'axes.titlesize': 20,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

# Fungsi pengolahan data
def create_daily_orders_df(df):
    daily_order_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_order_df = daily_order_df.reset_index()
    daily_order_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_order_df

def create_top_product_category_df(df):
    top_product_category_df = (
        df.groupby("product_category_name_english")
        .agg(
            total_revenue=("price", "sum"),
            total_quantity=("product_id", "count")
        )
        .sort_values(by="total_revenue", ascending=False)
        .reset_index()
    )
    return top_product_category_df

def create_top_products_df(df):
    top_products_df = df.groupby("product_id").price.sum().sort_values(ascending=False).reset_index()
    return top_products_df

def create_bycustomer_df(df):
    bycustomer_df = df.groupby("customer_state").customer_id.nunique().reset_index()
    bycustomer_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bycustomer_df

# Load data
final_table = pd.read_csv("final_table.csv", parse_dates=["order_purchase_timestamp"])
rfm_table = pd.read_csv("rfm_table.csv")

# Sidebar
min_date = final_table["order_purchase_timestamp"].min()
max_date = final_table["order_purchase_timestamp"].max()
category_list = final_table["product_category_name_english"].dropna().unique().tolist()

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>E-Commerce \nDashboard</h1>", unsafe_allow_html=True)
    st.markdown("## Data Filters")
    
    # Filter Rentang Waktu
    st.markdown("### Period")
    start_date, end_date = st.date_input(
        label="Select Period",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # with col2:
    if st.button("Reset Period"):
        start_date, end_date = min_date, max_date
    
    # Filter Kategori Produk
    selected_category = st.selectbox(
        "Select Product Category",
        options=["All"] + category_list,
        index=0
    )

# Filter Data
filtered_df = final_table[
    (final_table["order_purchase_timestamp"] >= str(start_date)) & 
    (final_table["order_purchase_timestamp"] <= str(end_date))
]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["product_category_name_english"] == selected_category]

# Proses ulang data setelah filter diterapkan
daily_orders_df = create_daily_orders_df(filtered_df)
top_category_products_df = create_top_product_category_df(filtered_df)
top_products_df = create_top_products_df(filtered_df)
bycustomer_df = create_bycustomer_df(filtered_df)

# Tampilan Data yang Difilter
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>E-Commerce Dashboard</h1>", unsafe_allow_html=True)

# Plot 1: Daily Orders
st.markdown("<h2 style='color: #FFC107;'>1. Daily Orders</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "USD", locale="en_US")
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_orders_df["order_purchase_timestamp"], daily_orders_df["order_count"], marker='o', linewidth=2, color="#03A9F4")
ax.set_title("Orders per Day")
ax.set_xlabel("Date")
ax.set_ylabel("Order Count")
st.pyplot(fig)

# Plot 2: Top Category Products
st.markdown("<h2 style='color: #FFC107;'>2. Top Performing Category Products</h2>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="total_revenue", y="product_category_name_english", data=top_category_products_df.head(10), palette="viridis", ax=ax)
ax.set_title("Top Category Products by Revenue")
ax.set_xlabel("Revenue")
ax.set_ylabel("Product Category")
st.pyplot(fig)

# Plot 3: Top Products
st.markdown("<h2 style='color: #FFC107;'>3. Top Performing Products</h2>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="price", y="product_id", data=top_products_df.head(10), palette="coolwarm", ax=ax)
ax.set_title("Top Products by Revenue")
ax.set_xlabel("Revenue")
ax.set_ylabel("Product ID")
st.pyplot(fig)

# Plot 4: Customers by State
st.markdown("<h2 style='color: #FFC107;'>4. Customers by State</h2>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="customer_count", y="customer_state", data=bycustomer_df.sort_values("customer_count", ascending=False), 
            palette="crest", ax=ax)
ax.set_title("Number of Customers by State")
ax.set_xlabel("Number of Customers")
ax.set_ylabel("State")
st.pyplot(fig)

# Plot 5: RFM Metrics
st.subheader("RFM Metrics")
filtered_rfm_df = rfm_table.copy()

if selected_category != "All":
    filtered_rfm_df = filtered_rfm_df[
        rfm_table["customer_id"].isin(
            final_table[final_table["product_category_name_english"] == selected_category]["customer_id"]
        )
    ]

col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(filtered_rfm_df.Recency.mean(), 1)
    st.metric("Average Recency", value=avg_recency)

with col2:
    avg_frequency = round(filtered_rfm_df.Frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(filtered_rfm_df.Monetary.mean(), "USD", locale="en_US")
    st.metric("Average Monetary", value=avg_monetary)

st.subheader("Best Customers by RFM")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))

sns.barplot(
    y="Recency",
    x="customer_id",
    data=filtered_rfm_df.sort_values(by="Recency").head(5),
    palette="Blues_r",
    ax=ax[0]
)
ax[0].set_title("Top 5 Customers by Recency")
ax[0].set_xlabel("Customer ID")
ax[0].set_ylabel("Recency (Days)")

sns.barplot(
    y="Frequency",
    x="customer_id",
    data=filtered_rfm_df.sort_values(by="Frequency", ascending=False).head(5),
    palette="Oranges_r",
    ax=ax[1]
)
ax[1].set_title("Top 5 Customers by Frequency")
ax[1].set_xlabel("Customer ID")
ax[1].set_ylabel("Frequency")

sns.barplot(
    y="Monetary",
    x="customer_id",
    data=filtered_rfm_df.sort_values(by="Monetary", ascending=False).head(5),
    palette="Greens_r",
    ax=ax[2]
)
ax[2].set_title("Top 5 Customers by Monetary")
ax[2].set_xlabel("Customer ID")
ax[2].set_ylabel("Monetary (USD)")

st.pyplot(fig)

st.caption("Created by Alhamdana")