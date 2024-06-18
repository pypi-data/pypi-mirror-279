import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

# Edit these according to your files.
from lambda_file import handler

@mock_aws
def test_object_creation_dynamo():
    dynamo = boto3.resource("dynamodb", "us-east-1")

    # Create the DynamoDB table with values {"name": str, "surname": str}
    dynamo.create_table(
        TableName='moto-dynamo',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'surname',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'surname',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Fill these, if needed.
    event = {}
    context = {}

    # This handler will create a record in the Dynamo table.
    handler(event, context)

    # Retrieve item to check if it has been successfully created.
    table = dynamo.Table("moto-dynamo")
    item = table.get_item(
        Key={
            "name": "John",
            "surname": "Doe"
        }
    )

    assert item["Item"]["name"] == "John"