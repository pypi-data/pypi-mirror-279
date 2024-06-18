"""
Why we have this function:

    * GrabGPT turbo will return output as a string like this:
    '''
    json
    TODO explain why we need this class


"""

import re
import json


class JsonUtils:
    """
    A utility class for handling JSON data.
    """

    def convert_json_text_to_dict(self, json_text: str) -> dict:
        """
        Convert a JSON string to a dictionary.

        This method uses a regular expression to locate the first JSON object
        within the input string. If a valid JSON object is found, it is then
        parsed into a Python dictionary using the json library.

        :param json_text: A string containing JSON data.
        :return: A dictionary representation of the JSON data.
        :raises ValueError: If no valid JSON object is found or if the JSON
                            object cannot be parsed.
        """
        # Regular expression pattern to match a JSON object
        pattern = re.compile(r"\{.*\}", re.DOTALL)

        # Search for the first JSON object in the input string
        match = pattern.search(json_text)

        if match:
            json_string = match.group(0)
            try:
                return json.loads(json_string)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON text: could not parse JSON object")
        else:
            raise ValueError("Invalid JSON text: no valid JSON object found")

    def convert_list_text_to_list(self, list_text: str) -> list:
        """
        Convert a string representing a list of dictionaries to a list.

        This method identifies the first JSON array in the input string and
        parses it into a list of dictionaries using the json library.

        :param list_text: A string containing a list of dictionaries in JSON format.
        :return: A list of dictionaries.
        :raises ValueError: If no valid JSON array is found or if the JSON array
                            cannot be parsed.
        """
        try:
            # Find the first occurrence of '[' and the last occurrence of ']'
            start = list_text.find("[")
            end = list_text.rfind("]")
            if start == -1 or end == -1:
                raise ValueError("Invalid list text: no valid JSON list found")

            # Extract the JSON string portion
            json_string = list_text[start : end + 1]

            # Use json.loads() to convert the string into a JSON object
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid list text: {e}")


# Example usage
if __name__ == "__main__":
    json_text = 'Random {"name": [{"real_name": "Kitty"}, {"nick_name": "Hello"}], "age": 30} Random'
    list_text = (
        'Random[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}] Random'
    )

    utils = JsonUtils()

    try:
        dict_result = utils.convert_json_text_to_dict(json_text)
        print(f"Dictionary result: {dict_result}")
    except ValueError as e:
        print(f"Error converting JSON text to dict: {e}")

    try:
        list_result = utils.convert_list_text_to_list(list_text)
        print(f"List result: {list_result}")
    except ValueError as e:
        print(f"Error converting list text to list: {e}")
