# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# from datetime import datetime
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import LSTM, Dense
# import mysql.connector
# import base64

# # Set page configuration
# st.set_page_config(page_title="Forecast Page", page_icon="📈", layout="wide")
# st.header("AGRICULTURE COMMODITIES FORECAST")

# # Load background image
# image_path = "data/home2.jpg"
# with open(image_path, "rb") as image_file:
#     base64_image = base64.b64encode(image_file.read()).decode()

# # Read the CSS file
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

# # Connect to MySQL database
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Mirza@haziq514",
#     database="agriculture"
# )

# # Load your dataframe here
# query = "SELECT * FROM agridata"
# df_selection = pd.read_sql(query, connection)

# # Convert 'PriceDate' column to datetime
# df_selection['PriceDate'] = pd.to_datetime(df_selection['PriceDate'])

# # Display real-time date and time
# current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# st.write(f"Current Date and Time: {current_datetime}")

# # Dropdown for selecting commodity category
# category = st.selectbox('Select Commodity Category', df_selection['Category'].unique())

# # Dropdown for selecting commodity product
# product = st.selectbox('Select Commodity Product', df_selection[df_selection['Category'] == category]['Product'].unique())

# # Dropdown for selecting state
# state = st.selectbox('Select State', df_selection['State'].unique())

# # Calendar input for selecting date
# forecast_date = st.date_input('Select Date for Forecast', min_value=datetime.now())

# # Convert forecast_date to datetime
# forecast_date = pd.to_datetime(forecast_date)

# # Filter the DataFrame based on selected product, state, and date
# filtered_df = df_selection[(df_selection['Product'] == product) & 
#                            (df_selection['State'] == state) & 
#                            (df_selection['PriceDate'] <= forecast_date)]

# # Check the length of filtered_df
# st.write(f"Total data points selected: {len(filtered_df)}")

# # Ensure at least 20 data points to have enough for sequences
# if len(filtered_df) < 20:
#     st.error("Not enough data to perform forecasting. At least 20 data points are required.")
#     forecast_result = pd.DataFrame()
# else:
#     forecast_result = filtered_df.tail(20)

# # Close MySQL connection
# connection.close()

# # LSTM Forecast
# def lstm_forecast(df_price):
#     if len(df_price) < 10:
#         st.error("Not enough data to perform forecasting. At least 10 data points are required.")
#         return np.array([])

#     scaler = MinMaxScaler()
#     scaled_data = scaler.fit_transform(df_price[['UnitPrice', 'Quantity']])
    
#     st.write(f"Scaled data shape: {scaled_data.shape}")

#     X = []
#     y = []
#     for i in range(10, len(df_price)):
#         X.append(scaled_data[i-10:i, :])
#         y.append(scaled_data[i, 0])  # Predicting only UnitPrice

#     X, y = np.array(X), np.array(y)

#     st.write(f"X shape: {X.shape}")
#     st.write(f"y shape: {y.shape}")

#     if len(X) == 0 or X.shape[1] == 0:
#         st.error("Error in data shape after processing. Unable to reshape data for LSTM.")
#         return np.array([])

#     # Reshape data for LSTM
#     X = np.reshape(X, (X.shape[0], X.shape[1], 2))
#     st.write(f"Reshaped X for LSTM: {X.shape}")

#     # Build LSTM model
#     model = Sequential()
#     model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 2)))
#     model.add(LSTM(units=50, return_sequences=False))
#     model.add(Dense(units=1))

#     # Compile the model
#     model.compile(optimizer='adam', loss='mean_squared_error')

#     # Train the model
#     model.fit(X, y, epochs=100, batch_size=32)

#     # Predictions
#     forecast_data = scaled_data[-10:, :]
#     forecast_data = np.reshape(forecast_data, (1, forecast_data.shape[0], forecast_data.shape[1]))
#     forecast = model.predict(forecast_data)

#     # Inverse transform
#     forecast = scaler.inverse_transform(np.array([[forecast[0, 0], 0]]))

#     return forecast

# # Button for forecasting
# if st.button('Perform Forecasting'):
#     if len(forecast_result) >= 10:
#         forecast_results = lstm_forecast(forecast_result)
#         if forecast_results.size > 0:
#             forecasted_price = round(forecast_results[0, 0], 2)
#             st.write(f"Forecasted prices for {product} in {state} on {forecast_date}")
#             st.write(f"Forecasted Average UnitPrice: {forecasted_price}")

#             # Plot price change in each week
#             st.subheader("Price Change Over Time")
#             price_change = forecast_result.groupby('PriceDate')['UnitPrice'].mean().reset_index()
#             fig, ax = plt.subplots(figsize=(10, 6))
#             sns.lineplot(data=price_change, x='PriceDate', y='UnitPrice', ax=ax)
#             ax.set_title('Price Change Over Time')

#             # Add average price line
#             avg_price = price_change['UnitPrice'].mean()
#             ax.axhline(avg_price, color='blue', linestyle='--', label=f'Average Price: {avg_price:.2f}')

#             if not forecast_result.empty:
#                 min_price = forecast_result['UnitPrice'].min()
#                 max_price = forecast_result['UnitPrice'].max()
                
#                 min_price_idx = forecast_result['UnitPrice'].idxmin()
#                 max_price_idx = forecast_result['UnitPrice'].idxmax()
                
#                 if not forecast_result.empty and not forecast_result.loc[min_price_idx, 'PriceDate'] is None:
#                     ax.annotate(f'Min Price: {min_price:.2f}', xy=(forecast_result.loc[min_price_idx, 'PriceDate'], min_price), xytext=(-50, 20),
#                                 textcoords='offset points', arrowprops=dict(arrowstyle='->', color='green'), color='green')
#                 if not forecast_result.empty and not forecast_result.loc[max_price_idx, 'PriceDate'] is None:
#                     ax.annotate(f'Max Price: {max_price:.2f}', xy=(forecast_result.loc[max_price_idx, 'PriceDate'], max_price), xytext=(-50, -20),
#                                 textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'), color='red')

#                 # Add forecasted price line
#                 ax.axhline(forecasted_price, color='orange', linestyle='dotted', label=f'Forecasted Price: {forecasted_price:.2f}')

#                 ax.legend()
#                 st.pyplot(fig)

#                 # Show statistics
#                 st.subheader("Price Statistics")
#                 min_price = round(forecast_result['UnitPrice'].min(), 2)
#                 max_price = round(forecast_result['UnitPrice'].max(), 2)
#                 median_price = round(forecast_result['UnitPrice'].median(), 2)
#                 std_dev = round(forecast_result['UnitPrice'].std(), 2)
#                 variance = round(forecast_result['UnitPrice'].var(), 2)
#                 average_price = round(forecast_result['UnitPrice'].mean(), 2)

#                 # Display statistics in a colored table
#                 stats_data = {
#                     'Statistic': ['Min Price', 'Max Price', 'Median Price', 'Standard Deviation', 'Variance', 'Average Price'],
#                     'Value': [min_price, max_price, median_price, std_dev, variance, average_price]
#                 }
#                 stats_df = pd.DataFrame(stats_data)

#                 st.markdown(stats_df.to_html(index=False, classes='stats-table', border=0), unsafe_allow_html=True)

#                 # Recommendations based on scenarios
#                 recommendations = []

#                 if forecasted_price > average_price:
#                     recommendations.append(
#                         """
#                         - Monitor Price Trends: Regularly monitor the price trends to identify any significant changes or patterns. This will help in making informed decisions.
#                         - Analyze Demand and Supply: Keep an eye on the demand and supply of the product to anticipate price fluctuations.
#                         - Consider Seasonal Factors: Seasonal changes can significantly impact prices. Plan your production and sales strategy accordingly.
#                         """
#                     )
#                 else:
#                     recommendations.append(
#                         """
#                         - Evaluate Cost Efficiency: With lower forecasted prices, focus on reducing production costs to maintain profitability.
#                         - Diversify Product Offerings: Explore other products to balance the potential lower income from the current product.
#                         - Enhance Marketing Efforts: Increase marketing efforts to boost demand and potentially increase prices.
#                         """
#                     )

#                 if std_dev > average_price * 0.1:
#                     recommendations.append(
#                         """
#                         - Hedge Against Volatility: Consider financial instruments to hedge against price volatility.
#                         - Flexible Pricing Strategy: Implement a flexible pricing strategy to quickly adapt to market changes.
#                         """
#                     )
#                 else:
#                     recommendations.append(
#                         """
#                         - Stable Pricing Strategy: Maintain a stable pricing strategy to build consumer trust and loyalty.
#                         - Cost Management: Focus on managing costs efficiently to maximize profitability in a stable price environment.
#                         """
#                     )

#                 if (forecast_result['UnitPrice'].iloc[-1] > forecast_result['UnitPrice'].iloc[0]):
#                     recommendations.append(
#                         """
#                         - Capitalize on Increasing Trends: Increase production to capitalize on rising prices.
#                         - Invest in Quality: Invest in improving product quality to justify higher prices.
#                         """
#                     )
#                 else:
#                     recommendations.append(
#                         """
#                         - Adjust Inventory Levels: Reduce inventory levels to avoid overstocking during decreasing price trends.
#                         - Enhance Sales Promotions: Run sales promotions to boost demand in a declining price market.
#                         """
#                     )

#                 if variance > average_price * 0.2:
#                     recommendations.append(
#                         """
#                         - Monitor Market Factors: Closely monitor factors that contribute to price volatility, such as weather and market demand.
#                         - Diversify Revenue Streams: Diversify revenue streams to mitigate risks associated with high price volatility.
#                         """
#                     )

#                 # ... (Add more recommendations based on different scenarios)

#                 # Display all recommendations
#                 st.markdown(
#                     """
#                     ### Recommendations
#                     {}
#                     """.format("                    ".join(recommendations)),
#                     unsafe_allow_html=True
#                 )

#     # Additional CSS for styling
#     st.markdown(
#         """
#         <style>
#         .stats-table {
#             width: 50%;
#             margin-left: 0;
#             border-collapse: collapse;
#         }
#         .stats-table th, .stats-table td {
#             border: 1px solid #dddddd;
#             text-align: center;
#             padding: 8px;
#         }
#         .stats-table th {
#             background-color: #f2f2f2;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import mysql.connector
import base64

# Set page configuration
st.set_page_config(page_title="Forecast Page", page_icon="📈", layout="wide")
st.header("AGRICULTURE COMMODITIES FORECAST")

# Load background image
image_path = "data/home2.jpg"
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode()

# Read the CSS file
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

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mirza@haziq514",
    database="agriculture"
)

# Load your dataframe here
query = "SELECT * FROM agridata"
df_selection = pd.read_sql(query, connection)

# Convert 'PriceDate' column to datetime
df_selection['PriceDate'] = pd.to_datetime(df_selection['PriceDate'])

# Display real-time date and time
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"Current Date and Time: {current_datetime}")

# Dropdown for selecting state
state = st.selectbox('Select State', df_selection['State'].unique())

# Filter categories based on selected state
categories = df_selection[df_selection['State'] == state]['Category'].unique()
category = st.selectbox('Select Commodity Category', categories)

# Filter products based on selected category
products = df_selection[(df_selection['State'] == state) & (df_selection['Category'] == category)]['Product'].unique()
product = st.selectbox('Select Commodity Product', products)

# Calendar input for selecting date
forecast_date = st.date_input('Select Date for Forecast', min_value=datetime.now())

# Convert forecast_date to datetime
forecast_date = pd.to_datetime(forecast_date)

# Filter the DataFrame based on selected product, state, and date
filtered_df = df_selection[(df_selection['Product'] == product) & 
                           (df_selection['State'] == state) & 
                           (df_selection['PriceDate'] <= forecast_date)]

# Check the length of filtered_df
st.write(f"Total data points selected: {len(filtered_df)}")

# Ensure at least 15 data points to have enough for sequences
if len(filtered_df) < 15:
    st.error("Not enough data to perform forecasting. At least 15 data points are required.")
    forecast_result = pd.DataFrame()
else:
    forecast_result = filtered_df.tail(20)

# Close MySQL connection
connection.close()

# LSTM Forecast
def lstm_forecast(df_price):
    if len(df_price) < 10:
        st.error("Not enough data to perform forecasting. At least 10 data points are required.")
        return np.array([])

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_price[['UnitPrice', 'Quantity']])
    
    st.write(f"Scaled data shape: {scaled_data.shape}")

    X = []
    y = []
    for i in range(10, len(df_price)):
        X.append(scaled_data[i-10:i, :])
        y.append(scaled_data[i, 0])  # Predicting only UnitPrice

    X, y = np.array(X), np.array(y)

    st.write(f"X shape: {X.shape}")
    st.write(f"y shape: {y.shape}")

    if len(X) == 0 or X.shape[1] == 0:
        st.error("Error in data shape after processing. Unable to reshape data for LSTM.")
        return np.array([])

    # Reshape data for LSTM
    X = np.reshape(X, (X.shape[0], X.shape[1], 2))
    st.write(f"Reshaped X for LSTM: {X.shape}")

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 2)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X, y, epochs=100, batch_size=32)

    # Predictions
    forecast_data = scaled_data[-10:, :]
    forecast_data = np.reshape(forecast_data, (1, forecast_data.shape[0], forecast_data.shape[1]))
    forecast = model.predict(forecast_data)

    # Inverse transform
    forecast = scaler.inverse_transform(np.array([[forecast[0, 0], 0]]))

    return forecast

# Button for forecasting
if st.button('Perform Forecasting'):
    if len(forecast_result) >= 10:
        forecast_results = lstm_forecast(forecast_result)
        if forecast_results.size > 0:
            forecasted_price = round(forecast_results[0, 0], 2)
            st.write(f"Forecasted prices for {product} in {state} on {forecast_date}")
            st.write(f"Forecasted Average UnitPrice: {forecasted_price}")

            # Plot price change in each week
            st.subheader("Price Change Over Time")
            price_change = forecast_result.groupby('PriceDate')['UnitPrice'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=price_change, x='PriceDate', y='UnitPrice', ax=ax)
            ax.set_title('Price Change Over Time')

            # Add average price line
            avg_price = price_change['UnitPrice'].mean()
            ax.axhline(avg_price, color='blue', linestyle='--', label=f'Average Price: {avg_price:.2f}')

            if not forecast_result.empty:
                min_price = forecast_result['UnitPrice'].min()
                max_price = forecast_result['UnitPrice'].max()
                
                min_price_idx = forecast_result['UnitPrice'].idxmin()
                max_price_idx = forecast_result['UnitPrice'].idxmax()
                
                if not forecast_result.empty and not forecast_result.loc[min_price_idx, 'PriceDate'] is None:
                    ax.annotate(f'Min Price: {min_price:.2f}', xy=(forecast_result.loc[min_price_idx, 'PriceDate'], min_price), xytext=(-50, 20),
                                textcoords='offset points', arrowprops=dict(arrowstyle='->', color='green'), color='green')
                if not forecast_result.empty and not forecast_result.loc[max_price_idx, 'PriceDate'] is None:
                    ax.annotate(f'Max Price: {max_price:.2f}', xy=(forecast_result.loc[max_price_idx, 'PriceDate'], max_price), xytext=(-50, -20),
                textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'), color='red')

                # Add forecasted price line
                ax.axhline(forecasted_price, color='orange', linestyle='dotted', label=f'Forecasted Price: {forecasted_price:.2f}')

                ax.legend()
                st.pyplot(fig)

                # Show statistics
                st.subheader("Price Statistics")
                min_price = round(forecast_result['UnitPrice'].min(), 2)
                max_price = round(forecast_result['UnitPrice'].max(), 2)
                median_price = round(forecast_result['UnitPrice'].median(), 2)
                std_dev = round(forecast_result['UnitPrice'].std(), 2)
                variance = round(forecast_result['UnitPrice'].var(), 2)
                average_price = round(forecast_result['UnitPrice'].mean(), 2)

                # Display statistics in a colored table
                stats_data = {
                    'Statistic': ['Min Price', 'Max Price', 'Median Price', 'Standard Deviation', 'Variance', 'Average Price'],
                    'Value': [min_price, max_price, median_price, std_dev, variance, average_price]
                }
                stats_df = pd.DataFrame(stats_data)

                st.markdown(stats_df.to_html(index=False, classes='stats-table', border=0), unsafe_allow_html=True)

                # Recommendations based on scenarios
                recommendations = []

                if forecasted_price > average_price:
                    recommendations.append(
                        """
                        - Monitor Price Trends: Regularly monitor the price trends to identify any significant changes or patterns. This will help in making informed decisions.
                        - Analyze Demand and Supply: Keep an eye on the demand and supply of the product to anticipate price fluctuations.
                        - Consider Seasonal Factors: Seasonal changes can significantly impact prices. Plan your production and sales strategy accordingly.
                        """
                    )
                else:
                    recommendations.append(
                        """
                        - Evaluate Cost Efficiency: With lower forecasted prices, focus on reducing production costs to maintain profitability.
                        - Diversify Product Offerings: Explore other products to balance the potential lower income from the current product.
                        - Enhance Marketing Efforts: Increase marketing efforts to boost demand and potentially increase prices.
                        """
                    )

                if std_dev > average_price * 0.1:
                    recommendations.append(
                        """
                        - Hedge Against Volatility: Consider financial instruments to hedge against price volatility.
                        - Flexible Pricing Strategy: Implement a flexible pricing strategy to quickly adapt to market changes.
                        """
                    )
                else:
                    recommendations.append(
                        """
                        - Stable Pricing Strategy: Maintain a stable pricing strategy to build consumer trust and loyalty.
                        - Cost Management: Focus on managing costs efficiently to maximize profitability in a stable price environment.
                        """
                    )

                if (forecast_result['UnitPrice'].iloc[-1] > forecast_result['UnitPrice'].iloc[0]):
                    recommendations.append(
                        """
                        - Capitalize on Increasing Trends: Increase production to capitalize on rising prices.
                        - Invest in Quality: Invest in improving product quality to justify higher prices.
                        """
                    )
                else:
                    recommendations.append(
                        """
                        - Adjust Inventory Levels: Reduce inventory levels to avoid overstocking during decreasing price trends.
                        - Enhance Sales Promotions: Run sales promotions to boost demand in a declining price market.
                        """
                    )

                if variance > average_price * 0.2:
                    recommendations.append(
                        """
                        - Monitor Market Factors: Closely monitor factors that contribute to price volatility, such as weather and market demand.
                        - Diversify Revenue Streams: Diversify revenue streams to mitigate risks associated with high price volatility.
                        """
                    )

                # ... (Add more recommendations based on different scenarios)

                # Display all recommendations
                st.markdown(
                    """
                    ### Recommendations
                    {}
                    """.format("                    ".join(recommendations)),
                    unsafe_allow_html=True
                )

    # Additional CSS for styling
    st.markdown(
        """
        <style>
        .stats-table {
            width: 50%;
            margin-left: 0;
            border-collapse: collapse;
        }
        .stats-table th, .stats-table td {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
        }
        .stats-table th {
            background-color: #f2f2f2;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


