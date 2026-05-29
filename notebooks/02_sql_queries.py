"""
Project 1: Marketing Funnel Dashboard
Option B: Run SQL queries directly in Python using sqlite3 (no extra install needed)
"""

import sqlite3
import pandas as pd
import os

# ── STEP 1: Load CSV and create in-memory SQLite database ─────────────────────
df = pd.read_csv('data/marketing_funnel_data.csv')

conn = sqlite3.connect(':memory:')
df.to_sql('marketing_funnel_data', conn, index=False, if_exists='replace')
print(f"Loaded {len(df)} rows into SQLite")
print(f"Columns: {list(df.columns)}\n")

# ── QUERY 1: Full Funnel Summary by Channel ────────────────────────────────────
q1 = """
SELECT
    channel,
    SUM(impressions)                                              AS total_impressions,
    SUM(clicks)                                                   AS total_clicks,
    SUM(leads)                                                    AS total_leads,
    SUM(customers)                                                AS total_customers,
    ROUND(SUM(spend_eur), 2)                                      AS total_spend_eur,
    ROUND(SUM(clicks) * 100.0 / NULLIF(SUM(impressions),0), 2)   AS ctr_pct,
    ROUND(SUM(leads)  * 100.0 / NULLIF(SUM(clicks),0), 2)        AS cvr_pct,
    ROUND(SUM(customers) * 100.0 / NULLIF(SUM(leads),0), 2)      AS close_rate_pct,
    ROUND(SUM(spend_eur) / NULLIF(SUM(customers),0), 2)           AS cac_eur
FROM marketing_funnel_data
GROUP BY channel
ORDER BY total_leads DESC;
"""
q1_df = pd.read_sql_query(q1, conn)
print("--- QUERY 1: Full Funnel Summary by Channel ---")
print(q1_df.to_string(index=False))
q1_df.to_csv('data/query1_funnel_summary.csv', index=False)
print("Saved to data/query1_funnel_summary.csv\n")

# ── QUERY 2: Monthly Trend by Channel ─────────────────────────────────────────
q2 = """
SELECT
    SUBSTR(week, 1, 7)       AS month,
    channel,
    SUM(leads)               AS monthly_leads,
    SUM(customers)           AS monthly_customers,
    ROUND(SUM(spend_eur),2)  AS monthly_spend_eur
FROM marketing_funnel_data
GROUP BY month, channel
ORDER BY month, channel;
"""
q2_df = pd.read_sql_query(q2, conn)
print("--- QUERY 2: Monthly Trend by Channel (first 10 rows) ---")
print(q2_df.head(10).to_string(index=False))
q2_df.to_csv('data/query2_monthly_trend.csv', index=False)
print("Saved to data/query2_monthly_trend.csv\n")

# ── QUERY 3: Weekly CAC — Paid Channels Only ──────────────────────────────────
q3 = """
SELECT
    week,
    channel,
    spend_eur,
    customers,
    ROUND(spend_eur / NULLIF(customers, 0), 2) AS cac_eur
FROM marketing_funnel_data
WHERE channel IN ('Google Ads', 'Facebook')
ORDER BY week, channel;
"""
q3_df = pd.read_sql_query(q3, conn)
print("--- QUERY 3: Weekly CAC Paid Channels (first 10 rows) ---")
print(q3_df.head(10).to_string(index=False))
q3_df.to_csv('data/query3_weekly_cac_paid.csv', index=False)
print("Saved to data/query3_weekly_cac_paid.csv\n")

# ── QUERY 4: Peak Week Per Channel ────────────────────────────────────────────
q4 = """
SELECT
    channel,
    week,
    leads AS peak_weekly_leads
FROM marketing_funnel_data
WHERE (channel, leads) IN (
    SELECT channel, MAX(leads)
    FROM marketing_funnel_data
    GROUP BY channel
)
ORDER BY peak_weekly_leads DESC;
"""
q4_df = pd.read_sql_query(q4, conn)
print("--- QUERY 4: Peak Week Per Channel ---")
print(q4_df.to_string(index=False))
q4_df.to_csv('data/query4_peak_week.csv', index=False)
print("Saved to data/query4_peak_week.csv\n")

conn.close()
print("All 4 queries complete. Results saved to /data folder.")
