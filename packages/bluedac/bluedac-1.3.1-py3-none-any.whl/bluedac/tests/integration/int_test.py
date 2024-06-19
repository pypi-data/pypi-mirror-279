import sys

# By default, resources path is project_root/resources. Edit this, if needed.
sys.path.append("./resources")

# Edit these according to your files.
from lambda_file import handler

def test_integration():

    # Fill these, if needed.
    event = {}
    context = {}

    # Since it's an integration test, handler will use internally
    # another resource (e.g. Lambda function).
    integration_response = handler(event, context)

    # Assertions
    assert integration_response["param"] == "expected_value"
