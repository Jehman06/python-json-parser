class JSON_parser:
    def __init__(self, json_string):
        self.json_string = json_string
        self.index = 0

    def parse(self):
        if not self.json_string:
            raise ValueError("Empty JSON string")

        return self.parse_value()

    # PARSE OBJECT METHOD
    def parse_object(self):
        # Skip the opening curly brace
        self.index += 1

        # Initialize an empty dictionary to store key-value pairs
        result = {}

        while self.json_string[self.index] != "}":
            # Skip whitespace characters
            while self.json_string[self.index].isspace():
                self.index += 1

            if self.json_string[self.index] == "}":
                break

            # Parse key
            key = self.parse_string()

            # Skip newline characters
            while self.json_string[self.index].isspace() and self.json_string[self.index] != "\n":
                self.index += 1

            # Check for the colon between key and value
            if self.json_string[self.index] != ":":
                raise ValueError("Expected colon (:) between the key and value in the object")

            self.index += 1

            # Skip whitespace characters after the colon
            while self.json_string[self.index].isspace():
                self.index += 1

            # Parse value
            value = self.parse_value()

            # Add key-value pair to the result dictionary
            result[key] = value

            # Skip newline characters
            while self.json_string[self.index].isspace() and self.json_string[self.index] != "\n":
                self.index += 1

            # Check for a comma indicating another key-value pair
            if self.json_string[self.index] == "," or self.json_string[self.index] == "\n":
                self.index += 1
            elif self.json_string[self.index] != "}":
                raise ValueError("Expected comma (,) or closing curly brace (}) after the value in the object")

        # Skip the closing curly brace
        self.index += 1

        return result

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

    # PARSE ARRAY METHOD
    def parse_array(self):
        # Skip the opening square bracket
        self.index += 1

        # Initialize an empty array to store the parsed array
        parsed_array = []

        while self.json_string[self.index] != ']':
            # Skip whitespace characters
            while self.json_string[self.index].isspace():
                self.index += 1

            # Parse value
            value = self.parse_value()
            parsed_array.append(value)

            # Skip whitespace characters
            while self.json_string[self.index].isspace():
                self.index += 1

            # Check for a comma indicating another element in the array
            if self.json_string[self.index] == ',':
                self.index += 1

        # Closing the square bracket
        self.index += 1

        return parsed_array

    # PARSE STRING METHOD
    def parse_string(self):
        # Skip the opening double quotes
        self.index += 1

        # Initialize an empty string to store the parsed string
        parsed_string = ""

        while self.json_string[self.index] != '"':
            if self.json_string[self.index] == "\\":
                # Handle escaped characters
                self.index += 1
                if self.json_string[self.index] == "n":
                    parsed_string += "\n"
                elif self.json_string[self.index] == "t":
                    parsed_string += "\t"
                else:
                    # Add other escaped characters as needed
                    parsed_string += "\\" + self.json_string[self.index]
            else:
                parsed_string += self.json_string[self.index]

            self.index += 1

        if self.json_string[self.index] == '"':
            # Skip the closing double quotes
            self.index += 1
        else:
            raise ValueError("Expected double quotes (\") at the end of the string")

        return parsed_string

    # PARSE NUMBER METHOD
    def parse_number(self):
        # Initialize variables to store the number and check for a decimal point
        number_str = ""
        has_decimal = False

        # Handle negative sign if present
        if self.json_string[self.index] == "-":
            number_str += "-"
            self.index += 1

        # Parse digits
        while self.index < len(self.json_string) and (self.json_string[self.index].isdigit() or self.json_string[self.index] == "."):
            if self.json_string[self.index] == ".":
                # Check for multiple decimal points
                if has_decimal:
                    raise ValueError("Invalid number format: multiple decimal points")
                has_decimal = True
            number_str += self.json_string[self.index]
            self.index += 1

        # Convert the string to a float or integer
        if has_decimal:
            return float(number_str)
        else:
            return int(number_str)

    # PARSE BOOLEAN/NULL METHOD
    def parse_keyword(self):
        # Extract the keyword from the JSON string
        keyword = ""
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