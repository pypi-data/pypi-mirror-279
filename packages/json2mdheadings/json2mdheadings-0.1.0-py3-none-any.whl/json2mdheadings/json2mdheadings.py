"""
A Python package for converting JSON data to Markdown with keys as headings. 

Since markdown only supports headings up to level 6, this will not work "correctly" for JSON data with more than 6 levels of nesting. Nested lists might be used for JSON data with more than 6 levels of nesting, but this is not currently implemented. 

For lists of dictionaries, an integer heading is written for each item and the keys of each dictionary are written as subheadings (can be nested as long as the overal heading level does not exceed 6) of the integer headings. 

Lists of lists from JSON don't currently write nested lists in Markdown. 

The package is currently intended to be used for JSON data with a maximum of 6 levels of nesting and no lists of lists.
"""

import json


class JSON2MD:
    def __init__(self):
        """
        Initializes an instance of the Json2MdHeadings class.

        Attributes:
        - md (str): The Markdown content, initially set to an empty string.
        - dict_list_level (None): The level for headings for a list of dictionaries, initially set to None.
        """

        self.md = ""
        self.dict_list_level = None

    def __call__(self, json_file):
        """
        Read in the JSON file. Convert the JSON data to Markdown and write it to a file.

        Parameters:
        - json_file (str): The path to the JSON file to be converted.

        Returns:
        None
        """

        md_file = json_file.replace(".json", ".md")

        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.json_to_md(data)

        with open(md_file, "w", encoding="utf-8") as file:
            file.write(self.md)

    def json_to_md(self, data, level=1):
        """
        Convert JSON data to Markdown recursively.

        Args:
            data (str): JSON data to convert.
            level (int): Current Markdown heading level, defaults to 1.

        Returns:
            None

        Raises:
            None
        """

        # If data is a dictionary, iterate over the keys and write them as headings in Markdown.
        if isinstance(data, dict):
            for key in data:
                self.md += f"{'#' * level} {key}\n\n"
                self.json_to_md(data[key], level + 1)

        # If data is a list, iterate over the items and write them in Markdown.
        # If the items are dictionaries,
        #     write an integer heading for each item and call the function recursively.
        elif isinstance(data, list):
            self.dict_list_level = level + 1

            for iitem, item in enumerate(data):
                if isinstance(item, dict):
                    self.md += f"{'#' * self.dict_list_level} {iitem}\n\n"
                    self.json_to_md(item, self.dict_list_level + 1)
                else:
                    self.md += f"- {item}\n"

            self.md += "\n"

        # Otherwise, write the data in Markdown.
        else:
            self.md += f"{data}\n\n"
