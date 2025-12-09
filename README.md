# Wise Funnel Analysis

## 1. Project Overview

### Background

Wise's Regional Expansion Tribe launched the INR → USD currency route to enable fast, low-cost transfers for education, travel, and business use cases. Following initial market validation, this project evaluates the route's first eight weeks of performance to understand adoption, conversion, and friction points.

The analysis addresses two core areas:

1. **Demand Estimation**
   - How can we assess potential demand for the corridor?
   - Is the route likely to be profitable for Wise?

2. **Post-Launch Evaluation**
   - Is performance on track after launch?
   - What insights should the product team act on?

### Methodology

#### A. Demand Estimation Approach

**1. External Market Sizing (Top-Down)**

Estimate potential corridor demand by assessing India–US cross-border money movement across major economic segments using publicly available data.

Potential data sources:
- **Department of Economic Affairs, Government of India:** Outward remittances
- **ICEF Monitor:** Indian student mobility and education spending
- **Ministry of Commerce:** Bilateral India–US trade flows
- **SEVIS:** Indian student enrolment in the US

These provide a macro-level view of monetary flows that could translate into INR → USD transfer volume.

**2. Internal Demand Signals (Bottom-Up)**

Quantify latent demand and behavioural intent using Wise's user and transaction data.

Key analytical lenses:
- **Customer base sizing:** Count active users with Indian residency or funding sources to estimate corridor-ready users
- **Proxy routes:** Identify multi-currency hops (e.g., INR → GBP → USD) indicating indirect demand
- **Intent analysis:** Review event logs where users attempted INR → USD before route availability
- **Customer feedback:** Analyse support tickets for repeated requests relating to USD payouts

#### B. Post-Launch Evaluation Framework

The analysis examines eight weeks of usage data through three complementary lenses:

1. **Post-Launch Adoption:** Assess adoption of the new route by tracking user volumes through each transfer step
2. **Funnel Analysis:** Identify potential drop-off points and churn across each user segment's transfer journey
3. **Friction Analysis:** Evaluate the lag across transfer stage transitions for users who complete the transfer

## 2. Project Structure

```
wise-funnel-analysis/
├── README.md                                  # Project documentation
├── pyproject.toml                             # UV project configuration & dependencies
├── uv.lock                                    # Locked dependency versions
│
├── config/
│   └── config.yaml                            # Database and application settings
│
├── data/
│   └── wise_funnel_events.csv                 # Raw funnel event data
│
├── database/
│   └── wise_analytics.duckdb                  # DuckDB analytical database
│
├── notebooks/
│   └── funnel_analysis.ipynb                  # Main Jupyter notebook for analysis
│
├── slides/
│   └── wise-case-study.pdf                    # Slide deck for case study presentation
│
├── sql/
│   ├── create_transactions_table.sql          # Table schema definition
│   ├── general_eda.sql                        # Exploratory data analysis
│   ├── eda_pivot_table.sql                    # Pivot table for EDA
│   ├── funnel_by_all.sql                      # Overall funnel metrics
│   ├── funnel_by_platform.sql                 # Funnel by platform (iOS/Android/Web)
│   ├── funnel_by_region_experience.sql        # Funnel by region & user experience
│   ├── funnel_stage_time_series.sql           # Time-series funnel trends
│   └── friction_duration.sql                  # Time-to-complete analysis
│
└── src/
    ├── __init__.py
    ├── database_manager.py                    # DuckDB connection & query execution
    └── dataframe_processor.py                 # Data transformation utilities
```

## 3. Getting Started

### Prerequisites

- **Python 3.12+** (specified in `.python-version`)
- **UV** (fast Python package manager) - [Install UV](https://docs.astral.sh/uv/)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/wise-funnel-analysis.git
cd wise-funnel-analysis
```

2. **Initialise UV environment**

UV will automatically detect the Python version from `.python-version`:

```bash
uv venv
```

3. **Activate the virtual environment**

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. **Sync dependencies**

Install all project dependencies from `pyproject.toml`:

```bash
uv sync
```

This will install:
- `duckdb` - Analytical database engine
- `pandas` - Data manipulation
- `plotly`, `matplotlib`, `seaborn` - Visualisation
- `jupyter` - Interactive notebook environment
- `pyyaml` - Configuration management
- `sqlfluff` - SQL linting

## 4. Usage

### Running the Analysis Notebook

1. **Start Jupyter Notebook**

```bash
jupyter notebook
```

2. **Open the analysis notebook**

Navigate to `notebooks/funnel_analysis.ipynb` and run cells sequentially.

The notebook will:
- Load data from `data/wise_funnel_events.csv`
- Execute SQL queries from the `sql/` folder via DuckDB
- Generate interactive visualisations with Plotly
- Output key metrics and insights

### Configuration Options

Edit `config/config.yaml` to customise:

```yaml
database:
  table_name: "TRANSACTIONS"                                # DuckDB table name
  database_path: "database/wise_analytics.duckdb"           # Database file location
  raw_data_path: "data/wise_funnel_events.csv"              # Source CSV data
  table_schema_path: "sql/create_transactions_table.sql"    # Schema definition
```

### Running SQL Queries Directly

You can execute SQL queries against DuckDB using the CLI.

**First, install DuckDB CLI:**

```bash
curl https://install.duckdb.org | sh
```

**Connect to the database:**

```bash
duckdb database/wise_analytics.duckdb
```

**Once inside the DuckDB CLI, you can:**

Run SQL queries directly:
```sql
SELECT * FROM TRANSACTIONS LIMIT 5;
```

Execute SQL files:
```sql
.read sql/funnel_by_platform.sql
```

**Alternatively, run queries without entering interactive mode:**

```bash
# Run a single query
duckdb database/wise_analytics.duckdb "SELECT * FROM TRANSACTIONS LIMIT 100;"

# Execute a SQL file and save output
duckdb database/wise_analytics.duckdb < sql/funnel_by_platform.sql
```

## 5. Future Work

### Potential Enhancements

- **Transaction value analysis:** Incorporate transfer amount data to understand relationship between cart size and conversion rates
- **Experimentation framework:** Design and implement A/B tests to validate insights and measure impact of product improvements
- **Predictive analytics:** Develop machine learning models to forecast transaction completion probability and identify at-risk users
- **Real-time dashboard:** Build Streamlit-based visualisation tool for stakeholders to monitor funnel performance dynamically
- **Longitudinal cohort study:** Analyse user journey progression from new to experienced customers over time (currently limited by data quality issues in sample dataset)

## 6. Authors

[Keith Sng](https://github.com/keithsngth)
