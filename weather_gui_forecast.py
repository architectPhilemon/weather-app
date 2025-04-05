import requests
import tkinter as tk
from tkinter import messagebox

def get_weather(city_name, api_key):
    """
    Fetch current weather and 5-day forecast for a given city using OpenWeatherMap API.
    """
    # Current weather API
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

    try:
        # Fetch current weather
        current_params = {"q": city_name, "appid": api_key, "units": "metric"}
        current_response = requests.get(current_weather_url, params=current_params)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Fetch 5-day forecast
        forecast_params = {"q": city_name, "appid": api_key, "units": "metric"}
        forecast_response = requests.get(forecast_url, params=forecast_params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Extract current weather data
        current_weather = {
            "city": current_data["name"],
            "temperature": current_data["main"]["temp"],
            "description": current_data["weather"][0]["description"],
            "humidity": current_data["main"]["humidity"],
            "wind_speed": current_data["wind"]["speed"],
        }

        # Extract 5-day forecast data (every 8th entry for daily forecast)
        forecast_list = forecast_data["list"]
        daily_forecast = []
        for i in range(0, len(forecast_list), 8):  # Every 8th entry is ~24 hours apart
            day = forecast_list[i]
            daily_forecast.append({
                "date": day["dt_txt"].split(" ")[0],
                "temperature": day["main"]["temp"],
                "description": day["weather"][0]["description"],
            })

        return current_weather, daily_forecast

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None, None
    except KeyError:
        messagebox.showerror("Error", "Invalid response from the API. Please check the city name or API key.")
        return None, None

def display_weather():
    """
    Fetch and display weather data in the GUI.
    """
    city_name = city_entry.get()
    if not city_name:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    current_weather, daily_forecast = get_weather(city_name, API_KEY)
    if current_weather and daily_forecast:
        # Display current weather
        current_weather_label.config(
            text=f"Current Weather in {current_weather['city']}:\n"
                 f"Temperature: {current_weather['temperature']}°C\n"
                 f"Condition: {current_weather['description'].capitalize()}\n"
                 f"Humidity: {current_weather['humidity']}%\n"
                 f"Wind Speed: {current_weather['wind_speed']} m/s"
        )

        # Display 5-day forecast
        forecast_text = "5-Day Forecast:\n"
        for day in daily_forecast:
            forecast_text += f"{day['date']}: {day['temperature']}°C, {day['description'].capitalize()}\n"
        forecast_label.config(text=forecast_text)

# Replace with your OpenWeatherMap API key
API_KEY = "aa3608119801723dff249350e3b68d58"

# Create the GUI
root = tk.Tk()
root.title("Weather App")

# Input field for city name
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=5)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

# Button to fetch weather
fetch_button = tk.Button(root, text="Get Weather", command=display_weather)
fetch_button.pack(pady=10)

# Labels to display weather data
current_weather_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
current_weather_label.pack(pady=10)

forecast_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
forecast_label.pack(pady=10)

# Run the GUI
root.mainloop()