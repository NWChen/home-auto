import requests


def is_sunny(lat, lon):
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(points_url)
    if response.status_code == 200:
        forecast_url = response.json()["properties"]["forecast"]
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            current_condition = forecast_data["properties"]["periods"][0][
                "shortForecast"
            ].lower()
            return "sunny" in current_condition or "clear" in current_condition
        else:
            raise Exception(f"Error fetching forecast: {forecast_response.status_code}")
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")
