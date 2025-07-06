import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# Connection properties matching your setup
server = 'localhost\\SQLEXPRESS'
database = 'HealthcareDB'

# PyODBC connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'TrustServerCertificate=yes;'
    'Trusted_Connection=yes;'
)

# Create SQLAlchemy engine using the pyodbc connection string
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={pyodbc.connect(conn_str).getinfo(pyodbc.SQL_DRIVER_NAME)}')

# Alternatively, build the connection URL like this:
import urllib
params = urllib.parse.quote_plus(conn_str)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

def load_csv_to_sql(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

# Example usage:
load_csv_to_sql('PatientDemographics.csv', 'PatientDemographics')
load_csv_to_sql('LabResults.csv', 'LabResults')
load_csv_to_sql('Diagnoses.csv', 'Diagnoses')
