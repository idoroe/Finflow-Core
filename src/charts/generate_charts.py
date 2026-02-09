"""
generate_charts.py — Creates 3 demo charts from ANALYTICS data in Snowflake.

HIGH-LEVEL EXPLANATION:
    This script connects to Snowflake, runs analytics queries, and turns
    the results into charts (PNG images) saved to the charts/ folder.

    Charts created:
      1. Monthly transaction volume (bar chart)
      2. Transaction type breakdown (pie chart)
      3. Performance improvement (before/after bar chart — no Snowflake needed)

WHY THIS MATTERS AT RBC:
    Data engineers often need to produce quick visualizations for stakeholders.
    matplotlib is the most common Python charting library. These charts could
    go into a slide deck, a Confluence page, or a Jupyter notebook.
"""

import logging
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend (no GUI window needed)
import matplotlib.pyplot as plt
from pathlib import Path

from src.config import get_snowflake_config
from src.load.snowflake_client import SnowflakeClient

logger = logging.getLogger("finflow.charts")

CHARTS_DIR = Path(__file__).resolve().parent.parent.parent / "charts"


def chart_monthly_volume(client: SnowflakeClient):
    """Bar chart: monthly transaction volume over time."""
    sql = """
    SELECT
        d.YEAR,
        d.MONTH,
        COUNT(*) AS TXN_COUNT
    FROM FINFLOW.ANALYTICS.FCT_TRANSACTIONS f
    JOIN FINFLOW.ANALYTICS.DIM_DATE d ON f.TRANSACTION_DATE = d.DATE_KEY
    GROUP BY d.YEAR, d.MONTH
    ORDER BY d.YEAR, d.MONTH
    """
    rows = client.execute(sql)
    labels = [f"{int(r[0])}-{int(r[1]):02d}" for r in rows]
    counts = [int(r[2]) for r in rows]

    # Show every 6th label to avoid crowding
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(range(len(counts)), counts, color="#2563eb", width=0.8)
    ax.set_xticks(range(0, len(labels), 6))
    ax.set_xticklabels(labels[::6], rotation=45, ha="right", fontsize=8)
    ax.set_title("Monthly Transaction Volume", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Transactions")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = CHARTS_DIR / "01_monthly_volume.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved: %s", path)


def chart_type_breakdown(client: SnowflakeClient):
    """Pie chart: credit vs debit transaction breakdown."""
    sql = """
    SELECT
        CASE TYPE
            WHEN 'PRIJEM' THEN 'Credit (PRIJEM)'
            WHEN 'VYDAJ' THEN 'Debit (VYDAJ)'
            ELSE TYPE
        END AS TXN_TYPE,
        COUNT(*) AS CNT
    FROM FINFLOW.ANALYTICS.FCT_TRANSACTIONS
    GROUP BY TYPE
    ORDER BY CNT DESC
    """
    rows = client.execute(sql)
    labels = [r[0] for r in rows]
    sizes = [int(r[1]) for r in rows]
    colors = ["#2563eb", "#dc2626", "#f59e0b", "#10b981"]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%",
        colors=colors[:len(labels)], startangle=90,
        textprops={"fontsize": 11}
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title("Transaction Type Breakdown", fontsize=14, fontweight="bold")
    fig.tight_layout()

    path = CHARTS_DIR / "02_type_breakdown.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved: %s", path)


def chart_performance():
    """Bar chart: query performance before/after clustering (no Snowflake needed)."""
    queries = ["Query 1\nMonthly Volume", "Query 2\nTop 10 Accounts", "Query 3\nDate Range"]
    before = [949, 546, 80]
    after = [312, 231, 101]

    x = range(len(queries))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar([i - width / 2 for i in x], before, width, label="Before Clustering", color="#94a3b8")
    bars2 = ax.bar([i + width / 2 for i in x], after, width, label="After Clustering (YEAR+MONTH)", color="#2563eb")

    # Add value labels on top of bars
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
                f"{int(bar.get_height())}ms", ha="center", fontsize=10)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
                f"{int(bar.get_height())}ms", ha="center", fontsize=10, fontweight="bold")

    ax.set_title("Query Performance: Before vs After Clustering", fontsize=14, fontweight="bold")
    ax.set_ylabel("Duration (ms)")
    ax.set_xticks(x)
    ax.set_xticklabels(queries, fontsize=10)
    ax.legend(fontsize=10)
    ax.set_ylim(0, max(before) * 1.2)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = CHARTS_DIR / "03_performance.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    logger.info("Saved: %s", path)


def generate_all_charts():
    """Generate all demo charts."""
    CHARTS_DIR.mkdir(exist_ok=True)
    logger.info("=== Generating Demo Charts ===")

    # Chart 3 doesn't need Snowflake
    chart_performance()

    # Charts 1 & 2 need Snowflake data
    sf_config = get_snowflake_config()
    with SnowflakeClient(sf_config) as client:
        chart_monthly_volume(client)
        chart_type_breakdown(client)

    logger.info("=== All charts saved to %s ===", CHARTS_DIR)


if __name__ == "__main__":
    from src.logging_config import setup_logging
    setup_logging()
    generate_all_charts()
