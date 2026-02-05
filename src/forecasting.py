import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class AccessUsageForecaster:
    def __init__(self, original_data, association_matrix):
        self.data = original_data
        self.association_matrix = association_matrix
        self.indicator_map = {"ACCESS":"Account Ownership Rate", "USAGE":"Digital Payment Usage"}
        self.forecast_results = {}

    def prepare_historical_data(self, indicator):
        indicator_name = self.indicator_map[indicator]
        df = self.data[self.data['indicator'] == indicator_name][['fiscal_year','value_numeric']].copy()
    
    # Ensure numeric
        df['fiscal_year'] = pd.to_numeric(df['fiscal_year'], errors='coerce')
        df['value_numeric'] = pd.to_numeric(df['value_numeric'], errors='coerce')
    
    # Drop rows with missing or invalid data
        df = df.dropna(subset=['fiscal_year','value_numeric'])
    
        if df.empty:
           print(f"⚠ Warning: No historical data for {indicator_name}. Using baseline=0.")
        df = pd.DataFrame({'fiscal_year':[2024], 'value_numeric':[0]})
        
        df = df.groupby('fiscal_year').mean().reset_index()
        df.rename(columns={'value_numeric':'value'}, inplace=True)
        return df



    def fit_trend(self, hist_df):
        X = hist_df['fiscal_year'].values.reshape(-1,1)
        y = hist_df['value'].values
        model = LinearRegression()
        model.fit(X, y)
        # residual std for confidence interval
        residual_std = np.std(y - model.predict(X))
        return model, residual_std

    def apply_events(self, forecast_df, indicator, events_to_apply, scaling=1.0):
        assoc = self.association_matrix.reset_index()[['indicator_event', indicator]].copy()
        assoc = assoc[assoc['indicator_event'].isin(events_to_apply)]
        event_impacts = dict(zip(assoc['indicator_event'], assoc[indicator]))
        forecast_df['value_with_events'] = forecast_df['trend_value']
        for event, impact in event_impacts.items():
            if pd.notna(impact):
                forecast_df['value_with_events'] += impact * scaling
        return forecast_df

    def forecast(self, indicator, events_to_apply=[], start_year=2025, end_year=2027):
        hist_df = self.prepare_historical_data(indicator)
        trend_model, residual_std = self.fit_trend(hist_df)

        years = np.arange(start_year, end_year+1)
        forecast_df = pd.DataFrame({'fiscal_year': years})
        forecast_df['trend_value'] = trend_model.predict(years.reshape(-1,1))

        # confidence interval
        forecast_df['ci_lower'] = forecast_df['trend_value'] - 1.96*residual_std
        forecast_df['ci_upper'] = forecast_df['trend_value'] + 1.96*residual_std

        # scenarios
        scenarios = {}
        for scenario, scale in [('Base',1.0), ('Optimistic',1.5), ('Pessimistic',0.5)]:
            scenarios[scenario] = self.apply_events(forecast_df.copy(), indicator, events_to_apply, scaling=scale)

        self.forecast_results[indicator] = {'forecast_df': forecast_df, 'scenarios': scenarios}
        return self.forecast_results[indicator]

    def plot_forecast(self, indicator):
        results = self.forecast_results.get(indicator)
        if not results:
            print("Run forecast() first")
            return

        df = results['forecast_df']
        plt.figure(figsize=(8,5))
        plt.plot(df['fiscal_year'], df['trend_value'], marker='o', label='Trend')
        plt.fill_between(df['fiscal_year'], df['ci_lower'], df['ci_upper'], color='gray', alpha=0.2, label='95% CI')

        # plot scenarios
        for scenario, scen_df in results['scenarios'].items():
            plt.plot(scen_df['fiscal_year'], scen_df['value_with_events'], marker='o', label=f'{scenario} Scenario')

        plt.title(f"{indicator} Forecast")
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        plt.legend()
        plt.grid(True)
        plt.show()

    def display_table(self, indicator):
        results = self.forecast_results.get(indicator)
        if not results:
            print("Run forecast() first")
            return
        display(results['forecast_df'])
        for scenario, df in results['scenarios'].items():
            print(f"\n{scenario} Scenario")
            display(df[['fiscal_year','value_with_events']])
