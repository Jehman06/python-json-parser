# Python JSON Parser

This Python JSON parser is a lightweight tool for parsing JSON strings into Python objects. It supports parsing JSON objects, arrays, strings, numbers, booleans, and null values.

## Features

- Parse JSON objects and arrays
- Handle strings, numbers, booleans, and null values
- Support for escaped characters in strings
- Easily extendable for additional functionality

## Getting Started

### Installation

Clone the repository or download the `json_parser.py` file. Add it to your project directory, and you're ready to use the parser.

### Usage

```python
# Example Usage
import requests
import pprint
from json_parser import JSON_parser

def make_api_request():
    # Make a request to a JSON API
    response = requests.get(https://api.example.com/)

    # Check if the request is successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response using the JSON parser
        json_parser = JSON_parser(response.text)
        parsed_data = json_parser.parse()

        # Display the parsed data
        pprint.pprint(parsed_data)
    else:
        print(f"Failed to make the API request. Status code {response.status_code}")

if __name__ == "__main__":
    make_api_request()
