# 🚕 YellowCab Intelligence
## NYC Yellow Taxi Trip Duration Predictor



![Python](https://img.shields.io/badge/Python-3.14-blue)




![LightGBM](https://img.shields.io/badge/Model-LightGBM-green)




![Streamlit](https://img.shields.io/badge/App-Streamlit-red)



## 🎯 Problem Statement
Given a taxi trip's pickup location, dropoff location, and time of day, 
can we accurately predict how long the trip will take in minutes?

## 📊 Dataset
- Source: NYC TLC Trip Record Data
- Period: January 2025 – December 2025
- Size: 46+ million trips cleaned and processed
- Format: Monthly CSV/Parquet files

## ✅ Success Metrics
- RMSE below 5.0 minutes
- R² above 0.80
- Must beat baseline (distance ÷ average speed)

## 💻 Models Compared
| Model | RMSE | MAE | R² |
|---|---|---|---|
| Baseline | 12.56 | 6.84 | -0.26 |
| Linear Regression | 5.29 | 3.56 | 0.78 |
| Ridge Regression | 5.29 | 3.56 | 0.78 |
| Random Forest | 4.22 | 2.65 | 0.86 |
| LightGBM ✅ | 4.18 | 2.63 | 0.86 |

## 🏆 Best Model: LightGBM
- RMSE: 4.18 minutes
- MAE: 2.63 minutes  
- R²: 0.8603

## ⚙️ Features Engineered
- pickup_hour, day_of_week, month
- is_weekend, is_rush_hour
- route_avg_duration (historical average per route)
- congestion_fee_flag
- pickup_borough, dropoff_borough

## 🚀 Live App
Run locally:

python -m streamlit run app/streamlit_app.py

## 📁 Project Structure
- notebooks/ — Full Jupyter analysis notebook
- models/ — Saved LightGBM and other model files
- data/ — Raw and processed taxi data
- app/ — Streamlit web application
- charts — All generated visualizations

## 🛠️ Tech Stack
Python, Pandas, NumPy, Scikit-learn, LightGBM, 
Matplotlib, Seaborn, Streamlit, Power BI

## 📌 Data Source
NYC TLC Trip Record Data
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page