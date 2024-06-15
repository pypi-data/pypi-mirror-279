import pytest

def test_minify(plugin):
    source_html = """
        <!DOCTYPE html>
        <html>
          <head>
          <body>
            <h1>Hola Mundo!</h1>
          </body>
        </html>
    """

    result = plugin.minify(source_html)

    expected_html = "<!doctypehtml><body><h1>Hola Mundo!</h1>"
    assert result == expected_html


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("tests/example-project/assets/static/check_circle.png", False),
        ("tests/example-project/assets/static/check_circle.css", True),
        ("tests/example-project/assets/static/check_circle.js", True),
        ("tests/example-project/assets/static/check_circle.html", True),
    ]
)
def test_minify_ignore_image(plugin, filename, expected):
    assert plugin.is_valid_minify(filename) is expected
