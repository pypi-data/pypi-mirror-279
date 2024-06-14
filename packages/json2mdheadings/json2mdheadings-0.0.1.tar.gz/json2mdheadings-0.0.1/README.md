# json2mdheadings

A Python package for converting JSON data to Markdown with keys as headings. Since markdown only supports headings up to level 6, this will not work "correctly" for JSON data with more than 6 levels of nesting. Nested lists might be used for JSON data with more than 6 levels of nesting, but this is not currently implemented. For lists of dictionaries, the keys of the dictionaries will not be converted to headings and the list will just be converted to a markdown list. The package is currently intended to be used for JSON data with a maximum of 6 levels of nesting and no lists of dictionaries.

## Installation

You can install json2mdheadings using pip:

```shell
pip install json2mdheadings
```

## Usage

To use json2mdheadings, import the `JSON2MD` class from the `json2mdheadings` module and create an instance of it. Then, call the instance with a JSON file as an argument to convert it to Markdown, or call the `json_to_md` method of the instance with a dictionary as an argument to convert it to Markdown. The Markdown content will be stored in the `md` attribute of the instance and written to a file with the same name as the JSON file but with a `.md` extension.

```python
import json
from json2mdheadings import JSON2MD

converter = JSON2MD()
converter.json_to_md({"title": "Test Title", "authors": ["Author 1", "Author 2"]})
print(converter.md)
```

This will output the following Markdown:

```markdown
# title

Test Title

# authors

- Author 1
- Author 2


```

## Testing

To run the tests for json2mdheadings, use the following command:

```shell
python -m pytest tests
```

## License

json2mdheadings is licensed under the MIT License. See [LICENSE](LICENSE) for more information.