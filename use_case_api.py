# Example usage of the Python JSON parser using the JSONPlaceholder API

import requests
import pprint
from json_parser import JSON_parser

def make_api_request():
    # Make a request to a JSON API endpoint
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Initialize the JSON parser with the API text response
        json_parser = JSON_parser(response.text)

        # Parse the JSON response using the JSON parser
        parsed_data = json_parser.parse()

        # Display the parsed data in a readable format
        print("Parsed data:")
        pprint.pprint(parsed_data)
    else:
        # Print an error message if the API request fails
        print(f"Failed to make API request. Status code: {response.status_code}")

if __name__ == "__main__":
    make_api_request()