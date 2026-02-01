# Ethiopia Financial Inclusion Forecasting Project

## 📌 Project Overview
This project develops a forecasting system to track Ethiopia's digital financial transformation. Using time series and event-driven analysis, the system predicts two core financial inclusion indicators:

- **Access**: Account ownership rate among adults  
- **Usage**: Digital payment adoption rate  

The dataset includes observations, events, impact links, and targets, covering multiple years and financial inclusion indicators. The project follows a structured workflow from data exploration to forecasting and visualization.

---

## ✅ Tasks

### **Task 1: Data Exploration and Enrichment**
**Objective:** Understand the dataset and enrich it with additional observations, events, and relationships to support forecasting.

**Key Activities:**
- Explore the unified dataset (`ethiopia_fi_unified_data.csv`) and review the schema
- Analyze records by `record_type`, `pillar`, and `source_type`
- Identify temporal gaps and sparse indicators
- Add new data points:
  - Observations relevant to Access and Usage  
  - Events (policy, product launches, infrastructure)  
  - Impact links connecting events to indicators  
- Document all additions in `data_enrichment_log.md`

**Deliverables:**
- Updated dataset and impact links
- `data_enrichment_log.md`
- Pull Request merging `task-1` branch into `main`

---

### **Task 2: Exploratory Data Analysis (EDA)**
**Objective:** Analyze patterns and factors influencing financial inclusion in Ethiopia.

**Key Activities:**
- Dataset overview:
  - Summary by `record_type`, `pillar`, and `source_type`  
  - Confidence levels and data quality assessment  
  - Identification of sparse indicators  
- Access analysis:
  - Account ownership trends (2011–2024)  
  - Growth rate calculation  
  - Investigation of post-2021 slowdown  
- Usage analysis:
  - Mobile money and digital payment adoption trends  
  - Registered vs. active usage gaps  
- Infrastructure & enablers:
  - Examine network coverage, ATM density, mobile penetration  
  - Identify leading indicators for Access and Usage  
- Event timeline:
  - Visualize key events and overlay on trends  
- Correlation analysis:
  - Identify relationships between indicators  
  - Insights from `impact_link` records  

**Deliverables:**
- EDA notebook with visualizations (`notebooks/task_2_eda.ipynb`)  
- At least 5 key insights with supporting evidence  
- Data quality assessment and limitations  
- Pull Request merging `task-2` branch into `main`

---

### **Upcoming Tasks**
**Task 3: Impact Modeling and Forecasting**
- Model effects of events on Access and Usage  
- Apply regression and intervention-based time series methods  
- Forecast indicators for 2025–2027  

**Task 4: Communication and Dashboarding**
- Present forecasts via interactive dashboards  
- Highlight uncertainty, assumptions, and policy insights  

---

## 🧭 Project Workflow
- Each task is developed in a separate Git branch (`task-1`, `task-2`, etc.)  
- Changes are merged into `main` via Pull Requests  
- Functions and logic are modular and stored in `src/eda.py` for reproducibility  
- Analysis, visualizations, and insights are documented in notebooks  

---

## Project Structure

Ethiopia Financial Inclusion Forecasting Project/

├── .github/workflows/

│   └── unittests.yml

├── data/

│   ├── raw/                      

│   │   ├── ethiopia_fi_unified_data.csv

│   │   └── Impact_sheet.csv

│   └── reference_codes.csv

│   └── processed/                

├── notebooks/

│   └── data_exploration.ipynb

│   └── EDA.ipynb

│   └── README.md

├── src/

│   ├── __init__.py

│   └── eda.ipynb

├── dashboard/

│   └── app.py

├── tests/

│   └── __init__.py

├── models/

├── reports/

│   └── figures/

├── requirements.txt

├── README.md

└── .gitignore