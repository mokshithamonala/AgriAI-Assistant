import os
import logging
import random
import requests
from pathlib import Path
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("WeatherService")

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    logger.warning(f".env file not found at {env_path}. Relying on system environment variables.")

# Retrieve API key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def _get_mock_weather(location: str) -> dict:
    """
    Generates realistic, deterministic mock weather data based on the location name.
    Useful for testing, development, or fallback when API keys are missing.
    """
    # Deterministic seed based on location name string
    seed_value = sum(ord(char) for char in location)
    rng = random.Random(seed_value)
    
    # Simulate realistic tropical/agricultural climates
    temp = round(rng.uniform(18.0, 38.0), 1)
    humidity = rng.randint(40, 95)
    
    conditions = [
        "Sunny", "Mostly Sunny", "Partly Cloudy", "Cloudy", 
        "Light Rain", "Heavy Rain", "Thundershower", "Mist", "Clear Sky"
    ]
    weather = rng.choice(conditions)
    
    # Rainfall in mm
    rainfall = 0.0
    if "Rain" in weather or "Thundershower" in weather:
        rainfall = round(rng.uniform(1.0, 35.0), 1)
        
    return {
        "temperature": temp,
        "humidity": humidity,
        "weather": f"{weather} (Mock)",
        "rainfall": rainfall
    }

def fetch_weather(location: str) -> dict:
    """
    Fetches current weather data for the specified location.
    Integrates with OpenWeatherMap API if the API key is configured.
    Otherwise, falls back to realistic mock weather data.
    
    Args:
        location (str): The name of the city or location.
        
    Returns:
        dict: Weather details with temperature, humidity, weather, and rainfall.
    """
    # Clean input
    location = location.strip()
    if not location:
        logger.error("Empty location provided to fetch_weather.")
        return _get_mock_weather("Unknown")

    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY.strip() == "your_openweather_api_key_here" or not OPENWEATHER_API_KEY.strip():
        logger.info(f"OpenWeatherMap API key is missing. Using mock weather data for location: '{location}'.")
        return _get_mock_weather(location)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # For Celsius
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        
        # Check HTTP status codes
        if response.status_code == 200:
            data = response.json()
            
            # Extract main metrics
            main = data.get("main", {})
            temp = main.get("temp", 25.0)
            humidity = main.get("humidity", 60.0)
            
            # Extract weather description
            weather_list = data.get("weather", [])
            weather_desc = weather_list[0].get("description", "Unknown").title() if weather_list else "Unknown"
            
            # Extract rainfall (check for 1h or 3h precipitations)
            rain_data = data.get("rain", {})
            rainfall = rain_data.get("1h", rain_data.get("3h", 0.0))
            
            logger.info(f"Successfully fetched live weather data for '{location}'.")
            return {
                "temperature": float(temp),
                "humidity": float(humidity),
                "weather": weather_desc,
                "rainfall": float(rainfall)
            }
            
        elif response.status_code == 404:
            logger.warning(f"Location '{location}' not found by OpenWeatherMap API. Falling back to mock data.")
            return _get_mock_weather(location)
            
        else:
            logger.error(f"OpenWeatherMap API returned status code {response.status_code}. Response: {response.text}")
            logger.info(f"Falling back to mock weather data for '{location}'.")
            return _get_mock_weather(location)

    except requests.exceptions.Timeout:
        logger.error(f"OpenWeatherMap API request timed out for location '{location}'. Falling back to mock data.")
        return _get_mock_weather(location)
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error calling OpenWeatherMap API for location '{location}': {e}. Falling back to mock data.")
        return _get_mock_weather(location)
    except Exception as e:
        logger.error(f"Unexpected error in fetch_weather for location '{location}': {e}. Falling back to mock data.")
        return _get_mock_weather(location)
