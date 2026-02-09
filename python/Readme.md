
# ✈️ Indian Domestic Flight Analysis

**End-to-End Data Analytics & Visualization Project (Python + PostgreSQL)**

> **Indian Domestic Flight Analysis**
> Built an end-to-end data analytics pipeline using Python and PostgreSQL to analyze airline market share, route saturation, airport connectivity, and seasonal trends. Engineered domain-specific KPIs and produced 20+ high-resolution visualizations to uncover operational and competitive insights in the Indian aviation sector.

---

## 📌 Project Overview

This project performs an **end-to-end analysis of Indian domestic flight operations** using real-world airline schedule data.
It covers the **complete analytics lifecycle**:

* Raw data ingestion into PostgreSQL
* Data cleaning & feature engineering
* Analytics-ready table creation
* Advanced exploratory data analysis (EDA)
* Business-driven KPIs & visualizations

The project is designed to be **resume-ready**, **interview-ready**, and **portfolio-grade**, following industry best practices used by analytics teams in aviation, consulting, and Big-4 firms.

---

## 📂 Dataset

**Source:** Kaggle – *Indian Domestic Airline Dataset*
🔗 [https://www.kaggle.com/datasets/kabil007/indian-domestic-airline-dataset](https://www.kaggle.com/datasets/kabil007/indian-domestic-airline-dataset)

### Dataset Description

The dataset contains **scheduled Indian domestic flight information**, including:

* Airline name
* Flight number
* Origin & destination airports
* Days of operation
* Scheduled departure & arrival times
* Validity periods

### Dataset Usage in This Project

* The raw Kaggle dataset was **cleaned, validated, and transformed**
* Invalid routes (same origin & destination) were removed
* Time-based, seasonal, and operational features were engineered
* The processed dataset was stored in PostgreSQL for scalable analysis

> **Note:**
> This project is strictly for **educational and analytical purposes**.
> All credit for the original dataset goes to the dataset creator on Kaggle.

---

## 🎯 Key Objectives

* Understand **airline market share & competition**
* Identify **busiest routes and airport hubs**
* Analyze **seasonality & time-of-day strategies**
* Measure **route saturation & network aggressiveness**
* Build **decision-ready KPIs** for airline and airport strategy

---

## 🗂️ Project Directory Structure

```text
flight_analysis/
│
├── dataset/
│   └── Air-Clean.csv                # Cleaned dataset derived from Kaggle source
│
├── python/
│   ├── charts/                      # Generated visual outputs (20+ charts)
│   │   ├── 01_airline_market_share_bar.png
│   │   ├── 02_airline_market_share_donut.png
│   │   ├── ...
│   │   └── 20_airline_strategy_scatter.png
│   │
│   ├── logs/
│   │   └── flight_analysis_20260209.log
│   │
│   ├── utils/
│   │   ├── connect_db.py             # PostgreSQL connection utility
│   │   ├── ingestion.py              # Data ingestion logic
│   │   └── logger.py                 # Centralized logging
│   │
│   ├── script/
│   │   ├── pre_processing.py         # Data cleaning & feature engineering
│   │   └── exploratory_data_analysis.py
│   │
│   ├── exploratory_data_analysis.ipynb
│   ├── pre_processing.ipynb
│   └── README.md
│
└── .gitignore
```

---

## 🧠 Data Pipeline Architecture

```text
Kaggle CSV Dataset
        ↓
PostgreSQL (flight_data)
        ↓
Data Cleaning & Feature Engineering
        ↓
Analytics Table (analyze_data)
        ↓
EDA + KPI Visualizations
```

---

## 🧪 Technologies Used

| Category        | Tools               |
| --------------- | ------------------- |
| Language        | Python              |
| Database        | PostgreSQL          |
| Libraries       | Pandas, NumPy       |
| Visualization   | Matplotlib, Seaborn |
| Logging         | Python logging      |
| Environment     | Conda               |
| Version Control | Git (recommended)   |

---

## 🧹 Data Cleaning & Feature Engineering

Key transformations performed:

* Removed invalid routes (same origin & destination)
* Converted operating days → **weekly frequency**
* Created **weekend operation flag**
* Calculated **flight duration (handling overnight flights)**
* Engineered:

  * Departure time buckets
  * Indian season classification
  * Route identifiers

### 🕒 Departure Time Buckets

```text
Early Morning | Morning | Afternoon | Night
```

### 🌦️ Indian Season Mapping

```text
Winter | Pre-Summer | Summer | Monsoon | Post-Monsoon
```

---

## 📊 Analytical Visualizations (20 Total)

### 1️⃣ Market & Competition

* Airline Market Share (Bar & Donut)
* Airline Market Share by Season
* Airline Network Aggressiveness Index

### 2️⃣ Route & Network Analysis

* Top 10 Busiest Routes
* Route Saturation Index (RSI)
* Route Density (Avg Weekly Flights)
* Airline Route Breadth vs Frequency (Scatter KPI)

### 3️⃣ Airport & Hub Analysis

* Airport Connectivity (Unique Destinations)
* Airport Connectivity Score (Log-Weighted KPI)

### 4️⃣ Time & Seasonality

* Departure Time Distribution
* Departure Time vs Weekend Heatmap
* Seasonal Capacity Distribution
* Season-wise Average Flight Duration

### 5️⃣ Operational Insights

* Flight Duration Distribution
* Duration by Season (Boxplot)
* Weekend vs Weekday Supply
* Airline Fleet Utilization Proxy

All charts are saved at **DPI = 1000** for high-resolution reporting.

---

## 📈 Key Business KPIs Explained

### ✳️ Route Saturation Index (RSI)

```text
RSI = Route Weekly Flights / Average Route Flights
```

Identifies **overcrowded routes**.

### ✳️ Airport Connectivity Score

```text
Connectivity = Destinations × log(1 + Total Flights)
```

Balances **breadth + scale**.

### ✳️ Airline Network Aggressiveness

```text
Aggressiveness = Total Flights / Unique Routes
```

Shows **frequency-focused vs network-expansion strategies**.

---

## 🧠 Key Insights

* A small number of airlines dominate **weekly flight supply**
* Morning & afternoon slots handle the **bulk of operations**
* Certain metro routes show **high saturation risk**
* Some airlines favor **frequency concentration**, others **route expansion**
* Major hubs balance **connectivity and throughput differently**

