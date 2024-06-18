import pytest
from json2mdheadings import JSON2MD


def test_init():
    """
    Test the initialization of the JSON2MD class.

    This function ensures that the Markdown content is initially set to an empty string,
    and the level for headings for a list of dictionaries is initially set to None.

    Args:
        None

    Returns:
        None
    """

    converter = JSON2MD()
    assert converter.md == ""
    assert converter.dict_list_level == None


def test_call(tmpdir):
    """
    Test the __call__ method of the JSON2MD class.

    This function creates a temporary JSON file, writes a JSON object to it, and then converts the JSON file to Markdown using the JSON2MD class. It asserts that the resulting Markdown file has the expected content.

    Args:
        tmpdir: A temporary directory provided by the pytest framework.

    Returns:
        None
    """

    # Create a temporary JSON file
    p = tmpdir.mkdir("sub").join("test.json")
    p.write('{"title": "Test Title"}')

    # Convert the JSON file to Markdown
    converter = JSON2MD()
    converter(str(p))
    assert p.new(ext="md").read() == "# title\n\nTest Title\n\n"


def test_json_to_md():
    """
    Test cases for the json_to_md method of the JSON2MD class.
    """

    converter = JSON2MD()

    # Empty dictionary
    converter.json_to_md({}, 1)
    assert converter.md == ""

    # Single key-value pair
    converter.md = ""
    converter.json_to_md({"title": "Test Title"}, 1)
    assert converter.md == "# title\n\nTest Title\n\n"

    # Multiple key-value pairs
    converter.md = ""
    converter.json_to_md({"title": "Test Title", "author": "Test Author"}, 1)
    assert converter.md == "# title\n\nTest Title\n\n# author\n\nTest Author\n\n"

    # Nested dictionary
    converter.md = ""
    converter.json_to_md({"title": "Test Title", "author": {"name": "Test Author"}}, 1)
    assert converter.md == "# title\n\nTest Title\n\n# author\n\n## name\n\nTest Author\n\n"

    # With a list
    converter.md = ""
    converter.json_to_md({"title": "Test Title", "authors": ["Author 1", "Author 2"]}, 1)
    assert converter.md == "# title\n\nTest Title\n\n# authors\n\n- Author 1\n- Author 2\n\n"

    # With a list of dictionaries
    converter.md = ""
    converter.json_to_md(
        {"title": "Test Title", "authors": [{"name": "Author 1"}, {"name": "Author 2"}]}, 1
    )
    assert (
        converter.md
        == "# title\n\nTest Title\n\n# authors\n\n### 0\n\n#### name\n\nAuthor 1\n\n### 1\n\n#### name\n\nAuthor 2\n\n\n"
    )
