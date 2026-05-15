import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import mysql.connector

# --- Page Config ---
st.set_page_config(page_title="PhonePe Pulse Insights", layout="wide", page_icon="📈")

# --- Custom CSS for better aesthetics ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6c5ce7;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Database Connection ---
DB_USER = "root"
DB_PASSWORD = "pavan"
DB_HOST = "localhost"
DB_NAME = "phonepe_pulse"

@st.cache_resource
def get_engine():
    return create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

engine = get_engine()

# --- Data Loading ---
@st.cache_data
def load_data(table_name):
    return pd.read_sql(table_name, engine)

# --- App Header ---
st.title("📈 PhonePe Pulse: Digital Payment Insights")
st.markdown("Explore the pulse of digital transactions across India with interactive visualizations.")

# --- Sidebar Filters ---
st.sidebar.image("https://www.phonepe.com/en/assets/images/phonepe-logo.svg", width=150)
st.sidebar.markdown("---")
st.sidebar.header("🔍 Global Filters")

# Global Filters
year_list = [2018, 2019, 2020, 2021, 2022, 2023]
year = st.sidebar.selectbox("Select Year", year_list, index=5)
quarter = st.sidebar.select_slider("Select Quarter", options=[1, 2, 3, 4], value=1)

# --- Data Loading ---
df_agg_trans = load_data("aggregated_transaction")
df_map_trans = load_data("map_transaction")
df_agg_user = load_data("aggregated_user")
df_map_user = load_data("map_user")
df_agg_ins = load_data("aggregated_insurance")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["💸 Transactions", "👥 Users", "🛡️ Insurance"])

# --- Helper Functions ---
def format_amount(amount):
    if amount >= 1e7:
        return f"₹{amount/1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"₹{amount/1e5:.2f} L"
    else:
        return f"₹{amount:.2f}"

# --- Tab 1: Transactions ---
with tab1:
    st.header("Transaction Analysis")
    
    # Filtered Data
    filtered_df = df_agg_trans[(df_agg_trans['Year'] == year) & (df_agg_trans['Quarter'] == quarter)]
    
    if not filtered_df.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Distribution by Category")
            fig_type = px.pie(filtered_df, values='Transaction_amount', names='Transaction_type', 
                              hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_type.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_type, use_container_width=True)
            
        with col2:
            st.subheader("Top 10 States (By Amount)")
            state_amt = filtered_df.groupby('State')['Transaction_amount'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_state = px.bar(state_amt, x='Transaction_amount', y='State', orientation='h',
                               color='Transaction_amount', color_continuous_scale='Viridis',
                               labels={'Transaction_amount': 'Total Amount', 'State': 'State'})
            fig_state.update_layout(showlegend=False)
            st.plotly_chart(fig_state, use_container_width=True)

        st.markdown("---")
        st.subheader("District-wise Deep Dive")
        filtered_map = df_map_trans[(df_map_trans['Year'] == year) & (df_map_trans['Quarter'] == quarter)]
        fig_dist = px.scatter(filtered_map, x='Count', y='Amount', size='Amount', hover_name='District',
                              color='State', title=f"Transaction Volume vs Value (Q{quarter} {year})",
                              labels={'Count': 'Transaction Count', 'Amount': 'Transaction Value'})
        st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.info(f"No transaction data found for {year} Q{quarter}")

# --- Tab 2: Users ---
with tab2:
    st.header("User Insights")
    
    filtered_user = df_agg_user[(df_agg_user['Year'] == year) & (df_agg_user['Quarter'] == quarter)]
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("Mobile Brand Preference")
        if not filtered_user.empty:
            brand_df = filtered_user.groupby('Brand')['Transaction_count'].sum().reset_index().sort_values(by='Transaction_count', ascending=True)
            fig_brand = px.bar(brand_df, x='Transaction_count', y='Brand', orientation='h', 
                               color='Transaction_count', color_continuous_scale='Bluered')
            st.plotly_chart(fig_brand, use_container_width=True)
        else:
            st.warning(f"Brand data is not available for {year}. PhonePe stopped reporting brand-specific data in recent years.")
            st.info("Try selecting a year between 2018 and 2022 to see brand trends.")
        
    with col4:
        st.subheader("Registered Users per State (Top 10)")
        map_user_filtered = df_map_user[(df_map_user['Year'] == year) & (df_map_user['Quarter'] == quarter)]
        if not map_user_filtered.empty:
            state_users = map_user_filtered.groupby('State')['RegisteredUsers'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_state_users = px.bar(state_users, x='RegisteredUsers', y='State', orientation='h',
                                     color='RegisteredUsers', color_continuous_scale='Teal')
            st.plotly_chart(fig_state_users, use_container_width=True)
        else:
            st.info("No user registration data found for this period.")

# --- Tab 3: Insurance ---
with tab3:
    st.header("Insurance Sector Performance")
    
    filtered_ins = df_agg_ins[(df_agg_ins['Year'] == year) & (df_agg_ins['Quarter'] == quarter)]
    
    if not filtered_ins.empty:
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("Top 10 States (Insurance Revenue)")
            ins_state = filtered_ins.groupby('State')['Transaction_amount'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_ins = px.bar(ins_state, x='Transaction_amount', y='State', orientation='h', 
                             color='Transaction_amount', color_continuous_scale='Magma')
            st.plotly_chart(fig_ins, use_container_width=True)
            
        with col6:
            st.subheader("Overall Insurance Adoption Trend")
            ins_trend = df_agg_ins.groupby('Year')['Transaction_count'].sum().reset_index()
            fig_ins_trend = px.line(ins_trend, x='Year', y='Transaction_count', markers=True, 
                                    line_shape='spline', render_mode='svg')
            st.plotly_chart(fig_ins_trend, use_container_width=True)
    else:
        st.info(f"Insurance data reporting started later in the dataset. Please check 2020-2023.")

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>PhonePe Pulse Data Visualization Project | Created for Data Analysis Portfolio</div>", unsafe_allow_html=True)
