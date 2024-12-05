import pandas as pd
import requests
from time import sleep

# Load your CSV file
df = pd.read_csv('/content/DATA_VZ (1).csv')  # Replace with your actual CSV file path

# Your Google API Key
API_KEY = 'PUT YOUR KEY HERE'  # Replace with your actual API key

# Function to get latitude and longitude from address using Google Maps Geocoding API
def get_lat_lon(address):
    try:
        # Define the endpoint and parameters for the request
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": API_KEY
        }
        
        # Make the request to Google API
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print(f"Geocoding error for address '{address}': {data['status']}")
                return None, None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error processing address '{address}': {e}")
        return None, None

# Apply the geocoding function to each address
df['Latitude'], df['Longitude'] = zip(*df['address'].apply(get_lat_lon))  # Make sure 'address' matches the column name in your CSV

# Save the updated DataFrame to a new CSV file
df.to_csv('addresses_with_lat_lon_google.csv', index=False)

print("Geocoding complete. New CSV saved as 'addresses_with_lat_lon_google.csv'")