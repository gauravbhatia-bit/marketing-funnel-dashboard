"""
Project 1: Marketing Funnel Dashboard
03_dashboard.py — Full dashboard using Matplotlib (dark theme)
Run from inside project1_marketing_funnel/ folder:
    python notebooks/03_dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ─────────────────────────────────────────────────────────────────
q1 = pd.read_csv('data/query1_funnel_summary.csv')
q2 = pd.read_csv('data/query2_monthly_trend.csv')
q3 = pd.read_csv('data/query3_weekly_cac_paid.csv')

# ── Colors ────────────────────────────────────────────────────────────────────
BG      = '#0F1117'
CARD_BG = '#1A1D2E'
WHITE   = '#FFFFFF'
GREY    = '#8B9BB4'
COLORS  = ['#4C9BE8','#2ECC71','#F1C40F','#E74C3C','#A855F7']

# ── Canvas ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 15), facecolor=BG)
fig.suptitle('Marketing Funnel Dashboard — 2024',
             fontsize=28, fontweight='bold', color=WHITE, y=0.98)
fig.text(0.5, 0.955, 'Source: Mock CRM & Paid Ads Data  |  PropTech SaaS Analytics',
         ha='center', fontsize=12, color=GREY)

gs = gridspec.GridSpec(3, 4, figure=fig,
                       top=0.93, bottom=0.07,
                       left=0.05, right=0.97,
                       hspace=0.6, wspace=0.45)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpi_colors = ['#4C9BE8','#2ECC71','#F1C40F','#E74C3C']
kpis = [
    ('Total Leads',     f"{int(q1['total_leads'].sum()):,}"),
    ('Total Customers', f"{int(q1['total_customers'].sum()):,}"),
    ('Total Spend',     f"€{q1['total_spend_eur'].sum():,.0f}"),
    ('Avg CAC',         f"€{q3['cac_eur'].mean():,.0f}"),
]
for i, ((label, value), col) in enumerate(zip(kpis, kpi_colors)):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(CARD_BG)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.axvline(x=0.04, color=col, linewidth=6)
    ax.text(0.5, 0.62, value, ha='center', va='center',
            fontsize=30, fontweight='bold', color=WHITE, transform=ax.transAxes)
    ax.text(0.5, 0.28, label, ha='center', va='center',
            fontsize=12, color=GREY, transform=ax.transAxes)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2A2F45')
        spine.set_linewidth(1.5)

# ── Line Chart: Monthly Leads by Channel ──────────────────────────────────────
ax2 = fig.add_subplot(gs[1, :2])
ax2.set_facecolor(CARD_BG)
pivot = q2.pivot_table(index='month', columns='channel', values='monthly_leads', aggfunc='sum')
pivot = pivot.sort_index()
x = range(len(pivot))
for idx, ch in enumerate(pivot.columns):
    ax2.plot(x, pivot[ch].values, marker='o', markersize=5,
             color=COLORS[idx], linewidth=2.2, label=ch)
xlabels = [m[5:] for m in pivot.index]
ax2.set_xticks(list(x))
ax2.set_xticklabels(xlabels, rotation=45, color=GREY, fontsize=8)
ax2.set_title('Monthly Leads by Channel', color=WHITE, fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Month', color=GREY, fontsize=9)
ax2.set_ylabel('Leads', color=GREY, fontsize=9)
ax2.tick_params(colors=GREY)
ax2.legend(fontsize=8, facecolor=CARD_BG, labelcolor=WHITE, loc='upper left', framealpha=0.5, ncol=2)
ax2.spines[['top','right']].set_visible(False)
ax2.spines[['left','bottom']].set_color('#2A2F45')
ax2.yaxis.grid(True, color='#2A2F45', linewidth=0.5)
ax2.set_axisbelow(True)

# ── Bar Chart: Customers by Channel ───────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 2:])
ax3.set_facecolor(CARD_BG)
q1s = q1.sort_values('total_customers', ascending=True)
bars = ax3.barh(q1s['channel'], q1s['total_customers'],
                color=COLORS[:len(q1s)], edgecolor='none', height=0.55)
for bar, val in zip(bars, q1s['total_customers']):
    ax3.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
             f'{int(val):,}', va='center', color=WHITE, fontsize=11, fontweight='bold')
ax3.set_title('Total Customers by Channel', color=WHITE, fontsize=13, fontweight='bold', pad=10)
ax3.set_xlabel('Total Customers', color=GREY, fontsize=9)
ax3.tick_params(colors=GREY)
ax3.spines[['top','right','left','bottom']].set_color('#2A2F45')
ax3.set_xlim(0, q1s['total_customers'].max() * 1.2)
ax3.xaxis.grid(True, color='#2A2F45', linewidth=0.5)
ax3.set_axisbelow(True)

# ── Line Chart: Weekly CAC Google vs Facebook ─────────────────────────────────
ax4 = fig.add_subplot(gs[2, :])
ax4.set_facecolor(CARD_BG)
for idx, ch in enumerate(['Google Ads', 'Facebook']):
    d = q3[q3['channel'] == ch].reset_index(drop=True)
    d['cac_smooth'] = d['cac_eur'].rolling(3, min_periods=1).mean()
    ax4.plot(d.index, d['cac_eur'], color=COLORS[idx], linewidth=1.2, alpha=0.3)
    ax4.plot(d.index, d['cac_smooth'], color=COLORS[idx], linewidth=2.5,
             label=f'{ch} (3-week avg)')
    ax4.fill_between(d.index, d['cac_smooth'], alpha=0.07, color=COLORS[idx])
    max_idx = d['cac_smooth'].idxmax()
    ax4.annotate(f"Peak €{d['cac_smooth'][max_idx]:.0f}",
                 xy=(max_idx, d['cac_smooth'][max_idx]),
                 xytext=(max_idx+1, d['cac_smooth'][max_idx]+15),
                 color=COLORS[idx], fontsize=8, fontweight='bold')
ax4.set_title('Weekly CAC — Google Ads vs Facebook (3-week rolling avg)',
              color=WHITE, fontsize=13, fontweight='bold', pad=10)
ax4.set_xlabel('Week (1–52)', color=GREY, fontsize=9)
ax4.set_ylabel('CAC (€)', color=GREY, fontsize=9)
ax4.tick_params(colors=GREY)
ax4.legend(fontsize=10, facecolor=CARD_BG, labelcolor=WHITE, framealpha=0.5)
ax4.spines[['top','right']].set_visible(False)
ax4.spines[['left','bottom']].set_color('#2A2F45')
ax4.yaxis.grid(True, color='#2A2F45', linewidth=0.5)
ax4.set_axisbelow(True)

# ── Save ──────────────────────────────────────────────────────────────────────
import os
os.makedirs('dashboards', exist_ok=True)
plt.savefig('dashboards/funnel_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.savefig('dashboards/funnel_dashboard.pdf', bbox_inches='tight',
            facecolor=BG, edgecolor='none')
print("Dashboard saved to dashboards/funnel_dashboard.png and .pdf")
# plt.show()  # ← Commenting out for terminal execution