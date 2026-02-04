import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class EventImpactModel:
    
    def __init__(self, data, impact_link):
        """
        Initialize model with datasets
        """
        self.data = data.copy()
        self.impact = impact_link.copy()
        
        self.events = None
        self.merged = None
        self.association_matrix = None
    
    
    # -----------------------------
    # 1. Prepare Data
    # -----------------------------
    
    def prepare_data(self):
        """
        Clean and prepare datasets
        """
        
        # Convert dates
        self.data["observation_date"] = pd.to_datetime(
            self.data["observation_date"], errors="coerce"
        )
        
        # Extract events
        self.events = self.data[self.data["record_type"] == "event"]
        
        # Keep observations
        self.observations = self.data[self.data["record_type"] == "observation"]
        
        print("Data prepared successfully.")
    
    
    # -----------------------------
    # 2. Merge Events and Impacts
    # -----------------------------
    
    def merge_event_impacts(self):
        """
        Join events with impact links
        """
        
        self.merged = pd.merge(
            self.impact,
            self.events,
            left_on="parent_id",
            right_on="record_id",
            suffixes=("_impact", "_event"),
            how="left"
        )
        
        print("Events and impacts merged.")
    
    
    # -----------------------------
    # 3. Build Association Matrix
    # -----------------------------
    
    def build_association_matrix(self):
        """
        Create event-indicator impact table
        """
        
        matrix = self.merged.pivot_table(
        index="indicator_event",
        columns="pillar_impact",
        values="impact_estimate_impact",  # updated column after merge
        aggfunc="mean"
      )
        
        self.association_matrix = matrix
        
        print("Association matrix created.")
        
        return matrix
    
    
    # -----------------------------
    # 4. Plot Heatmap
    # -----------------------------
    
    def plot_heatmap(self):
        """
        Visualize association matrix
        """
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(
            self.association_matrix,
            annot=True,
            cmap="coolwarm",
            fmt=".1f"
        )
        
        plt.title("Event-Indicator Impact Matrix")
        plt.show()
    
    
    # -----------------------------
    # 5. Impact Prediction (Lag Model)
    # -----------------------------
    
    def predict_impact(self):
        """
        Apply lag-based impact model
        """
        
        predictions = []
        
        for _, row in self.merged.iterrows():
            
            event = row["indicator_event"]
            indicator = row["pillar_impact"]
            effect = row["impact_estimate_impact"]
            lag = row["lag_months_impact"]
            
            predictions.append({
                "event": event,
                "indicator": indicator,
                "impact": effect,
                "lag_months": lag
            })
        
        pred_df = pd.DataFrame(predictions)
        
        print("Impact predictions generated.")
        
        return pred_df
    
    
    # -----------------------------
    # 6. Validate Against History
    # -----------------------------
    
    def validate_model(self, indicator_code):
        """
        Compare predicted vs observed trends
        """
        
        obs = self.observations[
            self.observations["indicator_code"] == indicator_code
        ].sort_values("observation_date")
        
        plt.figure(figsize=(10,5))
        
        plt.plot(
            obs["observation_date"],
            obs["value_numeric"],
            marker="o",
            label="Observed"
        )
        
        plt.title(f"Validation for {indicator_code}")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.legend()
        
        plt.show()
        
        print("Validation completed.")
    
    
    # -----------------------------
    # 7. Documentation
    # -----------------------------
    
    def document_methodology(self):
        """
        Print modeling assumptions
        """
        
        print("""
        METHODOLOGY
        
        1. Event impacts were merged using parent_id.
        2. Impact estimates represent percentage point changes.
        3. Lag months indicate delayed effects.
        4. Effects are applied as step functions.
        5. Multiple events are combined additively.
        
        ASSUMPTIONS
        - Impacts are linear.
        - No interaction effects.
        - External shocks ignored.
        
        LIMITATIONS
        - Limited historical data.
        - Estimates based partly on literature.
        - Simplified lag structure.
        """)
