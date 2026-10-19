
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_sales_data, load_inventory_data
from forecasting import forecast_sales
from inventory import make_inventory_plan


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="DemandIQ | Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. PREMIUM DESIGN SYSTEM
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d19;
    --panel: #101827;
    --panel2: #131e30;
    --border: rgba(148, 163, 184, 0.16);
    --text: #e8eef8;
    --muted: #8b9bb3;
    --blue: #60a5fa;
    --cyan: #22d3ee;
    --green: #34d399;
    --orange: #fb923c;
    --red: #fb7185;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(37,99,235,0.10), transparent 38%),
        var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color: #f1f5f9 !important;
    letter-spacing: -0.6px;
}

p, label, .stCaption {
    color: var(--muted);
}

.brand {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f8fafc;
}

.brand span {
    color: #60a5fa;
}

.brand-sub {
    color: #8b9bb3;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 3px;
}

.hero {
    padding: 28px 30px;
    border: 1px solid rgba(96,165,250,0.23);
    border-radius: 20px;
    background:
        radial-gradient(circle at 85% 10%, rgba(34,211,238,0.15), transparent 28%),
        linear-gradient(115deg, #111b30 0%, #12264a 55%, #102d50 100%);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.hero-title {
    font-size: clamp(25px, 3vw, 37px);
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -1.3px;
    margin-bottom: 8px;
}

.hero-desc {
    font-size: 14px;
    color: #b5c7df;
    margin-bottom: 15px;
}

.eyebrow {
    font-size: 10px;
    color: #7dd3fc;
    letter-spacing: 2px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-pill {
    display: inline-block;
    padding: 6px 11px;
    border: 1px solid rgba(125,211,252,0.25);
    border-radius: 20px;
    color: #bae6fd;
    background: rgba(8,145,178,0.12);
    font-size: 11px;
    margin-right: 6px;
    margin-top: 3px;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #edf4ff;
    margin: 10px 0 3px 0;
}

.section-subtitle {
    color: #8495ad;
    font-size: 12px;
    margin-bottom: 16px;
}

.kpi {
    background: linear-gradient(145deg, #121d2e, #0f1726);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 18px 16px 18px;
    min-height: 132px;
    margin-bottom: 10px;
    transition: border-color 0.2s ease;
}

.kpi:hover {
    border-color: rgba(96,165,250,0.55);
}

.kpi-label {
    font-size: 11px;
    color: #94a3b8;
    font-weight: 600;
    margin-bottom: 12px;
}

.kpi-value {
    color: #f8fafc;
    font-size: clamp(21px, 2vw, 29px);
    font-weight: 800;
    letter-spacing: -0.8px;
    overflow-wrap: anywhere;
}

.kpi-note {
    color: #91a1b8;
    font-size: 11px;
    margin-top: 10px;
}

.kpi-blue { border-top: 2px solid #60a5fa; }
.kpi-cyan { border-top: 2px solid #22d3ee; }
.kpi-green { border-top: 2px solid #34d399; }
.kpi-orange { border-top: 2px solid #fb923c; }
.kpi-red { border-top: 2px solid #fb7185; }

.panel {
    background: #101827;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
}

div[data-testid="stMetric"] {
    background: #101827;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #9aabc2;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid rgba(96,165,250,0.4);
    background: #173763;
    color: #f8fafc;
    font-weight: 600;
    min-height: 40px;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: #60a5fa;
    background: #204a7e;
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: #101827;
    border-color: #29364a;
}

hr {
    border-color: var(--border);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .hero {
        padding: 20px;
    }
    .kpi {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. DATA LOADING
# =========================================================
@st.cache_data(show_spinner=False)
def get_data():
    sales_df = load_sales_data()
    inventory_df = load_inventory_data()
    return sales_df, inventory_df


def money(value):
    if pd.isna(value):
        value = 0
    return f"₹{value:,.0f}"


def number(value):
    if pd.isna(value):
        value = 0
    return f"{value:,.0f}"


def show_kpi(label, value, note, style="blue"):
    st.markdown(
        f"""
        <div class="kpi kpi-{style}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color="#cbd5e1",
            size=11,
        ),
        title=dict(
            font=dict(size=15, color="#f1f5f9"),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=15, r=15, t=55, b=15),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(
            bgcolor="#101827",
            font_color="#f8fafc",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(148,163,184,0.15)",
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zeroline=False,
    )

    return fig


def section_heading(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def csv_download_button(df, filename, label):
    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        key=f"download_{filename}",
    )


try:
    with st.spinner("Loading sales and inventory intelligence..."):
        sales, inventory = get_data()

except Exception as exc:
    st.error(f"Data loading error: {exc}")
    st.info(
        "Check filenames and columns in data/raw/. "
        "Expected files: enterprise_revenue_dataset.xlsx "
        "and inventory_planning_10000.xlsx."
    )
    st.stop()


# Validate expected output schema from data_loader.py
sales_required = {
    "date", "product_id", "product_name", "units_sold", "revenue"
}
inventory_required = {
    "date", "product_id", "warehouse", "current_stock",
    "reorder_point", "lead_time_days", "supplier_rating",
    "stock_status"
}

if not sales_required.issubset(sales.columns):
    st.error(
        "Sales data schema mismatch. Missing: "
        + str(sorted(sales_required - set(sales.columns)))
    )
    st.stop()

if not inventory_required.issubset(inventory.columns):
    st.error(
        "Inventory data schema mismatch. Missing: "
        + str(sorted(inventory_required - set(inventory.columns)))
    )
    st.stop()

sales = sales.copy()
inventory = inventory.copy()

sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
sales["units_sold"] = pd.to_numeric(
    sales["units_sold"], errors="coerce"
).fillna(0)
sales["revenue"] = pd.to_numeric(
    sales["revenue"], errors="coerce"
).fillna(0)

sales = sales.dropna(subset=["date", "product_id"])
sales["product_id"] = sales["product_id"].astype(str)
sales["product_name"] = sales["product_name"].astype(str)

inventory["date"] = pd.to_datetime(
    inventory["date"], errors="coerce"
)

if sales.empty:
    st.error("Sales dataset is empty after data cleaning.")
    st.stop()


# =========================================================
# 4. GLOBAL CALCULATIONS
# =========================================================
total_revenue = float(sales["revenue"].sum())
total_units = float(sales["units_sold"].sum())
product_count = int(sales["product_id"].nunique())

daily_revenue = (
    sales.groupby("date", as_index=False)
    .agg(revenue=("revenue", "sum"))
    .sort_values("date")
)

average_daily_revenue = (
    daily_revenue["revenue"].mean()
    if not daily_revenue.empty else 0
)

reorder_count = int(
    (inventory["current_stock"] <= inventory["reorder_point"]).sum()
)

matching_products = (
    set(sales["product_id"].astype(str))
    & set(inventory["product_id"].astype(str))
)

# Calculate recent revenue change only when enough history exists.
revenue_change = None

if len(daily_revenue) >= 60:
    latest_date = daily_revenue["date"].max()
    last_30_start = latest_date - pd.Timedelta("29 days")
    previous_30_start = latest_date - pd.Timedelta("59 days")
    previous_30_end = latest_date - pd.Timedelta("30 days")
                                                

    last_30 = daily_revenue.loc[
        daily_revenue["date"].between(last_30_start, latest_date),
        "revenue",
    ].sum()

    previous_30 = daily_revenue.loc[
        daily_revenue["date"].between(
            previous_30_start, previous_30_end
        ),
        "revenue",
    ].sum()

    if previous_30 != 0:
        revenue_change = (last_30 - previous_30) / previous_30 * 100


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">Demand<span>IQ</span></div>
        <div class="brand-sub">Intelligence Platform</div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Sales Intelligence",
            "AI Forecast Lab",
            "Inventory Control Tower",
            "Data Quality Center",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("#### DATA STATUS")
    st.caption(f"Sales records · {len(sales):,}")
    st.caption(f"Inventory records · {len(inventory):,}")
    st.caption(f"Products · {product_count:,}")

    st.divider()

    if st.button("↻ Refresh Data", use_container_width=True):
        get_data.clear()
        st.rerun()

    st.markdown(
        """
        <div style="font-size:10px;color:#72839b;margin-top:14px;">
        DEMANDIQ · PORTFOLIO EDITION<br>
        Forecasts are estimates, not guarantees.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 6. EXECUTIVE OVERVIEW
# =========================================================
if page == "Executive Overview":

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">EXECUTIVE COMMAND CENTER</div>
            <div class="hero-title">Sales & Inventory Intelligence</div>
            <div class="hero-desc">
                One workspace to understand business performance,
                anticipate demand and identify inventory risk.
            </div>
            <span class="hero-pill">● Data Connected</span>
            <span class="hero-pill">AI Forecasting</span>
            <span class="hero-pill">Inventory Analytics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading(
        "Business at a glance",
        "Key performance indicators calculated from your loaded datasets.",
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        show_kpi(
            "TOTAL REVENUE",
            money(total_revenue),
            "Revenue across available sales records",
            "blue",
        )

    with k2:
        show_kpi(
            "UNITS SOLD",
            number(total_units),
            "Total units in the sales dataset",
            "cyan",
        )

    with k3:
        show_kpi(
            "PRODUCTS",
            number(product_count),
            "Distinct product IDs in sales",
            "green",
        )

    with k4:
        show_kpi(
            "REORDER ALERTS",
            number(reorder_count),
            "Inventory records at or below reorder point",
            "red" if reorder_count else "green",
        )

    if revenue_change is not None:
        change_label = (
            f"{revenue_change:+.1f}% over the previous 30-day period"
        )
    else:
        change_label = "Insufficient history for a 30-day comparison"

    st.write("")

    left, right = st.columns([1.65, 1])

    with left:
        section_heading(
            "Revenue trajectory",
            "Daily revenue across the available dataset.",
        )

        fig = px.area(
            daily_revenue,
            x="date",
            y="revenue",
            color_discrete_sequence=["#60a5fa"],
        )

        fig.update_traces(
            line=dict(width=2.5),
            fillcolor="rgba(96,165,250,0.13)",
            hovertemplate="%{x|%d %b %Y}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )

        fig.update_layout(
            title="Daily revenue",
            yaxis_title="Revenue (₹)",
            xaxis_title="",
        )

        st.plotly_chart(
            style_chart(fig, 370),
            use_container_width=True,
        )

        st.caption(change_label)

    with right:
        section_heading(
            "Inventory health",
            "Share of inventory records requiring attention.",
        )

        stock_mix = (
            inventory.assign(
                status=np.where(
                    inventory["current_stock"] <= inventory["reorder_point"],
                    "Reorder",
                    "Healthy",
                )
            )["status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="records")
        )

        fig = px.pie(
            stock_mix,
            names="status",
            values="records",
            hole=0.68,
            color="status",
            color_discrete_map={
                "Reorder": "#fb7185",
                "Healthy": "#34d399",
            },
        )

        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            hovertemplate="%{label}<br>Records: %{value:,}<extra></extra>",
        )

        fig.update_layout(
            title="Stock status distribution",
            showlegend=False,
        )

        st.plotly_chart(
            style_chart(fig, 370),
            use_container_width=True,
        )

    st.write("")

    left, right = st.columns([1.2, 1])

    with left:
        section_heading(
            "Top products by revenue",
            "Products generating the highest recorded revenue.",
        )

        top_products = (
            sales.groupby("product_name", as_index=False)
            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
            )
            .nlargest(10, "revenue")
            .sort_values("revenue", ascending=True)
        )

        fig = px.bar(
            top_products,
            x="revenue",
            y="product_name",
            orientation="h",
            color="revenue",
            color_continuous_scale=[
                "#172554", "#2563eb", "#67e8f9"
            ],
            hover_data={"units_sold": ":,.0f", "revenue": ":,.0f"},
        )

        fig.update_layout(
            title="Revenue leaders",
            xaxis_title="Revenue (₹)",
            yaxis_title="",
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 390),
            use_container_width=True,
        )

    with right:
        section_heading(
            "Business signals",
            "Useful context for interpreting the current data.",
        )

        show_kpi(
            "AVERAGE DAILY REVENUE",
            money(average_daily_revenue),
            "Mean revenue across days represented in sales data",
            "cyan",
        )

        show_kpi(
            "PRODUCT ID OVERLAP",
            number(len(matching_products)),
            "Products present in both datasets",
            "green" if matching_products else "orange",
        )

        if not matching_products:
            st.warning(
                "Sales and inventory product IDs do not overlap. "
                "Product-level demand joining needs a mapping table."
            )

        elif len(matching_products) < product_count:
            st.info(
                "Some sales products do not appear in inventory. "
                "Review product coverage before relying on reorder estimates."
            )

    st.caption(
        "Revenue is the sum of the revenue column. Revenue change is shown "
        "only when enough daily history exists; it is not a forecast."
    )


# =========================================================
# 7. SALES INTELLIGENCE
# =========================================================
elif page == "Sales Intelligence":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">COMMERCIAL PERFORMANCE</div>
            <div class="hero-title">Sales Intelligence</div>
            <div class="hero-desc">
                Explore product performance, seasonality, promotions
                and the daily revenue pattern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sales_view = sales.copy()

    min_date = sales_view["date"].min().date()
    max_date = sales_view["date"].max().date()

    c1, c2, c3 = st.columns([1.2, 1.2, 1])

    with c1:
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="sales_date_range",
        )

    with c2:
        product_options = sorted(
            sales_view["product_name"].dropna().unique().tolist()
        )

        selected_products = st.multiselect(
            "Products",
            product_options,
            default=[],
            help="Leave empty to include all products.",
        )

    with c3:
        sales_metric = st.selectbox(
            "Chart metric",
            ["Revenue", "Units Sold"],
        )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range

        sales_view = sales_view[
            sales_view["date"].dt.date.between(start_date, end_date)
        ]

    if selected_products:
        sales_view = sales_view[
            sales_view["product_name"].isin(selected_products)
        ]

    if sales_view.empty:
        st.warning("No sales records match these filters.")
        st.stop()

    metric_col = (
        "revenue" if sales_metric == "Revenue" else "units_sold"
    )

    filtered_revenue = float(sales_view["revenue"].sum())
    filtered_units = float(sales_view["units_sold"].sum())

    a, b, c = st.columns(3)

    a.metric("Filtered Revenue", money(filtered_revenue))
    b.metric("Filtered Units", number(filtered_units))
    c.metric("Products in View", f"{sales_view['product_id'].nunique():,}")

    st.write("")

    trend = (
        sales_view.groupby("date", as_index=False)
        .agg(value=(metric_col, "sum"))
        .sort_values("date")
    )

    fig = px.line(
        trend,
        x="date",
        y="value",
        markers=False,
        color_discrete_sequence=["#22d3ee"],
    )

    fig.update_traces(
        line=dict(width=2.5),
        hovertemplate="%{x|%d %b %Y}<br>%{y:,.2f}<extra></extra>",
    )

    fig.update_layout(
        title=f"Daily {sales_metric} trend",
        xaxis_title="Date",
        yaxis_title=sales_metric,
    )

    st.plotly_chart(
        style_chart(fig, 390),
        use_container_width=True,
    )

    left, right = st.columns(2)

    with left:
        product_perf = (
            sales_view.groupby("product_name", as_index=False)
            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
            )
            .nlargest(12, metric_col)
            .sort_values(metric_col, ascending=True)
        )

        fig = px.bar(
            product_perf,
            x=metric_col,
            y="product_name",
            orientation="h",
            color=metric_col,
            color_continuous_scale=["#1e3a8a", "#60a5fa"],
        )

        fig.update_layout(
            title=f"Top products by {sales_metric.lower()}",
            xaxis_title=sales_metric,
            yaxis_title="",
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True,
        )

    with right:
        # Season and promotion are optional fields.
        # Show charts only when the original Excel contains them.
        source_path = (
            Path(__file__).resolve().parent
            / "data" / "raw" / "enterprise_revenue_dataset.xlsx"
        )

        try:
            raw_sales = pd.read_excel(source_path, nrows=1)
            raw_columns = set(raw_sales.columns.astype(str).str.strip())
        except Exception:
            raw_columns = set()

        if "season" in raw_columns:
            try:
                season_data = pd.read_excel(source_path)
                season_data["revenue"] = pd.to_numeric(
                    season_data["revenue"], errors="coerce"
                ).fillna(0)

                season_summary = (
                    season_data.groupby("season", as_index=False)
                    .agg(revenue=("revenue", "sum"))
                    .sort_values("revenue", ascending=False)
                )

                fig = px.bar(
                    season_summary,
                    x="season",
                    y="revenue",
                    color="revenue",
                    color_continuous_scale=["#164e63", "#22d3ee"],
                )

                fig.update_layout(
                    title="Revenue by season",
                    xaxis_title="Season",
                    yaxis_title="Revenue (₹)",
                    coloraxis_showscale=False,
                )

                st.plotly_chart(
                    style_chart(fig, 430),
                    use_container_width=True,
                )
            except Exception:
                st.info("Seasonal analysis is unavailable for this dataset.")
        else:
            weekday_data = trend.copy()
            weekday_data["day_of_week"] = (
                pd.to_datetime(weekday_data["date"]).dt.day_name()
            )

            weekday_summary = (
                weekday_data.groupby("day_of_week", as_index=False)
                .agg(value=("value", "mean"))
            )

            day_order = [
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"
            ]

            weekday_summary["day_of_week"] = pd.Categorical(
                weekday_summary["day_of_week"],
                categories=day_order,
                ordered=True,
            )
            weekday_summary = weekday_summary.sort_values("day_of_week")

            fig = px.bar(
                weekday_summary,
                x="day_of_week",
                y="value",
                color_discrete_sequence=["#818cf8"],
            )

            fig.update_layout(
                title=f"Average {sales_metric.lower()} by weekday",
                xaxis_title="Weekday",
                yaxis_title=f"Average {sales_metric}",
            )

            st.plotly_chart(
                style_chart(fig, 430),
                use_container_width=True,
            )

    st.write("")
    section_heading(
        "Filtered sales records",
        "Download the filtered dataset for additional analysis.",
    )

    st.dataframe(
        sales_view.sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    csv_download_button(
        sales_view,
        "demandiq_filtered_sales.csv",
        "⬇ Download filtered sales",
    )


# =========================================================
# 8. AI FORECAST LAB
# =========================================================
elif page == "AI Forecast Lab":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">MACHINE LEARNING WORKSPACE</div>
            <div class="hero-title">AI Forecast Lab</div>
            <div class="hero-desc">
                Generate demand forecasts and inspect model evaluation metrics.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    product_options = sorted(
        sales["product_name"].dropna().unique().tolist()
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        selection = st.selectbox(
            "Forecast product",
            ["All Products"] + product_options,
        )

    with col2:
        horizon = st.selectbox(
            "Forecast horizon",
            [7, 14, 21, 30],
            index=1,
            format_func=lambda x: f"{x} days",
        )

    selected_sales = sales.copy()

    if selection != "All Products":
        selected_sales = selected_sales[
            selected_sales["product_name"] == selection
        ]

    st.info(
        "The model uses the forecasting logic in forecasting.py. "
        "MAE and RMSE are evaluation metrics, not accuracy percentages."
    )

    try:
        with st.spinner("Training model and generating forecast..."):
            result = forecast_sales(
                selected_sales,
                horizon=horizon,
            )

        forecast_df = result["forecast"].copy()
        history_df = result["history"].copy()

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "HOLDOUT MAE",
            f"{result['mae']:,.2f}",
            help="Mean Absolute Error; lower is generally better.",
        )

        m2.metric(
            "HOLDOUT RMSE",
            f"{result['rmse']:,.2f}",
            help="Root Mean Squared Error; lower is generally better.",
        )

        m3.metric(
            "FORECAST HORIZON",
            f"{horizon} days",
            "Future demand estimate",
        )

        if "forecast_units" not in forecast_df.columns:
            st.error(
                "The forecast output does not contain forecast_units."
            )
            st.stop()

        forecast_df["forecast_units"] = pd.to_numeric(
            forecast_df["forecast_units"],
            errors="coerce",
        ).clip(lower=0)

        forecast_total = forecast_df["forecast_units"].sum()
        forecast_daily_avg = forecast_df["forecast_units"].mean()

        x1, x2 = st.columns(2)

        x1.metric(
            "Forecasted Units",
            number(forecast_total),
            f"Over the next {horizon} days",
        )

        x2.metric(
            "Average Forecast / Day",
            f"{forecast_daily_avg:,.1f}",
            "Model estimate",
        )

        fig = go.Figure()

        history_df = history_df.tail(150)

        fig.add_trace(
            go.Scatter(
                x=history_df["date"],
                y=history_df["units_sold"],
                mode="lines",
                name="Historical units",
                line=dict(color="#60a5fa", width=2.5),
                hovertemplate="%{x|%d %b %Y}<br>Actual: %{y:,.1f}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=forecast_df["date"],
                y=forecast_df["forecast_units"],
                mode="lines+markers",
                name="Forecast",
                line=dict(
                    color="#fb923c",
                    width=3,
                    dash="dash",
                ),
                marker=dict(size=6),
                hovertemplate="%{x|%d %b %Y}<br>Forecast: %{y:,.1f}<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"Demand projection · {selection}",
            xaxis_title="Date",
            yaxis_title="Units sold",
            hovermode="x unified",
        )

        st.plotly_chart(
            style_chart(fig, 460),
            use_container_width=True,
        )

        st.write("")
        section_heading(
            "Forecast output",
            "Model-generated daily estimates for the selected horizon.",
        )

        st.dataframe(
            forecast_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_download_button(
            forecast_df,
            "demandiq_sales_forecast.csv",
            "⬇ Download forecast CSV",
        )

        with st.expander("How to interpret the metrics"):
            st.markdown("""
            - **MAE:** Average absolute difference between predicted and actual values on the holdout period.
            - **RMSE:** Penalizes larger errors more heavily than MAE.
            - Lower values generally indicate smaller errors, but should be compared with a simple baseline.
            - This dashboard does not claim a percentage accuracy score.
            - Forecasts depend on the available history and model assumptions.
            """)

    except Exception as exc:
        st.error(f"Forecast generation failed: {exc}")
        st.caption(
            "Check the minimum-history requirement and the input/output "
            "schema in forecasting.py."
        )


# =========================================================
# 9. INVENTORY CONTROL TOWER
# =========================================================
elif page == "Inventory Control Tower":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">SUPPLY CHAIN OPERATIONS</div>
            <div class="hero-title">Inventory Control Tower</div>
            <div class="hero-desc">
                Identify stock risks, review replenishment quantities
                and inspect inventory by warehouse.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        with st.spinner("Calculating inventory recommendations..."):
            plan = make_inventory_plan(inventory, sales).copy()

        needed_columns = [
            "date", "product_id", "warehouse", "current_stock",
            "reorder_point", "lead_time_days", "supplier_rating",
            "estimated_daily_demand", "stock_status",
            "suggested_order_qty",
        ]

        missing = [
            column for column in needed_columns
            if column not in plan.columns
        ]

        if missing:
            st.error(
                "Inventory planner is missing columns: "
                + ", ".join(missing)
            )
            st.stop()

        plan["current_stock"] = pd.to_numeric(
            plan["current_stock"], errors="coerce"
        ).fillna(0)

        plan["reorder_point"] = pd.to_numeric(
            plan["reorder_point"], errors="coerce"
        ).fillna(0)

        plan["suggested_order_qty"] = pd.to_numeric(
            plan["suggested_order_qty"], errors="coerce"
        ).fillna(0)

        reorder_plan = plan[
            plan["stock_status"] == "Reorder"
        ].copy()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Inventory Records", f"{len(plan):,}")
        c2.metric("Reorder Alerts", f"{len(reorder_plan):,}")
        c3.metric(
            "Suggested Units to Order",
            number(reorder_plan["suggested_order_qty"].sum()),
        )

        average_rating = plan["supplier_rating"].mean()

        c4.metric(
            "Average Supplier Rating",
            f"{average_rating:.2f}/5" if pd.notna(average_rating) else "N/A",
        )

        st.write("")

        col1, col2, col3 = st.columns([1.2, 1, 1])

        warehouse_options = sorted(
            plan["warehouse"].dropna().astype(str).unique().tolist()
        )

        with col1:
            selected_warehouse = st.selectbox(
                "Warehouse",
                ["All Warehouses"] + warehouse_options,
            )

        with col2:
            selected_statuses = st.multiselect(
                "Stock status",
                ["Reorder", "Healthy"],
                default=["Reorder", "Healthy"],
            )

        with col3:
            search_product = st.text_input(
                "Search product ID",
                placeholder="e.g. P058",
            )

        filtered = plan.copy()

        if selected_warehouse != "All Warehouses":
            filtered = filtered[
                filtered["warehouse"].astype(str) == selected_warehouse
            ]

        filtered = filtered[
            filtered["stock_status"].isin(selected_statuses)
        ]

        if search_product.strip():
            filtered = filtered[
                filtered["product_id"].astype(str).str.contains(
                    search_product.strip(),
                    case=False,
                    na=False,
                )
            ]

        left, right = st.columns([1.2, 1])

        with left:
            stock_distribution = (
                filtered.assign(
                    stock_status=filtered["stock_status"].astype(str)
                )["stock_status"]
                .value_counts()
                .rename_axis("status")
                .reset_index(name="records")
            )

            fig = px.bar(
                stock_distribution,
                x="status",
                y="records",
                color="status",
                color_discrete_map={
                    "Reorder": "#fb7185",
                    "Healthy": "#34d399",
                },
            )

            fig.update_layout(
                title="Filtered inventory status",
                xaxis_title="",
                yaxis_title="Records",
                showlegend=False,
            )

            st.plotly_chart(
                style_chart(fig, 320),
                use_container_width=True,
            )

        with right:
            warehouse_summary = (
                filtered.groupby("warehouse", as_index=False)
                .agg(
                    current_stock=("current_stock", "sum"),
                    suggested_order_qty=("suggested_order_qty", "sum"),
                )
                .nlargest(10, "suggested_order_qty")
            )

            fig = px.bar(
                warehouse_summary,
                x="warehouse",
                y="suggested_order_qty",
                color="suggested_order_qty",
                color_continuous_scale=["#7c2d12", "#fb923c"],
            )

            fig.update_layout(
                title="Suggested order quantity by warehouse",
                xaxis_title="Warehouse",
                yaxis_title="Suggested units",
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                style_chart(fig, 320),
                use_container_width=True,
            )

        st.write("")
        section_heading(
            "Replenishment recommendations",
            "Review the highest suggested order quantities first.",
        )

        display_columns = [
            "date",
            "product_id",
            "warehouse",
            "current_stock",
            "reorder_point",
            "lead_time_days",
            "supplier_rating",
            "estimated_daily_demand",
            "stock_status",
            "suggested_order_qty",
        ]

        filtered = filtered.sort_values(
            "suggested_order_qty",
            ascending=False,
        )

        st.dataframe(
            filtered[display_columns],
            use_container_width=True,
            hide_index=True,
        )

        csv_download_button(
            filtered[display_columns],
            "demandiq_inventory_recommendations.csv",
            "⬇ Download inventory recommendations",
        )

        st.caption(
            "Order quantities are planning estimates. Validate supplier "
            "minimum order quantities, open purchase orders and actual "
            "warehouse constraints before ordering."
        )

    except Exception as exc:
        st.error(f"Inventory planning failed: {exc}")


# =========================================================
# 10. DATA QUALITY CENTER
# =========================================================
elif page == "Data Quality Center":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">DATA GOVERNANCE</div>
            <div class="hero-title">Data Quality Center</div>
            <div class="hero-desc">
                Review dataset coverage, missing values and product ID overlap
                before relying on business recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overlap = (
        set(sales["product_id"].astype(str))
        & set(inventory["product_id"].astype(str))
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Sales Rows", f"{len(sales):,}")
    c2.metric("Inventory Rows", f"{len(inventory):,}")
    c3.metric("Sales Products", f"{sales['product_id'].nunique():,}")
    c4.metric("Matching Product IDs", f"{len(overlap):,}")

    st.write("")

    sales_quality = pd.DataFrame({
        "column": sales.columns,
        "missing_values": [
            int(sales[column].isna().sum())
            for column in sales.columns
        ],
        "missing_percent": [
            round(float(sales[column].isna().mean() * 100), 2)
            for column in sales.columns
        ],
        "data_type": [
            str(sales[column].dtype)
            for column in sales.columns
        ],
    })

    inventory_quality = pd.DataFrame({
        "column": inventory.columns,
        "missing_values": [
            int(inventory[column].isna().sum())
            for column in inventory.columns
        ],
        "missing_percent": [
            round(float(inventory[column].isna().mean() * 100), 2)
            for column in inventory.columns
        ],
        "data_type": [
            str(inventory[column].dtype)
            for column in inventory.columns
        ],
    })

    left, right = st.columns(2)

    with left:
        section_heading("Sales data profile")
        st.write(
            f"**Date coverage:** {sales['date'].min().date()} "
            f"to {sales['date'].max().date()}"
        )
        st.write(f"**Unique products:** {sales['product_id'].nunique():,}")
        st.dataframe(
            sales_quality,
            use_container_width=True,
            hide_index=True,
        )

    with right:
        section_heading("Inventory data profile")
        st.write(
            f"**Date coverage:** {inventory['date'].min().date()} "
            f"to {inventory['date'].max().date()}"
        )
        st.write(
            f"**Warehouses:** {inventory['warehouse'].nunique():,}"
        )
        st.dataframe(
            inventory_quality,
            use_container_width=True,
            hide_index=True,
        )

    st.write("")

    if not overlap:
        st.warning(
            "No product IDs overlap between sales and inventory. "
            "Forecasting and stock alerts can run independently, but "
            "product-level demand-based replenishment is not validated."
        )
    else:
        st.success(
            f"{len(overlap):,} product IDs exist in both datasets."
        )

    if sales["date"].duplicated().any():
        st.info(
            "Sales data contains multiple records per date, which is "
            "normal when multiple products are sold on the same day."
        )

    negative_sales = int(
        (
            (sales["units_sold"] < 0)
            | (sales["revenue"] < 0)
        ).sum()
    )

    if negative_sales:
        st.warning(
            f"{negative_sales:,} sales rows have negative units or revenue."
        )
    else:
        st.success("No negative units or revenue found in the cleaned sales data.")

    st.markdown("### Methodology & limitations")

    st.markdown("""
    - **Sales preparation:** records are grouped by date and product.
    - **Forecasting:** the model implementation is maintained in `forecasting.py`.
    - **Evaluation:** MAE and RMSE are used to describe holdout errors.
    - **Inventory:** current stock is compared with the reorder point.
    - **Recommendations:** suggested quantities are estimates, not purchase orders.
    - **Data quality:** matching product IDs are required for meaningful product-level joins.
    - **Production readiness:** monitor forecast drift, compare against baselines,
      and validate recommendations with real purchasing constraints.
    """)

    csv_download_button(
        sales_quality,
        "demandiq_sales_data_quality.csv",
        "⬇ Download sales quality report",
    )

    csv_download_button(
        inventory_quality,
        "demandiq_inventory_data_quality.csv",
        "⬇ Download inventory quality report",
    )


# =========================================================
# 11. FOOTER
# =========================================================
st.divider()

st.markdown(
    """
    <div style="
        display:flex;
        justify-content:space-between;
        flex-wrap:wrap;
        gap:8px;
        color:#718198;
        font-size:11px;
        padding:5px 0 10px 0;
    ">
        <span><b style="color:#93c5fd;">DemandIQ</b> · Sales & Inventory Intelligence</span>
        <span>Decision support only · Validate forecasts before operational use</span>
    </div>
    """,
    unsafe_allow_html=True,
)
