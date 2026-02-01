import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



sns.set_style("whitegrid")
def load_data(data, impact_links, ref_codes):
    data = pd.read_csv(data)
    impact_links = pd.read_csv(impact_links)
    ref_codes = pd.read_csv(ref_codes)
    
    return data, impact_links, ref_codes

def summarize_dataset(data,record_type):
    return {
    "by_record_type": data['record_type'].value_counts(),
    "by_pillar": data['pillar'].value_counts(dropna=False),
    "by_source": data['source_type'].value_counts()
}

def temporal_coverage(data):
    obs = data[data.record_type == 'observation'].copy()
    obs['year'] = pd.to_datetime(obs['observation_date']).dt.year
    pivot = obs.pivot_table(index='indicator_code', columns='year', values='value_numeric', aggfunc='count')


    plt.figure(figsize=(12,6))
    sns.heatmap(pivot.notnull(), cbar=False)
    plt.title("Temporal Coverage of Indicators")
    plt.show()

def filter_by_pillar(data, pillar):
    """
    Filter dataset by financial inclusion pillar.
    
    Parameters:
        df (pd.DataFrame): Unified dataset
        pillar (str): 'access' or 'usage'
    
    Returns:
        pd.DataFrame
    """
    return data[data["pillar"] == pillar].copy()


def confidence_distribution(data):
    data['confidence'].value_counts().plot(kind='bar')
    plt.title("Distribution of Confidence Levels")
    plt.ylabel("Count")
    plt.show()

def plot_account_ownership(data):
    acc = data[(data.indicator_code=='account_ownership_rate') & (data.record_type=='observation')]
    acc['year'] = pd.to_datetime(acc['observation_date']).dt.year


    plt.plot(acc['year'], acc['value_numeric'], marker='o')
    plt.title("Ethiopia – Account Ownership Rate")
    plt.ylabel("% of adults")
    plt.xlabel("Year")
    plt.show()

def growth_rates(data):
    acc = data[(data.indicator_code=='account_ownership_rate') & (data.record_type=='observation')]
    acc = acc.sort_values('observation_date')
    acc['growth_pp'] = acc['value_numeric'].diff()
    return acc[['observation_date','value_numeric','growth_pp']]

def plot_mobile_money(data):
    mm = data[(data.indicator_code=='mobile_money_account_ownership') & (data.record_type=='observation')]
    mm['year'] = pd.to_datetime(mm['observation_date']).dt.year


    plt.plot(mm['year'], mm['value_numeric'], marker='o', color='green')
    plt.title("Mobile Money Account Ownership")
    plt.ylabel("% of adults")
    plt.show()


def plot_infrastructure_vs_usage(data, infra_code, usage_code):
    infra = data[data.indicator_code==infra_code]
    usage = data[data.indicator_code==usage_code]


    merged = infra.merge(usage, on='observation_date', suffixes=('_infra','_usage'))


    plt.scatter(merged['value_numeric_infra'], merged['value_numeric_usage'])
    plt.xlabel(infra_code)
    plt.ylabel(usage_code)
    plt.title("Infrastructure vs Usage")
    plt.show()

def event_timeline(data):
    events = data[data.record_type=='event']
    events['event_date'] = pd.to_datetime(events['event_date'])


    plt.figure(figsize=(10,4))
    plt.scatter(events['event_date'], [1]*len(events))
    for _, row in events.iterrows():
      plt.text(row['event_date'], 1.01, row['event_name'], rotation=45)
    plt.yticks([])
    plt.title("Financial Inclusion Event Timeline")
    plt.show()

def correlation_matrix(data):
    obs = data[data.record_type=='observation']
    pivot = obs.pivot_table(index='observation_date', columns='indicator_code', values='value_numeric')


    plt.figure(figsize=(10,8))
    sns.heatmap(pivot.corr(), annot=True, cmap='coolwarm')
    plt.title("Indicator Correlations")
    plt.show()