# Example usage of the Python JSON parser using the JSONPlaceholder API

import requests
from json_parser import JSON_parser

def make_api_request():
    # Make a request to a JSON API
    response = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response using the JSON parser
        json_parser = JSON_parser(response.text)
        parsed_data = json_parser.parse()

        # Display the parsed data
        for key, value in parsed_data.items():
            print(f"{key}: {value} \n")
    else:
        print(f"Failed to make API request. Status code: {response.status_code}")

if __name__ == "__main__":
    make_api_request()