import mysql.connector
import streamlit as st

# Connection
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="Mirza@haziq514",
    db="agriculture"
)
c = conn.cursor()

# Fetch
def view_all_data():
    c.execute('SELECT * FROM agriculture.agridata')
    data = c.fetchall()
    return data

# Main code
data = view_all_data()
st.write(data)

# Close connection
conn.close()