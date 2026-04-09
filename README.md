# supply-chain-optimization-app
End to End Supply Chain Optimization app using Machine Learning to Forecast demand, optimize inventory, and determine profit-maximizing prices.

---

## Problem
Businesses face:

- Stockouts (loss of sales)
- Overstocking (extra inventory cost)
- Poor pricing decisions

---

## Solution

This app uses machine learning + business logic to:

- Predict future product demand  
- Calculate optimal inventory (Reorder Point)  
- Suggest pricing strategies to maximize profit  

---

## Demo

![Demo](demo.supply.gif)

---

## Features

-  Demand Forecasting (ML model)
-  Inventory Optimization (Reorder Point)
-  Price Optimization Logic

---

## Machine Learning

- Model: Random Forest Regressor  
- Target: units_sold  
- Features:
  - price
  - discount
  - day, month, weekday
  - lag features (previous demand)

---

## Sample Output

- Predicted Demand: 120 units
- Suggested Action: Increase inventory
- Profit Optimization: Adjust price for max revenue

---

## Tech Stack

- Python  
- Pandas  
- Scikit-learn  
- Streamlit  

---

## 🌐 Live App

👉 [Click to try the app](https://supply-chain-optimization-app-csjvboweuc28piacpjdj3s.streamlit.app/)

