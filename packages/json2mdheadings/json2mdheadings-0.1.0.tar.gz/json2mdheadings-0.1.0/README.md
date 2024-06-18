# json2mdheadings

A Python package for converting JSON data to Markdown with keys as headings. 

Since markdown only supports headings up to level 6, this will not work "correctly" for JSON data with more than 6 levels of nesting. Nested lists might be used for JSON data with more than 6 levels of nesting, but this is not currently implemented. 

For lists of dictionaries, an integer heading is written for each item and the keys of each dictionary are written as subheadings (can be nested as long as the overall heading level does not exceed 6) of the integer headings. See the example below.

Lists of lists from JSON are not currently written as nested lists in Markdown. 

The package is currently intended to be used for JSON data with a maximum of 6 levels of nesting and no lists of lists.

## Installation

You can install json2mdheadings using pip:

```shell
pip install json2mdheadings@git+https://github.com/bnovak1/json2mdheadings
```

## Usage

To use json2mdheadings, import the `JSON2MD` class from the `json2mdheadings` module and create an instance of it. Then, call the instance with a JSON file as an argument to convert it to Markdown, or call the `json_to_md` method of the instance with a dictionary as an argument to convert it to Markdown. The Markdown content will be stored in the `md` attribute of the instance and written to a file with the same name as the JSON file but with a `.md` extension.

### Examples

#### Nested JSON

```python
import json
from json2mdheadings import JSON2MD

converter = JSON2MD()
converter.json_to_md({"title": "Test Title", "author": {"name": "Test Author"}})
print(converter.md)
```

This will output the following Markdown:

```markdown
# title

Test Title

# author

## name

Test Author



```

#### With a list

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

#### With a list of dictionaries

```python
import json
from json2mdheadings import JSON2MD

converter = JSON2MD()
converter.json_to_md(
    {"title": "Test Title", "authors": [{"name": "Author 1"}, {"name": "Author 2"}]}
)
print(converter.md)
```

This will output the following Markdown:

```markdown
# title

Test Title

# authors

### 0

#### name

Author 1

### 1

#### name

Author 2



```

## Testing

To run the tests for json2mdheadings, use the following command:

```shell
python -m pytest tests
```

## License

json2mdheadings is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
