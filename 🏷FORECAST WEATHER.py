# import streamlit as st
# import requests
# import pandas as pd
# from datetime import datetime
# import mysql.connector
# import base64

# # Set page configuration
# st.set_page_config(page_title="Weather Forecast", page_icon="⛅", layout="wide")

# # Load background image
# image_path = "data/home2.jpg"
# with open(image_path, "rb") as image_file:
#     base64_image = base64.b64encode(image_file.read()).decode()

# # CSS for background image and styling
# st.markdown(
#     f"""
#     <style>
#         .stApp {{
#             background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
#             background-size: cover;
#         }}
#         .metric-card, .stButton button, .stSelectbox, .stMultiselect, .stDateInput, .stNumberInput {{
#             background-color: #FFFFFF;
#             border-left: 4px solid #686664;
#             border-radius: 10px;
#             padding: 10px;
#             margin-bottom: 10px;
#             color: #000000;
#             font-weight: bold;
#         }}
#         .stButton button:hover {{
#             background-color: #088F8F;
#             color: #FFFFFF;
#         }}
#         .stTextInput label, .stDateInput label, .stNumberInput label, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
#             color: black !important;
#             font-weight: bold !important;
#         }}
#         .stSelectbox div[role="combobox"], .stMultiselect div[role="combobox"] {{
#             color: #000000;
#             font-weight: bold;
#         }}
#         [data-testid="stSidebar"] {{
#             display: yes;
#         }}
#         .content-container {{
#             background: rgba(0, 0, 0, 0);
#             padding: 20px;
#             border-radius: 10px;
#         }}
#         div[data-testid="metric-container"] {{
#             background-color: green !important;
#             border: 1px solid #000000;
#             border-radius: 10px;
#             padding: 10px;
#             color: #FFFFFF;
#             font-weight: bold;
#         }}
#         .custom-write {{
#             color: black !important;
#             font-weight: bold !important;
#         }}
#         .stExpander div[role="button"] p {{
#             color: black !important;
#             font-weight: bold !important;
#         }}
#         .stExpander .stSelectbox, .stExpander .stMultiselect {{
#             color: black !important;
#             font-weight: bold;
#             background-color: rgba(255, 255, 255, 0.1);
#         }}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.markdown('<div class="content-container">', unsafe_allow_html=True)

# # Function to fetch weather data from Weatherbit API
# def fetch_weather_data(lat, lon, api_key):
#     url = f"https://api.weatherbit.io/v2.0/forecast/daily?lat={lat}&lon={lon}&key={api_key}"
#     response = requests.get(url)
#     return response

# # Define coordinates for each district in Malaysia
# districts_coordinates = {
#     "Johor": {
#         "Johor Bahru": (1.4927, 103.7414),
#         "Muar": (2.0442, 102.5689),
#         "Batu Pahat": (1.8548, 102.9325)
#     },
#     "Kedah": {
#         "Alor Setar": (6.1248, 100.3679),
#         "Sungai Petani": (5.6470, 100.4870),
#         "Kulim": (5.3652, 100.5610)
#     },
#     "Kelantan": {
#         "Kota Bharu": (6.1254, 102.2387),
#         "Pasir Mas": (6.0496, 102.1397),
#         "Tanah Merah": (5.8080, 102.1506)
#     },
#     "Melaka": {
#         "Melaka City": (2.1896, 102.2501),
#         "Alor Gajah": (2.3786, 102.2087),
#         "Jasin": (2.3080, 102.4288)
#     },
#     "Negeri Sembilan": {
#         "Seremban": (2.7297, 101.9381),
#         "Port Dickson": (2.5225, 101.7952),
#         "Jempol": (2.9288, 102.4531)
#     },
#     "Pahang": {
#         "Kuantan": (3.8077, 103.3260),
#         "Temerloh": (3.4515, 102.4216),
#         "Bentong": (3.5216, 101.9094)
#     },
#     "Perak": {
#         "Ipoh": (4.5975, 101.0901),
#         "Taiping": (4.8500, 100.7410),
#         "Teluk Intan": (4.0220, 101.0208)
#     },
#     "Perlis": {
#         "Kangar": (6.4334, 100.1981),
#         "Arau": (6.4253, 100.2738),
#         "Padang Besar": (6.6640, 100.3087)
#     },
#     "Penang": {
#         "George Town": (5.4141, 100.3288),
#         "Butterworth": (5.3991, 100.3636),
#         "Bayan Lepas": (5.2927, 100.2775)
#     },
#     "Sabah": {
#         "Kota Kinabalu": (5.9804, 116.0735),
#         "Sandakan": (5.8450, 118.0570),
#         "Tawau": (4.2448, 117.8914)
#     },
#     "Sarawak": {
#         "Kuching": (1.5535, 110.3593),
#         "Miri": (4.3991, 113.9911),
#         "Sibu": (2.2927, 111.8279)
#     },
#     "Selangor": {
#         "Shah Alam": (3.0738, 101.5183),
#         "Petaling Jaya": (3.1073, 101.6067),
#         "Klang": (3.0348, 101.4435),
#         "Cyberjaya": (2.9225, 101.6504)
#     },
#     "Terengganu": {
#         "Kuala Terengganu": (5.3302, 103.1408),
#         "Dungun": (4.7499, 103.4259),
#         "Kemaman": (4.2300, 103.4472)
#     },
#     "Kuala Lumpur": {
#         "Kuala Lumpur": (3.1390, 101.6869),
#         "Sentul": (3.1756, 101.6900),
#         "Ampang": (3.1500, 101.7600)
#     },
#     "Putrajaya": {
#         "Putrajaya": (2.9264, 101.6964)
#     }
# }

# # Function to fetch agriculture data from MySQL database
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         port="3306",
#         user="root",
#         passwd="Mirza@haziq514",
#         db="agriculture"
#     )

# def view_all_data():
#     with get_connection() as conn:
#         c = conn.cursor()
#         c.execute('select * from agridata')
#         data = c.fetchall()
#     return data

# # Streamlit app
# st.header("Real-Time Weather Forecast")

# # API key for Weatherbit
# # api_key = "11fdd5c4bc9f41a69ae48b112dff5d86"
# api_key = "a98ce7502541468c8596b5a4993161e2"

# # Sidebar for user inputs
# st.sidebar.header("Select Weather Forecast Date")
# selected_date = st.sidebar.date_input("Select Date", datetime.today())

# # Create a date string for the forecast
# selected_date_str = selected_date.strftime("%Y-%m-%d")

# # Create a list to store all forecasts
# all_forecasts = []

# # Fetch weather data for each district
# for state, districts in districts_coordinates.items():
#     for district, (lat, lon) in districts.items():
#         response = fetch_weather_data(lat, lon, api_key)
#         if response.status_code == 200:
#             # Parse API response
#             data = response.json()
#             daily_data = data['data']

#             # Find the forecast for the selected date
#             for day in daily_data:
#                 if day['valid_date'] == selected_date_str:
#                     forecast = {
#                         "State": state,
#                         "District": district,
#                         "Date": selected_date_str,
#                         "Temperature (°C)": day['temp'],
#                         "Feels Like (°C)": day['app_max_temp'],
#                         "Pressure (hPa)": day['pres'],
#                         "Humidity (%)": day['rh'],
#                                                 "Dew Point (°C)": day['dewpt'],
#                         "Cloud Cover (%)": day['clouds'],
#                         "Visibility (km)": day['vis'],
#                         "Wind Speed (m/s)": day['wind_spd'],
#                         "Weather Description": day['weather']['description']
#                     }
#                     all_forecasts.append(forecast)

# # Create a DataFrame from all forecasts
# forecast_df = pd.DataFrame(all_forecasts)

# # Display the forecast in a table format
# if not forecast_df.empty:
#     st.subheader(f"Weather Forecast for Malaysia on {selected_date_str}")
#     st.dataframe(forecast_df)
# else:
#     st.error("No weather data available for the selected date.")

# # Function to fetch data from MySQL and display it
# def show_agriculture_data():
#     data = view_all_data()
#     df = pd.DataFrame(data, columns=["agridata_id", "PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"])
#     st.subheader("Agriculture Data")
#     st.dataframe(df)

# # Display agriculture data
# show_agriculture_data()

# # Chatbot for agriculture-related queries
# st.subheader("Ask ATP Chatbot")
# user_input = st.text_input("Ask anything about agriculture in Malaysia:")

# # Enhanced chatbot logic to match user input with database data
# def chatbot_response(user_input, df):
#     keywords = user_input.split()
#     matching_data = pd.DataFrame()
    
#     for keyword in keywords:
#         keyword_lower = keyword.lower()
#         keyword_upper = keyword.upper()
#         # Exact match with District, State, Product, and Category columns
#         matches = df[
#             (df['District'].str.lower() == keyword_lower) |
#             (df['State'].str.lower() == keyword_lower) |
#             (df['Product'].str.lower() == keyword_lower) |
#             (df['Product'].str.upper() == keyword_upper) |
#             (df['Category'].str.lower() == keyword_lower)
#         ]
#         matching_data = pd.concat([matching_data, matches])
    
#     # Further refine matches if user input includes a specific product
#     product_keywords = [keyword for keyword in keywords if any(keyword in product for product in df['Product'].unique())]
#     if product_keywords:
#         matching_data = matching_data[matching_data['Product'].str.contains('|'.join(product_keywords), case=False, na=False)]

#     if not matching_data.empty:
#         return matching_data.drop_duplicates()
#     else:
#         return "No matching data found."

# if user_input:
#     st.write(f"You asked: {user_input}")
#     response = chatbot_response(user_input, pd.DataFrame(view_all_data(), columns=["agridata_id", "PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"]))
#     if isinstance(response, pd.DataFrame):
#         st.write("Here is the matching data:")
#         st.dataframe(response)
#     else:
#         st.write(response)

# st.markdown('</div>', unsafe_allow_html=True)






# api_key = "11fdd5c4bc9f41a69ae48b112dff5d86"





import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import base64

# Set page configuration
st.set_page_config(page_title="Weather Forecast", page_icon="⛅", layout="wide")

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

# Function to fetch weather data from Weatherbit API
def fetch_weather_data(lat, lon, api_key):
    url = f"https://api.weatherbit.io/v2.0/forecast/daily?lat={lat}&lon={lon}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 429:
        # st.error("Rate limit exceeded. Switching to backup data.")
        return None
    elif response.status_code != 200:
        st.error(f"Error fetching weather data: {response.status_code}")
        return None
    return response.json()

# Define coordinates for each district in Malaysia
districts_coordinates = {
    "Johor": {
        "Johor Bahru": (1.4927, 103.7414),
        "Muar": (2.0442, 102.5689),
        "Batu Pahat": (1.8548, 102.9325)
    },
    "Kedah": {
        "Alor Setar": (6.1248, 100.3679),
        "Sungai Petani": (5.6470, 100.4870),
        "Kulim": (5.3652, 100.5610)
    },
    "Kelantan": {
        "Kota Bharu": (6.1254, 102.2387),
        "Pasir Mas": (6.0496, 102.1397),
        "Tanah Merah": (5.8080, 102.1506)
    },
    "Melaka": {
        "Melaka City": (2.1896, 102.2501),
        "Alor Gajah": (2.3786, 102.2087),
        "Jasin": (2.3080, 102.4288)
    },
    "Negeri Sembilan": {
        "Seremban": (2.7297, 101.9381),
        "Port Dickson": (2.5225, 101.7952),
        "Jempol": (2.9288, 102.4531)
    },
    "Pahang": {
        "Kuantan": (3.8077, 103.3260),
        "Temerloh": (3.4515, 102.4216),
        "Bentong": (3.5216, 101.9094)
    },
    "Perak": {
        "Ipoh": (4.5975, 101.0901),
        "Taiping": (4.8500, 100.7410),
        "Teluk Intan": (4.0220, 101.0208)
    },
    "Perlis": {
        "Kangar": (6.4334, 100.1981),
        "Arau": (6.4253, 100.2738),
        "Padang Besar": (6.6640, 100.3087)
    },
    "Penang": {
        "George Town": (5.4141, 100.3288),
        "Butterworth": (5.3991, 100.3636),
        "Bayan Lepas": (5.2927, 100.2775)
    },
    "Sabah": {
        "Kota Kinabalu": (5.9804, 116.0735),
        "Sandakan": (5.8450, 118.0570),
        "Tawau": (4.2448, 117.8914)
    },
    "Sarawak": {
        "Kuching": (1.5535, 110.3593),
        "Miri": (4.3991, 113.9911),
        "Sibu": (2.2927, 111.8279)
    },
    "Selangor": {
        "Shah Alam": (3.0738, 101.5183),
        "Petaling Jaya": (3.1073, 101.6067),
        "Klang": (3.0348, 101.4435),
        "Cyberjaya": (2.9225, 101.6504)
    },
    "Terengganu": {
        "Kuala Terengganu": (5.3302, 103.1408),
        "Dungun": (4.7499, 103.4259),
        "Kemaman": (4.2300, 103.4472)
    },
    "Kuala Lumpur": {
        "Kuala Lumpur": (3.1390, 101.6869),
        "Sentul": (3.1756, 101.6900),
        "Ampang": (3.1500, 101.7600)
    },
    "Putrajaya": {
        "Putrajaya": (2.9264, 101.6964)
    }
}

# Dummy data for fallback
fallback_data = [
    {"State": "Johor", "District": "Johor Bahru", "Date": "2024-07-01", "Temperature (°C)": 30, "Feels Like (°C)": 32, "Pressure (hPa)": 1010, "Humidity (%)": 70, "Dew Point (°C)": 24, "Cloud Cover (%)": 40, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Kedah", "District": "Alor Setar", "Date": "2024-07-01", "Temperature (°C)": 29, "Feels Like (°C)": 31, "Pressure (hPa)": 1011, "Humidity (%)": 72, "Dew Point (°C)": 25, "Cloud Cover (%)": 30, "Visibility (km)": 9, "Wind Speed (m/s)": 2, "Weather Description": "Sunny"},
        {"State": "Kelantan", "District": "Kota Bharu", "Date": "2024-07-01", "Temperature (°C)": 28, "Feels Like (°C)": 30, "Pressure (hPa)": 1012, "Humidity (%)": 75, "Dew Point (°C)": 26, "Cloud Cover (%)": 50, "Visibility (km)": 8, "Wind Speed (m/s)": 4, "Weather Description": "Cloudy"},
    {"State": "Melaka", "District": "Melaka City", "Date": "2024-07-01", "Temperature (°C)": 31, "Feels Like (°C)": 33, "Pressure (hPa)": 1009, "Humidity (%)": 68, "Dew Point (°C)": 23, "Cloud Cover (%)": 45, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Negeri Sembilan", "District": "Seremban", "Date": "2024-07-01", "Temperature (°C)": 32, "Feels Like (°C)": 34, "Pressure (hPa)": 1010, "Humidity (%)": 65, "Dew Point (°C)": 22, "Cloud Cover (%)": 35, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Sunny"},
    {"State": "Pahang", "District": "Kuantan", "Date": "2024-07-01", "Temperature (°C)": 30, "Feels Like (°C)": 32, "Pressure (hPa)": 1012, "Humidity (%)": 70, "Dew Point (°C)": 24, "Cloud Cover (%)": 40, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Perak", "District": "Ipoh", "Date": "2024-07-01", "Temperature (°C)": 29, "Feels Like (°C)": 31, "Pressure (hPa)": 1011, "Humidity (%)": 72, "Dew Point (°C)": 25, "Cloud Cover (%)": 30, "Visibility (km)": 9, "Wind Speed (m/s)": 2, "Weather Description": "Sunny"},
    {"State": "Perlis", "District": "Kangar", "Date": "2024-07-01", "Temperature (°C)": 28, "Feels Like (°C)": 30, "Pressure (hPa)": 1012, "Humidity (%)": 75, "Dew Point (°C)": 26, "Cloud Cover (%)": 50, "Visibility (km)": 8, "Wind Speed (m/s)": 4, "Weather Description": "Cloudy"},
    {"State": "Penang", "District": "George Town", "Date": "2024-07-01", "Temperature (°C)": 31, "Feels Like (°C)": 33, "Pressure (hPa)": 1009, "Humidity (%)": 68, "Dew Point (°C)": 23, "Cloud Cover (%)": 45, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Sabah", "District": "Kota Kinabalu", "Date": "2024-07-01", "Temperature (°C)": 30, "Feels Like (°C)": 32, "Pressure (hPa)": 1010, "Humidity (%)": 70, "Dew Point (°C)": 24, "Cloud Cover (%)": 40, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Sarawak", "District": "Kuching", "Date": "2024-07-01", "Temperature (°C)": 29, "Feels Like (°C)": 31, "Pressure (hPa)": 1011, "Humidity (%)": 72, "Dew Point (°C)": 25, "Cloud Cover (%)": 30, "Visibility (km)": 9, "Wind Speed (m/s)": 2, "Weather Description": "Sunny"},
    {"State": "Selangor", "District": "Shah Alam", "Date": "2024-07-01", "Temperature (°C)": 32, "Feels Like (°C)": 34, "Pressure (hPa)": 1010, "Humidity (%)": 65, "Dew Point (°C)": 22, "Cloud Cover (%)": 35, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Sunny"},
    {"State": "Terengganu", "District": "Kuala Terengganu", "Date": "2024-07-01", "Temperature (°C)": 30, "Feels Like (°C)": 32, "Pressure (hPa)": 1012, "Humidity (%)": 70, "Dew Point (°C)": 24, "Cloud Cover (%)": 40, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Kuala Lumpur", "District": "Kuala Lumpur", "Date": "2024-07-01", "Temperature (°C)": 31, "Feels Like (°C)": 33, "Pressure (hPa)": 1010, "Humidity (%)": 68, "Dew Point (°C)": 23, "Cloud Cover (%)": 45, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Partly cloudy"},
    {"State": "Putrajaya", "District": "Putrajaya", "Date": "2024-07-01", "Temperature (°C)": 32, "Feels Like (°C)": 34, "Pressure (hPa)": 1011, "Humidity (%)": 66, "Dew Point (°C)": 22, "Cloud Cover (%)": 35, "Visibility (km)": 10, "Wind Speed (m/s)": 3, "Weather Description": "Sunny"}
]

# Function to display dummy weather data
def display_dummy_weather_data():
    forecast_df = pd.DataFrame(fallback_data)
    st.subheader(f"Weather Forecast for Malaysia on {datetime.today().strftime('%Y-%m-%d')} (Fallback Data)")
    st.dataframe(forecast_df)

# Function to fetch agriculture data from MySQL database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="Mirza@haziq514",
        db="agriculture"
    )

def view_all_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('select * from agridata')
        data = c.fetchall()
    return data

# Streamlit app
st.header("Real-Time Weather Forecast")




#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


# API key for Weatherbit

api_key = "11fdd5c4bc9f41a69ae48b112dff5d86"
# api_key = "a98ce7502541468c8596b5a4993161e2"







# Sidebar for user inputs
st.sidebar.header("Select Weather Forecast Date")
selected_date = st.sidebar.date_input("Select Date", datetime.today())

# Create a date string for the forecast
selected_date_str = selected_date.strftime("%Y-%m-%d")

# Create a list to store all forecasts
all_forecasts = []

# Track if rate limit is exceeded
rate_limit_exceeded = False

# Fetch weather data for each district
for state, districts in districts_coordinates.items():
    for district, (lat, lon) in districts.items():
        data = fetch_weather_data(lat, lon, api_key)
        if data is None:
            rate_limit_exceeded = True
            break
        else:
            daily_data = data['data']
            forecast_found = False
            for day in daily_data:
                if day['valid_date'] == selected_date_str:
                    forecast = {
                        "State": state,
                        "District": district,
                        "Date": selected_date_str,
                        "Temperature (°C)": day['temp'],
                        "Feels Like (°C)": day['app_max_temp'],
                        "Pressure (hPa)": day['pres'],
                        "Humidity (%)": day['rh'],
                        "Dew Point (°C)": day['dewpt'],
                        "Cloud Cover (%)": day['clouds'],
                        "Visibility (km)": day['vis'],
                        "Wind Speed (m/s)": day['wind_spd'],
                        "Weather Description": day['weather']['description']
                    }
                    all_forecasts.append(forecast)
                    forecast_found = True
                    break
            if not forecast_found:
                next_available_date = (datetime.strptime(selected_date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                for day in daily_data:
                    if day['valid_date'] == next_available_date:
                        forecast = {
                            "State": state,
                            "District": district,
                            "Date": next_available_date,
                            "Temperature (°C)": day['temp'],
                            "Feels Like (°C)": day['app_max_temp'],
                            "Pressure (hPa)": day['pres'],
                            "Humidity (%)": day['rh'],
                            "Dew Point (°C)": day['dewpt'],
                            "Cloud Cover (%)": day['clouds'],
                            "Visibility (km)": day['vis'],
                            "Wind Speed (m/s)": day['wind_spd'],
                            "Weather Description": day['weather']['description']
                        }
                        all_forecasts.append(forecast)
                        break

# If rate limit is exceeded, display fallback data
if rate_limit_exceeded:
    display_dummy_weather_data()
else:
    # Create a DataFrame from all forecasts
    forecast_df = pd.DataFrame(all_forecasts)

    # Display the forecast in a table format
    if not forecast_df.empty:
        st.subheader(f"Weather Forecast for Malaysia on {selected_date_str}")
        st.dataframe(forecast_df)
    else:
        st.error("No weather data available for the selected date.")

# Function to fetch data from MySQL and display it
def show_agriculture_data():
    data = view_all_data()
    df = pd.DataFrame(data, columns=["agridata_id", "PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"])
    st.subheader("Agriculture Data")
    st.dataframe(df)

# Display agriculture data
show_agriculture_data()

# Chatbot for agriculture-related queries
st.subheader("Ask ATP Chatbot")
user_input = st.text_input("Ask anything about agriculture in Malaysia:")

# Enhanced chatbot logic to match user input with database data
def chatbot_response(user_input, df):
    keywords = user_input.split()
    matching_data = pd.DataFrame()
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_upper = keyword.upper()
        # Exact match with District, State, Product, and Category columns
        matches = df[
            (df['District'].str.lower() == keyword_lower) |
            (df['State'].str.lower() == keyword_lower) |
            (df['Product'].str.lower() == keyword_lower) |
            (df['Product'].str.upper() == keyword_upper) |
            (df['Category'].str.lower() == keyword_lower)
        ]
        matching_data = pd.concat([matching_data, matches])
    
    # Further refine matches if user input includes a specific product
    product_keywords = [keyword for keyword in keywords if any(keyword in product for product in df['Product'].unique())]
    if product_keywords:
        matching_data = matching_data[matching_data['Product'].str.contains('|'.join(product_keywords), case=False, na=False)]

    if not matching_data.empty:
        return matching_data.drop_duplicates()
    else:
        return "No matching data found."

if user_input:
    st.write(f"You asked: {user_input}")
    response = chatbot_response(user_input, pd.DataFrame(view_all_data(), columns=["agridata_id", "PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"]))
    if isinstance(response, pd.DataFrame):
        st.write("Here is the matching data:")
        st.dataframe(response)
    else:
        st.write(response)

st.markdown('</div>', unsafe_allow_html=True)




