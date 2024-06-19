import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed.
sys.path.append("./resources")

# Edit these according to your files.
from lambda_file import handler

@mock_aws
def test_object_retrieve_bucket():

    # Since it's a virtual environment, a test bucket will be created.
    s3 = boto3.resource("s3", "us-east-1")
    s3.create_bucket(Bucket="moto-bucket")
    bucket = s3.Bucket("moto-bucket")

    # Fill these, if needed.
    event = {}
    context = {}

    # Put a test object in the bucket.
    bucket.put_object(
        Key="test_key",
        Body="test_value"
    )

    # This handler will retrieve an object from the bucket.
    response = handler(event, context)

    # Assertions
    assert response["body"]["param_containing_item"] == "test_value"
