Weatherapi
Welcome to weatherapi, a Streamlit application to explore air quality index values across different cities worldwide.

Project Setup
Requirements
Make sure to install the required Python packages by running the following command:

pip install -r requirements.txt
API Key
Replace the placeholder in aqi.py with your OpenWeatherMap API key:

python
OPENWEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
Usage
Run the aqi.py script to launch the Streamlit application. You can select a country and, if applicable, a city to visualize air quality and weather data. Choose primary and secondary parameters for the scatter plot.

Files
requirements.txt
pandas
numpy
plotly
streamlit
requests
aqi.py

The main Python script containing functions for fetching air pollution and weather data, plotting data on a map, and displaying relevant metrics.

Functions
get_air_pollution_data(latitude, longitude)
Fetches air pollution data using the OpenWeatherMap API based on latitude and longitude.

fetch_coordinates_by_country(country)
Fetches coordinates (latitude and longitude) of a country using the OpenWeatherMap API.

fetch_coordinates_by_city(city)
Fetches coordinates (latitude and longitude) of a city using the OpenWeatherMap API.

fetch_weather_data_by_country(country)
Fetches weather data for a country using the OpenWeatherMap API.

plot_by_country_city(dataframe, country, city, param1, param2)
Plots air quality and weather data on a map for a specific city.

plot_by_country(dataframe, country, param1, param2)
Plots air quality and weather data on a map for an entire country.

fetch_weather_data(city)
Fetches weather data for a specific city using the OpenWeatherMap API.

range_particulate_matter()
Displays the range of particulate matter for various pollutants.

Running the Application
Execute the script using the command:

bash

streamlit run aqi.py
Visit the Streamlit app in your web browser, select a country and, if applicable, a city, and explore air quality data along with weather details.

Feel free to customize the parameters and enhance the functionality based on your requirements