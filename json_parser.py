class JSON_parser:
    def __init__(self, json_string):
        # Initialize the JSONParser with the input JSON string.
        self.json_string = json_string
        self.index = 0

    def parse(self):
        # Parse the JSON string and return the corresponding Python object.
        if not self.json_string:
            raise ValueError("Empty JSON string")

        return self.parse_value()
    
    # PARSE VALUE METHOD
    def parse_value(self):
        # Skip whitespace character
        while self.index < len(self.json_string) and self.json_string[self.index].isspace():
            self.index += 1

        current_char = self.json_string[self.index]

        if current_char == "{":
            # Object parsing
            return self.parse_object()
        elif current_char == "[":
            # Array parsing
            return self.parse_array()
        elif current_char == '"':
            # String parsing
            return self.parse_string()
        elif current_char.isdigit() or current_char == "-":
            # Number parsing
            return self.parse_number()
        elif current_char.isalpha() or current_char in ['t', 'f', 'n']:
            # Boolean or null parsing
            return self.parse_keyword()
        else:
            # Invalid character
            raise ValueError(f"Invalid character: {current_char}")
        
    # PARSE STRING METHOD
    def parse_string(self):
        # Skip the opening double quotes
        self.index += 1

        # Initialize an empty string to store the parsed string
        parsed_string = ""

        # Mapping of escape sequences to replacements
        escape_mapping = {
            "n": "\n",
            "t": "\t",
            "\\": "\\",
            "\"": "\"",
            "/": "/",
            "b": "\b",
            "f": "\f",
            "r": "\r",
        }

        # Handle escaped characters within a double-quoted string
        while self.json_string[self.index] != '"':
            if self.json_string[self.index] == "\\":
                # Check for the backslash indicating an escaped character
                self.index += 1

                # Check the character following the backslash for escape sequences
                escape_char = self.json_string[self.index]
                if escape_char == "n":
                    parsed_string += "\n"
                elif escape_char == "t":
                    parsed_string += "\t"
                elif escape_char == "u":
                    # Handle Unicode escape sequence
                    unicode_sequence = self.json_string[self.index + 1 : self.index + 5]
                    parsed_string += chr(int(unicode_sequence, 16))
                    self.index += 4  # Skip the next 4 characters (representing the Unicode sequence)
                elif escape_char in escape_mapping:
                    # Handle other recognized escape sequences
                    parsed_string += escape_mapping[escape_char]
                else:
                    # Handle unrecognized escape sequence
                    raise ValueError("Unrecognized escape sequence: \\" + escape_char)
            else:
                # If not an escaped character, simply append to the parsed string
                parsed_string += self.json_string[self.index]

            # Move to the next character in the JSON string
            self.index += 1

        # Check if the loop ended with a closing double quote
        if self.json_string[self.index] == '"':
            # Skip the closing double quotes
            self.index += 1
        else:
            raise ValueError("Expected double quotes (\") at the end of the string")

        return parsed_string

    # PARSE OBJECT METHOD
    def parse_object(self):
        # Skip the opening curly brace
        self.index += 1

        # Initialize an empty dictionary to store key-value pairs
        result = {}

        # Keep iterating through the JSON string until a closing brace '}' is encountered
        while self.json_string[self.index] != "}":
            # Exit the loop if the closing brace is found to avoid unnecessary iterations
            if self.json_string[self.index] == "}":
                break

            # Parse key
            key = self.parse_string()

            # Check for the colon between key and value
            if self.json_string[self.index] != ":":
                raise ValueError("Expected colon (:) between the key and value in the object")

            # Skip whitespace after the colon
            self.index += 1

            # Parse value
            value = self.parse_value()

            # Add key-value pair to the result dictionary
            result[key] = value

            # Check for a comma indicating another key-value pair, or a new line
            if self.json_string[self.index] == "," or self.json_string[self.index] == "\n":
                self.index += 1
            # If the current character is neither a comma nor a closing brace,
            # raise a ValueError indicating an unexpected character in the object
            elif self.json_string[self.index] != "}":
                raise ValueError("Expected comma (,) or closing curly brace (}) after the value in the object")

        # Skip the closing curly brace
        self.index += 1

        return result

    # PARSE ARRAY METHOD
    def parse_array(self):
        # Skip the opening square bracket
        self.index += 1

        # Initialize an empty array to store the parsed array
        parsed_array = []

        # Keep iterating through the JSON string until a closing square bracket ']' is encountered
        while self.json_string[self.index] != ']':
            # Skip whitespace characters
            while self.json_string[self.index].isspace():
                self.index += 1

            # Parse value
            value = self.parse_value()
            parsed_array.append(value)

            # Check for a comma indicating another element in the array
            if self.json_string[self.index] == ',':
                self.index += 1

        # Skip the closing the square bracket
        self.index += 1

        return parsed_array

    # PARSE NUMBER METHOD
    def parse_number(self):
        # Initialize variables to store the number and check for a decimal point
        number_str = ""
        has_decimal = False

        # Handle negative sign if present
        if self.json_string[self.index] == "-":
            number_str += "-"
            self.index += 1

        # Iterate through the JSON string while there are characters left, and the current character is a digit or a dot
        while self.index < len(self.json_string) and (self.json_string[self.index].isdigit() or self.json_string[self.index] == "."):
            if self.json_string[self.index] == ".":
                # Check for multiple decimal points
                if has_decimal:
                    raise ValueError("Invalid number format: multiple decimal points")
                has_decimal = True

            # Append the current character to the number string
            number_str += self.json_string[self.index]

            # Move to the next character in the JSON string
            self.index += 1

        # Convert the string to a float or integer
        if has_decimal:
            return float(number_str)
        else:
            return int(number_str)

    # PARSE BOOLEAN/NULL METHOD
    def parse_keyword(self):
        keyword = ""
        # Extract the keyword from the JSON string while there are characters left, 
        # and the current character is an alphabet character or a valid keyword character (true, false, null)
        while self.index < len(self.json_string) and (self.json_string[self.index].isalpha() or self.json_string[self.index] in ['t', 'f', 'n']):
            keyword += self.json_string[self.index]
            self.index += 1

        # Check if the keyword represents a boolean or null
        if keyword.lower() == "true":
            return True
        elif keyword.lower() == "false":
            return False
        elif keyword.lower() == "null":
            return None
        else:
            raise ValueError(f"Invalid keyword: {keyword}")