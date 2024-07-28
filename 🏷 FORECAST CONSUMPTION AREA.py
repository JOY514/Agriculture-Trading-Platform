import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_folium import folium_static
import folium
import plotly.graph_objs as go
import plotly.express as px
from folium.plugins import MarkerCluster, HeatMap
from folium import plugins
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, LSTM, Flatten
from streamlit_extras.metric_cards import style_metric_cards
import datetime
import base64

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

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

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Database connection
def get_data_from_db():
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="Mirza@haziq514",
        database="agriculture"
    )
    query = "SELECT * FROM consumptionareas"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def add_google_maps(m):
    tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    attr = "Google Digital Satellite"
    folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)
    # Add labels for streets and objects
    label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
    label_attr = "Google Labels"
    folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)
    return m

def main():
    load_df = get_data_from_db()

    # Rename the column to remove BOM
    if 'State' in load_df.columns:
        load_df.rename(columns={'State': 'State'}, inplace=True)

    # Sidebar
    st.sidebar.image("data/logo2.png", caption="")
    selected_state = st.sidebar.selectbox("Select State", ["All"] + list(load_df["State"].unique()))
    selected_date = st.sidebar.date_input("Select Date", min_value=datetime.date.today())

    if selected_state == "All":
        df = load_df
    else:
        df = load_df[load_df["State"] == selected_state]

    # Format numerical data to two decimal places
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.round(2))

    # Main Content
    try:
        st.header("DEMAND AND CONSUMPTION AREA")
        items = len(df)
        total_price = df['TotalPrice'].sum()

        with st.expander("ANALYTICS"):
            a1, a2 = st.columns(2)
            a1.metric(label="Consumption Area", value=items, help=f"Demand: {total_price}", delta=total_price)
            a2.metric(label="Demand", value=total_price, help=f"Demand: {total_price}", delta=total_price)

        # Show table data based on user input
        with st.expander("DETAILS OF CONSUMPTION AREA"):
            shuffled_df = df.sample(frac=1)  # Shuffle the dataframe
            st.dataframe(shuffled_df, height=400)  # Make table scrollable

        # Show forecasted data based on selected date
        if selected_date:
            # Convert Quantity column to numeric
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

            # Filter out rows with NaN values in Quantity column
            df = df.dropna(subset=['Quantity'])

            # Group by Product and aggregate TotalPrice and Quantity
            forecast_df = df.groupby("Product").agg({"TotalPrice": "sum", "Quantity": "mean"}).reset_index()
            forecast_df["Required Stock"] = forecast_df["TotalPrice"] / forecast_df["Quantity"]
            forecast_df["Predicted UnitPrice"] = forecast_df["TotalPrice"] / forecast_df["Quantity"]

            # Round and format Required Stock and Predicted UnitPrice
            forecast_df["Required Stock"] = forecast_df["Required Stock"].round(2)
            forecast_df["Predicted UnitPrice"] = forecast_df["Predicted UnitPrice"].round(2)

            st.subheader("Forecasted Consumption Area")
            st.dataframe(forecast_df, height=400)  # Make table scrollable

        # Create a map with the filtered data
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)
        for i, row in df.iterrows():
            popup_content = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <ul class="list-group">
            <h3>Information of {row['State']}</h3>
            <hr class='bg-danger text-primary'>
            <div style='width:400px;height:200px;margin:10px;color:gray;text-size:18px;'>
            <li class="list-group-item"><b>State:</b> {row['State']}</li>
            <li class="list-group-item"><b>Most Consumption Area:</b> {row['Consumption']}<br></li>
            <li class="list-group-item"><b>Population:</b> {row['Population']}<br></li>
            <li class="list-group-item"><b>Product in Demand:</b> {row['Product']}<br></li>
            <li class="list-group-item"><b>Market Stock:</b> {row['Quantity']}<br></li>
            <li class="list-group-item"><h4>Total Sales: RM {row['TotalPrice']}</b><br></li>
            <li class="list-group-item"><h4>Vendor Centre: {row['phonenumber']}</h4></li>"""
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=row['State'],
                icon=folium.Icon(color='red', icon='fa-dollar-sign', prefix='fa')
            ).add_to(marker_cluster).add_child(folium.Popup(popup_content, max_width=600))

        # Heatmap Layer
        heat_data = [[row['Latitude'], row['Longitude']] for i, row in df.iterrows()]
        HeatMap(heat_data).add_to(m)

                # Fullscreen Control
        plugins.Fullscreen(position='topright', title='Fullscreen', title_cancel='Exit Fullscreen').add_to(m)

        # Drawing Tools
        draw = plugins.Draw(export=True)
        draw.add_to(m)

        # Add Google Maps layers
        m = add_google_maps(m)

        # Layer Control
        m.add_child(folium.LayerControl(collapsed=False))

        with st.expander("FORECAST CONSUMPTION AREA"):
            folium_static(m, width=1350, height=600)

        # Graphs
        col1, col2 = st.columns(2)
        with col1:
            fig2 = go.Figure(
                data=[go.Bar(x=df['State'], y=df['TotalPrice'])],
                layout=go.Layout(
                    title=go.layout.Title(text="BAR CHART STATES BY TOTAL SALES PERFORMANCE"),
                    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
                    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
                    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
                    font=dict(color='#cecdcd'),  # Set text color to gray
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # Create a donut chart
            fig = px.pie(df, values='TotalPrice', names='State', title='PIE CHART TOTAL SALES BY STATES')
            fig.update_traces(hole=0.4)
            fig.update_layout(width=800)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Unable to display data. Error: {}".format(e))

if __name__ == "__main__":
    main()

