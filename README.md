# Wise Funnel Analysis

## 1. Project Overview

This project analyses user conversion funnels for Wise's proposed **INR → USD currency transfer route**, focusing on post-launch performance evaluation and insights to guide product decisions.

### What It Does

The analysis examines user behaviour across the transfer funnel stages (transaction creation → verification → completion) to identify:
- Overall conversion rates and drop-off points
- Performance variations by platform (iOS, Android, Web)
- Regional and user experience differences
- Time-to-complete metrics and friction points
- Temporal trends in funnel performance

### Key Questions Addressed

Based on the investment decision framework, this analysis answers:

**Post-Launch Evaluation:**
- Is the route performance on track after launch?
- What are key post-launch insights for the product team?

**Demand Validation:**
- What is the actual user adoption rate?
- How does conversion vary by segment (platform, region, experience level)?
- Where are the main friction points causing drop-offs?

### Methodology

The analysis employs several complementary approaches:

1. **Funnel Analysis**: Step-by-step conversion tracking across transaction stages (create → verify → complete)
2. **Cohort Segmentation**: Comparing performance across:
   - Platforms (iOS, Android, Web)
   - User regions (India, USA, Other)
   - User experience levels (New vs. Experienced)
3. **Time-Series Analysis**: Tracking funnel metrics over time to identify trends and anomalies
4. **Friction Analysis**: Measuring time-to-complete and identifying stages with excessive duration
5. **SQL + Python Stack**: Leveraging DuckDB for analytical queries and Python (pandas, plotly) for visualisation

---

## 2. Project Structure

```
wise-funnel-analysis/
├── README.md                      # Project documentation (this file)
├── pyproject.toml                 # UV project configuration & dependencies
├── uv.lock                        # Locked dependency versions
│
├── config/
│   └── config.yaml                # Database and application settings
│
├── data/
│   └── wise_funnel_events.csv     # Raw funnel event data
│
├── database/
│   └── wise_analytics.duckdb      # DuckDB analytical database
│
├── notebooks/
│   └── funnel_analysis.ipynb      # Main Jupyter analysis notebook
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
    ├── main.py                    # Entry point for data pipeline
    ├── database_manager.py        # DuckDB connection & query execution
    └── dataframe_processor.py     # Data transformation utilities
```

---

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

1. **Start Jupyter Lab/Notebook**

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

You can execute SQL queries against DuckDB using the CLI:

```bash
duckdb database/wise_analytics.duckdb
```

Then run queries interactively or execute SQL files:

```sql
.read sql/funnel_by_platform.sql
```

## 5. Future Work

### Potential Enhancements
- **Transaction value analysis** - Incorporate transfer amount data to understand relationship between cart size and conversion rates
- **Experimentation framework** - Design and implement A/B tests to validate insights and measure impact of product improvements
- **Predictive analytics** - Develop machine learning models to forecast transaction completion probability and identify at-risk users
- **Real-time dashboard** - Build Streamlit-based visualisation tool for stakeholders to monitor funnel performance dynamically
- **Longitudinal cohort study** - Analyse user journey progression from new to experienced customers over time (currently limited by data quality issues in sample dataset)

## 6. Authors

[Keith Sng](https://github.com/keithsngth)
