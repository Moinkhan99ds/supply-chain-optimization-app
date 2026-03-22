import streamlit as st
import pandas as pd
import joblib

model = joblib.load("demand_model.pkl")

st.title("📦 Supply Chain Optimization App")

st.header("Enter Product Details")

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

if st.button("Run Analysis"):

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
  
    # Demand Prediction
    demand = model.predict(input_df)[0]

    st.subheader("📊 Demand Forecast")
    st.write(f"Predicted Units Sold: {round(demand, 2)}")

    # Inventory Decision
    reorder_point = demand * lead_time

    if current_stock < reorder_point:
        status = "Restock Required"
    else:
        status = "Stock is Enough"

    st.subheader("📦 Inventory Decision")
    st.write(f"Reorder Point: {round(reorder_point, 2)}")
    st.write(f"Status: {status}")

  # Price Optimization

    max_profit = float('-inf')
    best_price = 0

    cost = cost_price

    for p in range(100, 500, 10):
        input_df["price"] = p
        temp_demand = model.predict(input_df)[0]
        profit = (p - cost) * temp_demand

        if profit > max_profit:
            max_profit = profit
            best_price = p

    st.subheader(" Price Optimization")
    st.write(f"Best Price: {best_price}")
    st.write(f"Max Profit: {round(max_profit, 2)}")
