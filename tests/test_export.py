"""
Tests to check the validity of the generated HTML.

The HTMLParser has an option to set strict to True which can pick up some
errors in the HTML syntax. However the Reveal template in nbconvert 6.1.0
has the script tag outside of the <body> and this causes strict mode to
raise an error. That said setting it to False means so other issues may
not get flagged.

To test the output HTML, we instead pass it to the HTML parser and check that
the raised error is the one we expect. This can at least catch unclosed tags.
"""
from pathlib import Path
from html5lib.html5parser import HTMLParser, ParseError
from avocado import AvocadoExporter


def get_test_filepath(filename):
    """
    Gets the path to the file located alongside this file
    """
    parent_dir = Path(__file__).parent
    return parent_dir / filename


def html_parser():
    """
    Create an HTML5 parser.
    """
    return HTMLParser(strict=True)


def test_template_export():
    """
    Run the generation of the document from the template's
    exporter.
    """
    test_file = get_test_filepath("test_notebook.ipynb")
    stream, info = AvocadoExporter().from_filename(test_file)
    try:
        html_parser().parse(stream)
    except ParseError as err:
        if str(err) != "Unexpected start tag token (script) in the after body phase.":
            raise err
