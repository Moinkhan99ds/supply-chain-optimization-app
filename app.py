import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")


st.markdown("""
<style>
.block-container {
    padding-top: 3rem !important;
}

h1 {font-size: 26px !important;}
h2 {font-size: 22px !important;}
h3 {font-size: 18px !important;}

label {
    font-size: 14px !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
h1 {font-size: 26px !important;}
h2 {font-size: 22px !important;}
h3 {font-size: 18px !important;}
label {font-size: 14px !important; font-weight: 600;}
.block-container {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)


model = joblib.load("demand_model.pkl")


left, right = st.columns([1, 2])


with left:
    st.markdown("### ⚙️ Inputs")

    product_id = st.number_input("Product ID", min_value=1, value=1)
    price = st.number_input("Base Price", value=200)
    discount = st.slider("Discount", 0.0, 0.5, 0.1)
    competitor_price = st.number_input("Competitor Price", value=220)

    promotion = st.selectbox("Promotion", [0, 1])
    holiday = st.selectbox("Holiday", [0, 1])

    day_of_week = st.slider("Day (0=Mon)", 0, 6, 3)
    month = st.slider("Month", 1, 12, 6)
    weekend = st.selectbox("Weekend", [0, 1])

    cost_price = st.number_input("Cost Price", value=120)
    current_stock = st.number_input("Stock", value=100)
    lead_time = st.number_input("Lead Time", value=3)

    run = st.button("Run Analysis")


with right:

    st.markdown("## 📦 Supply Chain Optimization Dashboard")

    if run:

        
        df = pd.DataFrame({
            'product_id':[product_id],
            'day_of_week':[day_of_week],
            'month':[month],
            'weekend':[weekend],
            'price':[price],
            'discount':[discount],
            'cost_price':[cost_price],
            'competitor_price':[competitor_price],
            'promotion':[promotion],
            'holiday':[holiday],
            'current_stock':[current_stock],
            'lead_time':[lead_time]
        })

        features = [
            'product_id','day_of_week','month','weekend',
            'price','discount','cost_price','competitor_price',
            'promotion','holiday','current_stock','lead_time'
        ]

        df = df[features]

        
        demand = max(0, model.predict(df)[0])
        reorder_point = demand * lead_time

        
        prices = [int(price*0.8), price, int(price*1.2)]
        demands = []
        profits = []

        for p in prices:
            df["price"] = p
            d = max(0, model.predict(df)[0])

            
            ratio = p / competitor_price
            d = d * (1/ratio)

            profit = (p - cost_price) * d

            demands.append(round(d,2))
            profits.append(round(profit,2))

        
        m1, m2, m3 = st.columns(3)
        m1.metric("📊 Demand", round(demand,2))
        m2.metric("💰 Base Price", price)
        m3.metric("📈 Est. Profit", profits[1])

        
        if current_stock < reorder_point:
            st.error(f"⚠️ Restock Required (Reorder: {round(reorder_point,2)})")
        else:
            st.success(f"✅ Stock OK (Reorder: {round(reorder_point,2)})")

        
        chart_df = pd.DataFrame({
            "Price": prices,
            "Profit": profits
        })

        fig = px.bar(chart_df, x="Price", y="Profit",
                     title="💰 Profit Comparison Across Price Scenarios")

        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

        
        st.markdown("### 📊 Scenario Analysis")

        table_df = pd.DataFrame({
            "Price": prices,
            "Predicted Demand": demands,
            "Estimated Profit": profits
        })
        
        best_idx = profits.index(max(profits))
        best_price = prices[best_idx]

        st.info(f"📌 Recommended Price: ₹{best_price} for maximum profit.")

        
        st.caption("⚠️ Results based on simulated scenarios for decision support.")

        st.dataframe(table_df, use_container_width=True)
