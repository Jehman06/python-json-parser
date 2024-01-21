
class JSON_parser:
    def __init__(self, json_string):
        self.json_string = json_string
        self.index = 0

    def parse(self):
        # Start parsing from the first character
        return self.parse_value()
    
    def parse_value(self):
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
        elif current_char.isalpha():
            # Boolean or null parsing
            return self.parse_keyword()
        else:
            # Invalid character
            raise ValueError(f"Invalid character: {current_char}")
        
    def parse_object(self):
        # Skip de opening curly brace
        self.index += 1

        # Initialize en empty dictionary to store key-value pairs
        while self.json_string[self.index] != "}":
            # Parse key
            key = self.parse_string()

            # Skip the colon between key and value
            self.index += 1

            # Parse value
            value = self.parse_value()

            # Add key-value pair to the result dictionary
            result[key] = value

            # Check for a comma indicating another key-value pair
            if self.json_string[self.index] == ",":
                self.index += 1

            # Skip the closing curly brace
            self.index += 1

            return result

    def parse_array(self):
        # Parse logic here
        pass

    def parse_string(self):
        # Parse logic here
        pass

    def parse_number(self):
        # Parse logic here
        pass

    def parse_keyword(self):
        # Parse logic here
        pass

# Example usage:
json_parser = JSON_parser()
result = json_parser.parse({"key": "value", "numbers": [1, 2, 3]})
print(result)