import pandas as pd
import pyodbc
from sqlalchemy import create_engine

server = 'localhost\\SQLEXPRESS'
database = 'HealthcareDB'

conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'TrustServerCertificate=yes;'
    'Trusted_Connection=yes;'
)

engine = create_engine(f'mssql+pyodbc:///?odbc_connect={pyodbc.connect(conn_str).getinfo(pyodbc.SQL_DRIVER_NAME)}')

import urllib
params = urllib.parse.quote_plus(conn_str)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

def load_csv_to_sql(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

load_csv_to_sql('PatientDemographics.csv', 'PatientDemographics')
load_csv_to_sql('LabResults.csv', 'LabResults')
load_csv_to_sql('Diagnoses.csv', 'Diagnoses')
