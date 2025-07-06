import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import pyodbc
import urllib

server = 'localhost\\SQLEXPRESS'
database = 'HealthcareDB'

conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'TrustServerCertificate=yes;'
    'Trusted_Connection=yes;'
)

params = urllib.parse.quote_plus(conn_str)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

with engine.connect() as conn:
    df_patients = pd.read_sql(text("SELECT PatientID, Age, Gender, Region FROM PatientDemographics"), conn)
    df_labs = pd.read_sql(text("SELECT PatientID, TestDate, A1CValue FROM LabResults WHERE TestType = 'A1C'"), conn)
    df_diag = pd.read_sql(text("SELECT PatientID, DiagnosisDate, DiagnosisCode FROM Diagnoses WHERE DiagnosisCode LIKE 'E10%' OR DiagnosisCode LIKE 'E11%'"), conn)

for df, col in [(df_labs, 'TestDate'), (df_diag, 'DiagnosisDate')]:
    df[col] = pd.to_datetime(df[col])

df_first_diag = (
    df_diag.sort_values('DiagnosisDate')
           .groupby('PatientID', as_index=False)['DiagnosisDate']
           .first()
           .rename(columns={'DiagnosisDate': 'FirstDiagnosisDate'})
)

df_merged = df_patients.merge(df_first_diag, on='PatientID', how='left')
df_merged['DiagnosisYear'] = df_merged['FirstDiagnosisDate'].dt.year

years = df_merged['DiagnosisYear'].dropna().unique()
totals = pd.Series(len(df_patients), index=years).rename('TotalPatients')
diag_counts = (
    df_merged.dropna(subset=['DiagnosisYear'])
             .groupby('DiagnosisYear')
             .size()
             .rename('DiagnosedPatients')
)
df_prev = pd.concat([totals, diag_counts], axis=1).fillna(0)
df_prev['PrevalenceRate'] = (df_prev['DiagnosedPatients'] / df_prev['TotalPatients']) * 100
df_prev = df_prev.reset_index().rename(columns={'index': 'Year'})

df_prev['Year'] = df_prev['Year'].astype(int)

df_prev['PrevalenceRate'] = df_prev['PrevalenceRate'].replace([float('inf'), float('-inf')], 0)
df_prev['PrevalenceRate'] = df_prev['PrevalenceRate'].fillna(0)

df_prev = df_prev.sort_values('Year')

plt.figure(figsize=(10, 6))
plt.plot(df_prev['Year'].astype(int), df_prev['PrevalenceRate'], marker='o')
plt.xticks(df_prev['Year'].astype(int))  # Force discrete ticks
plt.title('Annual Diabetes Prevalence Rate')
plt.xlabel('Year')
plt.ylabel('Prevalence Rate (%)')
plt.grid(True)
plt.tight_layout()
plt.show()

with engine.begin() as conn:
    df_prev.to_sql('DiabetesPrevalence', conn, if_exists='replace', index=False)

print("Analysis complete. Results saved to DiabetesPrevalence table.")
