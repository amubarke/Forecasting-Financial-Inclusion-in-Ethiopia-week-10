# dashboard/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class FinancialInclusionDashboard:
    def __init__(self, data, forecasts, association_matrix):
        self.data = data
        self.forecasts = forecasts
        self.association_matrix = association_matrix

    # ---------------- Overview Page ----------------
    def overview_page(self):
        st.title("Financial Inclusion Dashboard - Overview")
        st.markdown("### Key Metrics")
        # Example metrics cards
        access_latest = self.data[self.data['indicator']=='ACCESS']['value_numeric'].iloc[-1]
        usage_latest = self.data[self.data['indicator']=='USAGE']['value_numeric'].iloc[-1]
        st.metric("Account Ownership (ACCESS)", f"{access_latest}%")
        st.metric("Digital Payment Usage (USAGE)", f"{usage_latest}%")
        
        st.markdown("### Growth Highlights")
        # Compute simple growth rates
        self.data['fiscal_year'] = pd.to_numeric(self.data['fiscal_year'], errors='coerce')
        growth_access = self.data[self.data['indicator']=='ACCESS']['value_numeric'].pct_change().iloc[-1]*100
        growth_usage = self.data[self.data['indicator']=='USAGE']['value_numeric'].pct_change().iloc[-1]*100
        st.metric("ACCESS Growth Rate", f"{growth_access:.2f}%")
        st.metric("USAGE Growth Rate", f"{growth_usage:.2f}%")
    
    # ---------------- Trends Page ----------------
    def trends_page(self):
        st.title("Trends Over Time")
        indicator = st.selectbox("Select Indicator", ["ACCESS","USAGE"])
        df = self.data[self.data['indicator']==indicator]
        date_min = df['fiscal_year'].min()
        date_max = df['fiscal_year'].max()
        selected_range = st.slider("Select Year Range", int(date_min), int(date_max), (int(date_min), int(date_max)))
        df_filtered = df[(df['fiscal_year']>=selected_range[0]) & (df['fiscal_year']<=selected_range[1])]
        
        st.line_chart(df_filtered.set_index('fiscal_year')['value_numeric'])
    
    # ---------------- Forecasts Page ----------------
    def forecasts_page(self):
        st.title("Forecasts")
        scenario = st.selectbox("Scenario", ["Base","Optimistic","Pessimistic"])
        for indicator, df in self.forecasts.items():
            st.subheader(f"{indicator} Forecast - {scenario} Scenario")
            forecast_df = df[scenario]
            st.line_chart(forecast_df.set_index('fiscal_year')['value_with_events'])
    
    # ---------------- Inclusion Projections Page ----------------
    def projections_page(self):
        st.title("Financial Inclusion Projections")
        target = 60
        scenario = st.selectbox("Scenario", ["Base","Optimistic","Pessimistic"], key="proj_scenario")
        for indicator, df in self.forecasts.items():
            forecast_df = df[scenario]
            st.subheader(f"{indicator} Projection - {scenario}")
            forecast_df['progress'] = forecast_df['value_with_events']/target*100
            st.bar_chart(forecast_df.set_index('fiscal_year')['progress'])
    
    # ---------------- Main Runner ----------------
    def run(self):
        page = st.sidebar.selectbox("Select Page", ["Overview","Trends","Forecasts","Projections"])
        if page=="Overview":
            self.overview_page()
        elif page=="Trends":
            self.trends_page()
        elif page=="Forecasts":
            self.forecasts_page()
        elif page=="Projections":
            self.projections_page()


# ---------------- Streamlit Runner ----------------
if __name__=="__main__":
    # Load your prepared data
    data = pd.read_csv("../data/raw/ethiopia_fi_unified_data.csv")
    # Forecasts dictionary example: {"ACCESS": {"Base": df_base, "Optimistic": df_opt, "Pessimistic": df_pes}}
    forecasts = pd.read_pickle("../data/forecasts.pkl")
    association_matrix = pd.read_pickle("../data/association_matrix.pkl")

    dashboard = FinancialInclusionDashboard(data, forecasts, association_matrix)
    dashboard.run()
