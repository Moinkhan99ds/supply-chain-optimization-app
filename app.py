import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# ---------- CSS FIX (NO TEXT CUT) ----------
st.markdown("""
<style>
label {
    font-size: 14px !important;
    font-weight: 600;
}
div[data-baseweb="input"] {
    width: 100% !important;
}
.stNumberInput, .stSlider, .stSelectbox {
    overflow: visible !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
model = joblib.load("demand_model.pkl")

# ---------- LAYOUT ----------
left, right = st.columns([1, 2])

# ================= LEFT PANEL =================
with left:
    st.subheader("⚙️ Inputs")

    product_id = st.number_input("Product ID", min_value=1, value=1)
    price = st.number_input("Price", value=200)
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

# ================= RIGHT PANEL =================
with right:

    st.title("📦 Supply Chain Dashboard")

    if run:

        # ---------- DATA ----------
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

        # ---------- PREDICTION ----------
        demand = max(0, model.predict(df)[0])   # negative avoid
        reorder_point = demand * lead_time

        # ---------- PRICE OPT (FIXED LOGIC) ----------
        price_range = list(range(100, 500, 10))
        profits = []

        for p in price_range:
            df["price"] = p
            d = model.predict(df)[0]

            # 🔥 REALISTIC DEMAND ADJUSTMENT
            price_factor = max(0.3, 1 - (p / 800))  
            d = max(0, d * price_factor)

            profit = (p - cost_price) * d
            profits.append(profit)

        best_price = price_range[profits.index(max(profits))]
        max_profit = max(profits)

        # ---------- METRICS ----------
        m1, m2, m3 = st.columns(3)
        m1.metric("📊 Demand", round(demand,2))
        m2.metric("💰 Best Price", best_price)
        m3.metric("📈 Profit", round(max_profit,2))

        # ---------- ALERT ----------
        if current_stock < reorder_point:
            st.error(f"⚠️ Restock Required (Reorder: {round(reorder_point,2)})")
        else:
            st.success(f"✅ Stock OK (Reorder: {round(reorder_point,2)})")

        # ---------- GRAPHS ----------
        g1, g2 = st.columns(2)

        # Demand graph
        demand_series = [demand * (0.8 + i*0.05) for i in range(10)]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            y=demand_series,
            mode='lines+markers',
            name="Demand",
            line=dict(color='cyan')
        ))
        fig1.update_layout(title="📈 Demand Trend", template="plotly_dark")
        g1.plotly_chart(fig1, use_container_width=True)
        # Profit graph
        fig2 = px.line(x=price_range, y=profits, title="💰 Profit vs Price")
        fig2.update_layout(template="plotly_dark")
        g2.plotly_chart(fig2, use_container_width=True)

        # ---------- DISCOUNT VS DEMAND ----------
        discounts = [i/10 for i in range(0,6)]
        sales = []

        for d in discounts:
            df["discount"] = d
            s = model.predict(df)[0]
            s = max(0, s)
            sales.append(s)

        fig3 = px.line(x=discounts, y=sales, title="🎯 Discount vs Demand")
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

        # ---------- INSIGHT ----------
        st.info(f"📌 Best price ₹{best_price} → Max profit ₹{round(max_profit,2)}. Consider increasing stock.")
