import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import plotly.graph_objs as go
import plotly.express as px
from folium.plugins import MarkerCluster, HeatMap
from folium import plugins
from folium.plugins import MarkerCluster
import pandas as pd
from query import view_vendor_data
from streamlit_extras.metric_cards import style_metric_cards
import base64

# Set page configuration
st.set_page_config(page_title="Vendor Directory", page_icon="📈", layout="wide")

# Load background image
image_path = "data/home2.jpg"  # Replace with the actual path to your image
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode()

# Load Style CSS and background image
st.markdown(
    f"""
    <style>
        .stApp {{
            background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
            background-size: cover;
        }}
        [data-testid=stSidebar] {{
             color: white;
             text-size:24px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    theme_plotly = None 

    load_df = pd.read_excel('VendorDirectory.xlsx')

    # Sidebar
    st.sidebar.image("data/logo2.png", caption="")
    
    name = st.sidebar.multiselect(
        "SELECT VENDOR",
        options=load_df["Name"].unique(),
        default=load_df["Name"].unique(),
    )
    df = load_df.query("Name==@name ")

    try:
        st.header("Vendors Directory & Production Area")
        items = load_df['Name'].count()
        total_sales = float(load_df['TotalSales'].sum())

        with st.expander("ANALYTICS"):
            a1, a2 = st.columns(2)
            a1.metric(label="Production Area", value=items, help=f""" Total Sales: {total_sales} """, delta=total_sales)
            a2.metric(label="Total Sales", value=total_sales, help=f""" Total Sales: {total_sales} """, delta=total_sales)
            style_metric_cards(background_color="#FFFFFF", border_left_color="#00462F", border_color="#070505", box_shadow="#F71938")

        # Create a map
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)
        
        for i, row in df.iterrows():
            popup_content = f"""
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                <ul class="list-group">
                <h3>Information of {row['Name']}</h3>
                <hr class='bg-danger text-primary'>
                <div style='width:400px;height:200px;margin:10px;color:gray;text-size:18px;'>
                <li class="list-group-item"><b>Vendor:</b> {row['Manager']}</li>
                <li class="list-group-item"><b>Farm Area:</b> {row['Collection']} sqft<br></li>
                <li class="list-group-item"><b>Name:</b> {row['Name']}<br></li>
                <li class="list-group-item"><b>Production:</b> {row['Quantity']}<br></li>
                <li class="list-group-item"><b>Unit Price:</b> {row['UnitPrice']}<br></li>
                <li class="list-group-item"><h4>Total Sales: RM {row['TotalSales']}</b><br></li>
                <li class="list-group-item"><h4>Phone {row['Phone']}</h4></li>"""
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=row['Name'],
                icon=folium.Icon(color='red', icon='fa-dollar-sign', prefix='fa'),
            ).add_to(marker_cluster).add_child(folium.Popup(popup_content, max_width=600))

        # Heatmap Layer
        heat_data = [[row['Latitude'], row['Longitude']] for i, row in df.iterrows()]
        HeatMap(heat_data).add_to(m)

        # Fullscreen Control
        plugins.Fullscreen(position='topright', title='Fullscreen', title_cancel='Exit Fullscreen').add_to(m)

        # Drawing Tools
        draw = plugins.Draw(export=True)
        draw.add_to(m)

        def add_google_maps(m):
            tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
            attr = "Google Digital Satellite"
            folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)
            # Add labels for streets and objects
            label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
            label_attr = "Google Labels"
            folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)
            return m

        with st.expander("Vendors and Production Area"):
            m = add_google_maps(m)
            m.add_child(folium.LayerControl(collapsed=False))
            folium_static(m, width=1350, height=600)
            folium.LayerControl().add_to(m)  # Add layer control to toggle different layers

        # Show table data when hovering over a marker
        with st.expander("SEARCH VENDOR OR PRODUCTION AREA"):
            selected_city = st.selectbox("Select Vendor", df['Name'])
            selected_row = df[df['Name'] == selected_city].squeeze()
            # Display additional information in a table
            st.table(selected_row)

        # Graphs
        col1, col2 = st.columns(2)
        with col1:
            fig2 = go.Figure(
                data=[go.Bar(x=df['Name'], y=df['TotalSales'])],
                layout=go.Layout(
                    title=go.layout.Title(text="BAR CHART VENDORS BY TOTAL SALES PERFORMANCE"),
                    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
                    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
                    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
                    font=dict(color='#cecdcd'),  # Set text color to black
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # Create a donut chart
            fig = px.pie(df, values='TotalSales', names='Name', title='PIE CHART TOTAL SALES BY VENDORS')
            fig.update_traces(hole=0.4)  # Set the size of the hole in the middle for a donut chart
            fig.update_layout(width=800)
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Unable to display null, select at least one business location. Error: {e}")

if __name__ == "__main__":
    main()
