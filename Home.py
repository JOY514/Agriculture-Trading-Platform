import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime, timedelta
from query import view_all_data
import time
import base64

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.markdown('<h1 style="color: black; text-align: center;">AGRICULTURE TRADING PLATFORM</h1>', unsafe_allow_html=True)

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

    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Fetch data
    data = view_all_data()
    df = pd.DataFrame(data, columns=["agridata_id", "PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"])

    # Define helper functions
    def clean_unitprice(series):
        return series.replace('', 0).astype(float)

    def clean_data(df):
        df['PriceDate'] = pd.to_datetime(df['PriceDate'], format='%Y-%m-%d')
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0).astype(float)
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        return df

    df_clean = clean_data(df)

    def reduce_data(df, column, n_categories=5):
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        df[column] = pd.qcut(df[column], q=n_categories, labels=False, duplicates='drop')
        return df

    df_clean = reduce_data(df_clean, 'Category')

    # Split data
    X = df_clean.drop(columns=['TotalPrice'])
    y = df_clean['TotalPrice']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def determine_k(X_train, k_range):
        distortions = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42).fit(X_train)
            distortions.append(kmeans.inertia_)
        return distortions

    def plot_elbow_curve(distortions):
        fig, ax = plt.subplots()
        ax.plot(range(1, len(distortions) + 1), distortions)
        ax.set_xlabel('Number of Clusters (K)')
        ax.set_ylabel('Distortion')
        ax.set_title('Elbow Curve')
        st.pyplot(fig)

    def create_time_series_features(df, column1, column2):
        df[column1] = pd.to_datetime(df[column1])
        df[column1] = df[column1].dt.normalize()
        df[column2] = df[column2].astype('category').cat.codes
        df[column2] = df[column2].replace(np.nan, 0)
        df.set_index(column1, inplace=True, drop=False)
        df['WeekOfYear'] = df.index.strftime('%W')
        df['Month'] = df.index.month
        df['Year'] = df.index.year
        df['DayOfWeek'] = df.index.dayofweek
        df['Day'] = df.index.day
        df['MonthYear'] = df.index.to_period('M')
        df['YearMonth'] = df.index.to_period('M')
        df['WeekYear'] = df.index.to_period('W')
        return df

    def split_data(df, date_col, target_col):
        X = df.drop(columns=[date_col, target_col])
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler

    def build_lstm_model(input_shape, output_size, neurons):
        model = Sequential()
        model.add(LSTM(neurons, input_shape=(input_shape[1], input_shape[2]), return_sequences=True))
        model.add(LSTM(neurons))
        model.add(Dense(output_size))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def lstm_forecast(model, X_future, scaler, n_days):
        X_future = np.array(X_future).reshape(1, n_days, 2)
        X_future = scaler.transform(X_future)
        forecast = model.predict(X_future)
        forecast = scaler.inverse_transform(forecast)
        return forecast

    def display_lstm_forecast(df_price, date_col, target_col, n_days):
        X_train, X_test, y_train, y_test, scaler = split_data(df_price.drop(columns=[date_col, target_col]), date_col, target_col)
        model = build_lstm_model(X_train.shape[1:], 1, 50)
        model.fit(X_train, y_train, epochs=100, batch_size=64, verbose=0)
        X_future = [[X_test[-1][0], X_test[-1][1]]]
        forecast = lstm_forecast(model, X_future, scaler, n_days)
        st.subheader('LSTM Forecast Results')
        st.write(f"Price forecast for the next {n_days} days:")
        st.write(forecast)

    def display_ui():
        st.markdown('<div class="custom-write">Select a category:</div>', unsafe_allow_html=True)
        categories = df['Category'].unique().tolist()
        category = st.selectbox('', categories)
        products = df[df['Category'] == category]['Product'].unique()
        product = st.selectbox('', products)
        date = st.date_input('Select date:')
        date = pd.to_datetime(date)
        n_weeks = st.number_input('Number of weeks to forecast:', min_value=1, max_value=12, value=8)
        st.markdown('<div class="custom-write">Price trend for the selected product:</div>', unsafe_allow_html=True)
        df_product = df[df['Product'] == product]
        df_price = create_time_series_features(df_product, 'PriceDate', 'UnitPrice')
        fig = px.line(df_price, x='PriceDate', y='UnitPrice', title=f'Price trend for {product}')
        st.plotly_chart(fig, use_container_width=True)
        if st.button('Forecast'):
            display_lstm_forecast(df_price, 'PriceDate', 'UnitPrice', 28)

    # Initialize the LSTM model
    if 'product' not in st.session_state:
        st.session_state['product'] = None
    product = st.session_state['product']
    if product is None:
        st.markdown('<div class="custom-write">Please select a product.</div>', unsafe_allow_html=True)
    else:
        df_product = df[df['Product'] == product]
        df_price = create_time_series_features(df_product, 'PriceDate', 'UnitPrice')
        X_train, X_test, y_train, y_test, scaler = split_data(df_price, 'PriceDate', 'UnitPrice')
        model = build_lstm_model(X_train.shape[1:], 1, 50)

    # Sidebar filters
    state = st.sidebar.multiselect(
        "SELECT STATE",
        options=df["State"].unique(),
        default=df["State"].unique(),
    )
    district = st.sidebar.multiselect(
        "SELECT DISTRICT",
        options=df["District"].unique(),
        default=df["District"].unique(),
    )
    category = st.sidebar.multiselect(
        "SELECT CATEGORY",
        options=df["Category"].unique(),
        default=df["Category"].unique(),
    )

    df_selection = df.query(
        "State==@state & District==@district & Category==@category"
    )

    def Home():
        with st.expander("VIEW AGRICULTURE COMMODITIES"):
            showData = st.multiselect('Filter:', df_selection.columns, default=["PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"])
            st.dataframe(df_selection[showData], use_container_width=True)

        unit_price = float(pd.Series(df_selection['UnitPrice']).sum())
        price_mode = float(pd.Series(df_selection['UnitPrice']).mode().iloc[0])
        price_mean = float(pd.Series(df_selection['UnitPrice']).mean())
        price_median = float(pd.Series(df_selection['UnitPrice']).median())
        product = float(pd.Series(df_selection['Product']).value_counts().sum())

        total1, total2, total3, total4, total5 = st.columns(5, gap='small')
        with total1:
            st.info('Sum Price', icon="💰")
            st.metric(label="Sum Price", value=f"{unit_price:,.0f}")

        with total2:
            st.info('Highest Price', icon="💰")
            st.metric(label="Highest Price", value=f"{price_mode:,.0f}")

        with total3:
            st.info('Mean Price', icon="💰")
            st.metric(label="Mean Price", value=f"{price_mean:,.0f}")
            
        with total4:
            st.info('Median Price', icon="💰")
            st.metric(label="Median Price", value=f"{price_median:,.0f}")

        with total5:
            st.info('Total Product', icon="📦")
            st.metric(label="Total Product", value=numerize(product), help=f"Total Product: {product}")

        style_metric_cards(
            background_color="#FFFFFF", 
            border_left_color="#686664", 
            border_color="#000000", 
            box_shadow="#F71938"
        )

        # Variable distribution Histogram
        with st.expander("DISTRIBUTIONS BY FREQUENCY"):
            df_selection.hist(figsize=(16, 8), color='#898784', zorder=2, rwidth=0.9, legend=['Product'])
            st.pyplot()

    def Progressbar():
        st.markdown(
            """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
            unsafe_allow_html=True,
        )
        target = 3000000000
        current = df_selection["Quantity"].sum()
        percent = round((current / target * 100))
        mybar = st.progress(0)

        if percent > 100:
            st.subheader("Target done!")
        else:
            st.write(f"You have {percent}% of {format(target, 'd')} TZS")
            for percent_complete in range(percent):
                time.sleep(0.1)
                mybar.progress(percent_complete + 1, text="Target Percentage")

    def sideBar():
        with st.sidebar:
            current_datetime = datetime.now()
            st.write(f"Current Date: {current_datetime.strftime('%Y-%m-%d')}")
            st.write(f"Current Time: {current_datetime.strftime('%H:%M:%S')}")

            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Progress"],
                icons=["house", "eye"],
                menu_icon="cast",
                default_index=0
            )

        if selected == "Home":
            Home()
        if selected == "Progress":
            Progressbar()

    hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .stSidebar .stSidebarItem {
        background-color: #ffff00;
        color: #333;
        border-radius: 5px;
        padding: 5px 10px;
    }

    .stSidebar .stSidebarItem:hover {
        background-color: #ffcc00;
    }

    .stSidebar .stSidebarItem.stSidebarItemSelected {
        background-color: #ff9900;
    }

    .sidebar-content {
        color: white;
    }

    [data-testid=stSidebar] {
        color: white;
    }

    .custom-write {
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """

    st.markdown(hide_st_style, unsafe_allow_html=True)

    sideBar()
    st.sidebar.image("data/logo2.png", caption="")

    st.markdown('<div class="custom-write">PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES</div>', unsafe_allow_html=True)
    feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)
    fig2 = go.Figure(
        data=[go.Box(x=df['Product'], y=df[feature_y])],
        layout=go.Layout(
            title=go.layout.Title(text="FEATURES BY QUARTILES OF QUANTITY"),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
            yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
            font=dict(color='#cecdcd'),
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

    hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """

    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if __name__ == "__main__":
        main()


