import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import base64

# Load background image
image_path = "data/home2.jpg"
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode()

#config page layout to wide
st.set_page_config(page_title="Home", page_icon="", layout="wide")

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

# Load Style css
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.success("**FREQUENCY DISTRIBUTION TABLE**")

# Load dataset
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

with st.expander("🔎 VIEW TRAINING DATASET"):
    showData = st.multiselect("", df.columns, default=["PriceDate", "State", "District", "Product", "Quantity", "UnitPrice", "TotalPrice", "Category", "Consumption"])
    st.dataframe(df[showData], use_container_width=True)

#side navigation 
st.sidebar.image("data/logo2.png")

#calculate a frequency
frequency = df.UnitPrice.value_counts().sort_index()

#calculate percentage frequency %
percentage_frequency = frequency / len(df.UnitPrice) * 100

#calculate cumulative frequency
cumulative_frequency = frequency.cumsum()

#relative frequency
relative_frequency = frequency / len(df.UnitPrice)

#cumulative relative frequency
cumulative_relative_frequency = relative_frequency.cumsum()

#create summarized table
summary_table = pd.DataFrame({
    'Frequency': frequency,
    'Percentage Frequency': percentage_frequency,
    'Cumulative Frequency': cumulative_frequency,
    'Relative Frequency': relative_frequency,
    'Cumulative Relative Frequency': cumulative_relative_frequency
})

showData = st.multiselect("### FREQUENCY OF UNIT PRICE", summary_table.columns, default=["Frequency", "Percentage Frequency", "Cumulative Frequency", "Relative Frequency", "Cumulative Relative Frequency"])
st.dataframe(summary_table[showData], use_container_width=True)

valid_unitprice_values = df['UnitPrice'].dropna().values

#FREQUENCY OF AGRICULTURE COMMODITIES

#calculate a frequency
frequency1 = df.Product.value_counts().sort_index()

#calculate percentage frequency %
percentage_frequency1 = frequency1 / len(df.Product) * 100

#calculate cumulative frequency
cumulative_frequency1 = frequency1.cumsum()

#relative frequency
relative_frequency1 = frequency1 / len(df.Product)

#cumulative relative frequency
cumulative_relative_frequency1 = relative_frequency1.cumsum()

#create summarized table
summary_table1 = pd.DataFrame({
    'Frequency1': frequency1,
    'Percentage Frequency1': percentage_frequency1,
    'Cumulative Frequency1': cumulative_frequency1,
    'Relative Frequency1': relative_frequency1,
    'Cumulative Relative Frequency1': cumulative_relative_frequency1
})

showData = st.multiselect("### FREQUENCY OF PRODUCTS", summary_table1.columns, default=["Frequency1", "Percentage Frequency1", "Cumulative Frequency1", "Relative Frequency1", "Cumulative Relative Frequency1"])
st.dataframe(summary_table1[showData], use_container_width=True)

valid_product_values = df['Product'].dropna().values

# Add legend and distribution line for mean age
mean_unitprice = valid_unitprice_values.mean()

# Plotting the histogram using Plotly and Streamlit
fig = px.histogram(df['UnitPrice'], y=df['UnitPrice'], nbins=10, labels={'UnitPrice': 'UnitPrice', 'count': 'Frequency'}, orientation='h')

# Add a dashed line for mean and customize its appearance
fig.add_hline(y=mean_unitprice, line_dash="dash", line_color="green", annotation_text=f"Mean UnitPrice: {mean_unitprice:.2f}", annotation_position="bottom right")

# Customize marker and line for bars
fig.update_traces(marker=dict(color='#51718E', line=dict(color='rgba(33, 150, 243, 1)', width=0.5)), showlegend=True, name='UnitPrice')

# Update layout for a materialized look, add gridlines, and adjust legend
fig.update_layout(
    title='UNIT PRICE DISTRIBUTION',
    yaxis_title='UnitPrice',
    xaxis_title='Frequency',
    bargap=0.1,
    legend=dict(title='Data', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)'),
    yaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)')
)
# Display the histogram using Streamlit
st.success("**UNIT PRICE DISTRIBUTION GRAPH**")
st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)



