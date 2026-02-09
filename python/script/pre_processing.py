import pandas as pd
import numpy as np
from IPython.display import display

import os
from dotenv import load_dotenv

from utils.connect_db import connect_db
from utils.ingestion import ingest_db


# -----------------------------
# Database configuration
# -----------------------------

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = connect_db(DB_URL)


# -----------------------------
# Load raw data and ingest
# -----------------------------
push_df = pd.read_csv("../dataset/Air-Clean.csv")
ingest_db(push_df, "flight_data", engine)


# -----------------------------
# Read data from DB
# -----------------------------
df = pd.read_sql("SELECT * FROM flight_data", engine)


# -----------------------------
# Basic cleaning
# -----------------------------

# Remove same origin-destination routes
df = df[df["origin"] != df["destination"]]

# Convert days string to list
df["days_list"] = df["daysOfWeek"].str.split(",")

# Weekly frequency
df["weekly_frequency"] = df["days_list"].apply(len)

# Weekend operation flag
weekend_days = {"Saturday", "Sunday"}
df["has_weekend_ops"] = df["days_list"].apply(
    lambda days: any(d in weekend_days for d in days)
)


# -----------------------------
# Time & date processing
# -----------------------------

df["dep_time"] = pd.to_datetime(df["scheduledDepartureTime"], format="%H:%M:%S")
df["arr_time"] = pd.to_datetime(df["scheduledArrivalTime"], format="%H:%M:%S")
df["valid_from"] = pd.to_datetime(df["validFrom"], errors="coerce")

# Convert time → minutes since midnight
dep_min = df["scheduledDepartureTime"].apply(lambda t: t.hour * 60 + t.minute)
arr_min = df["scheduledArrivalTime"].apply(lambda t: t.hour * 60 + t.minute)

# Flight duration
df["duration_min"] = arr_min - dep_min
df.loc[df["duration_min"] < 0, "duration_min"] += 1440  # overnight flights


# -----------------------------
# Feature engineering
# -----------------------------

# Route
df["route"] = df["origin"] + " → " + df["destination"]


def dep_bucket(hour):
    if hour < 6:
        return "Early Morning"
    elif hour < 12:
        return "Morning"
    elif hour < 18:
        return "Afternoon"
    else:
        return "Night"


df["dep_bucket"] = df["dep_time"].dt.hour.apply(dep_bucket)


def indian_season(month):
    if month in [1, 2]:
        return "Winter"
    elif month == 3:
        return "Pre-Summer"
    elif month in [4, 5, 6]:
        return "Summer"
    elif month in [7, 8, 9]:
        return "Monsoon"
    elif month == 10:
        return "Post-Monsoon"
    else:
        return "Winter"


df["season"] = df["valid_from"].dt.month.apply(indian_season)


# -----------------------------
# Final analysis dataframe
# -----------------------------
analysis_df = df[
    [
        "airline",
        "flightNumber",
        "origin",
        "destination",
        "scheduledDepartureTime",
        "scheduledArrivalTime",
        "route",
        "weekly_frequency",
        "has_weekend_ops",
        "dep_bucket",
        "duration_min",
        "season",
        "valid_from",
        "validTo",
    ]
].copy()

analysis_df.rename(
    columns={
        "flightNumber": "flight_number",
        "scheduledDepartureTime": "scheduled_departure_time",
        "scheduledArrivalTime": "scheduled_arrival_time",
        "validTo": "valid_to",
    },
    inplace=True,
)


# -----------------------------
# Ingest analysis table
# -----------------------------
ingest_db(analysis_df, "analyze_data", engine)
