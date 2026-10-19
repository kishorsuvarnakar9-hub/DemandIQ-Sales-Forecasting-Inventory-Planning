# DemandIQ — AI-Powered Sales Forecasting & Inventory Planning System

An end-to-end data science project that combines sales analytics, machine learning-based demand forecasting, and inventory planning to support data-driven business decisions.

## Overview

**DemandIQ** is an interactive analytics dashboard built with Python and Streamlit. It helps users explore historical sales, forecast future product demand, identify inventory risks, and generate suggested replenishment quantities.

The goal is to turn sales and inventory data into actionable business insights.

## Key Features

- **Executive Overview:** Monitor revenue, units sold, product performance, and inventory alerts.
- **Sales Intelligence:** Analyze sales trends, product performance, and seasonal patterns.
- **AI Forecast Lab:** Forecast future daily unit demand using a Random Forest regression model.
- **Inventory Control Tower:** Estimate demand during supplier lead time and calculate suggested replenishment quantities.
- **Data Quality Center:** Review dataset structure and identify potential data-quality issues.
- **Interactive Dashboard:** Explore data through interactive charts, filters, and downloadable reports.

## Technology Stack

- **Programming:** Python
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **Machine Learning:** Scikit-learn, Random Forest Regressor
- **Dashboard:** Streamlit
- **Data Sources:** Excel and CSV files
- **Deployment Target:** AWS EC2

## Project Structure

```text
DemandIQ/
├── app.py
├── data_loader.py
├── forecasting.py
├── inventory.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    └── raw/
        └── enterprise_revenue_dataset.xlsx
```

*Keep the project structure consistent with your actual files. Include any additional datasets required by the application.*

## Getting Started

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use an appropriate process-scoped execution policy for the current terminal session.

**Linux / AWS EC2:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Forecasting Methodology

The forecasting module uses a Random Forest regression model with time-based features, including:

- Previous-day demand (lag 1)
- Demand from the previous 7 and 14 days
- Rolling averages over 7 and 14 days
- Day of the week
- Month of the year

The model evaluates predictions on a chronological holdout set using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE), then fits a final model to generate future forecasts.

Forecast quality depends on the available history, data quality, seasonality, and model validation.

## Inventory Planning

The inventory planning module estimates demand during supplier lead time, applies a buffer, and calculates suggested replenishment quantities.

Recommendations are intended to support inventory decisions and should be reviewed against actual supplier constraints, stock policies, and business requirements.

## Deployment

The application is designed to run on an AWS EC2 Linux instance.

A typical deployment involves:

1. Launching an Ubuntu EC2 instance.
2. Installing Python, pip, and Git.
3. Cloning the repository.
4. Installing dependencies from `requirements.txt`.
5. Running Streamlit on the server.
6. Configuring secure network access and, for production use, HTTPS.

Deployment is complete only after the live application has been tested successfully.

## Business Value

DemandIQ demonstrates how data science can help businesses:

- Understand historical sales performance.
- Estimate future product demand.
- Identify potential stock shortages.
- Plan replenishment quantities.
- Support more informed inventory decisions.

## Future Enhancements

- Compare Random Forest against time-series forecasting baselines.
- Add product-level forecast evaluation and backtesting.
- Track model performance and demand drift.
- Automate data refresh and scheduled forecasts.
- Add authentication and secure production hosting.
- Introduce monitoring and model versioning.

## Author

**Kishor Suvarnakar**

Aspiring Data Scientist focused on Python, machine learning, data analytics, forecasting, and practical AI applications.

## Disclaimer

This project is intended for learning, portfolio demonstration, and decision-support purposes. Forecasts and inventory recommendations are estimates and should be validated before use in real business operations.
