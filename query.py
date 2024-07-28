import mysql.connector
import pandas as pd

# Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="Mirza@haziq514",
        db="agriculture"
    )

# Fetch
def view_all_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('select * from agridata')
        data = c.fetchall()
    return data

# Fetch all agriculture data
def view_all_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('select * from agridata')
        data = c.fetchall()
        columns = [desc[0] for desc in c.description]
    return pd.DataFrame(data, columns=columns)

def view_vendor_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('select * from vendordirectory')
        data = c.fetchall()
    return data
