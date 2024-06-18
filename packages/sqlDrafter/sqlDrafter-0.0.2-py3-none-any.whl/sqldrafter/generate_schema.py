import requests
from sqldrafter.util import identify_categorical_columns
from io import StringIO
import pandas as pd
import json







def generate_mysql_schema(
    self,
    tables: list,
    upload: bool = True,
    return_format: str = "csv",
    scan: bool = True,
    return_tables_only: bool = False,
) -> str:
    try:
        import mysql.connector
    except:
        raise Exception("mysql-connector not installed.")

    conn = mysql.connector.connect(**self.db_creds)
    cur = conn.cursor()
    schemas = {}

    if len(tables) == 0:
        # get all tables
        db_name = self.db_creds.get("database", "")
        cur.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';"
        )
        tables = [row[0] for row in cur.fetchall()]

    if return_tables_only:
        return tables

    print("Getting schema for the relevant table in your database...")
    # get the schema for each table
    for table_name in tables:
        cur.execute(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;",
            (table_name,),
        )
        rows = cur.fetchall()
        rows = [row for row in rows]
        rows = [{"column_name": i[0], "data_type": i[1]} for i in rows]
        if scan:
            rows = identify_categorical_columns(cur, table_name, rows)
        schemas[table_name] = rows

    conn.close()

    if upload:
        r = requests.post(
            f"{self.base_url}/get_schema_csv",
            json={
                "api_key": self.api_key,
                "schemas": schemas,
                "foreign_keys": [],
                "indexes": [],
            },
        )
        resp = r.json()
        if "csv" in resp:
            csv = resp["csv"]
            if return_format == "csv":
                pd.read_csv(StringIO(csv)).to_csv("sqldrafter.csv", index=False)
                return "sss.csv"
            else:
                return csv
        else:
            print(f"We got an error!")
            if "message" in resp:
                print(f"Error message: {resp['message']}")
            print(
                f""
            )
    else:
        return schemas





def generate_db_schema(
    self,
    tables: list,
    scan: bool = True,
    upload: bool = True,
    return_tables_only: bool = False,
    return_format: str = "csv",
) -> str:
    if self.db_type == "mysql":
        return self.generate_mysql_schema(
            tables,
            return_format=return_format,
            scan=scan,
            upload=upload,
            return_tables_only=return_tables_only,
        )
    else:
        raise ValueError(
            f""
        )
