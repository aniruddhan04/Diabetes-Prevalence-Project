# Diabetes Prevalence Analysis

This project analyzes annual diabetes prevalence rates using patient data stored in a SQL Server database.

## 📁 Project Structure

```
HealthcareDataAnalysis/
├── load_healthcare_data.py        # Script to load CSVs into the SQL Server database
├── diabetes_prevalence_analysis.py # Script to compute and visualize diabetes prevalence
├── PatientDemographics.csv
├── LabResults.csv
├── Diagnoses.csv
└── README.md
```

---

## 🚀 Step 1: Load Data into SQL Server

Make sure you have:

- Microsoft SQL Server installed (e.g., `SQLEXPRESS`)
- A database called **HealthcareDB**
- The CSV files:  
  - `PatientDemographics.csv`  
  - `LabResults.csv`  
  - `Diagnoses.csv`

### ✅ How to run the loading script:

1. Open a terminal (or VS Code terminal) and navigate to the project folder.
2. Run the following command:

```bash
python load_healthcare_data.py
```

This will:
- Connect to your local SQL Server instance
- Load each CSV into its respective table in `HealthcareDB`:
  - `PatientDemographics`
  - `LabResults`
  - `Diagnoses`

---

## 📊 Step 2: Run the Prevalence Analysis

This script reads from the SQL database, computes annual diabetes prevalence, and plots it.

### ✅ How to run the analysis script:

```bash
python diabetes_prevalence_analysis.py
```

This will:
- Query the three tables from SQL Server
- Calculate the number of diabetes diagnoses per year
- Plot the prevalence rate using Matplotlib
- Save results to a new table called `DiabetesPrevalence`

---

## 🧪 Requirements

Make sure you have the following Python packages installed:

```bash
pip install pandas matplotlib sqlalchemy pyodbc
```

You also need:
- **ODBC Driver 18 for SQL Server** (or adjust driver version in the script if needed)

---

## ⚙️ Configuration

If your SQL Server or database name is different, update the following section in both scripts:

```python
server = 'localhost\\SQLEXPRESS'
database = 'HealthcareDB'
```

---

## 📈 Output

The final output is:
- A line chart of diabetes prevalence per year
- A SQL table `DiabetesPrevalence` in your database for further reporting

---

## 📝 License

MIT License – you are free to use, modify, and distribute this project.
