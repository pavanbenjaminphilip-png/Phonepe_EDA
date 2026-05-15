import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text

# --- Page Config ---
st.set_page_config(page_title="PhonePe Pulse Insights", layout="wide", page_icon="📈")

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0f0f1a; }
    .stTabs [data-baseweb="tab-list"] { gap: 16px; background-color: #1a1a2e; border-radius: 10px; padding: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 44px; background-color: transparent; border-radius: 8px;
        color: #aaa; font-weight: 600; padding: 0 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #6c5ce7 !important; color: white !important; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #6c5ce7;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h3 { color: #a29bfe; font-size: 14px; margin: 0 0 8px 0; }
    .metric-card h1 { color: white; font-size: 26px; margin: 0; }
    .insight-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #6c5ce7;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        color: #dfe6e9;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB Connection ---
DB_USER = "root"
DB_PASSWORD = "pavan"
DB_HOST = "localhost"
DB_NAME = "phonepe_pulse"

@st.cache_resource
def get_engine():
    return create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

engine = get_engine()

@st.cache_data
def run_query(sql):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)

@st.cache_data
def load_table(name):
    return pd.read_sql_table(name, engine)

# --- Load Tables ---
try:
    df_agg_trans  = load_table("aggregated_transaction")
    df_agg_user   = load_table("aggregated_user")
    df_agg_ins    = load_table("aggregated_insurance")
    df_map_trans  = load_table("map_transaction")
    df_map_user   = load_table("map_user")
    df_map_ins    = load_table("map_insurance")
    df_top_trans  = load_table("top_transaction")
    df_top_user   = load_table("top_user")
    df_top_ins    = load_table("top_insurance")
    data_ok = True
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    data_ok = False

# --- Header ---
st.markdown("""
<div style='text-align:center; padding:20px 0'>
    <h1 style='color:#a29bfe; font-size:2.5rem; margin:0'>📈 PhonePe Pulse</h1>
    <p style='color:#636e72; font-size:1.1rem'>Digital Payment Intelligence Dashboard · India</p>
</div>
""", unsafe_allow_html=True)

if not data_ok:
    st.stop()

# --- Sidebar ---
st.sidebar.markdown("### 🔍 Global Filters")
years = sorted(df_agg_trans['Year'].unique().tolist())
year  = st.sidebar.selectbox("Year", years, index=len(years)-1)
quarter = st.sidebar.select_slider("Quarter", options=[1, 2, 3, 4])
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 About")
st.sidebar.info("SQL-powered analytics dashboard built on PhonePe Pulse data covering transactions, users, and insurance across India.")

# --- KPI Row (SQL Aggregates) ---
kpi1 = run_query(f"SELECT SUM(Transaction_amount) as total FROM aggregated_transaction WHERE Year={year} AND Quarter={quarter}")
kpi2 = run_query(f"SELECT SUM(Transaction_count) as total FROM aggregated_transaction WHERE Year={year} AND Quarter={quarter}")
kpi3 = run_query(f"SELECT SUM(RegisteredUsers) as total FROM map_user WHERE Year={year} AND Quarter={quarter}")
kpi4 = run_query(f"SELECT SUM(Transaction_amount) as total FROM aggregated_insurance WHERE Year={year} AND Quarter={quarter}")

def fmt(val):
    if val is None or pd.isna(val): return "N/A"
    val = float(val)
    if val >= 1e12: return f"₹{val/1e12:.2f}T"
    if val >= 1e9:  return f"₹{val/1e9:.2f}B"
    if val >= 1e7:  return f"₹{val/1e7:.2f}Cr"
    if val >= 1e5:  return f"₹{val/1e5:.2f}L"
    return f"{val:,.0f}"

k1 = kpi1['total'].iloc[0] if not kpi1.empty else 0
k2 = kpi2['total'].iloc[0] if not kpi2.empty else 0
k3 = kpi3['total'].iloc[0] if not kpi3.empty else 0
k4 = kpi4['total'].iloc[0] if not kpi4.empty else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><h3>💰 Total Transaction Value</h3><h1>{fmt(k1)}</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><h3>🔢 Total Transactions</h3><h1>{fmt(k2)}</h1></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><h3>👥 Registered Users</h3><h1>{fmt(k3)}</h1></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><h3>🛡️ Insurance Volume</h3><h1>{fmt(k4)}</h1></div>", unsafe_allow_html=True)

st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💸 Transactions", "🗺️ Geo Insights", "👥 Users & Brands",
    "🛡️ Insurance", "📈 Trend Analysis", "🏆 Top Performers"
])

# ===================== TAB 1: TRANSACTIONS =====================
with tab1:
    st.subheader("Transaction Analysis · SQL Business Case")

    sql_trans_type = f"""
        SELECT Transaction_type, 
               SUM(Transaction_amount) AS Total_Amount,
               SUM(Transaction_count)  AS Total_Count
        FROM aggregated_transaction
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY Transaction_type
        ORDER BY Total_Amount DESC
    """
    df_type = run_query(sql_trans_type)

    sql_top_states = f"""
        SELECT State, 
               SUM(Transaction_amount) AS Total_Amount,
               SUM(Transaction_count)  AS Total_Count
        FROM aggregated_transaction
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY State
        ORDER BY Total_Amount DESC
        LIMIT 10
    """
    df_top_states = run_query(sql_top_states)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Payment Category Breakdown**")
        fig = px.pie(df_type, values='Total_Amount', names='Transaction_type',
                     hole=0.5, color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent', 
                          hovertemplate='<b>%{label}</b><br>Value: ₹%{value:,.2f}<br>Percentage: %{percent}')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          margin=dict(t=10, b=10, l=10, r=10),
                          uniformtext=dict(minsize=12, mode='hide'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Top 10 States by Transaction Value**")
        df_top_states['State'] = df_top_states['State'].str.title()
        fig2 = px.bar(df_top_states.sort_values('Total_Amount'), x='Total_Amount', y='State',
                      orientation='h', color='Total_Amount', color_continuous_scale='Viridis',
                      labels={'Total_Amount': 'Total (₹)', 'State': ''})
        fig2.update_traces(hovertemplate='<b>%{y}</b><br>Value: ₹%{x:,.2f}')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font_color='white', coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> Peer-to-Peer and Merchant Payments dominate transaction volumes. Maharashtra, Karnataka, and Telangana consistently lead in transaction value — key states for targeted marketing and infrastructure investment.</div>", unsafe_allow_html=True)
    
    with st.expander("🔍 View SQL Query"):
        st.code(sql_trans_type + "\n\n" + sql_top_states, language='sql')

# ===================== TAB 2: GEO INSIGHTS =====================
with tab2:
    st.subheader("Geographical Payment Trends · District Level")

    sql_state_map = f"""
        SELECT State, 
               SUM(Amount) AS Total_Amount,
               SUM(Count)  AS Total_Count
        FROM map_transaction
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY State
        ORDER BY Total_Amount DESC
    """
    df_state_map = run_query(sql_state_map)

    sql_top_districts = f"""
        SELECT District, State,
               SUM(Amount) AS Total_Amount,
               SUM(Count)  AS Total_Count
        FROM map_transaction
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY District, State
        ORDER BY Total_Amount DESC
        LIMIT 15
    """
    df_dist = run_query(sql_top_districts)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**State-wise Transaction Distribution**")
        df_state_map['State'] = df_state_map['State'].str.title()
        fig = px.bar(df_state_map.head(15).sort_values('Total_Amount'), 
                     x='Total_Amount', y='State', orientation='h',
                     color='Total_Amount', color_continuous_scale='Plasma',
                     labels={'Total_Amount': 'Total Amount (₹)', 'State': ''})
        fig.update_traces(hovertemplate='<b>%{y}</b><br>Value: ₹%{x:,.2f}')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Top 15 Districts by Transaction Value**")
        df_dist['District'] = df_dist['District'].str.title()
        df_dist['State'] = df_dist['State'].str.title()
        fig2 = px.scatter(df_dist, x='Total_Count', y='Total_Amount',
                          size='Total_Amount', color='State', hover_name='District',
                          labels={'Total_Count': 'Transaction Count', 'Total_Amount': 'Transaction Value (₹)'})
        fig2.update_traces(hovertemplate='<b>%{hovertext}</b> (%{marker.color})<br>Count: %{x:,.0f}<br>Value: ₹%{y:,.2f}')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> Metro districts (Bangalore Urban, Mumbai Suburban, Hyderabad) generate disproportionately high transaction values. Tier-2 cities show rapid growth in count but lower average values — an opportunity for micro-merchant expansion.</div>", unsafe_allow_html=True)

    with st.expander("🔍 View SQL Query"):
        st.code(sql_state_map + "\n\n" + sql_top_districts, language='sql')

# ===================== TAB 3: USERS =====================
with tab3:
    st.subheader("User Engagement & Mobile Brand Analysis")

    sql_brands = f"""
        SELECT Brand, 
               SUM(Transaction_count) AS Users,
               AVG(Percentage) AS Avg_Share
        FROM aggregated_user
        WHERE Year={year} AND Quarter={quarter} AND Brand IS NOT NULL
        GROUP BY Brand
        ORDER BY Users DESC
        LIMIT 12
    """
    df_brand = run_query(sql_brands)

    sql_user_states = f"""
        SELECT State, 
               SUM(RegisteredUsers) AS Total_Users,
               SUM(AppOpens) AS Total_AppOpens
        FROM map_user
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY State
        ORDER BY Total_Users DESC
        LIMIT 10
    """
    df_user_states = run_query(sql_user_states)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Mobile Brand Market Share**")
        if not df_brand.empty:
            fig = px.bar(df_brand.sort_values('Users'), x='Users', y='Brand', orientation='h',
                         color='Users', color_continuous_scale='Teal',
                         labels={'Users': 'User Count', 'Brand': ''})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='white', coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Brand data not available for {year} Q{quarter}. Try 2018-2022.")

    with col2:
        st.markdown("**Top 10 States: Registered Users**")
        if not df_user_states.empty:
            fig2 = px.bar(df_user_states.sort_values('Total_Users'), x='Total_Users', y='State', orientation='h',
                          color='Total_Users', color_continuous_scale='Sunset',
                          labels={'Total_Users': 'Registered Users', 'State': ''})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font_color='white', coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> Xiaomi and Samsung dominate the PhonePe user base, reflecting India's affordable smartphone market. Uttar Pradesh and Maharashtra have the highest registered user counts — key markets for user retention campaigns.</div>", unsafe_allow_html=True)

    with st.expander("🔍 View SQL Query"):
        st.code(sql_brands + "\n\n" + sql_user_states, language='sql')

# ===================== TAB 4: INSURANCE =====================
with tab4:
    st.subheader("Insurance Sector Performance")

    sql_ins_states = f"""
        SELECT State,
               SUM(Transaction_amount) AS Revenue,
               SUM(Transaction_count)  AS Policies
        FROM aggregated_insurance
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY State
        ORDER BY Revenue DESC
        LIMIT 10
    """
    df_ins_states = run_query(sql_ins_states)

    sql_ins_trend = """
        SELECT Year, Quarter,
               SUM(Transaction_count)  AS Policies,
               SUM(Transaction_amount) AS Revenue
        FROM aggregated_insurance
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
    """
    df_ins_trend = run_query(sql_ins_trend)
    if not df_ins_trend.empty:
        df_ins_trend['Period'] = df_ins_trend['Year'].astype(str) + " Q" + df_ins_trend['Quarter'].astype(str)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 10 States: Insurance Revenue**")
        if not df_ins_states.empty:
            fig = px.bar(df_ins_states.sort_values('Revenue'), x='Revenue', y='State', orientation='h',
                         color='Revenue', color_continuous_scale='Magma',
                         labels={'Revenue': 'Revenue (₹)', 'State': ''})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='white', coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insurance data available from 2020 onwards. Please select 2020-2023.")

    with col2:
        st.markdown("**Insurance Adoption Over Time**")
        if not df_ins_trend.empty:
            fig2 = px.area(df_ins_trend, x='Period', y='Policies', markers=True,
                           color_discrete_sequence=['#a29bfe'],
                           labels={'Period': '', 'Policies': 'Policies Issued'})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> Insurance transactions show explosive growth from 2020 onwards, driven by pandemic awareness. Karnataka and Maharashtra lead in premium revenue — indicating a more financially mature user base in these states.</div>", unsafe_allow_html=True)

    with st.expander("🔍 View SQL Query"):
        st.code(sql_ins_states + "\n\n" + sql_ins_trend, language='sql')

# ===================== TAB 5: TREND ANALYSIS =====================
with tab5:
    st.subheader("Year-over-Year Trend Analysis · Fraud & Growth Detection")

    sql_yoy = """
        SELECT Year, Quarter,
               SUM(Transaction_amount) AS Total_Amount,
               SUM(Transaction_count)  AS Total_Count
        FROM aggregated_transaction
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
    """
    df_yoy = run_query(sql_yoy)
    if not df_yoy.empty:
        df_yoy['Period'] = df_yoy['Year'].astype(str) + " Q" + df_yoy['Quarter'].astype(str)

    sql_growth = """
        SELECT a.Year, a.Quarter,
               SUM(a.Transaction_amount) AS Cur_Amt,
               SUM(b.Transaction_amount) AS Prev_Amt
        FROM aggregated_transaction a
        LEFT JOIN aggregated_transaction b
          ON a.State = b.State AND a.Transaction_type = b.Transaction_type
          AND a.Year = b.Year + 1 AND a.Quarter = b.Quarter
        GROUP BY a.Year, a.Quarter
        ORDER BY a.Year, a.Quarter
    """
    df_growth = run_query(sql_growth)
    if not df_growth.empty:
        df_growth['Period'] = df_growth['Year'].astype(str) + " Q" + df_growth['Quarter'].astype(str)
        df_growth['Growth_%'] = ((df_growth['Cur_Amt'] - df_growth['Prev_Amt']) / df_growth['Prev_Amt'] * 100).round(1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Transaction Volume Growth Over Time**")
        if not df_yoy.empty:
            fig = px.line(df_yoy, x='Period', y='Total_Amount', markers=True,
                          color_discrete_sequence=['#6c5ce7'],
                          labels={'Period': '', 'Total_Amount': 'Total Amount (₹)'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Year-over-Year Growth Rate (%)**")
        if not df_growth.empty:
            df_plot = df_growth.dropna(subset=['Growth_%'])
            fig2 = px.bar(df_plot, x='Period', y='Growth_%',
                          color='Growth_%', color_continuous_scale='RdYlGn',
                          labels={'Period': '', 'Growth_%': 'YoY Growth %'})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font_color='white', coloraxis_showscale=False)
            fig2.update_xaxes(tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> PhonePe transactions grew 6x from 2018 to 2023. COVID-19 (2020) caused a brief dip in Q1 but accelerated digital adoption from Q2 2020 onwards. Negative YoY growth quarters warrant fraud pattern investigation.</div>", unsafe_allow_html=True)

    with st.expander("🔍 View SQL Query"):
        st.code(sql_yoy + "\n\n" + sql_growth, language='sql')

# ===================== TAB 6: TOP PERFORMERS =====================
with tab6:
    st.subheader("Top Performers · States, Districts & Pin Codes")

    sql_top_pin = f"""
        SELECT Pincode, State,
               SUM(Amount) AS Amount,
               SUM(Count)  AS Count
        FROM top_transaction
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY Pincode, State
        ORDER BY Amount DESC
        LIMIT 15
    """
    df_top_pin = run_query(sql_top_pin)

    sql_top_user_dist = f"""
        SELECT Pincode, State,
               SUM(RegisteredUsers) AS Users
        FROM top_user
        WHERE Year={year} AND Quarter={quarter}
        GROUP BY Pincode, State
        ORDER BY Users DESC
        LIMIT 10
    """
    df_top_user_dist = run_query(sql_top_user_dist)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 15 Pincodes by Transaction Value**")
        if not df_top_pin.empty:
            fig = px.bar(df_top_pin.sort_values('Amount'), x='Amount', y='Pincode', orientation='h',
                         color='State', labels={'Amount': 'Total Amount (₹)', 'Pincode': 'Pincode / District'},
                         hover_data=['State', 'Count'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No top pincode data available for this period.")

    with col2:
        st.markdown("**Top 10 Pincodes by Registered Users**")
        if not df_top_user_dist.empty:
            fig2 = px.bar(df_top_user_dist.sort_values('Users'), x='Users', y='Pincode', orientation='h',
                          color='State', labels={'Users': 'Registered Users', 'Pincode': ''})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No top user district data available for this period.")

    st.markdown("<div class='insight-box'>💡 <b>Insight:</b> A small number of pin codes in Mumbai, Bangalore, and Hyderabad account for a large share of total transaction value — classic Pareto distribution. Targeted premium services in these areas can maximize ROI.</div>", unsafe_allow_html=True)

    with st.expander("🔍 View SQL Query"):
        st.code(sql_top_pin + "\n\n" + sql_top_user_dist, language='sql')

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align:center; color:#636e72; font-size:13px'>PhonePe Pulse Data Visualization · SQL-Powered · Built with Streamlit & Plotly</div>", unsafe_allow_html=True)
