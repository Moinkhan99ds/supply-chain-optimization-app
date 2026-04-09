import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# Load model
model = joblib.load("demand_model.pkl")

st.set_page_config(page_title="Supply Chain App", layout="wide")

st.title("📦 Supply Chain Optimization Dashboard")

st.header("Enter Product Details")

# Inputs
product_id = st.number_input("Product ID", min_value=1, value=1)

price = st.number_input("Price", value=200)
discount = st.slider("Discount", 0.0, 0.5, 0.1)

competitor_price = st.number_input("Competitor Price", value=220)

promotion = st.selectbox("Promotion", [0, 1])
holiday = st.selectbox("Holiday", [0, 1])

day_of_week = st.slider("Day of Week (0=Mon,6=Sun)", 0, 6, 3)
month = st.slider("Month", 1, 12, 6)
weekend = st.selectbox("Weekend", [0, 1])

cost_price = st.number_input("Cost Price", value=120)
current_stock = st.number_input("Current Stock", value=100)
lead_time = st.number_input("Lead Time (days)", value=3)

# Button
if st.button("Run Analysis"):

    # Create DataFrame
    input_df = pd.DataFrame({
        'product_id': [product_id],
        'day_of_week': [day_of_week],
        'month': [month],
        'weekend': [weekend],
        'price': [price],
        'discount': [discount],
        'cost_price': [cost_price],
        'competitor_price': [competitor_price],
        'promotion': [promotion],
        'holiday': [holiday],
        'current_stock': [current_stock],
        'lead_time': [lead_time]
    })

    features = [
        'product_id', 'day_of_week', 'month', 'weekend',
        'price', 'discount', 'cost_price', 'competitor_price',
        'promotion', 'holiday', 'current_stock', 'lead_time'
    ]

    input_df = input_df[features]

    # =============================
    # 🔥 1. Demand Prediction
    # =============================
    demand = model.predict(input_df)[0]

    st.subheader("📊 Demand Forecast")

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Demand", round(demand, 2))
    col2.metric("Current Stock", current_stock)
    col3.metric("Lead Time", lead_time)

    # =============================
    # 🔥 2. Inventory Decision
    # =============================
    reorder_point = demand * lead_time

    st.subheader("📦 Inventory Decision")

    if current_stock < reorder_point:
        st.error(f"⚠️ Restock Required (Reorder Point: {round(reorder_point,2)})")
    else:
        st.success(f"✅ Stock is Enough (Reorder Point: {round(reorder_point,2)})")

    # =============================
    # 🔥 3. Price Optimization
    # =============================
    max_profit = float('-inf')
    best_price = 0
    cost = cost_price

    price_range = []
    profit_list = []

    for p in range(100, 500, 10):
        input_df["price"] = p
        temp_demand = model.predict(input_df)[0]
        profit = (p - cost) * temp_demand

        price_range.append(p)
        profit_list.append(profit)

        if profit > max_profit:
            max_profit = profit
            best_price = p

    st.subheader("💰 Price Optimization")

    col1, col2 = st.columns(2)
    col1.metric("Best Price", best_price)
    col2.metric("Max Profit", round(max_profit, 2))

    # =============================
    # 🔥 4. GRAPH (MAIN UPGRADE)
    # =============================
    st.subheader("📈 Profit vs Price Graph")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=price_range,
        y=profit_list,
        mode='lines+markers',
        name='Profit',
        line=dict(color='green')
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Price",
        yaxis_title="Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =============================
    # 🔥 5. TREND
    # =============================
    if len(profit_list) > 1:
        if profit_list[-1] > profit_list[-2]:
            st.success("📈 Profit Increasing Trend")
        else:
            st.error("📉 Profit Decreasing Trend")
