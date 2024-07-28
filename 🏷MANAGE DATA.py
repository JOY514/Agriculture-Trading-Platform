import streamlit as st
import pandas as pd
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
import mysql.connector
from datetime import date, timedelta
from add_data import add_data, delete_data_from_mysql, load_data  # Import load_data
import base64

# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # Load background image
    image_path = "data/home2.jpg"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    # CSS for background image and styling
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}
            .metric-card, .stButton button, .stSelectbox, .stMultiselect, .stDateInput, .stNumberInput {{
                background-color: #FFFFFF;
                border-left: 4px solid #686664;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                color: #000000;
                font-weight: bold;
            }}
            .stButton button:hover {{
                background-color: #088F8F;
                color: #FFFFFF;
            }}
            .stTextInput label, .stDateInput label, .stNumberInput label, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
                color: black !important;
                font-weight: bold !important;
            }}
            .stSelectbox div[role="combobox"], .stMultiselect div[role="combobox"] {{
                color: #000000;
                font-weight: bold;
            }}
            [data-testid="stSidebar"] {{
                display: yes;
            }}
            .content-container {{
                background: rgba(0, 0, 0, 0);
                padding: 20px;
                border-radius: 10px;
            }}
            div[data-testid="metric-container"] {{
                background-color: green !important;
                border: 1px solid #000000;
                border-radius: 10px;
                padding: 10px;
                color: #FFFFFF;
                font-weight: bold;
            }}
            .custom-write {{
                color: black !important;
                font-weight: bold !important;
            }}
            .stExpander div[role="button"] p {{
                color: black !important;
                font-weight: bold !important;
            }}
            .stExpander .stSelectbox, .stExpander .stMultiselect {{
                color: black !important;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.1);
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load CSS Style
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Header for the admin dashboard
    st.header("ADMIN DASHBOARD")

    # Load data from MySQL
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Mirza@haziq514",
        "database": "agriculture",
    }
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM agriculture.agridata"
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert 'PriceDate' column to datetime.date
    df['PriceDate'] = pd.to_datetime(df['PriceDate']).dt.date

    # Sidebar for date selection
    with st.sidebar:
        st.title("Select Date Range")
        start_date = st.date_input("Start Date", date.today() - timedelta(days=365*4))
        end_date = st.date_input("End Date", date.today())

    # Filter data based on date range
    df_filtered = df[(df['PriceDate'] >= start_date) & (df['PriceDate'] <= end_date)]

    # Display filtered data
    with st.expander("Filtered MySQL Dataset"):
        filtered_df = dataframe_explorer(df_filtered, case=False)
        st.dataframe(filtered_df, use_container_width=True)

    # Layout columns
    col1, col2 = st.columns([2, 1])

    # Add data section
    with col1:
        st.subheader('Add New Record to Database')
        add_data()

    # Dataset metrics section
    with col2:
        st.subheader('Dataset Metrics')
        st.metric(label="All Agriculture Products", value=df_filtered.Product.count(), delta="Total Commodities")
        st.metric(label="Sum of Product Price (RM)", value=f"{df_filtered.TotalPrice.sum():,.0f}", delta=df_filtered.TotalPrice.median())

        st.metric(label="Maximum Price (RM)", value=f"{df_filtered.TotalPrice.max():,.0f}", delta="High Price")
        st.metric(label="Minimum Price (RM)", value=f"{df_filtered.TotalPrice.min():,.0f}", delta="Low Price")
        st.metric(label="Total Price Range (RM)", value=f"{df_filtered.TotalPrice.max() - df_filtered.TotalPrice.min():,.0f}", delta="Income Range")


    # Delete data section
    with st.expander("Delete Record from Database"):
        st.subheader('Delete Record')
        
        # Display data
        df = load_data()  # Use the function from add_data.py to load data
        agridata_id = st.selectbox('Select record to delete', df['agridata_id'])
        
        # Delete button
        if st.button('Delete Record'):
            if delete_data_from_mysql(agridata_id):
                st.success(f"Record with ID {agridata_id} has been successfully deleted from the MySQL database!")
            else:
                st.error(f"Error: Unable to delete record with ID {agridata_id} from the MySQL database.")
        
        st.dataframe(df)


    # Dot plot and bar charts
    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Products & Total Price')
        chart = alt.Chart(df_filtered).mark_circle().encode(
            x='Product',
            y='TotalPrice',
            color='Category',
        ).properties(width=600, height=400)
        st.altair_chart(chart, use_container_width=True)

    with col4:
        st.subheader('Products & Unit Price')
        bar_chart = alt.Chart(df_filtered).mark_bar().encode(
            x="month(PriceDate):O",
            y="sum(UnitPrice):Q",
            color="Product:N"
        ).properties(width=600, height=400)
        st.altair_chart(bar_chart, use_container_width=True)

    # Scatter plot and quantity bar chart
    col5, col6 = st.columns(2)

    with col5:
        st.subheader('Features by Frequency')
        feature_x = st.selectbox('Select feature for x Qualitative data', df_filtered.select_dtypes("object").columns)
        feature_y = st.selectbox('Select feature for y Quantitative Data', df_filtered.select_dtypes("number").columns)

        fig, ax = plt.subplots()
        ax = sns.scatterplot(data=df_filtered, x=feature_x, y=feature_y, hue=df_filtered.Product)
        st.pyplot(fig)

    with col6:
        st.subheader('Products & Quantities')
        bar_chart_quantity = alt.Chart(df_filtered).mark_bar().encode(
            x="sum(Quantity):Q",
            y=alt.Y("Product:N", sort="-x")
        ).properties(width=600, height=400)
        st.altair_chart(bar_chart_quantity, use_container_width=True)

    # Footer image (styled as circular and smaller)
    st.sidebar.markdown(
        """
        <style>
        .footer-img {
            border-radius: 50%;
            width: 150px;
            height: 150px;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.sidebar.image("data/logo2.png", width=150, output_format='PNG')

    # Edit data section
    st.subheader('Edit Record in Database')

    # Display all records
    st.write('All records:')
    st.dataframe(df_filtered, use_container_width=True)

    # Select the record to edit
    selected_index_to_edit = st.selectbox('Select record to edit', df_filtered.index)
    record_to_edit = df_filtered.loc[selected_index_to_edit]

    # Display the selected record
    st.write('Selected record:', record_to_edit)

    # Convert values to appropriate types
    try:
        edit_quantity = int(float(record_to_edit['Quantity']))
        edit_unitprice = float(record_to_edit['UnitPrice'])
    except ValueError as e:
        st.error(f"Error converting values: {e}")
        edit_quantity = 0
        edit_unitprice = 0.0

    # Edit the fields

    # Dropdown for State
    edit_state = st.selectbox('State', df['State'].unique(), index=list(df['State'].unique()).index(record_to_edit['State']))

    # Dropdown for District based on selected State
    districts = df[df['State'] == edit_state]['District'].unique()
    edit_district = st.selectbox('District', districts, index=list(districts).index(record_to_edit['District']) if record_to_edit['District'] in districts else 0)

    # Dropdown for Consumption based on selected District
    consumption_areas = df[df['District'] == edit_district]['Consumption'].unique()
    edit_consumption = st.selectbox('Consumption', consumption_areas, index=list(consumption_areas).index(record_to_edit['Consumption']) if record_to_edit['Consumption'] in consumption_areas else 0)

    # Dropdown for Category
    edit_category = st.selectbox('Category', df['Category'].unique(), index=list(df['Category'].unique()).index(record_to_edit['Category']))

    edit_product = st.text_input('Product', record_to_edit['Product'])
    edit_quantity = st.number_input('Quantity', min_value=0, step=1, value=edit_quantity)
    edit_unitprice = st.number_input('Unit Price', min_value=0.0, step=0.01, value=edit_unitprice)
    # edit_category = st.text_input('Category', record_to_edit['Category'])

    # Calculate the total price
    edit_totalprice = edit_quantity * edit_unitprice
    st.write(f'Calculated Total Price: RM {edit_totalprice:.2f}')

    # Save the changes
    if st.button('Update Record'):
        update_query = """
        UPDATE agridata
        SET State=%s, District=%s, Product=%s, Quantity=%s, UnitPrice=%s, TotalPrice=%s, Category=%s, Consumption=%s
        WHERE agridata_id=%s
        """
        data = (
            edit_state,
            edit_district,
            edit_product,
            edit_quantity,
            edit_unitprice,
            edit_totalprice,
            edit_category,
            edit_consumption,
            int(record_to_edit['agridata_id'])  # Ensure id is a Python int
        )

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(update_query, data)
            conn.commit()
            cursor.close()
            conn.close()
            st.success('Record updated successfully')
        except mysql.connector.Error as e:
            st.error(f'Error updating record: {e}')

if __name__ == "__main__":
    main()

