# ENERGY CONSUMPTION FORECASTING AND ANALYTICS

An end-to-end data science, machine learning, time-series forecasting, MySQL analytics, and Tableau dashboard portfolio project using the UCI Appliances Energy Prediction dataset.

---

## Project Overview & Business Objective

Unplanned spikes in residential energy consumption create severe challenges for grid stability, peak load management, and household energy efficiency. This project delivers an end-to-end data science pipeline that:
1. Analyzes **19,735 energy consumption measurements** recorded at 10-minute intervals over a 4.5-month period.
2. Identifies temporal, weather, and environmental factors driving appliance energy demand.
3. Implements leak-free feature engineering (calendar, lag, and rolling window features).
4. Trains, evaluates, and tunes candidate Machine Learning algorithms (Linear Regression, Random Forest, Gradient Boosting, XGBoost) using **chronological 80/20 train/test splits** and **TimeSeriesSplit cross-validation**.
5. Deploys an out-of-sample multi-step autoregressive forecaster for predicting future energy demand.
6. Integrates a production MySQL database with 20 analytical queries and 6 Tableau-ready views for interactive business intelligence dashboards.

---

## Dataset & Characteristics

- **Dataset Name**: UCI Appliances Energy Prediction Dataset.
- **Record Count**: 19,735 observations at 10-minute frequency (Jan 11, 2016 – May 27, 2016).
- **Target Variable**: `Appliances` (Energy consumption in Watt-hours, Wh).
- **Primary Features**:
  - `date`: Timestamp (YYYY-MM-DD HH:MM:SS).
  - `lights`: Energy use of light fixtures (Wh).
  - `T1` - `T9`: Temperature readings in various rooms (°C).
  - `RH_1` - `RH_9`: Relative humidity readings in various rooms (%).
  - `T_out`, `Press_mm_hg`, `RH_out`, `Windspeed`, `Visibility`, `Tdewpoint`: Weather station measurements.
  - `rv1`, `rv2`: Random variables for validation.

---

## Technologies & Stack

- **Language & Runtime**: Python 3.11 / Python 3.13, VS Code Jupyter.
- **Data Manipulation & ML**: Pandas, NumPy, Scikit-learn, XGBoost, Joblib.
- **Database & SQL**: MySQL Server 8.0, PyMySQL, SQLAlchemy, MySQL Workbench.
- **Data Visualization**: Matplotlib, Seaborn, Tableau Desktop / Public.
- **Environment Management**: `python-dotenv` for zero-hardcoding credential security.

---

## Project Architecture

```
Appliances Energy Prediction/
│
├── .env                                 # Local MySQL credentials (Git-ignored)
├── .gitignore                           # Security & build exclusions
├── README.md                            # Comprehensive technical portfolio documentation
│
├── Data/                                # Raw and processed data storage
│   ├── energydata_complete.csv          # Original UCI dataset (19,735 rows)
│   ├── energy_consumption_cleaned.csv   # Cleaned dataset (19,735 rows)
│   └── energy_consumption_features.csv  # Engineered feature dataset (18,727 rows)
│
├── notebooks/                           # Chronological Jupyter notebooks
│   ├── 01_data_understanding.ipynb      # Data audit & quality reporting
│   ├── 02_eda.ipynb                     # Exploratory visual & statistical analysis
│   ├── 03_feature_engineering.ipynb     # Leak-free temporal, lag & rolling features
│   ├── 04_model_training.ipynb          # Chronological 80/20 train/test modeling
│   ├── 05_model_evaluation_and_tuning.ipynb # TimeSeriesSplit CV & hyperparameter tuning
│   └── 06_future_forecasting.ipynb      # Out-of-sample 24h energy forecasting
│
├── src/                                 # Modular production Python code
│   ├── data_cleaning.py                 # Pipeline for loading & validating raw data
│   ├── feature_engineering.py           # Pipeline for creating lag/rolling features
│   ├── train_model.py                   # Model training & baseline comparison
│   ├── evaluate_model.py                # TimeSeriesSplit CV tuning & model selection
│   └── predict.py                       # Production inference script
│
├── models/                              # Trained model artifacts
│   ├── final_energy_forecasting_model.pkl # Best trained model (Joblib)
│   └── feature_columns.pkl              # Feature schema (Joblib)
│
├── outputs/                             # CSV evaluation reports & metadata
│   ├── data_quality_report.csv          # Column stats & missing value summary
│   ├── eda_summary.csv                  # Target distribution summary
│   ├── feature_list.txt                 # 36 feature column names
│   ├── model_comparison.csv             # Baseline vs candidate model metrics
│   ├── final_model_comparison.csv       # Final evaluation table sorted by RMSE
│   ├── test_predictions.csv             # Actual vs predicted test predictions
│   └── future_energy_forecast.csv       # 24-hour out-of-sample future predictions
│
├── sql/                                 # Production MySQL database scripts
│   ├── 01_create_database.sql           # Database creation DDL
│   ├── 02_create_tables.sql             # Table schema & index DDL
│   ├── 03_load_data.sql                 # Data loading DDL & instructions
│   ├── 04_analysis_queries.sql          # 20 analytical SQL queries
│   ├── 05_tableau_views.sql             # 6 aggregated SQL views
│   └── load_data_mysql.py               # Automated MySQL python table loader
│
└── tableau/                             # Clean Tableau Desktop ready datasets & guide
    ├── README.txt                       # Tableau dataset mapping & connection instructions
    ├── daily_energy.csv                 # Daily consumption & weather aggregates (138 rows)
    ├── monthly_energy.csv               # Monthly volume & peak demand summaries (5 rows)
    ├── hourly_energy.csv                # Hourly load profile (0-23h) & peak hours (24 rows)
    ├── environment_energy.csv           # Indoor/Outdoor climate features (19,735 rows)
    └── forecast.csv                     # Test predictions & 24h future forecast (3,890 rows)
```

---

## Data Leakage Audit & Prevention Strategy

> [!IMPORTANT]
> Time-series modeling is highly vulnerable to data leakage. The following strict rules were enforced throughout this project:
> 1. **Rolling Feature Shift**: All rolling mean features (`rolling_mean_6`, `rolling_mean_144`) apply `.shift(1)` prior to rolling window calculations:
>    ```python
>    df["rolling_mean_6"] = df["Appliances"].shift(1).rolling(6).mean()
>    ```
> 2. **Chronological Train/Test Split**: Data was split sequentially (first 80% for training, last 20% for testing). Random shuffling was strictly prohibited.
> 3. **TimeSeriesSplit CV**: Hyperparameter tuning used `TimeSeriesSplit(n_splits=5)` so validation sets only occur after training windows in time.
> 4. **Recursive Forecasting**: Future forecasting updates lag and rolling features iteratively using past predicted values without referencing future actual target values.

---

## Machine Learning Results & Comparison

Models were trained on 14,981 samples and evaluated on 3,746 unseen test samples (May 1 – May 27, 2016).

| Model | MAE (Wh) | MSE | RMSE (Wh) | MAPE (%) | R² Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Linear Regression (Selected Final Model)** | **33.49** | **4827.73** | **69.48** | **32.44%** | **0.3661** |
| **XGBoost (Tuned)** | 42.29 | 5308.05 | 72.86 | 46.33% | 0.3030 |
| **Gradient Boosting (Tuned)** | 51.15 | 6437.91 | 80.24 | 59.38% | 0.1547 |
| **Baseline (Previous Hour Lag 6)** | 45.51 | 9928.14 | 99.64 | 39.90% | -0.3036 |
| **XGBoost (Untuned)** | 99.30 | 16855.72 | 129.83 | 135.87% | -1.2132 |
| **Random Forest (Tuned)** | 91.46 | 18338.37 | 135.42 | 103.71% | -1.4079 |
| **Random Forest (Untuned)** | 90.74 | 18368.64 | 135.53 | 102.40% | -1.4118 |
| **Gradient Boosting (Untuned)** | 141.88 | 32733.72 | 180.92 | 199.14% | -3.2980 |

### Key ML Findings:
- **Linear Regression** performed best overall (RMSE = 69.48 Wh), capitalizing on the strong linear relationships between short-term lag/rolling variables and energy demand.
- **Tuned XGBoost** (constrained with `max_depth=3`, `learning_rate=0.03`, `subsample=0.8`) achieved a low RMSE of **72.86 Wh**, outperforming the Naive Baseline (99.64 Wh).
- Complex untuned decision trees overfitted the training split when unconstrained, demonstrating the vital importance of regularization and `TimeSeriesSplit` cross-validation in time-series forecasting.

---

## MySQL Database & Analytics

The project establishes a production MySQL database named `energy_consumption_db`.

### Core Database Objects:
1. **Table `energy_consumption`**: Stores 19,735 records with indexed `date` timestamps.
2. **20 Analytical SQL Queries** (`sql/04_analysis_queries.sql`):
   - Total, Average, Min, and Max consumption.
   - Daily and Monthly total and average trends.
   - Hourly pattern & Peak consumption hour identification (17:00 – 18:00 PM peak).
   - Weekend vs Weekday consumption comparison (Weekends consume ~15% more energy).
   - Indoor/Outdoor temperature vs energy demand correlation.
   - Humidity and Windspeed relationship queries.
   - Top 10 energy consumption spikes and rolling 1-hour window averages.
3. **6 Tableau SQL Views** (`sql/05_tableau_views.sql`):
   - `vw_daily_energy`, `vw_monthly_energy`, `vw_hourly_energy`, `vw_weekday_energy`, `vw_environmental_energy`, `vw_forecast`.

---

## Tableau Dashboards Specification

3 interactive dashboard pages are designed for business stakeholders:

### DASHBOARD 1: ENERGY OVERVIEW
- **KPI Cards**: Total Energy Consumption (1.93M Wh), Average Hourly Consumption (97.69 Wh), Peak Demand (1,080 Wh), Minimum Demand (10 Wh).
- **Line Chart**: Daily Energy Consumption Trend (Jan – May 2016).
- **Bar Chart**: Hourly Consumption Pattern (0:00 – 23:00) highlighting evening peak (17:00–20:00 PM).
- **Heatmap**: Consumption by Day of Week vs Hour of Day.

### DASHBOARD 2: ENERGY AND ENVIRONMENT
- **Scatter Plot**: Outdoor Temperature (`T_out`) vs Energy Consumption (`Appliances`).
- **Dual Axis Chart**: Indoor Humidity (`RH_1`) vs Energy Consumption over time.
- **Bar Chart**: Wind Speed bins vs Average Energy Use.
- **Correlation Matrix**: Thermal comfort features vs appliance energy.

### DASHBOARD 3: FORECAST AND INSIGHTS
- **Line Chart**: Actual vs Predicted Consumption on the unseen test set.
- **Future Demand Curve**: 24-Hour Out-of-Sample Forecast (Next 144 steps).
- **Error Distribution Plot**: Residual analysis showing prediction variance.
- **Insight Callouts**: Automated energy-saving recommendations during peak hours.

---

## How to Setup and Run the Project

### 1. Python Environment Setup
Install required dependencies:
```bash
python -m pip install pandas numpy scikit-learn xgboost matplotlib seaborn pymysql sqlalchemy python-dotenv joblib nbformat nbconvert
```

### 2. Configure Environment Variables
Create a local `.env` file in the project root:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=energy_consumption_db
DB_USER=root
DB_PASSWORD=Aaraay@277
```

### 3. Run Pipeline Scripts
Execute the production modules sequentially:
```bash
# 1. Clean raw data
python src/data_cleaning.py

# 2. Engineer features
python src/feature_engineering.py

# 3. Train candidate models
python src/train_model.py

# 4. Tune models & export final model artifact
python src/evaluate_model.py

# 5. Run sample inference
python src/predict.py
```

### 4. Setup MySQL Database
Run the Python automated MySQL database setup and loader script:
```bash
python sql/load_data_mysql.py
```
Or execute `sql/01_create_database.sql`, `sql/02_create_tables.sql`, `sql/03_load_data.sql`, `sql/04_analysis_queries.sql`, and `sql/05_tableau_views.sql` inside **MySQL Workbench**.

### 5. Export Tableau Datasets
Export all Tableau-ready CSV files:
```bash
python tableau/export_tableau_data.py
```

### 6. Run Jupyter Notebooks
Open VS Code Jupyter or Jupyter Lab and run notebooks `01` through `06` in `notebooks/`.

---

## Business Insights & Recommendations

1. **Peak Load Shifting**: Energy consumption peaks between **17:00 PM and 20:00 PM** (reaching ~170 Wh avg vs ~40 Wh overnight). Smart appliances should be scheduled to operate outside these hours.
2. **Weekend Consumption Management**: Household energy use is **~15% higher on weekends** due to continuous occupancy. Smart thermostat and HVAC adjustments can yield up to 10-12% energy savings.
3. **Humidity & Temperature Thresholds**: Indoor humidity levels (`RH_1`) above 45% strongly correlate with increased appliance energy draw. Dehumidification controls can optimize appliance energy efficiency.
