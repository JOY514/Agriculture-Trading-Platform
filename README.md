# Agriculture Trading Platform (ATP)

Agriculture Trading Platform (ATP) is a web-based forecasting and analytical dashboard designed to provide insights into various agricultural metrics. The platform is built using Python with Streamlit for the frontend, MySQL for the database, and hosted on Streamlit Cloud.

## Features

- **Forecast Consumption Area**: Analyze and forecast the consumption areas for different crops.
- **Frequency Distributions**: Visualize frequency distributions of agricultural data.
- **Forecast Commodities**: Forecast the prices and trends of various agricultural commodities.
- **Forecast Weather**: Analyze and predict weather patterns affecting agriculture.
- **Manage Data**: Manage and update agricultural data.
- **Vendor Directory**: Maintain a directory of agricultural vendors.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **Hosting**: Streamlit Cloud
- **Visualization Libraries**: Plotly, Matplotlib, Folium
- **Machine Learning**: PyTorch

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/agriculture-trading-platform.git
    cd agriculture-trading-platform
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup the MySQL database**:
    - Ensure you have MySQL installed and running.
    - Create a database named `agriculture_trading`.
    - Update the database connection settings in the `config.py` file.

5. **Run the application**:
    ```bash
    streamlit run Home.py
    ```

6. **Access the application**:
    Open your web browser and go to `http://localhost:8501`.

## File Descriptions

- `Home.py`: Main entry point for the application.
- `🏷 FORECAST CONSUMPTION AREA.py`: Code for forecasting the consumption area.
- `🏷 FREQUENCY DISTRIBUTIONS.py`: Code for visualizing frequency distributions.
- `🏷 FORECAST COMMODITIES.py`: Code for forecasting agricultural commodities.
- `🏷 FORECAST WEATHER.py`: Code for forecasting weather patterns.
- `🏷 MANAGE DATA.py`: Code for managing and updating agricultural data.
- `🏷 VENDOR DIRECTORY.py`: Code for maintaining the vendor directory.

## Usage

1. **Forecast Consumption Area**:
    - Navigate to the Forecast Consumption Area section.
    - Select the crop and time range.
    - View the forecasted consumption areas.

2. **Frequency Distributions**:
    - Navigate to the Frequency Distributions section.
    - Select the data type and parameters.
    - Visualize the frequency distributions.

3. **Forecast Commodities**:
    - Navigate to the Forecast Commodities section.
    - Select the commodity and time range.
    - View the forecasted trends and prices.

4. **Forecast Weather**:
    - Navigate to the Forecast Weather section.
    - Select the location and time range.
    - View the predicted weather patterns.

5. **Manage Data**:
    - Navigate to the Manage Data section.
    - Add, update, or delete agricultural data.

6. **Vendor Directory**:
    - Navigate to the Vendor Directory section.
    - Add, update, or delete vendor information.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact MirzaNurhaziq at 1211303082@student.mmu.edu.my.
