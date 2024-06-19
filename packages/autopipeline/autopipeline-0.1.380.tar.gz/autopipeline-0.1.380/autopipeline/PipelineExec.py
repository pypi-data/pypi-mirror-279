import sqlite3
import pandas as pd

def query_exec(db, code, status, verbose):
    print(code)
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(code, conn)
    conn.close()
    status.append('code executed')
    return df, status, False, ""

def display(result, status, verbose):
    print(result)
    status.append('displayed')
    return status