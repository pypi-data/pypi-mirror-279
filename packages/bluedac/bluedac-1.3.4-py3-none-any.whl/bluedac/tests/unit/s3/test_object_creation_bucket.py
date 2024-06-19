import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

# Edit these according to your files.
from lambda_file import handler

@mock_aws
def test_object_creation_bucket():

    # Since it's a virtual environment, a test bucket will be created.
    s3 = boto3.resource("s3", "us-east-1")
    s3.create_bucket(Bucket="moto-bucket")

    # Fill these, if needed.
    event = {}
    context = {}

    # This handler will put a new object inside the bucket.
    handler(event, context)

    # Retrieve just created item.
    body = s3.Object("moto-bucket", "key").get()[
        "Body"].read().decode("utf-8")

    # Assertions
    assert body == "val"
