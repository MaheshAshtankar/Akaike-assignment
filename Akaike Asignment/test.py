# Importing necessary libraries
import requests

# Function to fetch data from an API
def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Sample API
    response = requests.get(url)  # Making a GET request
    if response.status_code == 200:
        print("✅ API Response:", response.json())  # Print JSON response
    else:
        print("❌ Failed to fetch data")

# Run the function
fetch_data()
