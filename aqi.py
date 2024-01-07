import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import requests

final = pd.read_csv('AQI and Lat Long of Countries.csv')
final.dropna(inplace=True)

OPENWEATHER_API_KEY = ''  # Replace with your OpenWeatherMap API key

def get_air_pollution_data(latitude, longitude):
    base_url = 'http://api.openweathermap.org/data/2.5/air_pollution'
    params = {'lat': latitude, 'lon': longitude, 'appid': OPENWEATHER_API_KEY}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch air pollution data.")
        return None

def fetch_coordinates_by_country(country):
    geocoding_api_url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        'q': f'{country}',
        'limit': 1,
        'appid': OPENWEATHER_API_KEY,
    }

    try:
        response = requests.get(geocoding_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and 'lat' in data[0] and 'lon' in data[0]:
            return {'lat': float(data[0]['lat']), 'lon': float(data[0]['lon'])}
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching coordinates: {e}")
        return None
    
def fetch_coordinates_by_city(city):
    geocoding_api_url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        'q': f'{city}',
        'limit': 1,
        'appid': OPENWEATHER_API_KEY,
    }

    try:
        response = requests.get(geocoding_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and 'lat' in data[0] and 'lon' in data[0]:
            return {'lat': float(data[0]['lat']), 'lon': float(data[0]['lon'])}
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching coordinates: {e}")
        return None

def fetch_weather_data_by_country(country):
    coordinates = fetch_coordinates_by_country(country)

    if coordinates is None:
        return None 

    api_key = OPENWEATHER_API_KEY
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': coordinates['lat'],
        'lon': coordinates['lon'],
        'appid': api_key,
        'units': 'metric',
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def plot_by_country_city(dataframe, country, city, param1, param2):
    weather_data = fetch_weather_data(city)

    if weather_data is None:
        return 

    coordinates = fetch_coordinates_by_city(city)
    print(coordinates)

    if coordinates is None:
        return None 

    air_pollution_data = get_air_pollution_data(coordinates['lat'], coordinates['lon'])

    if air_pollution_data is None:
        return

    temp_df = dataframe[(dataframe['Country'] == country) & (dataframe['City'] == city)]
    fig = px.scatter_mapbox(temp_df, lat='lat', lon='lng', size=param1, color=param2, size_max=20,
                            mapbox_style='carto-positron', hover_name=temp_df['City'], height=500, width=700, zoom=4)

    col1, col2, col3, col4 = st.columns(4)
    st.plotly_chart(fig, use_container_width=True)
    
    with col1:
        st.metric('Value of {} in {}'.format(param1, city), value=temp_df[param1].iloc[0])
    with col2:
        st.metric('Value of {} in {}'.format(param2, city), value=temp_df[param2].iloc[0])
    with col3:
        st.metric('Latitude of {}'.format(city), value=temp_df['lat'].iloc[0])
    with col4:
        st.metric('Longitude of {}'.format(city), value=temp_df['lng'].iloc[0])

    st.subheader(f"Weather Details for {city}")
    st.write(f"Temperature: {weather_data['main']['temp']} °C")
    st.write(f"Sky: {weather_data['weather'][0]['description']}")
    st.write(f"Humidity: {weather_data['main']['humidity']}%")
    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

    st.subheader(f"Air Pollution Details for {city}")
    print(air_pollution_data)
    st.write(f"AQI (Air Quality Index): {air_pollution_data['list'][0]['main']['aqi']}")
    st.write("Air Components:")
    components = air_pollution_data['list'][0]['components']
    for component, value in components.items():
        st.write(f"{component}: {value}")

    range_particulate_matter()
    st.markdown('---')

def plot_by_country(dataframe, country, param1, param2):
    weather_data = fetch_weather_data_by_country(country)

    if weather_data is None:
        return 

    air_pollution_data = get_air_pollution_data(weather_data['coord']['lat'], weather_data['coord']['lon'])

    if air_pollution_data is None:
        return

    weather_df = pd.DataFrame({
        'City': [weather_data['name']],
        'lat': [weather_data['coord']['lat']],
        'lng': [weather_data['coord']['lon']],
        'AQI Value': [air_pollution_data['list'][0]['main']['aqi']],
    })

    fig = px.scatter_mapbox(weather_df, lat='lat', lon='lng', size=param1, color='AQI Value', size_max=20,
                            mapbox_style='carto-positron', color_continuous_scale=px.colors.sequential.Agsunset_r,
                            hover_name='City', height=800, width=900, zoom=4,
                            title=f'{param1} vs AQI Value for {country}')

    map_center = {
        'lat': weather_df['lat'].mean(),
        'lon': weather_df['lng'].mean()
    }

    fig.update_geos(center=map_center, projection_scale=4)

    st.plotly_chart(fig, use_container_width=True)

    range_particulate_matter()
    st.markdown('---')

def fetch_weather_data(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def range_particulate_matter():
    st.subheader('Range of the particulate matter')

    data = {
    'Pollutant': ['PM2.5', 'PM10', 'Ozone', 'CO', 'NO2'],
    'Good': ['0-12 μg/m³', '0-54 μg/m³', '0-54 ppb', '0-4.4 ppm', '0-53 ppb'],
    'Moderate': ['12.1-35.4 μg/m³', '55-154 μg/m³', '55-70 ppb', '4.5-9.4 ppm', '54-100 ppb'],
    'Unhealthy for Sensitive Groups': ['35.5-55.4 μg/m³', '155-254 μg/m³', '71-85 ppb', '9.5-12.4 ppm', '101-360 ppb'],
    'Unhealthy': ['55.5-150.4 μg/m³', '255-354 μg/m³', '86-105 ppb', '12.5-15.4 ppm', '361-649 ppb'],
    'Very Unhealthy': ['150.5-250.4 μg/m³', '355-424 μg/m³', '106-200 ppb', '15.5-30.4 ppm', '650-1249 ppb'],
    'Hazardous': ['250.5+ μg/m³', '425+ μg/m³', '201+ ppb', '30.5+ ppm', '-'],
    }

    df = pd.DataFrame(data)

    st.write(df)

if __name__ == "__main__":
    st.set_page_config(page_title='AQI Globe', layout='wide')
    st.sidebar.header('AQI Globe')
    st.header('AQI Globe')
    st.markdown("*Explore air quality index values across different cities worldwide*")

    st.markdown("---")

    country = st.sidebar.selectbox('Select Country', list(sorted(final['Country'].unique())))

    temp_df = final[final['Country'] == country]
    city_list = list(sorted(temp_df['City'].unique()))
    city_list.insert(0, '-')
    city = st.sidebar.selectbox(f'Select a city in {country}', city_list)

    primary = st.sidebar.selectbox('Choose primary parameter', final.columns[2:12:2])
    secondary = st.sidebar.selectbox('Choose secondary parameter', [cols for cols in final.columns[2:12:2] if cols != primary])

    if city == '-':
        plot_by_country(final, country, primary, secondary)
    else:
        plot_by_country_city(final, country, city, primary, secondary)

    st.write('\n')
    st.write('\n')
    st.write('\n')
