# ENERGY CONSUMPTION FORECASTING AND ANALYTICS

An end-to-end data science, machine learning, time-series forecasting, MySQL analytics, and Tableau dashboard portfolio project using the UCI Appliances Energy Prediction dataset.

---

## AI-Assisted Development

AI was used as a development assistant rather than simply as a code generator.

## Areas Where AI Was Used

| Area | AI Assistance |
|---|---|
| Project Planning | Suggested complete project workflow |
| Architecture | Generated folder and file structure |
| Data Cleaning | Generated data inspection and cleaning code |
| EDA | Generated statistical analysis and visualizations |
| Feature Engineering | Suggested calendar, lag, and rolling features |
| Machine Learning | Generated model training pipelines |
| Model Evaluation | Generated evaluation metrics and comparison code |
| Forecasting | Assisted with time-series forecasting workflow |
| Debugging | Helped identify and fix Python errors |
| SQL | Generated analytical queries and database structures |
| MySQL | Assisted with database integration |
| Tableau | Prepared dashboard-ready datasets and visualization ideas |
| Documentation | Assisted in creating README and project documentation |


![Uploading 8de241c8-b64b-403f-b2ea-040acb666c2f.png…]()

## AI vs Human Data Science

AI can perform many implementation tasks quickly, but the responsibilities of a Data Scientist are broader than writing code.

| Task | AI Capability | Human Responsibility |
|---|---|---|
| Problem Definition | Suggests possible approaches | Understand the actual business problem |
| Data Understanding | Explains columns and statistics | Verify the meaning and quality of data |
| Data Cleaning | Generates cleaning code | Decide what should actually be removed or changed |
| EDA | Creates charts quickly | Identify meaningful patterns |
| Feature Engineering | Suggests many features | Select relevant and valid features |
| Model Selection | Suggests algorithms | Understand model assumptions and suitability |
| Model Training | Generates training pipelines | Verify the training process |
| Model Evaluation | Calculates metrics | Interpret whether results are meaningful |
| Forecasting | Generates forecasting approaches | Validate forecasting assumptions |
| Debugging | Suggests possible fixes | Understand and verify the actual problem |
| SQL | Generates queries | Check whether queries answer the right questions |
| Tableau | Suggests visualizations | Decide what information should be presented |
| Business Insights | Summarizes patterns | Validate conclusions using the data |
| Final Decision | Provides suggestions | Human makes the final decision |

## AI-Assisted Workflow

The project followed an iterative AI-assisted development process:

```text
Project Requirement
        ↓
Detailed Prompt
        ↓
AI-Generated Approach
        ↓
Code Implementation
        ↓
Run and Test
        ↓
Identify Errors
        ↓
AI-Assisted Debugging
        ↓
Human Review
        ↓
Validation
        ↓
Final Implementation
```
## Prompt Engineering

A major part of the development process was converting the project requirements into detailed prompts.

Instead of asking AI to simply:

```Build an energy forecasting project.```

# Debugging and Iteration

The AI-generated implementation was not always correct on the first attempt.

Several development issues required testing and correction, including:

Missing Python packages
Incorrect file paths
Missing feature columns
Notebook execution errors
XGBoost installation issues
Feature engineering problems
MySQL integration issues
Tableau workbook compatibility issues

This demonstrated that AI-assisted development is an iterative process, not a one-click solution.

# Data Validation

Special attention was given to validating the generated Data Science workflow.

The project checked:

Missing values
Duplicate records
Date and time formats
Chronological ordering
Feature availability
Lag calculations
Rolling calculations
Train/test separation
Data leakage
Model evaluation metrics
Data Leakage Awareness

Time-series forecasting requires additional care because future information must not be used to predict the past.

For example, rolling features were created using previous observations:

df["rolling_mean_6"] = (
    df["Appliances"]
    .shift(1)
    .rolling(6)
    .mean()
)

This ensures that the current target value is not directly included in its own prediction features.

The Complexity Challenge

AI can generate a large amount of code very quickly. However, more code does not necessarily mean a better project.

## A simple workflow:
```
Data
 ↓
EDA
 ↓
Model
 ↓
Evaluation

can quickly become:

Data Cleaning
 ↓
EDA
 ↓
Feature Engineering
 ↓
Lag Features
 ↓
Rolling Features
 ↓
Multiple Models
 ↓
Cross Validation
 ↓
Hyperparameter Tuning
 ↓
Forecasting
 ↓
MySQL
 ↓
SQL Views
 ↓
Tableau
```
# This created an important learning point:

Technical complexity should support the project objective rather than exist only for the sake of adding more technologies.

# Understanding Generated Code

One of the biggest challenges of AI-assisted development is that generated code can work without being fully understood by the developer.

Therefore, each major component should be explainable:

Why was this feature created?
Why was this model selected?
Why was this metric used?
Why is chronological splitting required?
Why is shift(1) used before rolling?
Why is this SQL query useful?
Why is this Tableau visualization included?

Being able to answer these questions is more important than simply being able to execute the code.

## Human Validation Layer

# The final development process can therefore be viewed as:

AI Generation
      ↓
Execution
      ↓
Testing
      ↓
Human Review
      ↓
Correction
      ↓
Validation
      ↓
Interpretation

AI provides speed and technical assistance, while human validation provides reliability and context.

# Key Learning

This project demonstrated that modern Data Science involves much more than writing Python code.

Important skills include:

Problem solving
Data understanding
Statistical thinking
Critical thinking
Feature engineering
Model evaluation
Debugging
Business understanding
Data visualization
Communication

AI can assist with many of these activities, but the developer must still understand the reasoning behind the final solution.

## Final Reflection

The main lesson from this project is:

AI can significantly accelerate Data Science development, but speed of implementation is not the same as depth of understanding.

AI was extremely useful for reducing repetitive development work and quickly exploring different approaches. At the same time, the project showed that generated solutions must be tested, reviewed, corrected, and understood before they can be considered reliable.

I therefore consider AI in this project as a development accelerator and technical assistant, while human reasoning remains responsible for validation, interpretation, and final understanding.

### *AI can generate the solution faster. Human understanding determines whether the solution is actually useful.*


