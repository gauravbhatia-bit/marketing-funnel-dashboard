"""
Project 1: Marketing Funnel Dashboard
Step-by-step analysis script
"""
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ── Set up paths ──────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, 'data', 'marketing_funnel_data.csv')
dashboards_path = os.path.join(project_root, 'dashboards')

# ── STEP 1: Load Data ─────────────────────────────────────────────────────────
df = pd.read_csv(data_path)
df['week'] = pd.to_datetime(df['week'])
df['month'] = df['week'].dt.to_period('M').astype(str)
print(f"Loaded {len(df)} rows | {df['channel'].nunique()} channels | {df['week'].nunique()} weeks")

# ── STEP 2: Funnel Overview ───────────────────────────────────────────────────
# Total funnel by channel
funnel_summary = df.groupby('channel').agg(
    total_impressions=('impressions', 'sum'),
    total_clicks=('clicks', 'sum'),
    total_leads=('leads', 'sum'),
    total_customers=('customers', 'sum'),
    total_spend=('spend_eur', 'sum')
).reset_index()
funnel_summary['ctr_pct']      = (funnel_summary['total_clicks'] / funnel_summary['total_impressions'] * 100).round(2)
funnel_summary['cvr_pct']      = (funnel_summary['total_leads'] / funnel_summary['total_clicks'] * 100).round(2)
funnel_summary['close_rate']   = (funnel_summary['total_customers'] / funnel_summary['total_leads'] * 100).round(2)
funnel_summary['cac_eur']      = (funnel_summary['total_spend'] / funnel_summary['total_customers'].replace(0, np.nan)).round(2)
print("\n--- Funnel Summary by Channel ---")
print(funnel_summary.to_string(index=False))

# ── STEP 3: Monthly Trend — Leads by Top 3 Channels ──────────────────────────
top3 = ['Google Ads', 'Meta Ads', 'Organic']
monthly = df[df['channel'].isin(top3)].groupby(['month','channel'])['leads'].sum().reset_index()
fig1 = px.line(monthly, x='month', y='leads', color='channel', markers=True,
               title='Monthly Leads by Top 3 Channels (2024)')
fig1.update_xaxes(title_text='Month', tickangle=45)
fig1.update_yaxes(title_text='Leads')
fig1.write_image(os.path.join(dashboards_path, 'chart1_leads_by_channel.png'))
print("\nChart 1 saved: Monthly Leads by Channel")

# ── STEP 4: CAC Trend — Google vs Meta ───────────────────────────────────────
paid = df[df['channel'].isin(['Google Ads','Meta Ads'])].copy()
cac_m = paid.groupby(['month','channel']).agg(
    spend=('spend_eur','sum'), customers=('customers','sum')
).reset_index()
cac_m['cac'] = (cac_m['spend'] / cac_m['customers'].replace(0, np.nan)).round(2)
fig2 = px.line(cac_m.dropna(), x='month', y='cac', color='channel', markers=True,
               title='Monthly CAC: Google Ads vs Meta Ads (2024)')
fig2.update_xaxes(title_text='Month', tickangle=45)
fig2.update_yaxes(title_text='CAC (€)')
fig2.write_image(os.path.join(dashboards_path, 'chart2_cac_comparison.png'))
print("Chart 2 saved: Monthly CAC Comparison")

# ── STEP 5: Export Summary Table ─────────────────────────────────────────────
funnel_summary.to_csv(os.path.join(project_root, 'data', 'funnel_summary_by_channel.csv'), index=False)
print("\nFunnel summary exported to data/funnel_summary_by_channel.csv")
print("\n✅ Analysis complete!")
