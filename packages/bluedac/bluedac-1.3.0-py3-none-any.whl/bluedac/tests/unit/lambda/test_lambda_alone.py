import sys

# By default, resources path is project_root/resources. Edit this, if needed.
sys.path.append("./resources")

# Edit these according to your files.
from lambda_file import handler

def test_lambda_alone():

    # Fill these, if needed.
    event = {}
    context = {}

    lambda_response = handler(event, context)

    # Assertions
    assert lambda_response["param"] == "expected_value"
