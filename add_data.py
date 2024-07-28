import streamlit as st
import pandas as pd
import mysql.connector

# Load data from MySQL database
def load_data():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Mirza@haziq514",
        "database": "agriculture"
    }
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM agridata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Save data to MySQL
def save_data_to_mysql(data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO agridata (PriceDate, State, District, Product, Quantity, UnitPrice, TotalPrice, Category, Consumption) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return False

# Add data
def add_data():
    df = load_data()
    states = df["State"].unique()

    if "selected_state" not in st.session_state:
        st.session_state.selected_state = states[0]
    if "selected_district" not in st.session_state:
        st.session_state.selected_district = ""
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = ""

    # State form
    with st.form("form_state"):
        state = st.selectbox("State", states, index=list(states).index(st.session_state.selected_state))
        st.session_state.selected_state = state
        state_confirmed = st.form_submit_button("Check State")

    if state_confirmed:
        districts = df[df["State"] == st.session_state.selected_state]["District"].unique()
        if "selected_district" not in st.session_state or st.session_state.selected_district not in districts:
            st.session_state.selected_district = districts[0] if len(districts) > 0 else ""

    # District form
    with st.form("form_district"):
        districts = df[df["State"] == st.session_state.selected_state]["District"].unique()
        district = st.selectbox("District", districts, index=list(districts).index(st.session_state.selected_district) if st.session_state.selected_district in districts else 0)
        st.session_state.selected_district = district
        district_confirmed = st.form_submit_button("Check District")

    if district_confirmed:
        consumption_areas = df[(df["State"] == st.session_state.selected_state) & (df["District"] == st.session_state.selected_district)]["Consumption"].unique()
        if "selected_category" not in st.session_state or st.session_state.selected_category not in consumption_areas:
            st.session_state.selected_category = consumption_areas[0] if len(consumption_areas) > 0 else ""

    # Data form
    with st.form("form_data"):
        pricedate = st.date_input("PriceDate")
        categories = df["Category"].unique()
        category = st.selectbox("Category", categories, index=list(categories).index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0)
        st.session_state.selected_category = category
        products = df[df["Category"] == category]["Product"].unique()
        product = st.selectbox("Product", products)
        quantity = st.number_input("Quantity", min_value=0, step=1)
        unitprice = st.number_input("UnitPrice", format="%.2f")
        totalprice = quantity * unitprice
        st.write(f"Total Price: RM {totalprice:.2f}")
        consumption_areas = df[(df["State"] == st.session_state.selected_state) & (df["District"] == st.session_state.selected_district)]["Consumption"].unique()
        consumption = st.selectbox("Consumption", consumption_areas)
        btn = st.form_submit_button("Save Data To MySQL Database", type="primary")

        if btn:
            if not all([pricedate, st.session_state.selected_state, st.session_state.selected_district, product, quantity, unitprice, category, consumption]):
                st.warning("All fields are required")
            else:
                data = (pricedate, st.session_state.selected_state, st.session_state.selected_district, product, quantity, unitprice, totalprice, category, consumption)
                if save_data_to_mysql(data):
                    st.success("Data has been successfully added to the MySQL database!")
                else:
                    st.error("Error: Unable to add data to the MySQL database.")

if __name__ == "__main__":
    add_data()

# Delete data from MySQL
def delete_data_from_mysql(agridata_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = conn.cursor()
        delete_query = "DELETE FROM agridata WHERE agridata_id = %s"
        cursor.execute(delete_query, (agridata_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return False
