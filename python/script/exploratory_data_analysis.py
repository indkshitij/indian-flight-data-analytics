# =====================================================
# Imports & Global Plot Settings
# =====================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

from utils.connect_db import connect_db

sns.set_style("whitegrid")

DPI = 1000
FIG_SMALL = (3, 3)
FIG_MEDIUM = (8, 5)
FIG_LARGE = (10, 6)

load_dotenv()
DB_URL = os.getenv("DB_URL")

# =====================================================
# Load Data
# =====================================================
engine = connect_db(DB_URL)
df = pd.read_sql("SELECT * FROM analyze_data", engine)


# =====================================================
# 1. Airline Market Share (Bar)
# =====================================================
airline_supply = (
    df.groupby("airline")["weekly_frequency"].sum().sort_values(ascending=False)
)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
airline_supply.plot(kind="bar", edgecolor="black")

plt.title("Airline Market Share by Weekly Scheduled Flights")
plt.xlabel("Airline")
plt.ylabel("Weekly Flight Count")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/01_airline_market_share_bar.png", dpi=DPI)
plt.close()


# =====================================================
# 2. Airline Market Share (Donut)
# =====================================================
colors = sns.color_palette("pastel", len(airline_supply))

plt.figure(figsize=FIG_SMALL, dpi=DPI)

plt.pie(
    airline_supply,
    colors=colors,
    startangle=90,
    wedgeprops={"width": 0.5, "edgecolor": "white"},
)

plt.title("Airline Market Share")

plt.legend(
    airline_supply.index,
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=5,
    frameon=False,
)

plt.tight_layout()
plt.savefig("charts/02_airline_market_share_donut.png", dpi=DPI)
plt.close()


# =====================================================
# 3. Top 10 Busiest Routes
# =====================================================
top_routes = (
    df.groupby("route")["weekly_frequency"].sum().sort_values(ascending=False).head(10)
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
top_routes.plot(kind="barh", edgecolor="black")

plt.title("Top 10 Busiest Domestic Routes")
plt.xlabel("Weekly Flight Count")
plt.ylabel("Route")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("charts/03_top_10_routes.png", dpi=DPI)
plt.close()


# =====================================================
# 4. Airport Connectivity (Unique Destinations)
# =====================================================
airport_connectivity = (
    df.groupby("origin")["destination"].nunique().sort_values(ascending=False).head(15)
)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
airport_connectivity.plot(kind="bar", edgecolor="black")

plt.title("Top 15 Airports by Connectivity")
plt.xlabel("Origin Airport")
plt.ylabel("Number of Destinations")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/04_airport_connectivity.png", dpi=DPI)
plt.close()


# =====================================================
# 5. Departure Time vs Weekend Operations (Heatmap)
# =====================================================
heatmap_data = df.pivot_table(
    index="dep_bucket",
    columns="has_weekend_ops",
    values="weekly_frequency",
    aggfunc="sum",
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="coolwarm")

plt.title("Departure Time vs Weekend Operations")
plt.xlabel("Operates on Weekend")
plt.ylabel("Departure Time Bucket")

plt.tight_layout()
plt.savefig("charts/05_departure_time_heatmap.png", dpi=DPI)
plt.close()


# =====================================================
# 6. Seasonal Capacity Distribution
# =====================================================
seasonal_supply = (
    df.groupby("season")["weekly_frequency"]
    .sum()
    .reindex(["Summer", "Monsoon", "Winter"])
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
seasonal_supply.plot(kind="bar", edgecolor="black")

plt.title("Seasonal Distribution of Domestic Flight Supply")
plt.xlabel("Season")
plt.ylabel("Weekly Flight Count")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/06_seasonal_capacity.png", dpi=DPI)
plt.close()


# =====================================================
# 7. Flight Duration Distribution
# =====================================================
plt.figure(figsize=FIG_LARGE, dpi=DPI)

sns.histplot(df["duration_min"], bins=40, kde=True, color="#1f77b4", edgecolor="white")

plt.title("Distribution of Flight Durations")
plt.xlabel("Flight Duration (minutes)")
plt.ylabel("Number of Flights")

plt.tight_layout()
plt.savefig("charts/07_flight_duration_distribution.png", dpi=DPI)
plt.close()


# =====================================================
# 8. Flight Duration by Season (Boxplot)
# =====================================================
plt.figure(figsize=FIG_MEDIUM, dpi=DPI)

sns.boxplot(
    x="season",
    y="duration_min",
    data=df,
    order=["Summer", "Monsoon", "Winter"],
    palette="coolwarm",
)

plt.title("Flight Duration by Season")
plt.xlabel("Season")
plt.ylabel("Flight Duration (minutes)")

plt.tight_layout()
plt.savefig("charts/08_duration_by_season_boxplot.png", dpi=DPI)
plt.close()


# =====================================================
# 9. Airline-wise Departure Time Distribution
# =====================================================
pivot = df.pivot_table(
    index="airline", columns="dep_bucket", values="weekly_frequency", aggfunc="sum"
)

dep_order = ["Early Morning", "Morning", "Afternoon", "Night"]
pivot = pivot[dep_order]

plt.figure(figsize=FIG_LARGE, dpi=DPI)
pivot.plot(kind="bar", stacked=True, edgecolor="white")

plt.title("Airline-wise Distribution of Departure Time Buckets")
plt.xlabel("Airline")
plt.ylabel("Weekly Flights")
plt.xticks(rotation=30, ha="right")

plt.legend(
    title="Departure Time", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False
)

plt.tight_layout()
plt.savefig("charts/09_airline_dep_bucket_stacked.png", dpi=DPI)
plt.close()


# =====================================================
# 10. Airline Market Share by Season
# =====================================================
season_share = (
    df.groupby(["season", "airline"])["weekly_frequency"]
    .sum()
    .groupby(level=0)
    .apply(lambda x: x / x.sum())
    .unstack()
)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
season_share.plot(kind="bar", stacked=True)

plt.title("Airline Market Share by Season")
plt.ylabel("Share of Weekly Flights")

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.savefig("charts/10_market_share_by_season.png", dpi=DPI)
plt.close()


# =====================================================
# 11. Route Saturation Index
# =====================================================
route_supply = df.groupby("route")["weekly_frequency"].sum()
avg_route_supply = route_supply.mean()

rsi = (route_supply / avg_route_supply).sort_values(ascending=False)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
rsi.head(10).plot(kind="barh", edgecolor="black")

plt.title("Top 10 Most Saturated Routes (RSI)")
plt.xlabel("Route Saturation Index")
plt.ylabel("Route")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("charts/11_route_saturation_index.png", dpi=DPI)
plt.close()


# =====================================================
# 12. Airport Connectivity Score
# =====================================================
airport_kpi = df.groupby("origin").agg(
    total_flights=("weekly_frequency", "sum"), destinations=("destination", "nunique")
)

airport_kpi["connectivity_score"] = airport_kpi["destinations"] * np.log1p(
    airport_kpi["total_flights"]
)

airport_kpi = airport_kpi.sort_values("connectivity_score", ascending=False)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
airport_kpi.head(10)["connectivity_score"].plot(kind="bar", edgecolor="black")

plt.title("Top Airports by Connectivity Score")
plt.xlabel("Airport")
plt.ylabel("Connectivity Score")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/12_airport_connectivity_score.png", dpi=DPI)
plt.close()


# =====================================================
# 13. Airline Network Aggressiveness
# =====================================================
airline_kpi = df.groupby("airline").agg(
    total_flights=("weekly_frequency", "sum"), unique_routes=("route", "nunique")
)

airline_kpi["network_aggressiveness"] = (
    airline_kpi["total_flights"] / airline_kpi["unique_routes"]
)

airline_kpi = airline_kpi.sort_values("network_aggressiveness", ascending=False)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
airline_kpi["network_aggressiveness"].plot(kind="bar", edgecolor="black")

plt.title("Airline Network Aggressiveness Index")
plt.xlabel("Airline")
plt.ylabel("Flights per Route")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/13_airline_network_aggressiveness.png", dpi=DPI)
plt.close()

# =====================================================
# 14. Weekend vs Weekday Flight Supply
# =====================================================
weekend_supply = (
    df.groupby("has_weekend_ops")["weekly_frequency"]
    .sum()
    .rename({True: "Includes Weekend", False: "Weekday Only"})
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
weekend_supply.plot(kind="bar", edgecolor="black")

plt.title("Weekly Flight Supply: Weekday vs Weekend")
plt.xlabel("Operation Type")
plt.ylabel("Weekly Flight Count")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/14_weekday_vs_weekend_supply.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 15. Average Flight Duration by Airline
# =====================================================
avg_duration_airline = (
    df.groupby("airline")["duration_min"].mean().sort_values(ascending=False)
)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
avg_duration_airline.plot(kind="bar", edgecolor="black")

plt.title("Average Flight Duration by Airline")
plt.xlabel("Airline")
plt.ylabel("Average Duration (minutes)")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/15_avg_duration_by_airline.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 16. Departure Time Distribution (Overall)
# =====================================================
dep_distribution = (
    df.groupby("dep_bucket")["weekly_frequency"]
    .sum()
    .reindex(["Early Morning", "Morning", "Afternoon", "Night"])
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
dep_distribution.plot(kind="bar", edgecolor="black")

plt.title("Overall Departure Time Distribution")
plt.xlabel("Departure Time Bucket")
plt.ylabel("Weekly Flight Count")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/16_departure_time_distribution.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 17. Average Weekly Frequency per Route (Route Density)
# =====================================================
route_density = (
    df.groupby("route")["weekly_frequency"].mean().sort_values(ascending=False)
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
route_density.head(10).plot(kind="barh", edgecolor="black")

plt.title("Top 10 Routes by Average Weekly Frequency")
plt.xlabel("Average Weekly Flights")
plt.ylabel("Route")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("charts/17_route_density.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 18. Airline Fleet Utilization Proxy
# (Flights per Day Approximation)
# =====================================================
airline_utilization = (df.groupby("airline")["weekly_frequency"].sum() / 7).sort_values(
    ascending=False
)

plt.figure(figsize=FIG_LARGE, dpi=DPI)
airline_utilization.plot(kind="bar", edgecolor="black")

plt.title("Airline Fleet Utilization Proxy (Avg Flights per Day)")
plt.xlabel("Airline")
plt.ylabel("Flights per Day")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("charts/18_airline_fleet_utilization.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 19. Season-wise Average Flight Duration
# =====================================================
season_duration = (
    df.groupby("season")["duration_min"].mean().reindex(["Summer", "Monsoon", "Winter"])
)

plt.figure(figsize=FIG_MEDIUM, dpi=DPI)
season_duration.plot(kind="bar", edgecolor="black")

plt.title("Average Flight Duration by Season")
plt.xlabel("Season")
plt.ylabel("Average Duration (minutes)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/19_avg_duration_by_season.png", dpi=DPI)
plt.show()
plt.close()

# =====================================================
# 20. Airline Route Breadth vs Frequency (Scatter KPI)
# =====================================================
plt.figure(figsize=FIG_LARGE, dpi=DPI)

# Scatter
plt.scatter(
    airline_kpi["unique_routes"],
    airline_kpi["total_flights"],
    s=50,
    alpha=0.7,
    color="#1f77b4",
    edgecolors="white",
    linewidth=0.5,
)

# Median reference lines
plt.axvline(
    airline_kpi["unique_routes"].median(), linestyle="--", linewidth=1, color="gray"
)
plt.axhline(
    airline_kpi["total_flights"].median(), linestyle="--", linewidth=1, color="gray"
)

# Label only TOP airlines (by total flights)
top_airlines = airline_kpi.sort_values("total_flights", ascending=False).head(5)

for airline in top_airlines.index:
    plt.text(
        airline_kpi.loc[airline, "unique_routes"] + 0.5,
        airline_kpi.loc[airline, "total_flights"],
        airline,
        fontsize=7,
        weight="bold",
    )

plt.title(
    "Airline Strategy: Route Breadth vs Flight Frequency",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Number of Unique Routes")
plt.ylabel("Total Weekly Flights")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/20_airline_strategy_scatter.png", dpi=DPI)
plt.show()
plt.close()
