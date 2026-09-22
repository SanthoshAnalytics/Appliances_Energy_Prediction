"""
MySQL Automated Data Loader for Energy Consumption Forecasting.
Reads credentials from .env, creates energy_consumption_db database & tables,
and loads 19,735 records reliably into MySQL.
"""

import os
from pathlib import Path
import pandas as pd
import pymysql
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "energy_consumption_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def setup_mysql_database():
    print(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    
    # 1. Connect without database context to create DB
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )
    cursor = conn.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"Database `{DB_NAME}` verified/created.")
    conn.close()

    # 2. Connect to database and execute table creation DDL
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True
    )
    cursor = conn.cursor()

    ddl = """
    CREATE TABLE IF NOT EXISTS energy_consumption (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATETIME NOT NULL,
        Appliances INT NOT NULL,
        lights INT NOT NULL,
        T1 DECIMAL(6,2),
        RH_1 DECIMAL(6,2),
        T2 DECIMAL(6,2),
        RH_2 DECIMAL(6,2),
        T3 DECIMAL(6,2),
        RH_3 DECIMAL(6,2),
        T4 DECIMAL(6,2),
        RH_4 DECIMAL(6,2),
        T5 DECIMAL(6,2),
        RH_5 DECIMAL(6,2),
        T6 DECIMAL(6,2),
        RH_6 DECIMAL(6,2),
        T7 DECIMAL(6,2),
        RH_7 DECIMAL(6,2),
        T8 DECIMAL(6,2),
        RH_8 DECIMAL(6,2),
        T9 DECIMAL(6,2),
        RH_9 DECIMAL(6,2),
        T_out DECIMAL(6,2),
        Press_mm_hg DECIMAL(7,2),
        RH_out DECIMAL(6,2),
        Windspeed DECIMAL(6,2),
        Visibility DECIMAL(6,2),
        Tdewpoint DECIMAL(6,2),
        rv1 DECIMAL(10,6),
        rv2 DECIMAL(10,6),
        INDEX idx_date (date)
    );
    """
    cursor.execute(ddl)
    print("Table `energy_consumption` verified/created.")

    # 3. Load CSV data into MySQL if table is empty
    cursor.execute("SELECT COUNT(*) FROM energy_consumption;")
    row_count = cursor.fetchone()[0]
    
    if row_count == 0:
        csv_path = project_root / "Data" / "energydata_complete.csv"
        print(f"Loading data from {csv_path} into MySQL...")
        df = pd.read_csv(csv_path)

        cols = ["date", "Appliances", "lights", "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4", "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8", "T9", "RH_9", "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint", "rv1", "rv2"]
        
        insert_query = f"""
        INSERT INTO energy_consumption ({','.join(cols)})
        VALUES ({','.join(['%s'] * len(cols))})
        """
        
        data_tuples = [tuple(x) for x in df[cols].values]
        cursor.executemany(insert_query, data_tuples)
        print(f"Successfully inserted {len(data_tuples)} records into MySQL table `energy_consumption`!")
    else:
        print(f"Table `energy_consumption` already contains {row_count} records.")

    conn.close()


if __name__ == "__main__":
    setup_mysql_database()
