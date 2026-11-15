import json
import logging
from services.weather_service import fetch_weather
from services.mandi_service import fetch_mandi_price

# Configure logging for test output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TestRunner")

def validate_schema(data: dict, expected_keys: set, service_name: str) -> bool:
    """Helper to validate that a dictionary contains all required keys and correct types."""
    actual_keys = set(data.keys())
    missing = expected_keys - actual_keys
    if missing:
        logger.error(f"[{service_name}] Schema validation FAILED! Missing keys: {missing}")
        return False
    logger.info(f"[{service_name}] Schema validation PASSED. Keys: {list(actual_keys)}")
    return True

def run_weather_tests():
    print("\n" + "="*50)
    print("RUNNING WEATHER SERVICE TESTS")
    print("="*50)
    
    # Test locations
    locations = ["New Delhi", "Pune", "Karnal", "London"]
    expected_keys = {"temperature", "humidity", "weather", "rainfall"}
    
    all_passed = True
    for loc in locations:
        print(f"\nFetching weather for: {loc}")
        try:
            weather_data = fetch_weather(loc)
            print(json.dumps(weather_data, indent=4))
            
            # Check keys
            if not validate_schema(weather_data, expected_keys, f"WeatherService - {loc}"):
                all_passed = False
                
            # Verify types
            if not isinstance(weather_data["temperature"], (int, float)):
                logger.error(f"Invalid temperature type: {type(weather_data['temperature'])}")
                all_passed = False
            if not isinstance(weather_data["humidity"], (int, float)):
                logger.error(f"Invalid humidity type: {type(weather_data['humidity'])}")
                all_passed = False
            if not isinstance(weather_data["weather"], str):
                logger.error(f"Invalid weather type: {type(weather_data['weather'])}")
                all_passed = False
            if not isinstance(weather_data["rainfall"], (int, float)):
                logger.error(f"Invalid rainfall type: {type(weather_data['rainfall'])}")
                all_passed = False
                
        except Exception as e:
            logger.error(f"Exception during weather test for {loc}: {e}")
            all_passed = False
            
    return all_passed

def run_mandi_tests():
    print("\n" + "="*50)
    print("RUNNING MANDI SERVICE TESTS")
    print("="*50)
    
    # Test cases: (Crop, State, District)
    test_cases = [
        ("Wheat", "Haryana", "Ambala"),
        ("Onion", "Maharashtra", "Nashik"),
        ("Paddy", "Punjab", "Ludhiana"),
        ("Potato", "Uttar Pradesh", "Agra")
    ]
    expected_keys = {"crop", "market", "price", "date"}
    
    all_passed = True
    for crop, state, district in test_cases:
        print(f"\nFetching mandi price for: {crop} in {district}, {state}")
        try:
            mandi_data = fetch_mandi_price(crop, state, district)
            print(json.dumps(mandi_data, indent=4))
            
            # Check keys
            if not validate_schema(mandi_data, expected_keys, f"MandiService - {crop}"):
                all_passed = False
                
            # Verify types
            if not isinstance(mandi_data["crop"], str):
                logger.error(f"Invalid crop type: {type(mandi_data['crop'])}")
                all_passed = False
            if not isinstance(mandi_data["market"], str):
                logger.error(f"Invalid market type: {type(mandi_data['market'])}")
                all_passed = False
            if not isinstance(mandi_data["price"], (int, float)):
                logger.error(f"Invalid price type: {type(mandi_data['price'])}")
                all_passed = False
            if not isinstance(mandi_data["date"], str):
                logger.error(f"Invalid date type: {type(mandi_data['date'])}")
                all_passed = False
                
        except Exception as e:
            logger.error(f"Exception during mandi test for {crop}: {e}")
            all_passed = False
            
    return all_passed

if __name__ == "__main__":
    print("Starting integration service tests...")
    
    weather_ok = run_weather_tests()
    mandi_ok = run_mandi_tests()
    
    print("\n" + "="*50)
    print("TEST SUITE SUMMARY")
    print("="*50)
    print(f"Weather Service: {'PASSED' if weather_ok else 'FAILED'}")
    print(f"Mandi Service:   {'PASSED' if mandi_ok else 'FAILED'}")
    print("="*50)
    
    if weather_ok and mandi_ok:
        print("All tests completed successfully!")
    else:
        print("Some tests failed. Please check log outputs.")
