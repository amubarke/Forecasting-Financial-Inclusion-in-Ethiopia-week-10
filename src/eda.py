import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

data = pd.read_csv("../data/raw/ethiopia_fi_unified_data.csv")
impact_link = pd.read_csv("../data/raw/impact_sheet.csv")
reference_data = pd.read_csv("../data/raw/reference_codes.csv")

# Ensure dates & numeri
# Ensure dates & numerics
sns.set(style="whitegrid")

# Ensure dates and numeric columns
data['observation_date'] = pd.to_datetime(data['observation_date'], errors='coerce')
data['year'] = data['observation_date'].dt.year

data['value_numeric'] = pd.to_numeric(data['value_numeric'], errors='coerce')
# 1️⃣ Dataset Overview
def dataset_overview(data):
    print("\n📊 DATASET OVERVIEW\n")
    
    # Record / pillar / source summaries
    print("🔹 Record type distribution:")
    print(data['record_type'].value_counts())
    
    print("\n🔹 Pillar distribution:")
    print(data['pillar'].value_counts())
    
    print("\n🔹 Source type distribution:")
    print(data['source_type'].value_counts())
    
    # Temporal coverage
    temporal = (
        data.dropna(subset=['year'])
            .groupby(['indicator', 'year'])
            .size()
            .unstack(fill_value=0)
    )
    
    if temporal.empty:
        print("\n⚠️ No temporal coverage data available.")
    else:
        plt.figure(figsize=(12, 6))
        sns.heatmap(temporal > 0, cmap="Greens", cbar=False)
        plt.title("Temporal Coverage of Indicators")
        plt.xlabel("Year")
        plt.ylabel("Indicator")
        plt.tight_layout()
        plt.show()


# 2️⃣ Access Analysis (Account Ownership)

def access_analysis(data):
    print("\n🏦 ACCESS ANALYSIS – ACCOUNT OWNERSHIP\n")
    
    # Robust indicator matching
    access = data[data['indicator'].str.strip().str.lower() == 'account ownership rate']
    
    # Keep national totals only
    access = access[
        (access['gender'].isna() | access['gender'].str.lower().isin(['total', 'all'])) &
        (access['location'].isna() | access['location'].str.lower().isin(['national', 'all']))
    ]
    
    # Year column
    access['year'] = pd.to_datetime(access['observation_date'], errors='coerce').dt.year
    access = access.dropna(subset=['year', 'value_numeric'])
    
    trajectory = access.groupby('year')['value_numeric'].first()
    
    print("🔹 Account ownership by year:")
    print(trajectory)
    
    if not trajectory.empty:
        plt.figure(figsize=(8, 5))
        plt.plot(trajectory.index, trajectory.values, marker='o', color='blue')
        plt.title("Ethiopia Account Ownership (National Total)")
        plt.xlabel("Year")
        plt.ylabel("Percent of Adults")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xticks(trajectory.index)
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.show()
        
        growth = trajectory.diff()
        print("\n📈 Growth between survey years (pp):")
        print(growth)
    else:
        print("⚠️ No access data available.")




# 3️⃣ Usage Analysis (Digital Payments / Mobile Money)

def usage_analysis(data):
    """
    Analyze Digital Payment / Mobile Money Usage indicators.

    Parameters:
    - data: pd.DataFrame, main dataset
    """
    # 1️⃣ Ensure 'year' exists
    if 'year' not in data.columns:
        if 'fiscal_year' in data.columns:
            data['year'] = data['fiscal_year'].astype(str).str[:4].astype(int)
        elif 'period_start' in data.columns:
            data['year'] = pd.to_datetime(data['period_start'], errors='coerce').dt.year
        else:
            raise ValueError("No column available to extract 'year'")
    
    # 2️⃣ Ensure numeric
    data['value_numeric'] = pd.to_numeric(data['value_numeric'], errors='coerce')

    # 3️⃣ Filter usage-related indicators
    usage_indicators = [
        'Mobile Money Account Rate',
        'Mobile Money Activity Rate',
        'M-Pesa Registered Users',
        'M-Pesa 90-Day Active Users',
        'Telebirr Registered Users',
        'Telebirr Transaction Value',
        'P2P Transaction Count',
        'P2P Transaction Value'
    ]
    usage_df = data[data['indicator'].isin(usage_indicators)].dropna(subset=['value_numeric', 'year'])

    if usage_df.empty:
        print("⚠️ No usage data available.")
        return

    # 4️⃣ Aggregate per year and indicator
    usage_trend = usage_df.groupby(['year', 'indicator'])['value_numeric'].mean().unstack()

    print("📱 Usage Indicators (mean values per year):")
    print(usage_trend)

    # 5️⃣ Mobile money penetration trend plot
    plt.figure(figsize=(10, 6))
    for col in usage_trend.columns:
        if 'Account Rate' in col or 'Registered' in col:
            plt.plot(usage_trend.index, usage_trend[col], marker='o', label=col)
    plt.title("Mobile Money Account Penetration Trend")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 6️⃣ Registered vs Active accounts
    reg_active_cols = ['M-Pesa Registered Users', 'M-Pesa 90-Day Active Users', 'Telebirr Registered Users']
    existing_cols = [c for c in reg_active_cols if c in usage_trend.columns]
    if existing_cols:
        plt.figure(figsize=(10, 6))
        usage_trend[existing_cols].plot(kind='bar')
        plt.title("Registered vs Active Accounts")
        plt.ylabel("Number of Accounts")
        plt.xlabel("Year")
        plt.grid(axis='y')
        plt.show()
    
    # 7️⃣ Payment use cases (P2P, merchant, bill pay, wages)
    usecase_cols = [c for c in usage_trend.columns if 'P2P' in c or 'Transaction' in c]
    if usecase_cols:
        plt.figure(figsize=(10, 6))
        usage_trend[usecase_cols].plot(marker='o')
        plt.title("Digital Payment Use Cases")
        plt.ylabel("Value")
        plt.xlabel("Year")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    print("✅ Usage analysis complete!")



# 4️⃣ Infrastructure & Enablers

def infrastructure_analysis(data):
    """
    Analyze Infrastructure & Enablers indicators:
    - 4G coverage, mobile subscription, ATM density
    - Relationships with inclusion outcomes
    - Potential leading indicators

    Parameters:
    - data: pd.DataFrame, main dataset
    """
    # 1️⃣ Ensure 'year' exists
    if 'year' not in data.columns:
        if 'fiscal_year' in data.columns:
            data['year'] = data['fiscal_year'].astype(str).str[:4].astype(int)
        elif 'period_start' in data.columns:
            data['year'] = pd.to_datetime(data['period_start'], errors='coerce').dt.year
        else:
            raise ValueError("No column available to extract 'year'")

    # 2️⃣ Ensure numeric
    data['value_numeric'] = pd.to_numeric(data['value_numeric'], errors='coerce')

    # 3️⃣ Filter infrastructure/enabler-related indicators
    infra_indicators = [
        '4G Population Coverage',
        'Mobile Subscription Penetration',
        'ATM Transaction Count',
        'ATM Transaction Value',
        'ATM/100k Population'
    ]
    infra_df = data[data['indicator'].isin(infra_indicators)].dropna(subset=['value_numeric', 'year'])

    if infra_df.empty:
        print("⚠️ No infrastructure data available.")
        return

    # 4️⃣ Aggregate per year and indicator
    infra_trend = infra_df.groupby(['year', 'indicator'])['value_numeric'].mean().unstack()

    print("🛰️ Infrastructure & Enablers Indicators (mean values per year):")
    print(infra_trend)

    # 5️⃣ Plot infrastructure trends
    plt.figure(figsize=(10, 6))
    for col in infra_trend.columns:
        plt.plot(infra_trend.index, infra_trend[col], marker='o', label=col)
    plt.title("Infrastructure & Enablers Trends")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 6️⃣ Examine relationships with inclusion outcomes (e.g., Account Ownership, Mobile Money Rate)
    inclusion_indicators = [
        'Account Ownership Rate',
        'Mobile Money Account Rate',
        'Mobile Money Activity Rate'
    ]
    inclusion_df = data[data['indicator'].isin(inclusion_indicators)]
    if not inclusion_df.empty:
        # Pivot both datasets for correlation
        infra_corr = infra_df.pivot(index='year', columns='indicator', values='value_numeric')
        inclusion_corr = inclusion_df.pivot(index='year', columns='indicator', values='value_numeric')
        
        # Align indices
        combined = pd.concat([infra_corr, inclusion_corr], axis=1)
        correlation_matrix = combined.corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Correlation: Infrastructure vs Inclusion Outcomes")
        plt.show()
        
        print("🔹 Correlation matrix (infrastructure vs inclusion outcomes):")
        print(correlation_matrix)
    else:
        print("⚠️ No inclusion outcome data available for correlation analysis.")

    print("✅ Infrastructure & Enablers analysis complete!")



# 5️⃣ Event Timeline & Visual Overlay

def event_timeline_analysis(data, impact_link):
    """
    Plots account ownership over time with major financial inclusion events
    and overlays impact links from the impact_sheet.
    """
    print("\n🗓️ EVENT TIMELINE ANALYSIS\n")
    
    # Ensure observation_date is datetime
    data['year'] = pd.to_datetime(data['observation_date'], errors='coerce').dt.year
    df_access = data[data['pillar'] == 'ACCESS']
    
    # Filter account ownership
    acc_ownership = df_access[df_access['indicator'] == 'Account Ownership Rate']
    
    if acc_ownership.empty:
        print("⚠️ No account ownership data available.")
        return
    
    # Aggregate duplicates per year
    acc_trend = acc_ownership.groupby('year')['value_numeric'].mean()
    print("🔹 Account Ownership by Year:")
    print(acc_trend)
    
    # Convert impact_link dates to year
    impact_link['year'] = pd.to_datetime(impact_link['collection_date'], errors='coerce').dt.year
    
    # Focus on events affecting ACCESS
    access_events = impact_link[impact_link['pillar'] == 'ACCESS']
    
    # Plot account ownership trend
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=acc_trend.index, y=acc_trend.values, marker='o', label="Account Ownership Rate")
    
    # Overlay impact events
    for _, row in access_events.iterrows():
        plt.axvline(x=row['year'], color='orange', linestyle='--', alpha=0.6)
        plt.text(
            row['year'], 
            acc_trend.max()*0.95,  # place text near top
            row['indicator'], 
            rotation=90, 
            verticalalignment='top', 
            color='orange'
        )
    
    # Manually annotate key events if missing
    key_events = {
        2021: "Telebirr Launch",
        2022: "Safaricom Entry",
        2023: "M-Pesa Entry"
    }
    
    for year, label in key_events.items():
        plt.axvline(x=year, color='red', linestyle='--', alpha=0.8)
        plt.text(
            year, 
            acc_trend.max()*0.9, 
            label, 
            rotation=90, 
            verticalalignment='top', 
            color='red', 
            fontweight='bold'
        )
    
    plt.title("Account Ownership Over Time with Major Events")
    plt.xlabel("Year")
    plt.ylabel("Account Ownership Rate (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()



# 6️⃣ Correlation Analysis (Print + Plot)

def correlation_analysis(data, impact_link=None, min_years=2):
    """
    Perform correlation analysis of financial inclusion indicators.
    
    Parameters:
    - data: pd.DataFrame, main dataset with indicators and numeric values
    - impact_link: pd.DataFrame, optional, dataset linking events to indicators
    - min_years: int, minimum number of years an indicator must have to be included
    """
    # 1️⃣ Ensure 'year' exists
    if 'year' not in data.columns:
        if 'fiscal_year' in data.columns:
            data['year'] = data['fiscal_year'].astype(str).str[:4].astype(int)
        elif 'period_start' in data.columns:
            data['year'] = pd.to_datetime(data['period_start'], errors='coerce').dt.year
        else:
            raise ValueError("No column available to extract 'year'")

    # 2️⃣ Ensure numeric values
    data['value_numeric'] = pd.to_numeric(data['value_numeric'], errors='coerce')

    # 3️⃣ Filter only numeric indicators
    df = data.dropna(subset=['value_numeric', 'year'])

    if df.empty:
        print("⚠️ No data available for correlation analysis.")
        return

    # 4️⃣ Pivot indicators as columns
    corr_data = df.pivot_table(index='year', columns='indicator', values='value_numeric', aggfunc='mean')

    # 5️⃣ Drop sparse indicators
    corr_data = corr_data.dropna(axis=1, thresh=min_years)

    if corr_data.empty:
        print("⚠️ Not enough data after filtering by minimum years.")
        return

    # 6️⃣ Compute correlation matrix
    corr_matrix = corr_data.corr()

    # 7️⃣ Print summary
    print("🔗 Correlation matrix:")
    print(corr_matrix)

    # Identify strongest associations for ACCESS and USAGE
    access_inds = [col for col in corr_matrix.columns if 'Ownership' in col or 'Account' in col]
    usage_inds = [col for col in corr_matrix.columns if 'Transaction' in col or 'Mobile' in col]

    if access_inds:
        access_corr = corr_matrix[access_inds].abs().mean().sort_values(ascending=False)
        print("\n🏦 Factors most associated with Access indicators:")
        print(access_corr)
    if usage_inds:
        usage_corr = corr_matrix[usage_inds].abs().mean().sort_values(ascending=False)
        print("\n📱 Factors most associated with Usage indicators:")
        print(usage_corr)

    # 8️⃣ Overlay impact_link insights if provided
    if impact_link is not None and not impact_link.empty:
        print("\n📌 Existing impact_link records:")
        links = impact_link[['indicator', 'impact_direction', 'impact_magnitude', 'impact_estimate']].drop_duplicates()
        print(links)

    # 9️⃣ Visualize correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Correlation Heatmap of Indicators")
    plt.tight_layout()
    plt.show()



