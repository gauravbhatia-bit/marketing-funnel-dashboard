# 📊 Marketing Funnel Dashboard

A data analytics project simulating a real-world B2C marketing funnel for a PropTech SaaS startup (modelled on MYNE Homes-style co-ownership platforms).

## Business Context
Marketing teams in SaaS/PropTech startups need to track how leads move through their funnel — from first impression to paying customer — across multiple acquisition channels. This project builds the full analytics layer for that funnel.

## Tools Used
| Layer | Tool |
|---|---|
| Data Generation & Analysis | Python (Pandas, NumPy) |
| SQL Transformations | SQLite / dbt-style .sql files |
| Visualisation | Power BI / Plotly |
| Version Control | Git + GitHub |

## Key Metrics Tracked
- **Impressions → Clicks → Leads → Customers** (full funnel)
- **CTR** (Click-Through Rate)
- **CVR** (Lead Conversion Rate)
- **CAC** (Customer Acquisition Cost) per channel
- **Weekly & Monthly trend analysis**

## Project Structure
```
project1_marketing_funnel/
├── data/
│   └── marketing_funnel_data.csv      # Raw mock dataset (260 rows, 52 weeks × 5 channels)
├── notebooks/
│   └── 01_funnel_analysis.py          # Step-by-step analysis script
├── sql/
│   └── funnel_summary.sql             # SQL aggregation queries
├── dashboards/
│   └── funnel_dashboard.pbix          # Power BI dashboard (instructions below)
└── README.md
```

## How to Run
1. Clone the repo: `git clone https://github.com/gauravbhatia-bit/marketing-funnel-dashboard`
2. Install dependencies: `pip install pandas numpy plotly`
3. Run analysis: `python notebooks/01_funnel_analysis.py`
4. Open Power BI and load `data/marketing_funnel_data.csv`

## Key Insights from the Data
- Google Ads consistently drives the highest lead volume
- Meta Ads has higher CAC volatility — peaks in Q3
- Organic channel delivers leads at zero cost — highest ROI channel
- Average funnel conversion rate: ~4.5% (click to customer)

## CV/Portfolio Description
> *"Built a marketing funnel analytics dashboard tracking 5 acquisition channels across 52 weeks, surfacing CAC trends and lead conversion rates for a PropTech SaaS startup using Python, SQL, and Power BI."*
