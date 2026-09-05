# Intenational-Debt-Analysis

## Project Overview

**International Debt Analysis System Using Python, SQL, and Visualization Tools**

This project is an end-to-end data analytics project based on international debt data. The project takes raw CSV datasets, performs data cleaning and preprocessing using Python, stores the processed data in a MySQL database, performs SQL analysis, and presents the results through Streamlit and Power BI.

The main purpose of the project is to analyze country-wise and indicator-wise international debt data and identify useful trends, comparisons, rankings, and patterns.

---

## Project Objectives

The main objectives of this project are:

- Load international debt data from CSV files.
- Understand the structure and contents of the datasets.
- Clean and preprocess the raw data using Python.
- Handle missing values and duplicate records.
- Convert data into suitable data types.
- Transform the main debt dataset into a SQL-friendly long format.
- Validate country and indicator codes.
- Store cleaned data in a structured MySQL database.
- Use primary keys and foreign keys for relational data modeling.
- Perform 30 SQL analytical questions.
- Create an interactive Streamlit application for SQL analysis.
- Create a Power BI dashboard for visualization.
- Generate useful country-wise and indicator-wise insights.

---

#  End-to-End Project Workflow

```text
Raw CSV Datasets
       ↓
Python Data Preprocessing
       ↓
Data Cleaning & Transformation
       ↓
Cleaned CSV Files
       ↓
MySQL Database
       ↓
SQL Queries & Analysis
       ↓
┌───────────────────────┐
│                       │
▼                       ▼
Streamlit            Power BI
SQL Application      Dashboard
│                       │
└───────────┬───────────┘
            ↓
     Insights & Reporting
```

---

# Datasets Used

Five CSV datasets were used in this project:

```text
1. IDS_ALLCountries_Data.csv
2. Country-Series - Metadata.csv
3. IDS_CountryMetaData.csv
4. IDS_FootNoteMetaData.csv
5. IDS_SeriesMetaData.csv
```

## Main Debt Dataset

The main debt dataset contains the following fields:

```text
Country Name
Country Code
Counterpart-Area Name
Counterpart-Area Code
Series Name
Series Code
Year
Debt Value
```

The original dataset contained separate year columns. During preprocessing, these year columns were transformed into `Year` and `Debt Value` columns.

---

#  Python Data Preprocessing

The complete preprocessing workflow is contained in:

```text
preprocessing.py
```

## What was done

### 1. Loaded all five datasets

Pandas was used to load the CSV files into DataFrames.

### 2. Dataset inspection

The datasets were checked for:

- Number of rows
- Number of columns
- Duplicate records
- Missing values
- Data structure

### 3. Removed completely empty rows

Rows containing no data were removed.

### 4. Removed duplicate records

Duplicate records were identified and removed.

### 5. Cleaned column names

Extra spaces around column names were removed.

### 6. Cleaned text and codes

Extra spaces were removed from country codes, series codes, names, and other text fields.

### 7. Required-field validation

Rows missing important fields such as:

```text
Country Name
Country Code
Series Name
Series Code
```

were removed from the main debt dataset.

### 8. Country code validation

Country codes were checked to make sure they contain three characters.

### 9. Data type conversion

Year and debt values were converted into appropriate numeric formats.

### 10. Missing debt values

Rows where `Debt Value` was missing were removed from the final long-format debt dataset.

### 11. Negative-value checking

Negative values were checked and reported.

Negative values were not automatically deleted because financial indicators can contain legitimate negative values.

### 12. Wide-to-long transformation

The original year columns were transformed into:

```text
Country Name
Country Code
Counterpart-Area Name
Counterpart-Area Code
Series Name
Series Code
Year
Debt Value
```

This format is more suitable for SQL analysis and visualization.

### 13. Code matching

Country codes were checked against country metadata.

Series codes were checked against series metadata.

### 14. Cleaned files

Exactly five cleaned CSV files are generated:

```text
cleaned_data/
│
├── cleaned_debt_data.csv
├── cleaned_country_series_metadata.csv
├── cleaned_country_metadata.csv
├── cleaned_footnote_metadata.csv
└── cleaned_series_metadata.csv
```

---

# MySQL Database

A MySQL database named:

```sql
international_debt
```

was created.

The database contains five tables:

```text
IDS_ALLCountries_Data
Country-Series - Metadata
IDS_CountryMetaData
IDS_FootNoteMetaData
IDS_SeriesMetaData
```

---

# Database Design

The main relational structure is:

```text
IDS_CountryMetaData
        │
        │ Code
        ▼
IDS_ALLCountries_Data
        ▲
        │ Series Code
        │
IDS_SeriesMetaData
```

## Primary Keys

### IDS_CountryMetaData

```text
Code
```

### IDS_SeriesMetaData

```text
Code
```

### IDS_ALLCountries_Data

```text
Debt ID
```

### IDS_FootNoteMetaData

```text
Footnote ID
```

## Foreign Keys

The main debt table uses:

```text
Country Code
    ↓
IDS_CountryMetaData.Code
```

and:

```text
Series Code
    ↓
IDS_SeriesMetaData.Code
```

This creates relationships between country information, indicator information, and debt records.

---

# 📊 SQL Analysis

A total of **30 SQL analytical questions** were implemented.

The questions are divided into:

- Basic
- Intermediate
- Advanced

## Basic SQL Analysis

1. Retrieve all distinct country names.
2. Count the total number of countries.
3. Find the total number of indicators.
4. Display the first 10 records.
5. Calculate total global debt.
6. List all unique indicator names.
7. Find the number of records for each country.
8. Display records where debt is greater than 1 billion USD.
9. Find minimum, maximum, and average debt.
10. Count the total number of records.

## Intermediate SQL Analysis

11. Find total debt for each country.
12. Display the top 10 countries with the highest total debt.
13. Find average debt per country.
14. Calculate total debt for each indicator.
15. Identify the indicator contributing the highest total debt.
16. Find the country with the lowest total debt.
17. Calculate total debt for each country and indicator combination.
18. Count how many indicators each country has.
19. Find countries whose total debt is above the global average.
20. Rank countries based on total debt.

## Advanced SQL Analysis

21. Find the top 5 indicators contributing most to global debt.
22. Calculate percentage contribution of each country to total global debt.
23. Find the top 3 countries for each indicator.
24. Find the difference between maximum and minimum debt for each country.
25. Create a view for the top 10 countries.
26. Categorize countries into High, Medium, and Low Debt.
27. Calculate cumulative debt per country using window functions.
28. Find indicators whose average debt is higher than the overall average.
29. Identify countries contributing more than 5% of global debt.
30. Find the most dominant indicator for each country.

---

#  Streamlit SQL Application

The Streamlit application is contained in:

```text
sql_queries.py
```

The application connects to the MySQL database and allows the user to execute the SQL questions interactively.

## Streamlit Features

- MySQL connection status
- SQL question dropdown
- Selected question display
- SQL query display
- Execute Query button
- MySQL query execution
- Query result display
- Number of returned rows
- SQL error handling

## Streamlit Workflow

```text
Select SQL Question
        ↓
View SQL Query
        ↓
Click Execute Query
        ↓
Connect to MySQL
        ↓
Execute SQL
        ↓
Display Query Result
```

---

# 📈 Power BI Dashboard

A Power BI dashboard was created as part of the visualization stage.

The dashboard is used for:

- Country-wise debt analysis
- Indicator-wise analysis
- Debt trend analysis
- Country comparison
- Debt distribution
- Interactive filtering
- Data exploration

The Power BI file is stored in:

```text
PowerBI/
└── International_Debt_Dashboard.pbix
```

Screenshots of the dashboard can be stored in:

```text
screenshots/
```

---



#  Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/international-debt-analysis.git
```

Go to the project folder:

```bash
cd international-debt-analysis
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# 🐍 Run Data Preprocessing

Run:

```bash
python preprocessing.py
```

The cleaned datasets will be created inside:

```text
cleaned_data/
```

---


---

#  Project Outcomes

The project includes:

- ✅ Raw CSV datasets
- ✅ Python preprocessing
- ✅ Missing-value analysis
- ✅ Duplicate handling
- ✅ Data type conversion
- ✅ Data validation
- ✅ Wide-to-long transformation
- ✅ Five cleaned CSV datasets
- ✅ MySQL database
- ✅ Relational database structure
- ✅ Primary keys
- ✅ Foreign keys
- ✅ 30 SQL analytical queries
- ✅ SQL aggregations
- ✅ SQL ranking
- ✅ SQL window functions
- ✅ SQL view
- ✅ Streamlit SQL application
- ✅ Power BI dashboard
- ✅ Data visualization
- ✅ Country-wise analysis
- ✅ Indicator-wise analysis
- ✅ End-to-end analytics workflow

---

# 💡 Analysis and Insights

The project provides a structured way to explore:

- Country-wise debt distribution
- Countries with high and low debt
- Debt values across indicators
- Debt trends over time
- Indicator-wise contributions
- Country rankings
- Percentage contribution to global debt
- Maximum and minimum debt differences
- Dominant indicators for countries

---

# 🚀 Future Improvements

Future improvements can include:

- Deploying the Streamlit application online.
- Automating data updates.
- Adding more dashboard visualizations.
- Adding advanced filters.
- Adding additional economic indicators.
- Creating automated reports.
- Adding predictive analysis for future debt trends.

---

# 👨‍💻 Project Information

**Project Title:**  
International Debt Analysis System Using Python, SQL, and Visualization Tools

**Domain:**  
Finance Analytics & Global Economic Data Analysis

**Technologies:**  

```text
Python
Pandas
NumPy
MySQL
SQL
Streamlit
Power BI
Plotly
GitHub
```

---

# 📜 Conclusion

This project demonstrates a complete data analytics pipeline starting from raw international debt CSV datasets and ending with SQL analysis and interactive visualization.

The project combines Python data preprocessing, relational database design, SQL analytics, Streamlit application development, and Power BI visualization into a single end-to-end International Debt Analysis System.
