import pandas as pd
import numpy as np

class EventImpactModel:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with merged and cleaned dataset including:
        - Ethiopia FI data
        - Impact links
        """
        self.data = data.copy()
        
        # Ensure a numeric year column exists
        if 'fiscal_year' in self.data.columns:
            self.data['year'] = pd.to_numeric(self.data['fiscal_year'], errors='coerce')
        elif 'period_start' in self.data.columns:
            self.data['year'] = pd.to_numeric(self.data['period_start'], errors='coerce')
        else:
            raise ValueError("No year column found. Add fiscal_year or period_start.")
        
        # Keep only rows with a valid parent_id as events
        self.events = self.data[~self.data['parent_id'].isna()].copy()
        self.indicators = self.data['indicator'].unique().tolist()

    def build_event_indicator_matrix(self, indicators=None):
        """Build matrix: rows=events, columns=indicators, values=impact magnitude"""
        if indicators is None:
            indicators = self.indicators

        matrix = pd.DataFrame(index=self.events['parent_id'].unique(), columns=indicators, dtype=float)

        for _, row in self.events.iterrows():
            event_id = row['parent_id']
            ind = row['indicator']
            if ind in indicators:
                try:
                    matrix.at[event_id, ind] = pd.to_numeric(row['impact_estimate'], errors='coerce')
                except:
                    matrix.at[event_id, ind] = np.nan
        self.event_indicator_matrix = matrix
        return matrix

    def impact_time_profile(self, event_id, indicator, horizon_years=5):
        """
        Simulate the effect of a single event on an indicator over time
        using lag_months and impact_estimate.
        """
        event_row = self.events[self.events['parent_id'] == event_id]
        if event_row.empty:
            raise ValueError(f"No event found with parent_id={event_id}")
        
        lag_months = int(event_row['lag_months'].iloc[0])
        total_impact = float(event_row['impact_estimate'].iloc[0])
        start_year = int(event_row['year'].iloc[0])
        
        # Create yearly profile
        years = np.arange(start_year, start_year + horizon_years)
        profile = pd.Series(index=years, dtype=float)
        
        # Apply gradual effect proportional to lag
        for i, y in enumerate(years):
            if i == 0 and lag_months == 0:
                profile[y] = total_impact
            else:
                profile[y] = total_impact / horizon_years  # simple uniform spread
        return profile

    def predict_event_impacts(self, indicators=None, horizon_years=5):
        """Predict impact of all events on all indicators"""
        if indicators is None:
            indicators = self.indicators

        predictions = pd.DataFrame()

        for event_id in self.events['parent_id'].unique():
            for ind in indicators:
                try:
                    profile = self.impact_time_profile(event_id, ind, horizon_years=horizon_years)
                    profile.name = f"{event_id}_{ind}"
                    predictions = pd.concat([predictions, profile], axis=1)
                except:
                    continue
        return predictions

    def validate_against_history(self, indicator):
        """Compare predicted impact to historical changes for a given indicator"""
        pred = self.predict_event_impacts([indicator])
        hist = self.data.groupby('year')[indicator].mean()
        combined = pd.concat([hist, pred.sum(axis=1)], axis=1)
        combined.columns = ['Historical', 'Predicted']
        return combined
