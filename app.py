import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="BigBasket Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 BigBasket Product Analytics Dashboard")
st.markdown("Interactive visualization of BigBasket products, brands, categories, and pricing.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("BigBasket.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

filtered_df = df[df["Category"].isin(category)]

# KPIs
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(filtered_df))

with col2:
    st.metric("Total Categories", filtered_df["Category"].nunique())

with col3:
    st.metric("Total Brands", filtered_df["Brand"].nunique())

with col4:
    st.metric(
        "Average Price",
        f"₹ {filtered_df['Price'].mean():.2f}"
    )

st.divider()

# Top Categories
col1, col2 = st.columns(2)

with col1:
    category_count = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = ["Category", "Count"]

    fig = px.bar(
        category_count.head(10),
        x="Category",
        y="Count",
        title="Top Categories"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    brand_count = (
        filtered_df["Brand"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    brand_count.columns = ["Brand", "Count"]

    fig = px.pie(
        brand_count,
        names="Brand",
        values="Count",
        title="Top 10 Brands"
    )

    st.plotly_chart(fig, use_container_width=True)

# Price Distribution
st.subheader("💰 Product Pricing Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered_df,
        x="Price",
        nbins=30,
        title="Price Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        filtered_df,
        x="DiscountPrice",
        nbins=30,
        title="Discount Price Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Price vs Discount Price
st.subheader("📉 Price vs Discount Price")

sample_df = filtered_df.sample(
    min(1000, len(filtered_df)),
    random_state=42
)

fig = px.scatter(
    sample_df,
    x="Price",
    y="DiscountPrice",
    color="Category",
    hover_data=["ProductName", "Brand"],
    title="Price vs Discount Price"
)

st.plotly_chart(fig, use_container_width=True)

# Average Category Price
st.subheader("🏷 Average Price by Category")

avg_price = (
    filtered_df
    .groupby("Category")["Price"]
    .mean()
    .reset_index()
    .sort_values(by="Price", ascending=False)
)

fig = px.bar(
    avg_price,
    x="Category",
    y="Price",
    color="Price",
    title="Average Price by Category"
)

st.plotly_chart(fig, use_container_width=True)

# Product Table
st.subheader("📋 Product Details")

search = st.text_input("Search Product")

if search:
    display_df = filtered_df[
        filtered_df["ProductName"]
        .str.contains(search, case=False, na=False)
    ]
else:
    display_df = filtered_df

st.dataframe(display_df, use_container_width=True)

# Download Option
csv = display_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="bigbasket_filtered.csv",
    mime="text/csv"
)